from mysql import Mysql
import json

config = json.loads(open('config.json').read())
basefilepath = config["basefilepath"]

class User:
    def __init__(self,username) -> None:
        self.username = username
        self.mysql = Mysql()

    def update(self):
        self.password = self.getPasswd()
        self.filepath = self.getFilePath()

    def getPasswd(self) -> str:
        data = self.mysql.select(self.username)
        return data[0][1]
    
    def getFilePath(self) -> str:
        data = self.mysql.select(self.username)
        return data[0][2]

def login(username,password) -> User:
    user = User(username)
    mysql = Mysql()
    data = mysql.select(username)
    mysql.close()
    if data:
        if data[0][1] == password:
            user.update()
            return user 
        else:
            raise Exception("password error")
    else:
        raise Exception("username error")    

def register(username,password):
    filepath = basefilepath + username
    print(filepath)
    mysql = Mysql()
    data = mysql.select(username)
    if data:
        raise Exception("username exist")
    else:
        mysql.insert(username,password,filepath)
    mysql.close()    

if __name__ == "__main__":
    user = login('6','6')
    print(user.username,user.password,user.filepath)