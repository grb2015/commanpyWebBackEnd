from django.shortcuts import render

# Create your views here.
from django.conf.urls import url

from . import views
from django.http import HttpResponse


def index(request):
    return HttpResponse("欢迎访问我的博客首页！")