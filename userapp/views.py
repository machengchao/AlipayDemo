from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import login
from .models import *

# Create your views here.

def mylogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/index/')
        else:
            return redirect('/user/zhuche/')


def myzhuche(request):
    if request.method == 'GET':
        return render(request, 'zhuche.html')
    else:
        username = request.POST.get('username')
        emai = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = BlogUser.objects.get(username=username)
            return render(request, 'zhuche.html', {"error": "用户已存在"})
        except BlogUser.DoesNotExist:
            user = BlogUser.objects.create_user(username, emai, password)
            if user:
                return redirect('/user/login/')
            else:
                return render(request, 'zhuche.html', {"error": '用户创建失败'})
