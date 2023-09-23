from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from .models import Clinic, Doctor, Faculty, Government, Phone, Skill, SkillType, Specialization, State, User
from .forms import add_user_form
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q




def register(request):
    if request.user.is_authenticated:
        return redirect("home:index")
    form   = add_user_form()
    if request.method == "POST":
        # if request.POST['password'] != request.POST['retypepassword']:
        #     messages.error(request,"Password doesn't match Retype Password")
        #     return redirect("accounts:register")
        form = add_user_form(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            if "is_doctor" in request.POST:
                f.is_doctor = True
                f.save()
            else:
                f.is_doctor = False
                f.save()
            # after saving form we should signin to account
            user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                ## save date in session should be string not date -> we made [tagned_date, end_date] in str form
                user._mutable = True
                user.joined_at = str(user.joined_at)
                # save user in sessions
                request.session.user = user
            
                # logged in successfully after regestration
                messages.info(request,user.username+" added succesfully")
                return redirect("accounts:profile", uuid=user.uuid) 
            
            # logged in Failed after regestration
            messages.error(request,"Login Failed after registeration contact admin")
            return redirect("accounts:register")
        # Registration failed
        messages.error(request,"Registration failed")
        return render(request,"accounts/register.html",{"form":form})

    
    # GET request should pass here
    return render(request,"accounts/register.html",{"form":form})




def user_login(request):
    if request.user.username:
        return redirect("home:index")
    if request.method == "POST":
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is not None:

            login(request, user)

            ## save date in session should be string not date -> we made [tagned_date, end_date] in str form
            user._mutable = True
            user.joined_at = str(user.joined_at)

            # save user in sessions
            request.session.user = user

            # logged in successfully
            if request.user.is_doctor:
                doc = Doctor.objects.get(user=request.user)
                if doc.bio == None or doc.coverletter == None or doc.skills == None or doc.specialization == None :
                    messages.info(request, "<a class='child-arrow' href='/accounts/add-doc/'>There is some data you need to complerte to increase your chance in search appearance ! <br> <span class='fw-bold text-primary'>go here to complete <i class='text-primary fas fa-angles-right'></i></span></a>")
            # messages.info(request," welcome back "+request.user.username)
            return redirect("home:index")
        
        # no user 
        messages.error(request,"Login failed with Email or Password")
        return redirect("accounts:login")
    # get request - NOT POST
    return render(request,"accounts/login.html",{})



# @login_required
def profile(request,uuid):
        return render(request,"accounts/profile.html",{"user":User.objects.get(uuid=uuid)})


@login_required
def logout_user(request):
        logout(request)
        return redirect("home:index")



@login_required
def upgradeAccount(request):
    user = User.objects.get(uuid=request.user.uuid)
    user.is_doctor=True
    user.save()
    doc = Doctor.objects.create(user=user)
    doc.save()
    Clinic.objects.create(doctor=doc).save()
    return redirect("accounts:adddoc")

# 
def is_doctor(request):
    if not request.user.is_doctor:
        messages.error(request,request.user.username+"<a class='child-arrow' href='/accounts/upgrade-account/'> Not registered as Doctor do you want to upgrade your account? <br> <span class='fw-bold text-primary'>go here to complete <i class='text-primary fas fa-angles-right'></i></span></a>")
        return redirect("home:index")

@login_required
def addDocData(request):
    is_doctor(request)
    try:
        doc = Doctor.objects.get(user=request.user)
    except:
        messages.error(request,request.user.username+"<a class='child-arrow' href='/accounts/add-doc/'> Not registered as Doctor do you want to upgrade your account? <br> <span class='fw-bold text-primary'>go here to complete <i class='text-primary fas fa-angles-right'></i></span></a>")
        return redirect("home:index")
    
    if  request.method == "POST":
        if "bio" in request.POST:
            doc.bio = request.POST['bio']
        if "coverletter" in request.POST:
            doc.coverletter = request.POST['coverletter']
        if 'skill' in request.POST:
            length = len(request.POST.getlist('skill'))
            skills_length = len(doc.skills.all()) 
            for index in range(length):
                if index <= skills_length-1:
                
                    skill = Skill.objects.get(id=doc.skills.all()[index].id)
                    skill_type = SkillType.objects.get(id=skill.type.id)
                    skill_type.name = request.POST.getlist("skill_type")[index]
                    skill_type.save()
                    skill.name = request.POST.getlist("skill")[index]
                    skill.date = request.POST.getlist("skill_date")[index]
                    if "certificate" in  request.FILES:
                        skill.certificate = request.FILES['certificate']
                    skill.save()
                
                else:
                    if request.POST.getlist("skill_type")[index] and request.POST.getlist("skill")[index]:
                        try:
                            skillType = SkillType.objects.get(name=request.POST.getlist("skill_type")[index])
                        except:
                            skillType = SkillType.objects.create(name=request.POST.getlist("skill_type")[index])
                        currSkill = request.POST.getlist("skill")[index]
                        skill_date = request.POST.getlist("skill_date")[index]
                        skill = Skill.objects.create(name=currSkill, type=skillType)
                        if skill_date:
                            skill.date = skill_date
                        if "certificate" in  request.FILES:
                            skill.certificate= request.FILES['certificate']
                        skill.save()
                        doc.skills.add(skill)
                # doc.save()
        if'specialization' in request.POST:
            try:
                specialization = Specialization.objects.get(name=request.POST['specialization'])
            except:
                specialization = Specialization.objects.create(name=request.POST['specialization'])

            doc.specialization = specialization
        if doc.skills.count() > 0 and doc.specialization!="" and doc.image.url!="/media/users/logo.webp" and doc.coverletter!="" and doc.bio!="":
            doc.is_completed = True
        doc.save()
        messages.info(request,doc.user.username+" updated succesfully")
        return redirect("accounts:addClinic")
    return render(request,"accounts/docform.html",{"doc":doc, "SkillTypes":SkillType.objects.all(), "specializations":Specialization.objects.all(), })


def getStates(request, name):
    gover = Government.objects.filter(Q(ar_name__contains=name)|Q(name__contains=name))
    return JsonResponse({
            "states":list(State.objects.filter(government__in=gover).values('id', 'name', 'ar_name'))})


@login_required
def addClinic(request):
    try:
        doc = Doctor.objects.get(user=request.user)
        clinic = Clinic.objects.get(doctor=doc)
    except:
        messages.error(request,doc.user.username+"<a class='child-arrow' href='/accounts/add-doc/'> Not registered as Doctor do you want to upgrade your account? <br> <span class='fw-bold text-primary'>go here to complete <i class='text-primary fas fa-angles-right'></i></span></a>")
        return redirect("home:index")
    
    if  request.method == "POST":
        if 'government' in request.POST:
            try:
                government = Government.objects.get(name=request.POST['government'])
            except:
                government = Government.objects.create(name=request.POST['government'])
            clinic.government = government
        if 'state' in request.POST:
            try:
                state = State.objects.get(name=request.POST['state'])
            except:
                state = State.objects.create(name=request.POST['state'], government=government)
            clinic.state = state
        if 'detailLocation' in request.POST:
            clinic.detailLocation = request.POST['detailLocation']
        if 'mapsLocation' in request.POST:
            clinic.mapsLocation = request.POST['mapsLocation']
        if 'phone' in request.POST:
            phones = request.POST.getlist('phone')
            clinic_phones = len(clinic.phones.all())
            for index in range(len(phones)):
                if index <= clinic_phones-1:
                    currphone = Phone.objects.get(id=clinic.phones.all()[index].id)
                    currphone.phone = phones[index].strip()
                    currphone.save()
                else:
                    currphone = Phone.objects.create(phone=phones[index])
                    currphone.save()
                    clinic.phones.add(currphone)
                
        clinic.save()
        return redirect("accounts:profile", clinic.doctor.user.uuid)
    
    return render(request, 'accounts/clinicform.html', {"clinic":clinic, 'governments':Government.objects.all()})





