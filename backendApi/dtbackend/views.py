from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from hotel.helperCollection import logger # 这里必须加上hotel 不然会报错
import json
from common import UTF8JSONRenderer,JSONResponse,JSONResponseEx,DateEncoder,DecimalEncoder

def getuserinfo(request):
	rt = {"result":1,'data': None}
	rt_code = 201
	try:
		requestData = JSONParser().parse(request)
		logger.info('requestData  = ')
		logger.info(requestData)
		auth_flag = 0
		# TODO 验证用户名和密码
		if auth_flag == 0: # 验证失败
			rt['result'] = 0
	except Exception as e:
		logger.info(e)
		rt['result'] = -1
		rt['data'] = str(e)
		rt_code = 400
	data=json.dumps(rt, cls=DecimalEncoder)
	return HttpResponse(data,status=rt_code)
   