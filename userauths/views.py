import django
from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User


User = settings.AUTH_USER_MODEL



def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
           new_user = form.save()
           username = form.cleaned_data.get("username")
           messages.success(request,f"Hey {username} , Your account has been created.")
           new_user = authenticate(username=form.cleaned_data['email'],
                                                            password=form.cleaned_data['password1']
           )
           login(request,new_user)
           return redirect("core:index")                   

        
    else:
        form = UserRegisterForm()
    
    context = {
        'form':form,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already logged in ")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            # user = User.objects.get(email=email)
            user= authenticate(request,email=email,password=password)
            if user is not None:
                        login(request,user)
                        messages.success(request,"You are logged in.")
                        return redirect("core:index")
            else:
                        messages.warning(request,"User does not exist create account.")
        
        except:
            messages.warning(request, f"User with this {email} t does not exist")
            
    
    return render(request,"userauths/sign-in.html")
# def login_view(request):
#     if request.user.is_authenticated:
#         messages.warning(request, "Hey you are already logged in")
#         return redirect("core:index")
    
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
        
#         try:
#             user = User.objects.get(email=email)
#             authenticated_user = authenticate(request, email=email, password=password)
        
#             if authenticated_user is not None:
#                 login(request, authenticated_user)
#                 messages.success(request, "You are logged in.")
#                 return redirect("core:index")
#             else:
#                 messages.warning(request, "Invalid email or password.")
            
#         except User.DoesNotExist:
#             messages.warning(request, f"User with this {email} does not exist")
            
#     return render(request, "userauths/sign-in.html", {})


def testrender(request):
    return render(request,"userauths/sign-in.html")

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# def login_view(request):
#     print("login_view called")
#     if request.user.is_authenticated:
#         messages.warning(request, "Hey, you are already logged in.")
#         print("User is already authenticated")
#         return redirect("core:index")
    
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         print(f"POST request with email: {email}")

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             messages.warning(request, f"User with email {email} does not exist.")
#             print(f"User with email {email} does not exist.")
#             return render(request, "userauths/sign-in.html", {})

#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
#             login(request, user)
#             messages.success(request, "You are logged in.")
#             print("User authenticated and logged in")
#             return redirect("core:index")
#         else:
#             messages.warning(request, "Invalid email or password.")
#             print("Invalid email or password")
#             return render(request, "userauths/sign-in.html", {})
    
#     print("Rendering sign-in page")
#     return render(request, "userauths/sign-in.html", {})

def logout_view(request):
    logout(request)
    messages.success(request,"You logged out")
    return redirect("userauths:sign-in")