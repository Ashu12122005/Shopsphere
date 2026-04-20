from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators  import login_required
from base.models import CartModel
import re
from django.contrib import messages


# Create your views here.
def login_(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pasw = request.POST.get('pasw')   # corrected key

        user = authenticate(request, username=uname, password=pasw)

        if user is not None:
            login(request, user)
            return redirect('home')   # change if your homepage url name differs
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login_.html')

def valid_pasw(pasw):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
    return  re.match(pattern,pasw)


def register(request):


    if request.method == "POST":

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        uname = request.POST['uname']
        pasw = request.POST['pasw']

        # check username exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        # password validation
        if not valid_pasw(pasw):
            messages.error(request, "Password should be a strong combination!")
            return redirect("register")

        # create user
        user = User.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            username=uname
        )

        user.set_password(pasw)
        user.save()

        messages.success(request, "Account created successfully! Please login.")

        return redirect("login")

    return render(request, "register.html")

@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect(login_)

@login_required(login_url='login_')
def profile(request):
    if request.user.is_authenticated:
        cartproductscount = CartModel.objects.filter(host=request.user).count()
    else:
        cartproductscount = False
    return render(request,'profile.html',{'cartproductscount':cartproductscount,'profile_nav':True})


@login_required(login_url='login_')
def reset(request):
    user = request.user
    print(user)

    if request.method == 'POST':

        if 'old_pasw' in request.POST:
            old_pass = request.POST['old_pasw']
            auth_user = authenticate(username = user.username,password = old_pass)
            print(auth_user)

            if auth_user:
                return render(request,'reset.html',{'new_pass':True})
            else:
                return render(request,'reset.html',{'error':True})
            
        if 'new_pasw' in request.POST:   
            new_pasw = request.POST['new_pasw']
            pasw = new_pasw
            if not valid_pasw(pasw):
                return render(request,'reset.html',{'error_pasw':'not a combi'})
            user.set_password(pasw)
            user.save()
            return redirect('login_')
    
    return render(request,'reset.html',{'profile_nav':True})

def new_pasw(request):
    uname = request.session.get('fp_user')

    if uname is None:
        return redirect('forget_pasw')
    
    user = User.objects.get(username = uname)

    if request.method == 'POST':
        new_pasw = request.POST['new_pass']

        user.set_password(new_pasw)
        user.save()

        del request.session['fp_user']
        return redirect('login_')

    return render(request,'new_pasw.html',{'login_nav':True})

def forget_pasw(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        try:
            u = User.objects.get(username = uname)
            request.session['fp_user'] = u.username
            return redirect('new_pasw')
            print(u)
        except User.DoesNotExist:
            return render(request,'forget_pasw.html',{'error':True})

    return render(request,'forget_pasw.html',{'login_nav':True})


@login_required(login_url='login_')
def update(request):
    user = request.user  

    if request.method == 'POST':
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.username = request.POST['uname']

        user.save()

        return redirect('profile')

    return render(request, 'update.html', {'user': user,'profile_nav':True})
