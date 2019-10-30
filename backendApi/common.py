from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
# from routerview.conditionModels import ConditionModels,ConditionModelsEx
# from dataaccess.dbhelper import DBHelper 
import json  
import datetime 
import time
import multiprocessing
import threading
import queue
import  decimal
class UTF8JSONRenderer(JSONRenderer):
        chartset = 'utf-8'
class JSONResponse(HttpResponse):
    def __init__(self,data,**kwargs):
        content = UTF8JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse,self).__init__(content,**kwargs)
class JSONResponseEx(HttpResponse):
    def __init__(self,data,**kwargs):
        content = data
        kwargs['content_type'] = 'application/json'
        if 'Access-Control-Allow-Credentials' in kwargs:
            response=HttpResponse()
            return response
            super(JSONResponseEx,self).__init__(content,**kwargs)
        else:
            super(JSONResponseEx,self).__init__(content,**kwargs)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj) 

class CommonHelper:
    @staticmethod
    def CombineStr(array):
        result = ''
        for item in array:
            result += "'"+item+"'" + ","
        result = result[:-1]
        return result;
    @staticmethod
    def Log(info): 
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%f" % (data_head, data_secs)
        print(info+time_stamp)   

# class ConditionHelper:
#     def CombineCondition(requestData):
#         # if("meterguids" not in requestData.keys() or "spaceguids" not in requestData.keys()):
#         #     print('error1')
#         #     return False
#         # print("### common.py --[CombineCondition]  requestData = ")
#         # print(requestData)
#         if( ("date" in requestData.keys() and "step" in requestData.keys()) or ("begindate" in requestData.keys() and "enddate" in requestData.keys()) ):
#             getmeterguid = "''"
#             if("meterguids"  in requestData.keys() ):
#                 for guid in requestData["meterguids"]:
#                     getmeterguid += "," + "'"+guid+"'"  
#             getspaceguid = "''"
#             if("spaceguids"  in requestData.keys()):
#                 for guid in requestData["spaceguids"]:
#                     getspaceguid += "," + "'"+guid+"'"

#             tenant_guids = "''"
#             if("tenant_guid" in requestData.keys() ):
#                 for guid in requestData["tenant_guid"]:
#                     tenant_guids += "," + "'"+guid+"'"  
#             step =  "''"
#             if("step" in requestData.keys()):
#                 if(requestData["date"]==""):
#                     return False
#                 selectdate = requestData["date"].split(' - ')
#                 begindate = selectdate[0]
#                 enddate = selectdate[1]
#                 step = requestData["step"]
#                 print('step exist')
#                 condition = ConditionModels(getmeterguid,getspaceguid,tenant_guids,begindate,enddate,step)
#                 return condition
#             else:
#                 if(requestData["begindate"]=="" or requestData["enddate"]==""):
#                     return False
#                 begindate = requestData["begindate"]
#                 enddate = requestData["enddate"]
#                 print("step doesn't exist")
#                 condition = ConditionModels(getmeterguid,getspaceguid,tenant_guids,begindate,enddate,step)
#                 #condition = ConditionModelsEx(getmeterguid,getspaceguid,tenant_guids,begindate,enddate)
#                 return condition
#         elif(requestData['query_table'] == 'tbl_tenant'):
#             guids = "''"
#             if("tenant_guid" in requestData.keys()):
#                 for guid in requestData["tenant_guid"]:
#                     guids += "," + "'"+guid+"'"  
#             condition = ConditionModels(tenant_guids = guids ) 
#             return condition               
#         else:
#             print('error2')
#             return False

# class MaxId:
#     def getNewId():
#         # if request.method == "POST":
#         helper=DBHelper()
#         sql=( 
#             ' SELECT MAX(maxid) as maxId  FROM (SELECT MAX(id) maxid FROM seed_building_db.`tbl_space`'
#             ' UNION ALL'
#             ' SELECT MAX(id) maxid FROM seed_building_db.tbl_meter'
#             ' UNION ALL' 
#             ' SELECT MAX(id) maxid FROM seed_building_db.`tbl_sensor`) temp'
#             )
#         print(sql)
#         rows= helper.queryAll(sql)  
#         newId=json.dumps(rows)
#         print("-----------")
#         print(newId)
#         print(type(newId))
#         id= eval(newId)
#         print(type(id))

#         print(id[0])
#         for i in id:
#             ids=id[0]["maxId"]
#             newIds=ids+1
#             return newIds
       
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


    
        


    
