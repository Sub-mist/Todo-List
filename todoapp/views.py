from django.shortcuts import render,redirect# ignore
from django.contrib import messages
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate,login,logout # type: ignore
from .models import todo
from django.contrib.auth.decorators import login_required
# Create your views here.
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('uname')
        password=request.POST.get('pass')
    
        validate_user=authenticate(username=username,password=password)
        if validate_user is not None:
            login(request,validate_user)
            return redirect('home')
        else:
            messages.error(request,"wrong credentials or user doesn't exist")
            return redirect('login')
        
    return render(request,'main/login.html',{})

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password1=request.POST.get('repassword')
        
        if len(password)<8:
            messages.error(request,'Password must contain at least 8 characters')
            return redirect('register')
        
        if password!=password1:
            messages.error(request,'Password are not same')
            return redirect('register')

        all_username_check = User.objects.filter(username=username)
        if all_username_check:
            messages.error(request, 'Username already exists')
            return redirect('register')
    

        new_user=User.objects.create_user(username=username,email=email,password=password)
        new_user.save()

        messages.success(request,'User created Successfully')
        return redirect('login')
    return render(request,'main/register.html',{})

@login_required
def homepage(request):
    if request.method=='POST':
        task=request.POST.get('task')
        new_todo=todo(user=request.user,todo_name=task)
        new_todo.save()

    all_todos=todo.objects.filter(user=request.user)
    context={
        'todos':all_todos
    }
    return render(request,'main/home.html',context)

def LogoutView(request):
    logout(request)
    return redirect('login')

@login_required
def DeleteTask(request,name):
    get_todo=todo.objects.get(user=request.user,todo_name=name)
    get_todo.delete()
    return redirect('home')

@login_required
def Update(request,name):
    get_todo=todo.objects.get(user=request.user,todo_name=name)
    get_todo.status=True
    get_todo.save()
    return redirect('home')
