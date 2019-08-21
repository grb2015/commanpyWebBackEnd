import sqlite3
import os
import logging
from logging.handlers import TimedRotatingFileHandler

HOTEL_LOG_DIR = './logs/hotelLogs.txt'  #在manager.py目录下的logs

########################################################################################################
#        brief: sqlite3的辅助class
#        input:
#        returns:    
########################################################################################################
class sqliteOperate:  
    def __init__(self,dbfile='hotel.sqlite3'): 
        try:  
            self.conn = sqlite3.connect(dbfile)
            self.cursor=self.conn.cursor()  
        except Exception as e: 
            print ('连接数据库出错：')  
            print (e)  
      
    def select(self,sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()  
        return rows


########################################################################################################
#        brief: 打印log的辅助函数
#        input:  无
#        return: 无 
#         note:     1.log路径由全局变量HOTEL_LOG_DIR变量指定
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
    rotatingFileHandler = logging.handlers.TimedRotatingFileHandler(filename = HOTEL_LOG_DIR, when="D", interval=1, backupCount=3)
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
logger = get_logger()