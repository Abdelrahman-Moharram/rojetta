from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from .forms import add_user_form
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required



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



def register(request):
    if request.user.is_authenticated:
        return redirect("home:index")
    form   = add_user_form()
    if request.method == "POST":
        if request.POST['password'] != request.POST['retypepassword']:
            messages.error(request,"Password doesn't match Retype Password")
            return redirect("Auth:register")
        form = add_user_form(request.POST)
        if form.is_valid():
            form = form.save()

            # after saving form we should signin to account
            user = authenticate(request, username=request.POST['militry_id'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                ## save date in session should be string not date -> we made [tagned_date, end_date] in str form
                user._mutable = True
                user.tagned_date = str(user.tagned_date)
                user.end_date = str(user.end_date)

                # save user in sessions
                request.session.user = user
            
                # logged in successfully after regestration
                messages.info(request,form.fullname+" added succesfully")
                return redirect("Auth:profile", militry_id=form.militry_id) # تمام القوة انهارده
            
            # logged in Failed after regestration
            messages.error(request,"Login Failed after registeration contact admin")
            return redirect("Auth:register")
        # Registration failed
        messages.error(request,"Registration failed")
        return redirect("Auth:register")
    
    # GET request should pass here
    return render(request,"Auth/register.html",{"form":form})




def user_login(request):
    if request.user.username:
        return redirect("home:index")
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print("User logged: ", request.POST)
        if user is not None:
            login(request, user)
            print("User logged: ", user)

            ## save date in session should be string not date -> we made [tagned_date, end_date] in str form
            user._mutable = True
            user.date_joined = str(user.date_joined)

            # save user in sessions
            request.session.user = user

            # logged in successfully
            messages.info(request," أهلا "+request.user.username+" مرحبا بعودتك")
            return redirect("Auth:profile", militry_id=request.user.militry_id) # تمام القوة انهارده
        
        # no user 
        messages.error(request,"فشل تسجيل الدخول تأكد من الرقم العسكري وكلمة المرور")
        return redirect("Auth:login")
    # get request - NOT POST
    return render(request,"Auth/login.html",{})



@login_required
def profile(request,militry_id):
    return render(request,"Auth/profile.html",{"user":User.objects.get(militry_id=militry_id)})


@login_required
def logout_user(request):
        # user = User.objects.get(user=request.user)
        # user.is_active = False
        # user.save()
        logout(request)
        return redirect("home:index")

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
    return render(request,"Auth/addUser.html",{"u":user,
                                                   "workCategories":Work_Category.objects.all(),
                                                    "moahltypes":Moahl_Type.objects.all(),
                                                    "ranks":Rank.objects.all()
                                                })
@login_required
def delete(request, militry_id):
    user = User.objects.get(militry_id=militry_id)
    user.delete()
    return redirect("Auth:index")