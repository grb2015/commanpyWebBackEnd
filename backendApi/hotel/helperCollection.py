import sqlite3
class sqliteOperate:  
    def __init__(self,dbfile='hotel.sqlite3'): 
        try:  
            self.conn = sqlite3.connect(dbfile)
            self.cursor=self.conn.cursor()  
        except Exception as e: 
            print ('连接数据库出错：')  
            print (e)  
      
    def execute(self,sql):
		rows = self.cursor.execute(sql)
		return rows
def justTest():
	return 'ehie'