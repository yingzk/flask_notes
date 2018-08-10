## 1. 课程准备

### 环境

Python 3.6

IDE: PyCharm 2018.2

### 安装虚拟环境

virtualenv

### 安装Flask

`pip install flask`



## 2. 认识Web

### 2.1 URL(Uniform Resource Locator) 统一资源定位符

`scheme://host:port/path/?query-string=xxx#anchor`

- scheme: 代表访问协议，一般为http, https及ftp等
- host: 主机ip或主机名
- port: 端口号，访问网站默认使用80端口
- path: 查找路径，网站文件的路径
- query-string: url携带的参数，参数之间用`&`连接
- anchor: 锚点，一般用于前端页面定位

url种所有的字符都是ascii字符集，如果出现非ascii字符，如中文，会被浏览器先进行编码，再传输。



### 2.2 Web服务器和应用服务器以及Web应用框架 

### web服务器：
负责处理http请求，响应静态文件，常见的有Apache，Nginx以及微软的IIS.

### 应用服务器：
负责处理逻辑的服务器。比如php、python的代码，是不能直接通过nginx这种web服务器来处理的，只能通过应用服务器来处理，常见的应用服务器有uwsgi、tomcat等。

### web应用框架：
一般使用某种语言，封装了常用的web功能的框架就是web应用框架，flask、Django以及Java中的SSH(Structs2+Spring3+Hibernate3)框架都是web应用框架。

![](web服务器+应用服务器+web应用框架.png)



## 3. Flask入门

Flask由多个不同的系列组成：：https://github.com/pallets

### Flask简介

Flask是一款流行的Python Web框架，出生于2010年，作者是Armin Ronacher

### Flask的特点

- 微框架、简洁、拓展性很强
- Flask和相关的依赖（如：Jinja2, Werkzeug）都设计的很好
- 开发效率非常高，比如使用SQLAlchemy的ORM操作数据库可以节省大量书写sql的时间
- 社会活跃度很高

## 4. 第一个Flask程序

```Python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
	return "Hello World!"
  
if __name__ == "__main__":
    app.run(port=8000)
```