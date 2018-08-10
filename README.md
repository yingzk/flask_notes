学习Flask的笔记
加上一个BBS论坛项目

博客： https://www.yingjoy.cn
里面有在线笔记~

笔记1：  https://www.yingjoy.cn/642.html
1-4
笔记2：  https://www.yingjoy.cn/645.html
5-18
笔记3：  https://www.yingjoy.cn/648.html
19-26
笔记4：  https://www.yingjoy.cn/649.html
26-28
笔记5：  https://www.yingjoy.cn/652.html
29-37
笔记6：  https://www.yingjoy.cn/655.html
38-49
笔记7：  https://www.yingjoy.cn/658.html
50-57
笔记8：  https://www.yingjoy.cn/659.html
58-67
笔记9：  https://www.yingjoy.cn/669.html
68-75
笔记10： https://www.yingjoy.cn/678.html
76

## 1. 课程准备
环境
安装虚拟环境
安装Flask
## 2. 认识Web
2.1 URL(Uniform Resource Locator) 统一资源定位符
2.2 Web服务器和应用服务器以及Web应用框架
web服务器：
应用服务器：
web应用框架：
## 3. Flask入门
Flask简介
Flask的特点
## 4. 第一个Flask程序
## 5. Debug模式
配置Debug模式的四种方式
## 6. 配置文件
6.1 使用app.config.from_object(config)来加载配置文件
6.2 使用app.config.from_pyfile('config.py')来加载配置文件
## 7. URL与视图函数的映射：
传递参数：
参数的数据类型：
接收用户传递的参数：
## 8.url_for()
url_for的基本使用：
为什么需要url_for：
强烈建议以后在使用url的时候，使用url_for来反转url
## 9. 自定义URL转换器
自定义URL转换器的方式：
to_python的作用：
to_url的作用：
## 10. 其它细节问题
在局域网中让其他电脑访问我的网站：
指定端口号：
url唯一：
GET请求和POST请求：
## 11. 重定向笔记：
flask中重定向：
## 12. response：
视图函数中可以返回哪些值：
实现一个自定义的Response对象：
## 13. Jinja2介绍及查找路径
使用其它目录作为模板文件目录
Jinja2简介
Jinja2的特点
引申： Marko
## 14. Jinja2模板传参及技巧
## 15. 模板中使用url_for()
## 16. 过滤器的基本使用
## 17. 自定义过滤器
## 18. 自定义时间过滤器
## 19. Jinja2模板中的if语句
## 20. Jinja2模板中的for循环语句
## 21. 案例 - Jinja2实现九九乘法表
## 22. 宏的概念和基本使用方法
导入宏：
## 23. include标签
## 24. set和with语句
## 25. 加载静态文件
## 26. 模板继承
为什么需要模版继承：
模版继承语法：
block语法：
调用父模版代码block中的代码：
调用另外一个block中的代码：
其他注意事项：
## 26. add_url_rule和approute原理解析
add_url_rule(rule,endpoint=None,view_func=None)
app.route(rule,**options)装饰器：
## 27. 类视图
标准类视图：
基于请求方法的类视图：
类视图中的装饰器：
## 28. 蓝图的基本使用
28.1 基本语法：
蓝图实现子域名：
## 29. MySQL数据库
安装：
MySQL Workbench
## 30. SQLAlchemy连接数据库
使用SQLAlchemy连接数据库：
## 31. ORM（Object Relationship Mapping）框架
将ORM模型映射到数据库中：
## 32. ORM中的增删改查
用session做数据的增删改查操作
## 33. SQLAlchemy中常用的数据类型
## 34. Column常用参数
## 35. query函数的参数
## 36. filter过滤条件
## 37. 外键和四种约束
## 38. ORM关系以及一对多：
## 39. 一对一的关系：
## 40. 多对多的关系：
## 41. ORM层面删除数据注意事项
## 42. relationship中的cascade参数
## 43. 三种排序
## 44. limit、offset及切片(slice)操作
## 45. 数据库的懒加载技术
## 46. 高级查询
group_by
having
join
subquery：
## 47. Flask-SQLAlchemy
安装：
数据库连接：
创建ORM模型：
将ORM模型映射到数据库：
使用session：
查询数据：
## 48. alembic数据库迁移工具
安装
常用命令：
经典错误：
## 49. flask-sqlalchemy中配置alembic
## 50. Flask-Script
命令的添加方式：
## 51. 项目中的循环引用问题
## 52. Flask-Migrate
安装：
在manage.py中的代码：
flask_migrate常用命令：
## 53. Flask-WTF
做表单验证：
常用的验证器：
自定义验证器：
## 54. 使用WTForms渲染模板
## 55. 文件上传
## 56. 使用flask_wtf对上传文件使用表单验证：
## 57. Cookie和Session
什么是cookie：
flask操作cookie：
session：
flask操作session：
## 58. CSRF攻击与防御
CSRF攻击原理
防御CSRF攻击
AJAX的CSRF保护
## 59. Local线程隔离对象
Thread Local对象
## 60. app上下文和request上下文
为什么上下文需要放在栈中：
## 62. 保存全局对象的g对象：
## 63. 常用的钩子函数：
## 64. 信号机制及使用场景
## 65. Flask内置的信号：
## 66. Restful API规范
协议
数据传输格式
url链接
HTTP请求的方法
状态码
## 67. Flask-Restful
安装：
基本使用：
参数验证：
重命名属性：
默认值：
复杂结构：
Flask-restful注意事项：
## 68. Memcached
## 69. Memcached的安装和启动
## 70. Memcached 的参数
## 71. 使用Telnet操作memcached
1. 添加数据
2. 获取数据
3. 删除数据
  其它
## 72. 使用Python操作Memcached
1. 安装python-memcached
2. 建立连接
3. 设置数据
4. 获取数据
5. 删除数据
6. 自增
7. 自减
## 73. Memcached的安全机制
## 74. Redis
1. Redis的使用场景
2. Redis和Memcached的比较
3. Redis的安装
4. Redis的操作
5. 操作列表
6. 操作集合(set)
7. 操作哈希(hash)
8. 事务操作
9. 发布/订阅操作
10. 数据持久化
11. 给redis指定密码
12. 其他机器连接redis
## 75. Python操作Redis
安装
建立连接
对字符串进行操作
对列表进行操作
事务（管道）操作
发布与订阅
## 76. 部署
在开发机上做准备
在服务器上的准备工作
安装uwsgi
编写uwsgi配置文件：
安装nginx：
收集静态文件：
编写nginx配置文件：
使用supervisor配置：	
nginx+uwsgi+supervisor关系图
