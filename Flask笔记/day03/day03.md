## 19. Jinja2模板中的`if`语句

`if`条件判断语句必须放在`{% if statement %}`中间，并且还必须有结束的标签`{% endif %}`。和`python`中的类似，可以使用`>，<，<=，>=，==，!=`来进行判断，也可以通过`and，or，not，()`来进行逻辑合并操作。

```jinja2
{% if statement %}
{% elif statement %}
{% else %}
{% endif %}
```



## 20. Jinja2模板中的`for`循环语句

在`jinja2`中的`for`循环，跟`python`中的`for`循环基本上是一模一样的。也是`for...in...`的形式。并且也可以遍历所有的序列以及迭代器。但是唯一不同的是，**`jinja2`中的`for`循环没有`break`和`continue`语句。**

```jinja2
{% for statement %}
{% else %}
{% endfor %}
```

如果`for`语句里面不执行的时候，则运行else里面的语句

可以使用以下变量来获取当前遍历的状态：

| 变量            | 描述                     |
| ------------- | ---------------------- |
| loop.index    | 当前迭代的索引（从1开始）          |
| loop.index0   | 当前迭代的索引（从0开始）          |
| loop.reindex  | 反向 当前迭代的索引（从1开始）       |
| loop.reindex0 | 反向 当前迭代的索引（从0开始）       |
| loop.first    | 是否第一次迭代，返回True或False   |
| loop.last     | 是否是最后一次迭代，返回True或False |
| loop.length   | 序列的长度                  |



## 21. 案例 - Jinja2实现九九乘法表

```jinja2
<table border="1">
    <tbody>
        {% for i in range(1, 10) %}
            <tr>
                {% for j in range(1, 10) if j < i %}
				<td>{{ j }} * {{ i }} = {{ i*j }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>
```



## 22. 宏的概念和基本使用方法

类似Python中的函数,可以传递参数，但是不能有返回值，可以将一些经常用到的代码片段放到宏中，然后把一些不固定的值抽取出来当成一个变量。
使用宏的时候，参数可以为默认值。相关示例代码如下：

1. 定义宏：
    ```html
    {% macro input(name, value='', type='text') %}
    <input type="{{ type }}" name="{{ name }}" value="{{
    value }}">
    {% endmacro %}
    ```
2. 使用宏：
    ```html
    <p>{{ input('username') }}</p>
    <p>{{ input('password', type='password') }}</p>
    ```

### 导入宏：
1. `import "宏文件的路径" as xxx`。
2. `from '宏文件的路径' import 宏的名字 [as xxx]`。
3. 宏文件路径，不要以相对路径去寻找，都要以`templates`作为绝对路径去找。
4. 如果想要在导入宏的时候，就把当前模版的一些参数传给宏所在的模版，那么就应该在导入的时候使用`with context`。示例：`from 'xxx.html' import input with context`。

单独使用import时必须使用as给宏文件重命名。

引入templates目录下的文件路径时，均是相对templates的绝对路径。

宏文件无法获取从视图函数中传递的变量，若需要获取这些变量，则导入的时候应该加上`with context`

```jinja2
from 'macros/macros.html' import input with context
```



## 23. `include`标签

相当于把另外一个模板文件的内容复制粘贴过来。

1.html

```jinja2
<p>1. Hello World!</p>

{% include '2.html' %}
```

2.html

```jinja2
<p>2. Hello World!</p>
```

结果：

```jinja2
1. Hello World!
2. Hello World!
```

1. 这个标签相当于是直接将指定的模版中的代码复制粘贴到当前位置。
2. `include`标签，如果想要使用父模版中的变量，直接用就可以了，不需要使用`with context`。
3. `include`的路径，也是跟`import`一样，直接从`templates`根目录下去找，不要以相对路径去找。



## 24. `set`和`with`语句

`set`设置全局变量，include调用的模板中也可以使用

```jinja2
{% set 变量=xxx %}
调用： {{ 变量 }}
```

with设置局部变量，变量生存周期仅局限于with代码块

```jinja2
{% with %}
    {% set b= 5 %}
    {{ b }}
{% endwith %}
```

超过变量生存区域就无法调用，jinja2最终渲染空白



## 25. 加载静态文件

静态文件： css  js   图片  视频  字体等等。

加载静态文件使用的是`url_for`函数。然后第一个参数需要为`static`，第二个参数需要为一个关键字参数`filename='路径'`。示例：

```jinja2
​```html
{{ url_for("static",filename='xxx') }}
​```
```
路径查找，要以当前项目的`static`目录作为根目录。

如果要更改路径，可以参考之前修改templates文件夹



## 26. 模板继承

### 为什么需要模版继承：
模版继承可以把一些公用的代码单独抽取出来放到一个父模板中。以后子模板直接继承就可以使用了。这样可以重复性的代码，并且以后修改起来也比较方便。

### 模版继承语法：
使用`extends`语句，来指明继承的父模板。父模板的路径，也是相对于`templates`文件夹下的绝对路径。示例代码如下：
`{% extends "base.html" %}`。

### block语法：
一般在父模版中，定义一些公共的代码。子模板可能要根据具体的需求实现不同的代码。这时候父模版就应该有能力提供一个接口，让父模板来实现。从而实现具体业务需求的功能。
在父模板中：
```html
{% block block的名字 %}
{% endblock %}
```
在子模板中：
```html
{% block block的名字 %}
子模板中的代码
{% endblock %}
```

### 调用父模版代码block中的代码：
默认情况下，子模板如果实现了父模版定义的block。那么子模板block中的代码就会覆盖掉父模板中的代码。如果想要在子模板中仍然保持父模板中的代码，那么可以使用`{{ super() }}`来实现。示例如下：
父模板：
```html
{% block body_block %}
        <p style="background: red;">这是父模板中的代码</p>
    {% endblock %}
```
子模板：
```html
{% block body_block %}
    {{ super() }}
    <p style="background: green;">我是子模板中的代码</p>
{% endblock %}
```

可以使用`{{ super() }}`来继承父模板中的代码

### 调用另外一个block中的代码：

如果想要在另外一个模版中使用其他模版中的代码。那么可以通过`{{ self.其他block名字() }}`就可以了。示例代码如下：
```html
{% block title %}
    课堂首页
{% endblock %}

{% block body_block %}
    {{ self.title() }}
    <p style="background: green;">我是子模板中的代码</p>
{% endblock %}
```

### 其他注意事项：
1. 子模板中的代码，第一行，应该是`extends`。
2. 子模板中，如果要实现自己的代码，应该放到block中。如果放到其他地方，那么就不会被渲染。




## 26. `add_url_rule`和`approute`原理解析

### `add_url_rule(rule,endpoint=None,view_func=None)`
这个方法用来添加url与视图函数的映射。如果没有填写`endpoint`，那么默认会使用`view_func`的名字作为`endpoint`。以后在使用`url_for`的时候，**endpoint可以不写，如果不写，则默认使用视图函数的名字**。

```python
def my_list():
    return 'list'

app.add_url_rule('/list/', endpoint='xxx', view_func=my_list)
```

此处的endpoint用于`url_for()`，当添加自定义规则后，必须使用endpoint定义的名称才可以访问。

```python
@app.route('/', endpoint='index')
def index():
    return redirect(url_for('xxx'))
```

否则报错：`werkzeug.routing.BuildError`

### `app.route(rule,**options)`装饰器：

这个装饰器底层，其实也是使用`add_url_rule`来实现url与视图函数映射的。



## 27. 类视图

### 标准类视图：
1. 标准类视图，必须继承自`flask.views.View`.
2. 必须实现`dipatch_request`方法，以后请求过来后，都会执行这个方法。这个方法的返回值就相当于是之前的函数视图一样。也必须返回`Response`或者子类的对象，或者是字符串，或者是元组。
3. 必须通过`app.add_url_rule(rule,endpoint,view_func)`来做url与视图的映射。`view_func`这个参数，需要使用类视图下的`as_view`类方法类转换：`ListView.as_view('list')`。
4. 如果指定了`endpoint`，那么在使用`url_for`反转的时候就必须使用`endpoint`指定的那个值。如果没有指定`endpoint`，那么就可以使用`as_view(视图名字)`中指定的视图名字来作为反转。
5. 类视图有以下好处：可以继承，把一些共性的东西抽取出来放到父视图中，子视图直接拿来用就可以了。但是也不是说所有的视图都要使用类视图，这个要根据情况而定。

```python
class ListView(View):
    def dispatch_request(self):
        return 'list view'

# ListView.as_view('list') 把类转为函数，并添加函数名
app.add_url_rule('/list/', endpoint='list', view_func=ListView.as_view('list'))

@app.route('/')
def index():
    return redirect(url_for('list'))
```

### 基于请求方法的类视图：
1. 基于方法的类视图，是根据请求的`method`来执行不同的方法的。如果用户是发送的`get`请求，那么将会执行这个类的`get`方法。如果用户发送的是`post`请求，那么将会执行这个类的`post`方法。其他的method类似，比如`delete`、`put`。
2. 这种方式，可以让代码更加简洁。所有和`get`请求相关的代码都放在`get`方法中，所有和`post`请求相关的代码都放在`post`方法中。就不需要跟之前的函数一样，通过`request.method == 'GET'`。

```python
class LoginView(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        return "%s, %s" % (username, pwd)

app.add_url_rule('/login/', view_func=LoginView.as_view('login'))
```

### 类视图中的装饰器：
1. 如果使用的是函数视图，那么自己定义的装饰器必须放在`app.route`下面。否则这个装饰器就起不到任何作用。
2. 类视图的装饰器，需要重写类视图的一个类属性`decorators`，这个类属性是一个列表或者元组都可以，里面装的就是所有的装饰器。

```python
class ListView(View):
  	decorators = [xxx, xxx]
    def dispatch_request(self):
        return 'list view'
app.add_url_rule('/list/', view_func=ListView.as_view('list'))
```

## 28. 蓝图的基本使用

蓝图的作用就是让我们的Flask项目更加模块化，结构更加清晰。可以将相同模块的视图函数放在同一个蓝图下，同一个文件中，方便管理。

### 28.1 基本语法：
在蓝图文件中导入Blueprint：
```python
from flask import Blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')
```
`url_predix`后面不要加`/`如果加了，之后的视图路由名称之前不要加`/`

在主app文件中注册蓝图：


```python
from blueprints.user import user_bp
app.regist_blueprint(user_bp)
```

如果想要某个蓝图下的所有url都有一个url前缀，那么可以在定义蓝图的时候，指定url_prefix参数：

```python
user_bp = Blueprint('user',name,url_prefix='/user/')
```
在定义url_prefix的时候，要注意后面的斜杠，如果给了，那么以后在定义url与视图函数的时候，就不要再在url前面加斜杠了。

之后访问域名： `127.0.0.1:5000/user/xxx`

1. 蓝图模版文件的查找：
    如果项目中的templates文件夹中有相应的模版文件，就直接使用了。
    如果项目中的templates文件夹中没有相应的模版文件，那么就到在定义蓝图的时候指定的路径中寻找。并且蓝图中指定的路径可以为相对路径，相对的是当前这个蓝图文件所在的目录。比如：
    ```python
    news_bp = Blueprint('news',__name__,url_prefix='/news',template_folder='bp_templates')
    ```
    **这里模板文件的相对路径是相对蓝图文件的路径，这里蓝图文件路径在blueprints中所以，最终该蓝图模板文件在项目目录下的blueprints目录下的bp_templates中**

    因为这个蓝图文件是在blueprints/news.py，那么就会到blueprints这个文件夹下的bp_templates文件夹中寻找模版文件。

2. 蓝图中静态文件的查找规则：
    在模版文件中，加载静态文件，如果使用url_for('static')，那么就只会在app指定的静态文件夹目录下查找静态文件。
    如果在加载静态文件的时候，指定的蓝图的名字，比如`news.static`，那么就会到这个蓝图指定的static_folder下查找静态文件。

3. url_for反转蓝图中的视图函数为url：
    如果使用蓝图，那么以后想要反转蓝图中的视图函数为url，那么就应该在使用url_for的时候指定这个蓝图。比如`news.news_list`。否则就找不到这个endpoint。在模版中的url_for同样也是要满足这个条件，就是指定蓝图的名字。
    即使在同一个蓝图中反转视图函数，也要指定蓝图的名字。

### 蓝图实现子域名：
1. 使用蓝图技术。
2. 在创建蓝图对象的时候，需要传递一个`subdomain`参数，来指定这个子域名的前缀。例如：`cms_bp = Blueprint('cms',__name__,subdomain='cms')`。
3. **必需要在主app文件中，需要配置app.config的SERVER_NAME参数。**例如：
    ```python
    app.config['SERVER_NAME'] = 'test.com:5000'
    ```
    * ip地址不能有子域名。
    * localhost也不能有子域名。
4. 在`C:\Windows\System32\drivers\etc`下，找到hosts文件，然后添加域名与本机的映射。例如：
    ```python
    127.0.0.1   test.com
    127.0.0.1   test.jd.com
    ```
    域名和子域名都需要做映射。