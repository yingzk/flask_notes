## 5. Debug模式

- 快速定位错误

- 方便调试

- 保存python文件即重启服务器

  `app.config['DEBUG'] = True` 或者 `app.run(debug=True)`

### 配置Debug模式的四种方式 

1. `app.run(debug=True)`
2. `app.config['DEBUG'] = True`
3. `app.debug = True`
4. `app.config.update(DEBUG=True)`

还可以写在外部文件`config.py`中

导入`config.py`后`app.config.from_object(config)`

注：dict的`update`方法可以追加字典内容

如：

```python
a = {'a':1}
b = {'b': 2}
a.update(b)
结果:
a = {'a': 1, 'b': 2}
```

调试模式还可以直接在网站上进行调试， 错误行的右侧有一个控制台的图标，点击，然后输入PIN码（程序开始运行时会写出），PIN码会自动记住8小时，存放到这个网站的cookies中。



## 6. 配置文件 

用来存放项目的配置文件

### 6.1 使用`app.config.from_object(config)`来加载配置文件

```python
import config
app.config.from_object(config)
```

### 6.2 使用`app.config.from_pyfile('config.py')`来加载配置文件

不需要导入配置文件，直接写配置文件的路径即可**（记得加后缀）**

```
app.config.from_pyfile('config.py', silent=False)
```

这里也可以不是`py`文件，`txt`文件也可以

还有一个`silent`参数，默认为False，如果加载的配置文件不存在，则直接报错，如果改成True，则忽略，不报错。



## 7. URL与视图函数的映射：

### 传递参数：
传递参数的语法是：`/<参数名>/`。然后在视图函数中，也要定义同名的参数。


### 参数的数据类型：
1. 如果没有指定具体的数据类型，那么默认就是使用`string`数据类型。
2. `int`数据类型只能传递`int`类型。
3. `float`数据类型只能传递`float`类型。
4. `path`数据类型和`string`有点类似，都是可以接收任意的字符串，但是`path`可以接收路径，也就是说可以包含斜杠。
5. `uuid`数据类型只能接收符合`uuid`的字符串。`uuid`是一个全宇宙都唯一的字符串，一般可以用来作为表的主键。（长度太长，不方便进行查找）
6. `any`数据类型可以在一个`url`中指定多个路径。例如：
    ```python
    @app.route('/<any(blog, user):url_path>/<id>/')
    def detail(url_path, id):
        if url_path == 'blog':
            return "Blog %s" % id
        if url_path == 'user':
            return "User %s" % id
    ```



### 接收用户传递的参数：
1. 第一种：使用path的形式（将参数嵌入到路径中），就是上面讲的。

2. 第二种：使用查询字符串的方式，就是通过`?key=value`的形式传递的。
    ```python
    @app.route('/d/')
    def d():
        wd = request.args.get('wd')
        return '您通过查询字符串的方式传递的参数是：%s' % wd
    ```

3. 如果你的这个页面的想要做`SEO`优化，就是被搜索引擎搜索到，那么推荐使用第一种形式（path的形式）。如果不在乎搜索引擎优化，那么就可以使用第二种（查询字符串的形式）。

## 8.`url_for()` 

### `url_for`的基本使用：
`url_for`第一个参数，应该是视图函数的名字的字符串。后面的参数就是传递给`url`。
如果传递的参数之前在`url`中已经定义了，那么这个参数就会被当成`path`的形式给
`url`。如果这个参数之前没有在`url`中定义，那么将变成查询字符串的形式放到`url`中。
```python
@app.route('/post/list/<page>/')
def my_list(page):
    return 'my list'

print(url_for('my_list',page=1,count=2))
# 构建出来的url：/my_list/1/?count=2
```

如果一个视图函数上面定义了多个路由，则`url_for()`返回最后一个

### 为什么需要`url_for`：

1. 将来如果修改了`URL`，但没有修改该URL对应的函数名，就不用到处去替换URL了。
2. `url_for`会自动的处理那些特殊的字符，不需要手动去处理。
    ```python
    url = url_for('login',next='/')
    # 会自动的将/编码，不需要手动去处理。
    # url=/login/?next=%2F
    ```

### 强烈建议以后在使用url的时候，使用`url_for`来反转url。



## 9. 自定义URL转换器

```python
from werkzeug.routing import BaseConverter

class TelConverter(BaseConverter):
    """手机号转换器"""
    regex = r'1[85734]\d{9}'

app.url_map.converters['tel'] = TelConverter

@app.route('/tel/<tel:phone>')
def tel(phone):
    return phone
```

### 自定义URL转换器的方式：
1. 实现一个类，继承自`BaseConverter`。
2. 在自定义的类中，重写`regex`，也就是这个变量的正则表达式。
3. 将自定义的类，映射到`app.url_map.converters`上。比如：
    ```python
    app.url_map.converters['tel'] = TelephoneConverter
    ```

### `to_python`的作用：
这个方法的返回值，将会传递到view函数中作为参数。

```python
class PostConverter(BaseConverter):
    def to_python(self, value):
        return value.split('+')

app.url_map.converters['list'] = PostConverter

@app.route('/posts/<list:boards>')
def posts(boards):
    return "boards: %s" % boards
```

### `to_url`的作用：
这个方法的返回值，将会在调用url_for函数的时候生成符合要求的URL形式。

```python
class PostConverter(BaseConverter):
    def to_python(self, value):
        return value.split('+')
    def to_url(self, value):
        return "+".join(value)
      
app.url_map.converters['list'] = PostConverter

@app.route('/')
@app.route('/index/')
def index():
    return url_for('posts', boards=['a', 'b'])
 
最终返回/posts/a+b
```



## 10. 其它细节问题

### 在局域网中让其他电脑访问我的网站：
如果想在同一个局域网下的其他电脑访问自己电脑上的Flask网站，
设置`host='0.0.0.0'`才能访问得到。

`app.run(host='0.0.0.0')`

### 指定端口号：
Flask项目，默认使用`5000`端口。如果想更换端口，那么可以设置`port=9000`。

### url唯一：
在定义url的时候，一定要记得在最后加一个斜杠。
1. 如果不加斜杠，那么在浏览器中访问这个url的时候，如果最后加了斜杠，那么就访问不到。这样用户体验不太好。
2. 搜索引擎会将不加斜杠的和加斜杠的视为两个不同的url。而其实加和不加斜杠的都是同一个url，那么就会给搜索引擎造成一个误解。加了斜杠，就不会出现没有斜杠的情况。

### `GET`请求和`POST`请求：
在网络请求中有许多请求方式，比如：GET、POST、DELETE、PUT请求等。那么最常用的就是`GET`和`POST`请求了。
1. `GET`请求：只会在服务器上获取资源，不会更改服务器的状态。这种请求方式推荐使用`GET`请求。
2. `POST`请求：会给服务器提交一些数据或者文件。一般POST请求是会对服务器的状态产生影响，那么这种请求推荐使用POST请求。
3. 关于参数传递：
    * `GET`请求：把参数放到`url`中，通过`?xx=xxx`的形式传递的。因为会把参数放到url中，所以如果视力好，一眼就能看到你传递给服务器的参数。这样不太安全。
    * `POST`请求：把参数放到`Form Data`中。会把参数放到`Form Data`中，避免了被偷瞄的风险，但是如果别人想要偷看你的密码，那么其实可以通过抓包的形式。因为POST请求可以提交一些数据给服务器，比如可以发送文件，那么这就增加了很大的风险。所以POST请求，对于那些有经验的黑客来讲，其实是更不安全的。
4. 在`Flask`中，`route`方法，默认将只能使用`GET`的方式请求这个url，如果想要设置自己的请求方式，那么应该传递一个`methods`参数。



## 11. 重定向笔记：

重定向分为永久性重定向和暂时性重定向，在页面上体现的操作就是浏览器会从一个页面自动跳转到另外一个页面。比如用户访问了一个需要权限的页面，但是该用户当前并没有登录，因此我们应该给他重定向到登录页面。

* 永久性重定向：`http`的状态码是`301`，多用于旧网址被废弃了要转到一个新的网址确保用户的访问，最经典的就是京东网站，你输入`www.jingdong.com`的时候，会被重定向到`www.jd.com`，因为`jingdong.com`这个网址已经被废弃了，被改成`jd.com`，所以这种情况下应该用永久重定向。

* 暂时性重定向：`http`的状态码是`302`，表示页面的暂时性跳转。比如访问一个需要权限的网址，如果当前用户没有登录，应该重定向到登录页面，这种情况下，应该用暂时性重定向。

### flask中重定向：
`flask`中有一个函数叫做`redirect`，可以重定向到指定的页面。示例代码如下：
```python
from flask import Flask,request,redirect,url_for

app = Flask(__name__)

@app.route('/login/')
def login():
    return '这是登录页面'

@app.route('/profile/')
def profile():
    if request.args.get('name'):
        return '个人中心页面'
    else:
        # redirect 重定向
        return redirect(url_for('login'))
```


## 12. response：

### 视图函数中可以返回哪些值：
1. 可以返回字符串：返回的字符串其实底层将这个字符串包装成了一个`Response`对象。
2. 可以返回元组：元组的形式是(响应体,状态码,头部信息)，也不一定三个都要写，写两个也是可以的。返回的元组，其实在底层也是包装成了一个`Response`对象。
3. 可以返回`Response`及其子类。(这种情况你可以直接设置cookie)


```python
from flask import Response
@app.route('/')
def index():
    response = Response("Index")
    response.set_cookie('a', 1)
    return response
```



### 实现一个自定义的`Response`对象：
1. 继承自`Response`类。
2. 实现方法`force_type(cls,rv,environ=None)`。
3. 指定`app.response_class`为你自定义的`Response`对象。
4. 如果视图函数返回的数据，不是字符串，也不是元组，也不是Response对象，那么就会将返回值传给`force_type`，然后再将`force_type`的返回值返回给前端。

`jsonify` 可以直接将`dict`转换为`json`格式，并且将其包装成一个Response对象



## 13. Jinja2介绍及查找路径

`render_template()`进行模板渲染， 默认从项目根目录下的`templates`文件夹下寻找模板

### 使用其它目录作为模板文件目录

可以查看`Flask(app = Flask(__name__))`的代码

```python
    def __init__(
        self,
        import_name,
        static_url_path=None,
        static_folder='static',
        static_host=None,
        host_matching=False,
        subdomain_matching=False,
        template_folder='templates',
        instance_path=None,
        instance_relative_config=False,
        root_path=None
    ):
```

指定其它目录

```
app = Flask(__name__, template_folder='my_templates')
```

### Jinja2简介

Jinja是日本寺庙的意思，寺庙的英文是temple，和英文的template发音类似。Jinja2是默认的仿Django模板的一个模板引擎，由Flask作者开发。

### Jinja2的特点

- 让开发前后端分离
- 减少Flask代码的耦合性，页面逻辑放在模板中，业务逻辑放在视图函数中，有利于代码的维护
- 提供了控制语句，继承等高级功能，减少开发的复杂度

### 引申： Marko

Marko是一个知名的模板，他从Django和Jinja2等模板中借鉴了很多语法，它的特点：

- 性能和Jinja2相近
- 大型网站在用，如Reddit和豆瓣
- 知名的Web框架支持，Pylons和Pyramid，这两个框架的内置模板就是Marko
- 支持在模板文件中写近乎原生的Python语法代码，对Pythoner比较友好，开发效率高
- 自带完整的缓存系统，也提供了非常好的拓展接口，很容易切换成其他的缓存系统。



## 14. Jinja2模板传参及技巧

```python
@app.route('/index/')
def index():
    dic = {
        'name':'ying',
        'age': 18
    }
    return render_template('index.html', dic=dic)
  	# 或者return render_template('index.html', **dic)
    # 用了**传，则渲染时不需要加dic.name 直接使用name即可
```



## 15. 模板中使用`url_for()`

```html
<a href="{% url_for('login', ref='/') %}">Login</a>
```
```python
@app.route('/')
@app.route('/index/')
def index():
    dic = {
        'name':'ying',
        'age': 18
    }
    return render_template('index.html', dic=dic)

@app.route('/login/')
def login():
    return 'login'
```

`url_for('视图函数名称')`

```
{{ 用于存放变量 }}
{% 用于执行函数和逻辑代码 %}
{# 注释 #}
```



## 16. 过滤器的基本使用

过滤器是通过管道符号（|）进行使用的，例如：`{{ name|length }}`，将返回name的长度。过滤器相当于是一个函数，把当前的变量传入过滤器中，然后根据过滤器自己的功能，在返回相应的值，之后在将结果渲染到页面中。Jinja2内置了很多过滤器

```json
FILTERS = {
    'abs':                  abs,
    'attr':                 do_attr,
    'batch':                do_batch,
    'capitalize':           do_capitalize,
    'center':               do_center,
    'count':                len,
    'd':                    do_default,
    'default':              do_default,
    'dictsort':             do_dictsort,
    'e':                    escape,
    'escape':               escape,
    'filesizeformat':       do_filesizeformat,
    'first':                do_first,
    'float':                do_float,
    'forceescape':          do_forceescape,
    'format':               do_format,
    'groupby':              do_groupby,
    'indent':               do_indent,
    'int':                  do_int,
    'join':                 do_join,
    'last':                 do_last,
    'length':               len,
    'list':                 do_list,
    'lower':                do_lower,
    'map':                  do_map,
    'pprint':               do_pprint,
    'random':               do_random,
    'reject':               do_reject,
    'rejectattr':           do_rejectattr,
    'replace':              do_replace,
    'reverse':              do_reverse,
    'round':                do_round,
    'safe':                 do_mark_safe,
    'select':               do_select,
    'selectattr':           do_selectattr,
    'slice':                do_slice,
    'sort':                 do_sort,
    'string':               soft_unicode,
    'striptags':            do_striptags,
    'sum':                  do_sum,
    'title':                do_title,
    'trim':                 do_trim,
    'truncate':             do_truncate,
    'upper':                do_upper,
    'urlencode':            do_urlencode,
    'urlize':               do_urlize,
    'wordcount':            do_wordcount,
    'wordwrap':             do_wordwrap,
    'xmlattr':              do_xmlattr,
    'tojson':               do_tojson,
}
```

例如
```python
render_template("index.html", position=-9)
```

```jinja2
{{ position | abs }}
{{ sign | default('此人很懒...', boolean=True) }}
```

这里添加`boolean=True`后，即使传进去的参数为None或者空字符串、列表等，也会显示默认值，否则显示None

使用下面的方法也可以替代`{{ default ,boolean=True }}`

```jinja2
{{ sign or "此人很懒..." }}
```

#### 转义过滤器 escape

Jinja2模板会自动转义，把需要渲染的变量中的html符号进行转义

```python
render_template("index.html", sign='<script>alert("hello")</script>')
```

```jinja2
结果为： <script>alert("hello")</script>
```

使用下面语句可以关闭自动转义

```jinja2
{% autoescape off %}
    {{ sign or '此人很懒...' }}
{% endautoescape %}
```

也可以使用`safe`过滤器取消自动转义

```jinja2
{{ sign | safe }}
```

使用多个过滤器直接使用`|`隔开

```jinja2
{{ ['hello', '2'] | first | length }}
```

#### first过滤器

获取到`list`第一条数据

#### last过滤器

获取到`list`最后一条数据

#### format过滤器

格式化字符串

```jinja2
{{ "%s, %s" | format('hello', 'world') }}
```

#### join过滤器

和Python一样，指定分隔符组装`list`

```jinja2
{{ ['1', '2'] | join("+") }}
```

#### int    float    string    lower   upper过滤器

转换整形，浮点型，小写，大写

#### replace过滤器

替换字符串

```jinja2
{{ "abc" | replace('ab', 'a') }}
```

#### wordcount过滤器

计算一个长字符串单词的个数

```jinja2
{{ "This is a very meaningful thing." | wordcount }}    结果是: 6
```

#### truncate过滤器

截取指定长度的字符串

```jinja2
{{ "This is a very meaningful thing." | truncate(10, killwords=True) }}
```

这里如果没有开启killwords，则默认直接到下一个单词接下来的空格的长度才有效。并且，结尾的三个点也要算进去

上面的例子： 

截取This：`{{ "This is a very meaningful thing." | truncate(7) }}`后面还存在3个点

截取is: `{{ "This is a very meaningful thing." | truncate(11) }}`

截取a: `{{ "This is a very meaningful thing." | truncate(13) }}`

#### striptags过滤器

删除字符串中所有的`HTML`标签，如果发现多个空格，则替换为1个

```jinja2
{{ "<p>Good       Job!</p>" | striptags }}
```

结果为: `Good Job!`中间只有一个空格

#### trim过滤器

去除字符串前面和后面的空白字符，如果发现多个空格，则替换为1个

```jinja2
{{ "    Good \t<br>   Job!\t<br>" | striptags }}
```

这里返回: `Good Job!`



## 17. 自定义过滤器

定义过滤器就是定义函数

例如：需求： 删除字符串中所有的hello

```python
@app.template_filter('my_cut')
def cut(value):
    value = value.replace('hello', '')
    return value
```

```jinja2
{{ "hello my hello lady" | my_cut }}
```

设置模板自动重新载入：

```python
app.config['TEMPLATES_AUTO_RELOAD'] = True
```



## 18. 自定义时间过滤器

类似`flask-momment`的功能

```python
@app.template_filter('handle_time')
def handle_time(time):
    """
    1. 距离现在的时间
    2. 如果时间小于1分钟显示刚刚
    3. 如果大于1分钟，小于1小时，显示xx分钟前
    4. 如果大于1小时，小于24小时，显示xx小时前
    5. 如果大于24小时，小于30天，显示xx天之前
    6. 否则显示具体时间
    """
    if isinstance(time, datetime):
        now = datetime.now()
        # 获取两个时间之间相差的秒数
        timestamps = (now - time).total_seconds()
        if timestamps < 60:
            return "刚刚"
        elif timestamps >= 60 and timestamps < 60*60:
            minutes = timestamps / 60
            return "%s分钟前" % int(minutes)
        elif timestamps >= 60*60 and timestamps < 60*60*24:
            hours = timestamps / (60*60)
            return '%s小时前' % int(hours)
        elif timestamps >= 60*60*24 and timestamps < 60*60*24*30:
            days = timestamps / (60*60*24)
            return "%s天以前" % days
        else:
            # return "%s年%s月%s日" % (time.year, time.month, time.day)
            return time.strftime("%Y-%m-%d %H:%M")
    else:
        return time
```

```jinja2
{{ addtime | handle_time }}
```

