## 29. MySQL数据库

### 安装：

见当前目录下的`MySQL安装详解.doc`

###MySQL Workbench 

MySQL Workbench是一款专为MySQL设计的ER/数据库建模工具。它是著名的数据库设计工具DBDesigner4的继任者。你可以用MySQL Workbench设计和创建新的数据库图示，建立数据库文档，以及进行复杂的MySQL 迁移。

具体使用可以参考：https://blog.csdn.net/soulandswear/article/details/60966808



## 30. SQLAlchemy连接数据库

在Python3中直接安装`pymysql`， Python2中使用`MySQLdb`

### 使用SQLAlchemy连接数据库：
使用SQLALchemy去连接数据库，需要使用一些配置信息，然后将他们组合成满足条件的字符串：
```python
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'test'
USERNAME = 'root'
PASSWORD = 'root'

# dialect+driver://username:password@host:port/database
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD,host=HOSTNAME,port=PORT,db=DATABASE)
```
然后使用`create_engine`创建一个引擎`engine`，然后再调用这个引擎的`connect`方法，就可以得到这个对象，然后就可以通过这个对象对数据库进行操作了：
```python
engine = create_engine(DB_URI)

with engine.connect() as con:
  rs = con.execute("SELECT 1")
  print(rs.fetchone())
```


## 31. ORM（Object Relationship Mapping）框架

ORM是对象关系映射，也就是对象模型与数据库表之间的映射

### 将ORM模型映射到数据库中：
1. 用`declarative_base`根据`engine`创建一个ORM基类。

2. 用这个`Base`类作为基类来写自己的ORM类。要定义`__tablename__`类属性，来指定这个模型映射到数据库中的表名。

3. 创建属性来映射到表中的字段，所有需要映射到表中的属性都应该为Column类型

4. 使用`Base.metadata.create_all()`来将模型映射到数据库中。

5. 一旦使用`Base.metadata.create_all()`将模型映射到数据库中后，即使改变了模型的字段，也不会重新映射了。

   如果你想要让他重新映射，在前面加`Base.metadata.drop_all()`或者使用后面的`alembic`或`flask-migrate。`

在这个ORM模型中创建一些属性，来跟表中的字段进行一一映射。这些属性必须是sqlalchemy给我们提供好的数据类型。

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

DB_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8"

engine = create_engine(DB_URI)

# 这个函数返回元类(MetaClass)
Base = declarative_base(engine)

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)

Base.metadata.create_all()
```

## 32. ORM中的增删改查

### 用session做数据的增删改查操作：
1. 构建session对象：所有和数据库的ORM操作都必须通过一个叫做`session`的会话对象来实现，通过以下代码来获取会话对象：
    ```python
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(DB_URI)
    session = sessionmaker(engine)()
    ```
    注意`session = sessionmaker(engine)()`后面还有一对括号

2. 添加对象：

    * 创建对象，也即创建一条数据：
        ```python
        p = Person(name='ying',age=18,country='china')
        ```
    * 将这个对象添加到`session`会话对象中：
        ```python
        session.add(p)
        ```
    * 将session中的对象做commit操作（提交）：
        ```python
        session.commit()
        ```
    * 一次性添加多条数据：
        ```python
        p1 = Person(name='ying1',age=19,country='china')
        p2 = Person(name='ying2',age=20,country='usa')
        session.add_all([p1,p2])
        session.commit()
        ```

3. 查找对象：
    ```python
    # 查找某个模型对应的那个表中所有的数据：
    all_person = session.query(Person).all()
    # 使用filter_by来做条件查询
    all_person = session.query(Person).filter_by(name='ying').all()
    # 使用filter来做条件查询
    all_person = session.query(Person).filter(Person.name=='ying').all()
    # 使用get方法查找数据，get方法是根据id来查找的，只会返回一条数据或者None
    person = session.query(Person).get(primary_key)
    # 使用first方法获取结果集中的第一条数据
    person = session.query(Person).first()
    ```

4. 修改对象：首先从数据库中查找对象，然后将这条数据修改为你想要的数据，最后做commit操作就可以修改数据了。
    ```python
    person = session.query(Person).first()
    person.name = 'ying'
    session.commit()
    ```

5. 删除对象：将需要删除的数据从数据库中查找出来，然后使用`session.delete`方法将这条数据从session中删除，最后做commit操作就可以了。
    ```python
    person = session.query(Person).first()
    session.delete(person)
    session.commit()
    ```



## 33. SQLAlchemy中常用的数据类型

1. Integer：整形，映射到数据库中是int类型。

2. Float：浮点类型，映射到数据库中是float类型。32位。

3. Double：双精度浮点类型，映射到数据库中是double类型，64位。

4. String：可变字符类型，映射到数据库中是varchar类型.

5. Boolean：布尔类型，映射到数据库中的是tinyint类型。

6. DECIMAL：定点类型。是专门为了解决浮点类型精度丢失的问题的。在存储钱相关的字段的时候建议大家都使用这个数据类型。并且这个类型使用的时候需要传递两个参数，第一个参数是用来标记这个字段总能能存储多少个数字，第二个参数表示小数点后有多少位。

    例如，我要存，6位整数，4位小数：`Column(DECIMAL(10, 4))`，如果插入数据的时候数据不在改范围内，报错。

7. Enum：枚举类型。指定某个字段只能是枚举中指定的几个值，不能为其他值。在ORM模型中，使用Enum来作为枚举，示例代码如下：
    ```python
    class Article(Base):
        __tablename__ = 'article'
        id = Column(Integer,primary_key=True,autoincrement=True)
        tag = Column(Enum("python",'flask','django'))
    ```
    在Python3中，已经内置了enum这个枚举的模块，我们也可以使用这个模块去定义相关的字段。示例代码如下：
    ```python
    class TagEnum(enum.Enum):
        python = "python"
        flask = "flask"
        django = "django"

    class Article(Base):
        __tablename__ = 'article'
        id = Column(Integer,primary_key=True,autoincrement=True)
        tag = Column(Enum(TagEnum))

    article = Article(tag=TagEnum.flask)
    ```


8. Date：存储时间，只能存储年月日。映射到数据库中是date类型。在Python代码中，可以使用`datetime.date`来指定。示例代码如下：
    ```python
    class Article(Base):
        __tablename__ = 'article'
        id = Column(Integer,primary_key=True,autoincrement=True)
        create_time = Column(Date)

    article = Article(create_time=date(2018,10,10))
    ```
9. DateTime：存储时间，可以存储年月日时分秒毫秒等。映射到数据库中也是datetime类型。在Python代码中，可以使用`datetime.datetime`来指定。示例代码如下：
    ```python
    class Article(Base):
        __tablename__ = 'article'
        id = Column(Integer,primary_key=True,autoincrement=True)
        create_time = Column(DateTime)

    article = Article(create_time=datetime(2011,11,11,11,11,11))
    ```
10. Time：存储时间，可以存储时分秒。映射到数据库中也是time类型。在Python代码中，可以使用`datetime.time`来至此那个。示例代码如下：
  ```python
  class Article(Base):
      __tablename__ = 'article'
      id = Column(Integer,primary_key=True,autoincrement=True)
      create_time = Column(Time)

  article = Article(create_time=time(hour=11,minute=11,second=11))
  ```
11. Text：存储长字符串。一般可以存储6W多个字符。如果超出了这个范围，可以使用LONGTEXT类型。映射到数据库中就是text类型。
12. LONGTEXT：长文本类型，映射到数据库中是longtext类型。



## 34. Column常用参数

1. primary_key：设置某个字段为主键。
2. autoincrement：设置这个字段为自动增长的。
3. default：设置某个字段的默认值。在发表时间这些字段上面经常用。
4. nullable：指定某个字段是否为空。默认值是True，就是可以为空。
5. unique：指定某个字段的值是否唯一。默认是False。
6. onupdate：更新数据的时候调用，常用案例：修改文章时间，修改了文章，就默认把当前时间设置为now，update_time`（每次更新数据的时候都要更新的值）， **第一次插入数据的时候不会被调用。**可以使用default设置初始默认值
7. name：指定ORM模型中某个属性映射到表中的字段名。如果不指定，那么会使用这个属性的名字来作为字段名。如果指定了，就会使用指定的这个值作为参数。这个参数也可以当作位置参数，在第1个参数来指定。
    ```python
    title = Column(String(50),name='title',nullable=False)
    title = Column('my_title',String(50),nullable=False)
    ```



## 35. `query`函数的参数

1. 模型对象。指定查找这个模型中所有的对象。

2. 模型中的属性。可以指定只查找某个模型的其中几个属性。

3. 聚合函数。
    * `func.count`：统计行的数量。

      ```python
      session.query(func.count(Article.price)).first()
      ```

    * `func.avg`：求平均值。

      ```python
      session.query(func.avg(Article.price)).first()
      ```

    * `func.max`：求最大值。

    * `func.min`：求最小值。

    * `func.sum`：求和。
      `func`上，其实没有任何聚合函数。但是因为他底层做了一些魔术，**只要mysql中有的聚合函数，都可以通过`func`调用。**

* **注： 重写类的`__repr__`函数可以自定义类的返回**

```python
def __repr__(self):
  return 'Title: %s' % self.title
返回： Title: xxx
```



## 36. filter过滤条件

过滤是数据提取的一个很重要的功能，以下对一些常用的过滤条件进行解释，并且这些过滤条件都是只能通过filter方法实现的：

1. equals：
    ```python
    article = session.query(Article).filter(Article.title == "title0").first()
    print(article)
    ```
2. not equals:
    ```python
    query.filter(User.name != 'ed')
    ```
3. like：  （ilike：不区分大小写）
    ```python
    query.filter(User.name.like('%ed%'))
    ```

4. in：
    ```python
    query.filter(User.name.in_(['ed','wendy','jack']))
    # 同时，in也可以作用于一个Query
    query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%'))))
    ```

5. not in：
    ```python
    query.filter(~User.name.in_(['ed','wendy','jack']))
    query().filter(User.name.notin_(['ed','wendy','jack']))
    ```
6.  is null：
    ```python
    query.filter(User.name==None)
    # 或者是
    query.filter(User.name.is_(None))
    ```

7. is not null:
    ```python
    query.filter(User.name != None)
    # 或者是
    query.filter(User.name.isnot(None))
    ```

8. and：
    ```python
    from sqlalchemy import and_
    query.filter(and_(User.name=='ed',User.fullname=='Ed Jones'))
    # 或者是传递多个参数
    query.filter(User.name=='ed',User.fullname=='Ed Jones')
    # 或者是通过多次filter操作
    query.filter(User.name=='ed').filter(User.fullname=='Ed Jones')
    ```

9. or：
    ```python
    from sqlalchemy import or_ query.filter(or_(User.name=='ed',User.name=='wendy'))
    ```

如果想要查看`ORM`底层转换的`SQL`语句，可以在filter方法后面不要再执行任何方法直接打印就可以看到了。比如：
```python
articles = session.query(Article).filter(or_(Article.title=='abc',
                                             Article.content=='abc'))
    print(articles)
```
- **注： 如果想得到查找的SQL语句，直接返回`filter`即可，不需要在后面加`first()`或`all()`**



## 37. 外键和四种约束

使用SQLAlchemy创建外键非常简单。在从表中增加一个字段，指定这个字段外键的是哪个表的哪个字段就可以了。**从表中外键的字段，必须和父表的主键字段类型保持一致。**
示例：
```python
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(50),nullable=False)

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(50),nullable=False)
    content = Column(Text,nullable=False)

    uid = Column(Integer,ForeignKey("user.id"))
```
外键约束有以下几项： 
1. RESTRICT：父表数据被删除，会阻止删除。默认就是这一项。 
2. NO ACTION：在MySQL中，同RESTRICT。 
3. CASCADE：级联删除。 父删子删
4. SET NULL：父表数据被删除，子表数据会设置为NULL。**注意：字段属性不能有nullable=False**
```python
id = Column(Integer, ForeignKey("user.id", ondelete="RESTRICT"))
```

- **注：如果要使用外键，则数据库的引擎必须为： `InnoDB`**