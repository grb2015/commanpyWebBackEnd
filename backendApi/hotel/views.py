from django.shortcuts import render
from rest_framework.parsers import JSONParser
import json
# Create your views here.
from django.conf.urls import url
from . import views
from django.http import HttpResponse
from hotel.helperCollection import sqliteOperate,logger # 这里必须加上hotel 不然会报错
import sqlite3

def hotel_index(request):
    logger.info("## 欢迎访问我的博客首页！")
    return HttpResponse("欢迎访问我的博客首页！")

def hotel_login(request):
    print("##### hotel_login")
    db = sqliteOperate('hotel.sqlite3')
    rows = db.select("select * from user")
    print("rows = ")
    print(rows)
    requestData = JSONParser().parse(request)
    print(requestData)
    return HttpResponse("欢迎登陆!")

   