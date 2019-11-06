# from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework.parsers import JSONParser
# import json
# from common import UTF8JSONRenderer,JSONResponse,JSONResponseEx,DateEncoder,DecimalEncoder

from helperCollection import logger,DBHelper # 这里必须加上hotel 不然会报错


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

###############################################################################################
'''
# breif :   查询数据权限树
# inputs:   无
					
# returns:	[dict]      {"result":xx,"data":'xxxx'}
#                        result :        bool        True :成功 / False: 异常发生
#                        data   :        list         若: result 为True ,  data 包含的功能树
#                                                     若: result 为False , data为异常信息
#     
#     举例:                      
data = [
{"id": 100, "name": "报警类型",  "pId": undefined,"isLeaf":false},
{"id": 1, "name": "强开报警",  "pId": 100,"isLeaf":true},
{"id": 2, "name": "设备故障报警",  "pId": 100,"isLeaf":true},
{"id": 3, "name": "超高能耗报警", "pId": 100,"isLeaf":true},
{"id": 4, "name": "室内环境超限报警",  "pId": 100,"isLeaf":true},
{"id": 5, "name": "变频电电流超限报警",  "pId": 100,"isLeaf":true},
{"id": 6, "name": "入侵报警",  "pId": 100,"isLeaf":true},
{"id": 200, "name": "工单类型",   "pId": undefined,"isLeaf":false},
{"id": 1, "name": "设备报修工单", "pId": 200,"isLeaf":true},
{"id": 2, "name": "冷机运行异常工单",  "pId": 200,"isLeaf":true},
{"id": 4, "name": "门禁报警工单",  "pId": 200,"isLeaf":true},
{"id": 4, "name": "照明系统异常工单",  "pId": 200,"isLeaf":true},
]
'''
################################################################################################*/
def query_DataPermission_Tree():
	rt = {"result":True,"data":[]}
	rt_code = 201
	sql = '''SELECT * FROM datang_user_db.tbl_all_permission;'''
	g_helper = DBHelper()
	root_id_base = 100
	try:
		rows = g_helper.queryAll(sql)
		logger.info("rows = ")
		logger.info(rows)
		# rt['data']  = rows

		# 构造树结构
		for row in rows:
			logger.info("############ row ")
			logger.info(row)
			tbl_tree_list = getTreeBranch(row['permission_tblname'],root_id_base)
			logger.info("########### tbl_tree_list =")
			logger.info(tbl_tree_list)
			for info in tbl_tree_list:
				rt['data'].append(info)
			root_id_base =  root_id_base *2 
	except Exception as e:
		logger.info("异常发生！！！！")
		logger.info(e) 
		rt['result'] = False
		rt_code = 400
	logger.info("query_DataPermission_Tree  rt = ")
	logger.info(rt)
	logger.info("###########################打印结果\n\n\n")
	for row in rt['data']:
		logger.info(row)
	# data=json.dumps(rt, cls=DecimalEncoder)
	# return HttpResponse(data,status=rt_code)

'''
breif 	: 	将一个表转为树结构
input	: 	tblname  
			rootId
return		[list]   	树结构
示例:
tblname = datang_worksheet_db.tbl_worksheet_type
rootId  = 200
则返回
[
	{"id": 200, "name": "工单类型",   "pId": undefined,"isLeaf":false},
	{"id": 1, "name": "设备报修工单", "pId": 200,"isLeaf":true},
	{"id": 2, "name": "冷机运行异常工单",  "pId": 200,"isLeaf":true},
	{"id": 4, "name": "门禁报警工单",  "pId": 200,"isLeaf":true},
	{"id": 4, "name": "照明系统异常工单",  "pId": 200,"isLeaf":true},
]


'''
def getTreeBranch(tblname,rootId):
	rt = []
	logger.info(" ##### getTreeBranch tblname = ")
	logger.info(tblname)
	logger.info(" ##### getTreeBranch rootId = ")
	logger.info(rootId)
	rootInfo = {"id": rootId, "name": get_tblnameCN(tblname),   "pId": None,"isLeaf":False}
	rt.append(rootInfo)
	sql = '''SELECT * FROM %s'''%(tblname)
	g_helper = DBHelper()
	try:
		rows = g_helper.queryAll(sql)
		logger.info("rows = ")
		logger.info(rows)
		column = []
		for key in rows[0]:
			column.append(key)
		logger.info(column)
		for row in rows:
			logger.info("row =")
			logger.info(row)
			tmp = {}
			tmp['id'] = row[column[0]]
			tmp['name'] = row[column[1]]
			tmp['pId']	= rootId
			tmp['isLeaf']	= True
			rt.append(tmp)
	except Exception as e:
		logger.info("异常发生")
		logger.info(e) 
		return None
	logger.info(rt)
	for rti in rt:
		logger.info(rti)
	return rt


'''
获取中文表名
'''
def get_tblnameCN(tblname):
	g_helper = DBHelper()
	sql = '''SELECT * FROM datang_user_db.tbl_tblname_cn
			where tblname =  '%s'  '''%(tblname)
	logger.info(sql)
	rows = g_helper.queryAll(sql)
	return rows[0]['tblname_CN']

if __name__ == "__main__":
	query_DataPermission_Tree()
	# getTreeBranch('datang_worksheet_db.tbl_worksheet_type',200)
	# logger.info( get_tblnameCN('datang_alarm_db.tbl_alarm_category') )