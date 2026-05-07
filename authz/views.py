from django.shortcuts import render,redirect,resolve_url
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        username=request.POST.get('username')
        email=request.POST.get('email')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        password=request.POST.get('password')
        if not username or not email or not firstname or not lastname or not password:
            messages.error(request,'all field are required')
            return render(request,'signup.html')
        if len(password)<8:
            messages.error(request,'password too short')
            return render(request,'signup.html')
        if len(username)<5:
            messages.error(request,'username too short')
            return render(request,'signup.html')
        

        username = username.lower()
        email = email.lower()
        if User.objects.filter(username=username).exists():
            messages.error(request,'username alredy exist')
            return render(request,'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request,'email already taken')
            return render(request,'signup.html')

        

        user= User.objects.create(username=username, email=email, first_name=firstname,last_name=lastname)
        user.set_password(password)
        user.save()
        messages.success(request,'account created successfully')

        return redirect(resolve_url('home'))

    
# Create your views here.
