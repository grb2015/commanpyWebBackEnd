#--encoding:utf-8--
#
import time
import hashlib
import random
import sys
import pymysql
import codecs
import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler
g_config_dict  =  {}
LOG_DIR = './logs/log.txt'  #在manager.py目录下的logs
def read_config():

    # 得到配置文件所在的目录。
    # 注意这里不能写 config_file = '..\\settting'  ,config_file必须是绝对路径
    curFileDir =  os.path.dirname( os.path.realpath(__file__) )
    config_file = curFileDir + r'\user_setting.json'
    print('################################## config_file = ',config_file)
    # 若配置文件不存在,则创建
    if  not os.path.exists(config_file):
        print("[read_config]  setting.json 不存在,创建")
        default_config ={
                            "ALLOWED_HOSTS":[
                                "127.0.0.1"
                            ],
                            "mysql_info":{
                                "host":"127.0.0.1",
                                "port":3306,
                                "user":"root",
                                "password":"password"
                            }
                        }
        with codecs.open(config_file, 'w+',encoding ='utf-8')  as f:
            json.dump(default_config, f)

    # 读取配置文件
    with codecs.open(config_file, 'r',encoding ='utf-8')  as f:
        try:
            config_dict = json.load(f)
        except Exception as e: # 文件为空或Json格式不正确
            print(r"读取配置错误，请检查配置文件格式")
            print(config_file)
            print(e)
            exit(1)
    # print("config_dict  = ",config_dict)
    return config_dict

class DBHelper:
    myVersion=0.1
    g_config_dict = read_config()
    info = g_config_dict['mysql_info']
    def __init__(self,host=info['host'],user=info['user'],password=info['password'],port = info['port'],charset="utf8"):
        self.host=host
        self.user=user
        self.password=password
        self.charset=charset
        self.port=port
        try:
            self.conn=pymysql.connect(host=self.host,user=self.user,passwd=self.password,port=self.port,charset=self.charset)
            #self.conn.set_character_set(self.charset)
            self.cursor=self.conn.cursor()
            
        except Exception as e:
            print ('MySql Error : %d %s' %(e.args[0],e.args[1]))

    def setDB(self,db):
        try:
            self.conn.select_db(db)
        except Exception as e:
            print ('MySql Error : %d %s' %(e.args[0],e.args[1]))

    def query(self,sql):
        try:
            rows=self.cursor.execute(sql)
            return rows
        except Exception as e:
            logger.info(e)
            raise

    def queryOnlyRow(self,sql):
        try:
            self.query(sql)
            result=self.cursor.fetchone()
            desc=self.cursor.description
            row={}
            for i in range(0,len(result)):
                row[desc[i][0]]=result[i]
            return row
        except Exception as e:
            logger.info(e)

    def queryAll(self,sql):
        try:
            logger.info(sql)
            self.query("set names 'utf8'")
            self.query(sql)
            self.commit()
            result=self.cursor.fetchall()
            desc=self.cursor.description
            rows=[]
            for cloumn in result:
                row={}
                for i in range(0,len(cloumn)):
                    row[desc[i][0]]=cloumn[i]
                rows.append(row)
            return rows
        except Exception as e:
            logger.info(e)
            raise

    def insert(self,tableName,pData):
        try:
            newData={}
            for key in pData:
                newData[key]="'"+pData[key]+"'"
            key=','.join(newData.keys())
            value=','.join(newData.values())
            sql="insert into "+tableName+"("+key+") values("+value+")"
            self.query("set names 'utf8'")
            self.query(sql)
            self.commit()
        except Exception as e:
            self.conn.rollback()
            print('MySql Error: %s %s'%(e.args[0],e.args[1]))
        finally:
            self.close()

    
    ############################################################################################### 

    # breif : 	向数据库插入数据(支持同时插入多条)
    # inputs: 	[list]    rows :要插入的数据,key为数据库的列名,value为要插入的值
    #                           [
    #                               {column1:value1,column2:value2,...},
    #                               {column1:value1,column2:value2,...},
    #                               ...
    #                           ]
    #           [string] tblname:要插入的表名
    # returns:	bool  标志是否插入成功
    # 调用示例：
    #   rows =  [    {'device_name': 'fake冷机20', 'description': '', 'device_category_id': '1'}, 
    #                {'device_name': 'fake冷机21', 'description': '', 'device_category_id': '1'}]
    #       insert_rows(rows,'jcimate_device_db.tbl_device')
    ################################################################################################/
    def insert_rows(self,rows,tblname):
        try:
            logger.info(rows)
            columns = get_columns_from_row(rows[0])

            all_values = get_values_from_row(rows[0])
            for i in range(1, len(rows)):
                values = get_values_from_row(rows[i])
                all_values = all_values + ',' + values
            logger.info(all_values)
            sql = '''   insert	 into %s  %s values %s
                        ''' % (tblname, columns, all_values)
            logger.info(sql)
            rt = self.queryAll(sql)
            logger.info(rt)
        except Exception as e:
            logger.info(e)
            raise
    def update(self,tableName,pData,whereData):
        try:
            newData=[]
            keys=pData.keys()
            for i in keys:
                item="%s=%s"%(i,"'""'"+pData[i]+"'")
                newData.append(item)
            items=','.join(newData)
            newData2=[]
            keys=whereData.keys()
            for i in keys:
                item="%s=%s"%(i,"'""'"+whereData[i]+"'")
                newData2.append(item)
            whereItems=" AND ".join(newData2)
            sql="update "+tableName+" set "+items+" where "+whereItems
            self.query("set names 'utf8'")
            self.query(sql)
            self.commit()
        except Exception as e:
            self.conn.rollback()
            print('MySql Error: %s %s'%(e.args[0],e.args[1]))
        finally:
            self.close()

    def getLastInsertRowId(self):
        return self.cursor.lastrowid

    def getRowCount(self):
        return self.cursor.rowcount

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    # 移植php的uniqid
    def uniqid(self,pre):
        return str(pre) + hex(int(time.time()))[2:10] + hex(int(time.time()*1000000) % 0x100000)[2:7]

    # 生成guid
    def guid(self):
        uniqid_guid=self.uniqid(random.randint(0,sys.maxsize))
        hl = hashlib.md5()
        hl.update(uniqid_guid.encode(encoding='utf-8'))
        md5=hl.hexdigest()
        guid=md5[0:8]+"-"+md5[8:12]+"-"+md5[12:16]+"-"+md5[16:20]+"-"+md5[20:32]
        print("guid")
        print(guid)
        return guid

    def queryProcedure(self,sql):
        conn = pymysql.connect(host=self.host,database="seed_tenant_db",user=self.user,password=self.password,port = self.port,charset=self.charset)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            print("调用存储过程开始")
            print(sql)
            cursor.execute(sql)
            conn.commit()
            print("调用存储过程完毕")
            success=True
        except Exception as e:
            conn.rollback()
            print(e)
            success=False
        conn.close()
        return success

    def queryProcExport(self,sql):
        #con=self.conn
        cursor=self.cursor
        try:
            cursor.execute(sql)
            resu=cursor.fetchall()
            desc=self.cursor.description
            rows=[]
            for cloumn in resu:
                #print(column)
                row={}
                for i in range(0,len(cloumn)):
                    print(cloumn[i])
                    row[desc[i][0]]=cloumn[i]
                rows.append(row)
            return rows
        except Exception as e:
            logger.info(e)

########################################################################################################
#        brief: 打印log的辅助函数
#        input:  无
#        return: 无 
#         note:     1.log路径由全局变量LOG_DIR变量指定
#                   2.日志级别 ：
#                        日志等级(从高到低)：CRITICAL->ERROR->WARNING->INFO->DEBUG
#                        一旦设置了日志等级，则调用比等级低的日志记录函数则不会输出
########################################################################################################
def get_logger():
    #set up logging to file
    logs_dir = os.path.join(os.path.curdir, "logs")
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass
    else:
        os.mkdir(logs_dir)
    # 向文件输出
    # 仅保留最近三天的日志 
    rotatingFileHandler = logging.handlers.TimedRotatingFileHandler(filename = LOG_DIR, when="D", interval=1, backupCount=3)
    #for test   10创建一个新log文件,最多保留2个问题log文件
    #rotatingFileHandler = logging.handlers.TimedRotatingFileHandler(filename="./logs/log_weather.txt", when="S", interval=10, backupCount=2) 

    formatter = logging.Formatter('%(asctime)s   %(levelname)-8s %(filename)s line: %(lineno)s   [%(funcName)s]   %(message)s')
    rotatingFileHandler.setFormatter(formatter)
    logging.getLogger("").addHandler(rotatingFileHandler)

    # 向屏幕输出
    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s   %(levelname)-8s %(filename)s line: %(lineno)s   [%(funcName)s]   %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    # set initial log level
    logger = logging.getLogger("")
    

    # # 日志等级(从高到低)：CRITICAL->ERROR->WARNING->INFO->DEBUG
    # # 一旦设置了日志等级，则调用比等级低的日志记录函数则不会输出
    logger.setLevel(logging.DEBUG)  ## 调试时可设置为DEBUG

    return logger


############################################################################################### 
# breif :   将dict的keys转为sql格式的字符串(sql列名的形式)
# inputs: 	[dict]    row  =
#      {'attribute_name':xx,'is_complex_attr':xx,'complex_attr_id1':xx,'complex_operate_id':xx,'complex_attr_id2':xx,'description':xx},
# returns:	[str]      (attribute_name,is_complex_attr,complex_attr_id1,complex_operate_id,complex_attr_id2,description)
# note: 
#       要注意我们得到不是('attribute_name','is_complex_attr','complex_attr_id1','complex_operate_id','complex_attr_id2','description')
#       
################################################################################################/
def get_columns_from_row(row):
    columns = '('
    for column in row:
        columns += column + ','
    columns = columns[0:-1] + ')' 
    return columns



############################################################################################### 
# breif :   将dict的keys转为sql格式的字符串(sql列名的形式)
# inputs: 	[list]    pylist ： python的列表 如[1,2]
# returns:	[str]     sqltuple (1,2)
# note: 
#       要注意我们得到不是('1','2')
#       
################################################################################################/
def transList2Sqltuple(pylist):
    sqltuple = '('
    for l in pylist:
        sqltuple += str(l) + ','
    sqltuple = sqltuple[0:-1] + ')' 
    return sqltuple

############################################################################################### 
# breif :   从dict中获取所有value,并转为sql格式的字符串
# inputs: 	[dict]    row  =
#      {'attribute_name':'test2','is_complex_attr':1,'complex_attr_id1':1,'complex_operate_id':1,'complex_attr_id2':1,'description':'COND-AP - COND-AP'}
# returns:	[str]  ('test2',1,1,1,1,'COND-AP - COND-AP')
# note: 
#       None的处理
#       inputs: {'attribute_name':'test1','is_complex_attr':0,'complex_attr_id1':None,'complex_operate_id':None,'complex_attr_id2':None,'description':''},
#       output: ('test1',0,NULL,NULL,NULL,'')
#       
################################################################################################/
def get_values_from_row(row):
    values = '('
    for value in row.values():
        if value  == None:
            value = 'NULL'
        elif isinstance (value,str):
            value = "'" +value+"'"
        values += str(value) + ','
    values = values[0:-1] + ')' 
    return values
    


logger = get_logger()

if __name__ == '__main__':
    # test_row = {'attribute_name':'test1','is_complex_attr':0,'complex_attr_id1':None,'complex_operate_id':None,'complex_attr_id2':None,'description':''}
    # values = get_values_from_row(test_row)
    # print(values)
    pylist = [1]
    print( transList2Sqltuple(pylist) )

