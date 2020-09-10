from django.shortcuts import render
from rest_framework.parsers import JSONParser
import json
# Create your views here.
from django.conf.urls import url
from . import views
from django.http import HttpResponse
# from hotel.helperCollection import sqliteOperate,logger # 这里必须加上hotel 不然会报错
from hotel.helperCollection import  logger,DBHelper # 这里必须加上hotel 不然会报错
import sqlite3

def hotel_index(request):
    logger.info("## 欢迎访问我的博客首页！")
    return HttpResponse("欢迎访问我的博客首页！")

def hotel_login(request):
    g_helper = DBHelper()
    requestData = JSONParser().parse(request)
    logger.info("[hotel_login] requestData = ")
    logger.info(requestData)
    response = {"result":'',"data":{}}
    sql = 'SELECT * FROM grb_farmhouse_db.tbl_user_info;'
    rows=  g_helper.queryAll(sql)
    logger.info(" [hotel_login] rows = ")
    logger.info(rows)
    for row in rows:
        if row['user_name'] == requestData['userName'] and row['user_password'] == requestData['password']:
            response['result'] = 'success'
            response['userName'] = requestData['userName']
            response['userAuthStr'] = requestData['password']
            response['guid'] = 'xx3'
            data=json.dumps(response)
            return HttpResponse(data, status = 201)
    response['result'] = 'fail'
    response['userName'] = requestData['userName']
    response['userAuthStr'] = requestData['password']
    response['guid'] = 'xx3'
    data=json.dumps(response)
    return HttpResponse(data, status = 400)
