# 基于Python flask的简易网盘
## 项目来源：某个python课的结课作业！！！
## 项目功能：
- 用户注册登录
- 文件上传下载
- （可以当靶场用，全是漏洞，以后有时间再改🥰）

## 使用方法：
- 1.clone项目到本地 `git clone https://github.com/zhangpy0/Py_netdisk.git`
- 2.安装依赖 `pip install -r requirements.txt`
- 3.mysql数据库配置
    - 3.1.创建数据库 `create database netdisk;`
    - 3.2.选择数据库 `use netdisk;`
    - 3.3.创建表 `create table user(username varchar(50),password varchar(50),filepath varchar(255));`
    
- 4.修改配置文件 `config.py`
    - 4.1.修改数据库配置 mysqlhost （默认 localhost）,mysqluser（mysql用户名）,mysqlpwd（密码）,mysqldb（数据库名称）,mysqlport （端口 默认3306）
    - 4.2.修改文件路径 filepath （用户文件夹将在这里创建）
- 5.运行项目 `python app.py`

## 感谢支持🥰🥰🥰