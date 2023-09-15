from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Doctor, Faculty, Skill, SkillType, Specialization, User
from .forms import add_user_form
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required





def register(request):
    if request.user.is_authenticated:
        return redirect("home:index")
    form   = add_user_form()
    if request.method == "POST":
        # if request.POST['password'] != request.POST['retypepassword']:
        #     messages.error(request,"Password doesn't match Retype Password")
        #     return redirect("Auth:register")
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
                return redirect("home:profile", uuid=user.uuid) 
            
            # logged in Failed after regestration
            messages.error(request,"Login Failed after registeration contact admin")
            return redirect("Auth:register")
        # Registration failed
        messages.error(request,"Registration failed")
        return render(request,"Auth/register.html",{"form":form})

    
    # GET request should pass here
    return render(request,"Auth/register.html",{"form":form})




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
                    messages.info(request, "<a class='child-arrow' href='/auth/add-doc/'>There is some data you need to complerte to increase your chance in search appearance ! <br> <span class='fw-bold text-primary'>go here to complete <i class='text-primary fas fa-angles-right'></i></span></a>")
            # messages.info(request," welcome back "+request.user.username)
            return redirect("home:index")
        
        # no user 
        messages.error(request,"Login failed with Email or Password")
        return redirect("Auth:login")
    # get request - NOT POST
    return render(request,"Auth/login.html",{})



# @login_required
def profile(request,uuid):
        return render(request,"Auth/profile.html",{"user":User.objects.get(uuid=uuid)})


@login_required
def logout_user(request):
        logout(request)
        return redirect("home:index")


# 
@login_required
def addDocData(request):
    try:
        doc = Doctor.objects.get(user=request.user)
    except:
        messages.error(request,doc.user.username+"<a class='child-arrow' href='/auth/add-doc/'> Not registered as Doctor do you want to upgrade your account? <br> <span class='fw-bold text-primary'>go here to complete <i class='text-primary fas fa-angles-right'></i></span></a>")
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

                        skillType = SkillType.objects.get(name=request.POST.getlist("skill_type")[index])
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
        print(request.POST)
        if'specialization' in request.POST:
            specialization = Specialization.objects.get(name=request.POST['specialization'])
            doc.specialization = specialization
        doc.save()

        messages.info(request,doc.user.username+" updated succesfully")
        return redirect("Auth:adddoc")
    return render(request,"Auth/docform.html",{"doc":doc, "SkillTypes":SkillType.objects.all(), "specializations":Specialization.objects.all(), })









################################## NOT IMPLEMENTED YET ##################################

@login_required
def index(request): ## for sub-admin
    return render(request, "Auth/index.html", {"users":User.objects.all()})

@login_required
def addUser(request): ## for sub-admin & super-admin
    form   = add_user_form()
    if request.method == "POST":
        if request.POST['password'] != request.POST['retypepassword']:
            messages.error(request,"Password doesn't match Retype Password")
            return redirect("Auth:register")
        form = add_user_form(request.POST)

        if form.is_valid():
            form = form.save()
            messages.info(request,form.username+" added succesfully")
            if "_submit" in  request.POST:
                return redirect("Auth:add")
            return redirect("Auth:index") # جدول فيه كل اليوزرز
    return render(request,"Auth/addUser.html",{"form":form})









@login_required
def edit(request, militry_id):
    user = User.objects.get(militry_id=militry_id)
    if  request.method == "POST":
        user.fullname = request.POST['fullname']
        user.militry_id = request.POST['militry_id']
        user.moahl = request.POST['moahl']
        user.tagned_date = request.POST['tagned_date']
        user.end_date = request.POST['end_date']
        user.password = request.POST['password']
        user.save()
        messages.info(request,"تم تعديل بيانات "+user.fullname+ " بنجاح")
        return redirect("Auth:index")
    return render(request,"Auth/addUser.html",{"u":user})
@login_required
def delete(request, militry_id):
    user = User.objects.get(militry_id=militry_id)
    user.delete()
    return redirect("Auth:index")


######################################################################################################