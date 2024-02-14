from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here.
def loginpage(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('List/')
        else:
            messages.info(request, 'Username/Password is incorrect')
    return render(request, 'User\login.html')

def registerpage(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username is already taken')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save() 
            messages.info(request, 'Your registration is successful.')
            auth.login(request,user)
            return redirect('/List/')
    return render(request,'User\\register.html')





