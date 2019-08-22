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
    requestData = JSONParser().parse(request)
    print(requestData)
    print("##### query in sqlite3")
    db = sqliteOperate('hotel.sqlite3')
    rows = db.select("select * from user")
    print("rows = ")
    print(rows)
    for row in rows:
        if row[1] == requestData['userName'] and row[2] == requestData['password']:
            data = json.dumps({ 'result': 'success',
                                'userName': requestData['userName'],
                                'userAuthStr':requestData['password'],
                                'guid':'xx3'
                            })
            response = HttpResponse(data, status=201)
            return response
    data = json.dumps({ 'result': 'fail',
                        'userName': requestData['userName'],
                        'userAuthStr':requestData['password'],
                        'guid':'xx3'
                    })
    response = HttpResponse(data, status=201)
    return response

   