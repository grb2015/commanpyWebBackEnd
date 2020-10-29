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



################################################################################## 
#   breif   ：  用户注册
#   input   :   userName   [string]     用户名
#               password [string]     md5加密后的密码
#   returns : [json]      {"result":xx,"data":'xxxx'}
#                           result :        bool    值为True/False 表明是否执行成功
#                          data:  string  给前端的附带信息 
#                           # 1.若result为True , data 为空
#                           # 2.若result为False, data为错误信息
################################################################################## 
def sign_up(request):
    g_helper = DBHelper()
    requestData = JSONParser().parse(request)
    logger.info("[sign_up] requestData = ")
    logger.info(requestData)
    logger.info(requestData['userName'])
    logger.info(requestData['password'])

    insert_rows = []
    insert_rows.append( {'user_name': requestData['userName'],'user_password': requestData['password']} )
    try:
        insert_into_db(insert_rows,'grb_farmhouse_db.tbl_user_info')
        rt = json.dumps( {"result":True,"data":None} )
        logger.info("########### [join_family] 新增成功。")
        return HttpResponse(rt, status = 201)
    except Exception as e:
        logger.info("######### [join_family] 新增失败  e = ")
        logger.info(e)
        rt = json.dumps( {"result":False,"data":"插入出错"+str(e)} )
        return HttpResponse(rt,status=400)



############################################################################################### 
# breif : 	向数据库插入数据(支持同时插入多条),然后给前端返回信息
# inputs: 	[list]    rows :要插入的数据,key为数据库的列名,value为要插入的值
#                           [
#                               {column1:value1,column2:value2,...},
#                               {column1:value1,column2:value2,...},
#                               ...
#                           ]
#           [string] tblname:要插入的表名
# returns:	无
# 调用示例：
#   rows = [
#                 {'attribute_name':'test1','is_complex_attr':0,'point_id1':None,'complex_operate_id':None,'point_id2':None,'note':''},
#                 {'attribute_name':'test1','is_complex_attr':0,'point_id1':None,'complex_operate_id':None,'point_id2':None,'note':''},
#             ]
#   tblname = 'jcimate_alarm_rules.tbl_attribute'
# insert_into_db(rows,tblname)
################################################################################################/
def insert_into_db(rows,tblname):
    g_helper = DBHelper()
    try:
        logger.info(rows)
        g_helper.insert_rows(rows,tblname)
    except Exception as e:
        logger.info(e)
        raise


