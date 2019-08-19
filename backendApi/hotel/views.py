from django.shortcuts import render

# Create your views here.
from django.conf.urls import url
from helperCollection import sqliteOperate,justTest

from . import views
from django.http import HttpResponse
import sqlite3

def hotel_index(request):
    justTest()
    return HttpResponse("欢迎访问我的博客首页！")


def hotel_login(request):
    conn = sqlite3.connect('hotel.sqlite3')
    print("Opened database successfully")
    return HttpResponse("欢迎登陆！")
    db = sqliteOperate('hotel.sqlite3')
    sql = 'select *from user;'
    rows = db.execute(sql)
    print(rows)
    # if request.method == 'GET':
    #     sql = "select * from user"
    #     helper = DBHelper()
    #     helper.setDB("hotel.sqlite3")
    #     rows= helper.queryAll(sql)
    #     data=json.dumps(rows, cls=DecimalEncoder)
    #     if len(data)>0:
    #         return JSONResponseEx(data, status = 201)
    #     return JSONResponseEx("出错",status=400)
    # if request.method == 'POST':
    #     requestData = JSONParser().parse(request)
    #     helper=DBHelper()
    #     helper.setDB("seed_building_db")
    #     sql = "update seed_building_db.tbl_setting set svalue = '%s' where skey = 'electricityprice';"%(requestData["elecPrice"])
    #     rows= helper.queryAll(sql)
    #     data=json.dumps(rows)
    #     if len(data)>0:
    #         return JSONResponseEx(data, status = 201)
    #     return JSONResponseEx("出错",status=400)