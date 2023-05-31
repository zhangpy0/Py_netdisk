from flask import Flask,render_template_string,redirect,request,session,url_for,send_from_directory
import os
import sys
from werkzeug.utils import secure_filename
import USER

app = Flask(__name__)
app.secret_key = '123456'

@app.route('/')
def index_():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    login_page = '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>登录</title>
            <meta name="description" content="">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="">
        </head>
        <body>
            <h1>Login</h1>
                <form action="{{url_for('login')}}" method="post">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username"><br><br>
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password"><br><br>
                    <input type="submit" value="Submit">
                </form>
                <a href="{{url_for('register')}}">Register</a>
        </body>
    </html>
    '''
    return render_template_string(login_page)

@app.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    print(username)
    print(password)
    user = USER.login(username,password)
    if (user):
        print("login success")
        session['username'] = username
        session['password'] = password
        session['filepath'] = user.filepath
        return redirect(url_for('filelist'))
    else:
        return 'Login Failed'
    
@app.route('/register')
def register():
    register_page = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>注册</title>
    </head>
    <body>
        <h2>注册</h2>
        <form action="{{url_for('do_register')}}" method="post">
            <p>用户名：<input type="text" name="username"></p>
            <p>密码：<input type="password" name="password"></p>
            <p>确认密码：<input type="password" name="password2"></p>
            <p><input type="submit" value="注册"></p>
        </form>
    
        <a href="{{url_for('index')}}">Login</a>
    </body>
    </html>
    '''
    return render_template_string(register_page)

@app.route('/do_register',methods=['POST'])
def do_register():
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if password == password2:
        try:
            user = USER.register(username,password)
            if user:
                print("register success")
                return redirect(url_for('index'))
        except Exception as e:
            return str(e)
        return redirect(url_for('index'))
    else:
        return 'Register Failed'
    
@app.route('/filelist')
def filelist():
    if 'username' in session:
        username = session['username']
        password = session['password']
        filepath = session['filepath']
        user = USER.login(username,password)
        if (os.path.exists(filepath) == False):
            os.mkdir(filepath)
        files = os.listdir(filepath)
        filescount = len(files)
        filelist_page_1 = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title> %s 文件列表</title>
        </head>
        <body>
            <h2> %s 的文件列表</h2>
            <hr>
            <form action="{{url_for('upload')}}" method="post" enctype="multipart/form-data">
                <p>上传文件：<input type="file" name="file"></p>
                <p><input type="submit" value="上传"></p>   
            </form>
            <hr>
            <ul>
            <p>文件数量：%d</p>
        ''' % (username,username,filescount)
        filelist_page_2 = ''''''
        for file in files:
            filelist_page_2 += '<li><a href="{{url_for(\'download\',filename=\'%s\')}}">%s</a></li>\n' % (file,file)
        filelist_page_3 = '''
            </ul>
            <hr>
            <a href="{{url_for('index')}}">Logout</a>
        </body>
        </html>
        '''
        filelist_page = filelist_page_1 + filelist_page_2 + filelist_page_3

        if user:
            user.update()
            return render_template_string(filelist_page)
        else:
            return 'Login Failed'
    else:
        return 'Login Failed'
    
@app.route('/upload',methods=['POST'])
def upload():
    if 'username' in session:
        username = session['username']
        password = session['password']
        filepath = session['filepath']
        user = USER.login(username,password)
        if user:
            user.update()
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(filepath,filename))
            return 'Upload Success'
        else:
            return 'Login Failed'
    else:
        return 'Login Failed'
    
@app.route('/download/<filename>')
def download(filename):
    if 'username' in session:
        username = session['username']
        password = session['password']
        filepath = session['filepath']
        print(filepath)
        user = USER.login(username,password)
        if user:
            user.update()
            return send_from_directory(filepath,filename,as_attachment=True)
        else:
            return 'Login Failed'
    else:
        return 'Login Failed'

if __name__ == '__main__':
    app.run(port=80,debug=False)