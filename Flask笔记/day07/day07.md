## 58. CSRF攻击与防御

CSRF(Cross Site Request Forgery)跨站域请求伪造是一种网络攻击方式。

### CSRF攻击原理

网站是通过`cookie`来实现登录功能的，而cookie只存在于浏览器中，那么浏览器访问这个cookie的服务器的时候，就会自动携带cookie上去，这时候存在漏洞：如果你访问了一个病毒网站，这个网站可以在源代码中插入js代码，使用js代码给其它服务器发送请求（如银行的转账请求），那么在发送请求的时候，浏览器会自动的携带cookie发送给对应的服务器，这时服务器就不知道这个请求是伪造的，就被欺骗了，从而达到在用户不知情的情况下，给服务器发送了一个请求：比如转账。

### 防御CSRF攻击

CSRF攻击的要点就是在向服务器发送请求的时候，相应的cookie会自动发送给对应的服务器，造成服务器不知道这个请求用户发送的还是伪造的，这时候，每当用户访问表单页面的时候，我们可以在网页源代码中添加一个随机字符串叫`csrf_token`，在cookie中加入一个相同值的csrf_token字符串，以后给服务器发送请求的时候，必须在body中以及cookie中携带csrf_token，服务器只有检测到cookie中的csrf_token和body中的csrf_token相同时，才认为这个请求是正常的。

```python
from flask_wtf import CSRFProtect
CSRFProtect(app)
```

表单页面添加：

```jinja2{
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}" >
```

### AJAX的CSRF保护

在AJAX中要使用csrf保护，则必须手动添加x-CSRFToken到Header中，但是csrf还是需要在模板中渲染，Flask推荐使用meta标签来渲染csrf

```jinja
<meta name="csrf_token" content="{{ csrf_token() }}">
```

如果要使用AJAX请求，则在发送之前添加CSRF，代码如下：

```js
var csrftoken = $('meta[name=csrf_token]').attr('content')
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})
```

把csrf_token放在meta标签中也更容易继承。

#### 封装AJAX

先在页面中添加meta标签

```jinja2
<meta name="csrf_token" content="{{ csrf_token() }}">
```

文件： yajax.js

```js
// 对jquery的ajax的封装

'use strict';
var yajax = {
	'get':function(args) {
		args['method'] = 'get';
		this.ajax(args);
	},
	'post':function(args) {
		args['method'] = 'post';
		this.ajax(args);
	},
	'ajax':function(args) {
		// 设置csrftoken
		this._ajaxSetup();
		$.ajax(args);
	},
	'_ajaxSetup': function() {
		$.ajaxSetup({
			'beforeSend':function(xhr,settings) {
				if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
			}
		});
	}
};
```

```js
// 整个文档都加载完毕后才会执行这个函数
$(function () {
    $('#submit').click(function (event) {
        // 阻止默认的提交表单的行为
        event.preventDefault();
        var email = $('input[name=email]').val();
        var password = $('input[name=password]').val();
        
        yajax.post({
            'url': '/login/',
            'data': {
                'email': email,
                'password': password
            },
            'success': function (data) {
                console.log(data);
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
});
```



## 59. Local线程隔离对象

```python
from werkzeug.local import Local
local = Local()
local.session / local.g / local.request # 这三个都是线程隔离的
```

在Flask中。类似`request`的对象，其实是绑定到了`werkzeug.local.Local`对象上。这样，在多线程中，每个对象都是隔离的。说白了就是，不同用户访问时，数据是独立的。

### Thread Local对象

只要满足绑定到这个对象上的属性，在每个线程中都是隔离的，那么它就叫`Thread Local`对象。



##60. app上下文和request上下文

应用上下文和请求上下文都是存放到一个`LocalStack`的栈中。和应用app相关的操作就必须要用到应用上下文，比如通过`current_app`获取当前的这个`app`。和请求相关的操作就必须用到请求上下文，比如使用`url_for`反转视图函数。
1. 在视图函数中，不用担心上下文的问题。因为视图函数要执行，那么肯定是通过访问url的方式执行的，那么这种情况下，Flask底层就已经自动的帮我们把请求上下文和应用上下文都推入到了相应的栈中。
2. 如果想要在视图函数外面执行相关的操作，比如获取当前的app(current_app)，或者是反转url，那么就必须要手动推入相关的上下文：
    * 手动推入app上下文：
        ```python
        # 第一种方式：
        app_context = app.app_context()
        app_context.push()
        # 第二种方式：
        with app.app_context():
            print(current_app)
        ```
    * 手动推入请求上下文：推入请求上下文到栈中，会首先判断有没有应用上下文，如果没有那么就会先推入应用上下文到栈中，然后再推入请求上下文到栈中：
        ```python
        with app.test_request_context():
            print(url_for('my_list'))
        ```

### 为什么上下文需要放在栈中：
1. 应用上下文：Flask底层是基于werkzeug，werkzeug是可以包含多个app的，所以这时候用一个栈来保存。如果你在使用app1，那么app1应该是要在栈的顶部，如果用完了app1，那么app1应该从栈中删除。方便其他代码使用下面的app。
2. 如果在写测试代码，或者离线脚本的时候，我们有时候可能需要创建多个请求上下文，这时候就需要存放到一个栈中了。使用哪个请求上下文的时候，就把对应的请求上下文放到栈的顶部，用完了就要把这个请求上下文从栈中移除掉。


## 62. 保存全局对象的g对象：

g对象是在整个Flask应用运行期间都是可以使用的。并且他也是跟request一样，是线程隔离的。这个对象是专门用来存储开发者自己定义的一些数据，方便在整个Flask程序中都可以使用。一般使用就是，将一些经常会用到的数据绑定到上面，以后就直接从g上面取就可以了，而不需要通过传参的形式，这样更加方便。

```PYTHON
g.username = username
```



## 63. 常用的钩子函数：

在Flask中钩子函数是使用特定的装饰器装饰的函数。为什么叫做钩子函数呢，是因为钩子函数可以在正常执行的代码中，插入一段自己想要执行的代码。那么这种函数就叫做钩子函数。（hook）
1. `before_first_request`：Flask项目第一次部署后会执行的钩子函数。

2. `before_request`：请求已经到达了Flask，但是还没有进入到具体的视图函数之前调用。一般这个就是在视图函数之前，我们可以把一些后面需要用到的数据先处理好，方便视图函数使用。

3. `context_processor`：使用这个钩子函数，必须返回一个字典。这个字典中的值在所有模版中都可以使用。这个钩子函数的函数是，如果一些在很多模版中都要用到的变量，那么就可以使用这个钩子函数来返回，而不用在每个视图函数中的`render_template`中去写，这样可以让代码更加简洁和好维护。

    ```python
    @app.context_processor
    def context_processor():
      return {"username":"ying"}
    ```

4. `errorhandler`：在发生一些异常的时候，比如404错误，比如500错误。那么如果想要优雅的处理这些错误，就可以使用`errorhandler`来出来。需要注意几点：
    * 在errorhandler装饰的钩子函数下，记得要返回相应的状态码。
    * 在errorhandler装饰的钩子函数中，必须要写一个参数，来接收错误的信息，如果没有参数，就会直接报错。
    * 使用`flask.abort`可以手动的抛出相应的错误，比如开发者在发现参数不正确的时候可以自己手动的抛出一个400错误。
      示例代码如下：

```python
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404
```


## 64. 信号机制及使用场景

Flask信号，安装blinker，blinker是一个第三方插件。一般用于记录日志，如用户一登陆就把相关信息写入文件。

```shell
pip install blinker
```

使用信号分为3步，第一是定义一个信号，第二是监听一个信号，第三是发送一个信号。以下将对这三步进行讲解：

1. 定义信号：定义信号需要使用到blinker这个包的Namespace类来创建一个命名空间。比如定义一个在访问了某个视图函数的时候的信号。示例代码如下：
    ```python
    # Namespace的作用：为了防止多人开发的时候，信号名字冲突的问题
    from blinker import Namespace

    mysignal = Namespace()
    visit_signal = mysignal.signal('visit-signal')
    ```
2. 监听信号：监听信号使用singal对象的connect方法，在这个方法中需要传递一个函数，用来接收以后监听到这个信号该做的事情。示例代码如下：
    ```python
    def visit_func(sender,username):
        print(sender)
        print(username)
    mysignal.connect(visit_func)
    ```
3. 发送信号：发送信号使用singal对象的send方法，这个方法可以传递一些其他参数过去。示例代码如下：
  ```python
  mysignal.send(username='zhiliao')
  ```

## 65. Flask内置的信号：

1. template_rendered：模版渲染完成后的信号。

   ```python
   def template_rendered_func(sender, template, context):
       print('sender', sender)
       print('template', template)
       print('context', context)
   template_rendered.connect(template_rendered_func)

   @app.route('/')
   def index():
       return render_template('index.html')
   ```

   before_render_template：模版渲染之前的信号。

2. request_started：模版开始渲染。

3. request_finished：模版渲染完成。

4. request_tearing_down：request对象被销毁的信号。

5. got_request_exception：视图函数发生异常的信号。一般可以监听这个信号，来记录网站异常信息。

6. appcontext_tearing_down：app上下文被销毁的信号。

7. appcontext_pushed：app上下文被推入到栈上的信号。

8. appcontext_popped：app上下文被推出栈中的信号

9. message_flashed：调用了Flask的`flashed`方法的信号。

- 注： 以下方法可以获取ip地址

  ```python
  from flask import request
  ip = request.remote_addr
  ```

  ​

## 66. Restful API规范

Restful API 是用于前后端通信的一套规范，这个规范可以使得前后端开发更加轻松。

### 协议

采用http或https协议

### 数据传输格式

数据之间传输的格式应该都是用json格式，而不使用xml

### url链接

url链接中，不能有动词，只能由名词，并且名词如果位复数，就要在后面加`s`

### HTTP请求的方法

1. `GET`：从服务器上获取资源
2. `POST`：在服务器上新创建一个资源
3. `PUT`：在服务器上更新资源（客户端提供所有改变后的数据）
4. `PATCH`在服务器上更新资源（客户端只提供需要改变的属性）
5. `DELETE`：从服务器上删除资源

### 状态码

| 状态码  |         原生描述          |                   描述                    |
| :--: | :-------------------: | :-------------------------------------: |
| 200  |          ok           |              服务器成功响应客户端请求               |
| 400  |    invalid request    |       用户发出的请求有误，服务器没有进行新建或修改数据的操作       |
| 401  |     unauthorized      |              用户没有权限访问这个请求               |
| 403  |       forbidden       |             因为某些原因禁止访问这个请求              |
| 404  |       not found       |              用户发送请求的url不存在              |
| 406  |    not acceptable     | 用户请求不被服务器接收（比如服务器期望客户端发送某个字段，但是客户端没有发送） |
| 500  | internal server error |              内部服务器错误，代码错误               |



## 67. Flask-Restful

### 安装：
Flask-Restful需要在Flask 0.8以上的版本，在Python2.6或者Python3.3上运行。通过pip install flask-restful即可安装。

### 基本使用：
1. 从`flask_restful`中导入`Api`，来创建一个`api`对象。
2. 写一个视图函数，让他继承自`Resource`，然后在这个里面，使用你想要的请求方式来定义相应的方法，比如你想要将这个视图只能采用`post`请求，那么就定义一个`post`方法。
3. 使用`api.add_resource`来添加视图与`url`。
  示例代码如下：
```python
class LoginView(Resource):
    def post(self,username=None):
        return {"username":"ying"}

api.add_resource(LoginView,'/login/<username>/','/regist/')
```
注意事项：
* 如果你想返回json数据，那么就使用flask_restful，如果你是想渲染模版，那么还是采用之前的方式，就是`app.route`的方式。
* url还是跟之前的一样，可以传递参数。也跟之前的不一样，可以指定多个url。
* endpoint是用来给url_for反转url的时候指定的。如果不写endpoint，那么将会使用视图的名字的小写来作为endpoint。


### 参数验证：
Flask-Restful插件提供了类似WTForms来验证提交的数据是否合法的包，叫做reqparse。以下是基本用法：
```python
parser = reqparse.RequestParser()
parser.add_argument('username',type=str,help='请输入用户名')
args = parser.parse_args()
```
add_argument可以指定这个字段的名字，这个字段的数据类型等。以下将对这个方法的一些参数做详细讲解： 
1. default：默认值，如果这个参数没有值，那么将使用这个参数指定的值。 
2. required：是否必须。默认为False，如果设置为True，那么这个参数就必须提交上来。 3. type：这个参数的数据类型，如果指定，那么将使用指定的数据类型来强制转换提交上来的值。 
3. choices：选项。提交上来的值只有满足这个选项中的值才符合验证通过，否则验证不通过。 
4. help：错误信息。如果验证失败后，将会使用这个参数指定的值作为错误信息。 
5. trim：是否要去掉前后的空格。

其中的type，可以使用python自带的一些数据类型，也可以使用flask_restful.inputs下的一些特定的数据类型来强制转换。比如一些常用的： 
1. url：会判断这个参数的值是否是一个url，如果不是，那么就会抛出异常。 
2. regex：正则表达式。 
3. date：将这个字符串转换为datetime.date数据类型。如果转换不成功，则会抛出一个异常。

```python
class LoginView(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='用户名验证错误', default='yingjoy')
        parser.add_argument('password', type=str, help='密码验证错误', required=True)
        parser.add_argument('homepage', type=inputs.url, help='homepage验证错误')
        args = parser.parse_args()
        return args
```

对于一个视图函数，你可以指定好一些字段用于返回。以后可以使用ORM模型或者自定义的模型的时候，他会自动的获取模型中的相应的字段，生成json数据，然后再返回给客户端。这其中需要导入flask_restful.marshal_with装饰器。并且需要写一个字典，来指示需要返回的字段，以及该字段的数据类型。示例代码如下：

```python
class ProfileView(Resource):
    resource_fields = {
        'username': fields.String,
        'age': fields.Integer,
        'school': fields.String
    }

    @marshal_with(resource_fields)
    def get(self,user_id):
        user = User.query.get(user_id)
        return user
```
在get方法中，返回user的时候，flask_restful会自动的读取user模型上的username以及age还有school属性。组装成一个json格式的字符串返回给客户端。

### 重命名属性：

很多时候你面向公众的字段名称是不同于内部的属性名。使用 attribute可以配置这种映射。比如现在想要返回user.school中的值，但是在返回给外面的时候，想以education返回回去，那么可以这样写：
```python
resource_fields = {
    'education': fields.String(attribute='high school')
}
```

### 默认值：
在返回一些字段的时候，有时候可能没有值，那么这时候可以在指定fields的时候给定一个默认值，示例代码如下：
```python
resource_fields = {
    'age': fields.Integer(default=18)
}
```

### 复杂结构：
有时候想要在返回的数据格式中，形成比较复杂的结构。那么可以使用一些特殊的字段来实现。比如要在一个字段中放置一个列表，那么可以使用fields.List，比如在一个字段下面又是一个字典，那么可以使用fields.Nested。以下将讲解下复杂结构的用法：
```python
class ArticleView(Resource):

    resource_fields = {
        'aritlce_title':fields.String(attribute='title'),
        'content':fields.String,
        'author': fields.Nested({
            'username': fields.String,
            'email': fields.String
        }),
        'tags': fields.List(fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        })),
        'read_count': fields.Integer(default=10)
    }

    @marshal_with(resource_fields)
    def get(self,article_id):
        article = Article.query.get(article_id)
        return article
```


### Flask-restful注意事项：
1. 在蓝图中，如果使用`flask-restful`，那么在创建`Api`对象的时候，就不要再使用`app`了，而是使用蓝图。
2. 如果在`flask-restful`的视图中想要返回`html`代码，或者是模版，那么就应该使用`api.representation`这个装饰器来定义一个函数，在这个函数中，应该对`html`代码进行一个封装，再返回。示例代码如下：
```python
@api.representation('text/html')
def output_html(data,code,headers):
    print(data)
    # 在representation装饰的函数中，必须返回一个Response对象
    resp = make_response(data)
    return resp

class ListView(Resource):
    def get(self):
        return render_template('index.html')
api.add_resource(ListView,'/list/',endpoint='list')
```