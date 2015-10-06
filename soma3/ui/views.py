import logging

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_GET, require_POST

def index(req):
    req.user.ok = req.user.is_authenticated() and req.user.is_active

    return render(req, 'ui/global.html')

@require_POST
def signin(req):
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(username=username, password=password)
    if user and user.is_active:
        login(req, user)
        return redirect('/ui/')

    return redirect('/ui/')

@require_GET
def signout(req, **kwargs):
    logout(req)
    
    return redirect('/ui/')