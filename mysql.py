import pymysql
import json

config = json.loads(open('config.json').read())

class Mysql:
    def __init__(self) -> None:
        self.db = pymysql.connect(host=config["mysqlhost"],user=config["mysqluser"],
                                  password=config["mysqlpwd"],database=config["mysqldb"],
                                  port=config["mysqlport"])

    def print(self):
        cursor = self.db.cursor()
        cursor.execute("select * from user")
        data = cursor.fetchall()
        print(data)

    def insert(self,username,password,filepath):
        cursor = self.db.cursor()
        sql = "insert into user(username,password,filepath) values('%s','%s','%s')"%(username,password,filepath)
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception("insert error")

    def select(self,username) -> list:
        cursor = self.db.cursor()
        sql = "select * from user where username = '%s'"%(username)
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            data = list(data)
            return data
        except:
            raise Exception("select error")
        
    def delete(self,username):
        cursor = self.db.cursor()
        sql = "delete from user where username = '%s'"%(username)
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            raise Exception("delete error")

    def close(self):
        self.db.close()
        
if __name__ == '__main__':
    mysql = Mysql()
    mysql.delete('6')
    mysql.print()
    mysql.close()
    
