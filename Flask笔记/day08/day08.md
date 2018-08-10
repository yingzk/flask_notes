## 68. Memcached

Memcached是一个高性能的**分布式**的**内存对象**缓存系统，用来分担数据库的压力。Memcached可以存储各种各样的数据，包括图像，视频，文件以及数据库检索的结果等等，简单来说就是**将数据存储到内存中，然后再从内存中读取，从而大大提高读取速度。**实际是不会将二进制文件直接存储到Memcached中的，只存储二进制文件的路径。

Memcached经常被用于以下情况：存储验证码、图形验证码、短信验证码、登录session等所有不是至关重要的数据。



## 69. Memcached的安装和启动

Windows: （尽量使用管理员模式来安装）

不在管理员下运行会报错：

`failed to install service or service already installed`

如果出现提示信息，缺失pthreadGC2.dll文件，将其拷贝到`C:\Windows\System32`下即可0

参考和文件下载：https://commaster.net/content/installing-memcached-windows

memcached没有提供windows下的安装包，需要自己编译

- 安装： `memcached.exe -d install`
- 启动： `memcached.exe -d start`

Linux(Ubuntu):

- 安装： `sudo apt-get install memcached`
- 启动： `sudo service memcached start`

Linux如果想要指定参数，就不能使用上面的方式启动，而应该使用下面的方法来运行

```shell
/usr/bin/memcached 参数(需要指定-u 用户)
如：
/usr/bin/memcached -u memcached -m 1024 -p 11212 -d start
```



## 70. Memcached 的参数

- `-d` 这个参数是让memcached在后台运行
- `-m` 指定占用多少内存，以M为单位，默认64M
- `-p` 指定占用端口，默认使用11211端口
- `-l` 其它机器可以通过哪个ip地址连接本机的memcached，如果Linux使用service方式启动的话，那么只有本机可以访问，其他机器不行，如果需要其他机器访问，则设置参数`-l`为`0.0.0.0`



## 71. 使用Telnet操作memcached

语法：

```shell
telnet ip port
如：
telnet 127.0.0.1 11211
------------------------------------
set username 0 60 3		# 60:过期时间  3:长度
abc
------------------------------------
get username
```



### 1. 添加数据

参考：https://blog.csdn.net/codetomylaw/article/details/43015295

- set

  语法：

  ```shell
  set key flas timeout value_length 
  # flas 代表是否需要压缩， 一般设置为0，不需要压缩
  # timeout 代表过期时间
  # value_length 代表值长度， 长度必须要一致，否则无法存储
  value
  ```

  如果key存在，则覆盖

  示例：

  ```shell
  set username 0 60 4
  ying
  ```

- add，只能添加 不存在的key，不想set可以覆盖

  语法：

  ```shell
  add key flas(0) timeout value_length
  value
  ```

  示例：

  ```shell
  add username 0 60 4
  ying
  ```



### 2. 获取数据

- get

  语法：获取多个值空格隔开

  ```shell
  get key
  ```

  示例：

  ```shell
  get username
  ```



### 3. 删除数据

- delete

  语法：

  ```shell
  delete key
  ```

  示例：

  ```shell
  delete username
  ```

- flash_all

  删除memcached中所有的数据

  语法：

  ```shell
  flash_all
  ```

  ​

### 其它

- replace

替换

语法：

```shell
replace key flas timeout value_length
value
```

示例：

```shell
replace username 0 80 7
yingjoy
```

- incr

给对应的值加上一定的值

语法

```shell
incr key add
```

示例：

```shell
set age 0 120 2
18
----------------
incr age 2
----------------
get age
20
```

对应decr，进行减操作



- append往后追加：`append  key datablock  status`
- prepend往前追加：`prepend key datablock status`


- 监察存储命令cas



- stats 

  查看memcached当前的状态，可以计算出命中率，从而判断memcached中是否存在很多垃圾文件。

  - `get_hists` 获取命中多少次
  - `get_misses`获取get空的次数
  - `curr_items`当前memcached中键值对的个数
  - `total_connections` 从`memcached`开启到现在总共的连接数
  - `curr_connections`当前连接数



- 注： Memcached默认最大连接数为1024



## 72. 使用Python操作Memcached

### 1. 安装`python-memcached`

```shell
pip install python-memcached
```

### 2. 建立连接

```python
import memcache
mc = memcache.Client(['192.168.1.200', '11211'], debug=True)
# 这里可以分布式，在list后面再添加memcached服务器即可
```

### 3. 设置数据

```python
mc.set('welcome', 'hello world', time=60*5)
mc.set_multi({'username':'ying', 'age':18}, time=60*5)
```

### 4. 获取数据

```python
result = mc.get_multi(['welcome', 'username', 'age'])
print(result)
# 这里result是字典类型
```

### 5. 删除数据

```python
mc.delete('welcome')
result = mc.get('welcome')
print(result)
```

### 6. 自增

```python
mc.incr('age', delta=1)
result = mc.get('age')
print(result)
```

### 7. 自减

```python
mc.decr('age', delta=10)
result = mc.get('age')
print(result)
```

分布式的时候，存的值是按照memcached的算法分配的，不同字段会在集群上不同的机器上存储。



## 73. Memcached的安全机制

由于Memcached登录的时候不需要输入用户名和密码，只需直到memcached服务器的ip和端口号即可，导致不安全，下面是解决方案：

1. 开启服务器的时候`-l`参数不使用`0.0.0.0`设置仅允许本地可以连接
2. 使用防火墙，关闭memcached端口，这样也可以防止其它服务器访问
3. 编写防火墙规则

一般Memcached都在内网使用，不会在公网使用。



## 74. Redis

Redis是一种`NoSQL`数据库，他们的数据是保存在内存中，同时Redis也可以定时的把内存数据同步到磁盘中，即可以将数据持久化，并且他比Memcached支持更多的数据结构，(string, list[队列和栈], set[集合], sorted set[有序集合], hash(hash表))。参考文档：

http://redisdoc.com/index.html

### 1. Redis的使用场景

- 登录会话存储，存储在redis比memcached相比，数据不会丢失
- 排行榜/计数器：做排行耪用
- 作为消息队列：比如celery就是使用redis做中间件
- 当前在线人数
- 一些常用的数据缓存：比如bbs论坛，板块不会经常变换，但是每次访问首页都需要从mysql中获取，可以在redis中缓存起来，不用每次都请求mysql数据库。
- 把前200篇文章缓存或者评论缓存：一般用户浏览网站，只会浏览网站前面一部分文章或者评论，那么可以把前面200篇文章或者评论缓存起来，用户访问超过缓存数的文章，就访问数据库获取，并且把之前的缓存删除。
- 好友关系：如微博，QQ好友关系
- 发布和订阅功能，可以用来做聊天软件

### 2. Redis和Memcached的比较

|        | Memcached         | Redis           |
| ------ | ----------------- | --------------- |
| 类型     | 纯内存缓存系统（数据库）      | 内存磁盘同步数据库       |
| 数据类型   | 在定义value时需要固定数据类型 | 不需要             |
| 虚拟内存   | 不支持               | 支持              |
| 过期策略   | 支持                | 支持              |
| 存储数据安全 | 不支持               | 可以将数据同步到dump.db |
| 灾难恢复   | 不支持               | 可以将磁盘中的数据恢复到内存中 |
| 分布式    | 支持                | 主从同步            |
| 发布与订阅  | 不支持               | 支持              |

### 3. Redis的安装

建议在Linux系统

```shell
yum install gcc
wget http://download.redis.io/releases/redis-4.0.2.tar.gz
tar xzf redis-4.0.2.tar.gz
cd redis-4.0.2
make
make install
```

后台运行：

https://blog.csdn.net/ksdb0468473/article/details/52126009

添加环境遍历

```shell
vim /etc/profile
------------------------------
PATH=$PATH:/usr/local/bin
export PATH
------------------------------
source /etc/profile
```

### 4. Redis的操作

#### 启动redis:

```shell
redis-server /usr/local/bin/redis.conf
```

#### 连接redis

```python
redis-cli -h [ip] -p [port]
-----------------------------------
127.0.0.1:6379>
```

#### 添加数据

```mysql
set key value
eg: 
set username ying
```

当值为字符串且有空格时，使用单/双引号包裹`set welcome "hello world"`

#### 获取数据

```mysql
get key
eg:
get username
```

#### 删除数据

```mysql
del key
eg:
del username
```

#### 设置过期时间

```
expire key timeout(秒)
eg:
set username 5
```

```python
1. set key value EX timeout
2. setex key timeout value
eg:
set username ying EX 5
setex username 5 ying
```

如果没有指定过期时间，则默认不过期

#### 查看过期时间

```
ttl key
eg:
ttl username
```

可以查看`key`距离过期还有多少秒

#### 查看当前redis中所有的key

```
keys pattern
eg:
keys *
```

pattern：正则匹配

### 5. 操作列表

Redis的列表分左右表头

#### 在列表的左边添加元素

```
lpush key value
eg:
lpush user ying
```

将值列表key的**表头**。如果列表key不存在，一个空列表会被创建，然后再执行lpush操作，当key存在的时候，会报错。

可以添加多个值，多个值使用空格隔开

```
lpush user user1 user2
```

#### 在列表右边添加元素

```
rpush key value
eg:
rpush user ying
```

将值插列表key的**表尾**。如果列表key不存在，一个空列表会被创建，然后再执行rpush操作，当key存在的时候，会报错。

#### 查看列表中的元素

```
lrange key start stop
```

返回列表中指定的区域，区间的偏移量是start和stop，如果要从左边的第一个到最后一个`lrange key 0 -1`

#### 移除列表中的值

```
lpop key
rpop key
eg:
lpop user
rpop user
```

 #### 移除并返回列表key的中间元素

```
lrem key count value
eg:
lrem user 3 ying
```

从左将删除key列表中，count个值为value的元素

如果要删除所有，则设置count为0

- count为正，则从表头到表尾删除


- count为负，则从表尾到表头删除

#### 指定返回第几个元素

```
lindex key index
eg:
lindex user 4
```

这个索引是从0开始的

#### 获取列表中元素的个数

```
llen key
eg:
llen user
```

### 6. 操作集合(set)

**集合元素不能重复**

#### 添加元素

 添加元素的位置是**随机**的

```
sadd set value1 value2 ...
eg:
sadd user user1 user2
```

#### 查看元素

```
smembers set
eg:
smembers user
```

#### 移除元素

```
srem set member
eg:
srem user user1
```

#### 查看集合中元素的个数

```
scard set
eg:
scard user
```

#### 获取多个集合的交集

```
sinter set1 set2
eg:
sinter user username
```

#### 获取多个集合的并集

```
sunion set1 set2
eg:
sunion user username
```

#### 获取多个集合的差集

```
sdiff set1 set2
eg:
sdiff user username
```

### 7. 操作哈希(hash)

#### 添加一个新值

```
hset key field value
eg:
hset user username ying age 18
```

如果key不存在，则创建一个新的hash表，如果存在，则覆盖。

也可以使用`hmset`

#### 获取hash中对应的field值

```
hget key field
eg:
hget user username
```

#### 删除hash中某个field

```
hdel key field
eg:
hdel user age
```

#### 获取hash中所有的field和value

```
hgetall key
eg:
hgetall user
```

#### 获取hash中所有的field

```
hkeys key
eg:
hkeys user
```

#### 获取hash中所有的value

```
hvals key
eg:
hvals user
```

#### 获取hash中总共有多少键值对

```
hlen key
eg:
hlen user
```



### 8. 事务操作

Redis可以一次性执行多个命令，事务具有以下特点：

- 隔离操作：事务中所有的命令会被序列化，按顺序执行，不会被其他命令打扰
- 原子操作：事务中的命令要不全部执行，要不全部都不执行

#### 开启一个事务

```
multi
```

以后执行的所有命令都会在这个事务中执行。

#### 执行事务

````
exec
````

#### 退出事务

````
discard
````

#### 监视一个或多个key

```
watch key
```

先进行监视，再进入事务，如果监听的值与事务中有误，则不会执行事务。如，在另一个窗口中重新修改事务中key的值。

#### 取消所有key的监视

```
uwatech
```



### 9. 发布/订阅操作

#### 给某个频道发消息

```
publish channel message
```

#### 订阅某个频道的消息

```
subscribe channel
```

### 10. 数据持久化

Redis提供了两种数据备份的方式，一种是RDB，另一种是AOF。

#### RDB同步机制：

1. 开启和关闭：默认情况下是开启了。如果想关闭，那么注释掉`redis.conf`文件中的所有`save`选项就可以了。
2. 同步机制：
    * save 900 1：如果在900s以内发生了1次数据更新操作，那么就会做一次同步操作。
    * save 300 10：如果在300s以内发生了10数据更新操作，那么就会做一次同步操作。
    * save 60 10000：如果在60s以内发生了10000数据更新操作，那么就会做一次同步操作。
3. 存储内容：具体的值，而是命令。并且是经过压缩后存储进去的。
4. 存储路径：根据`redis.conf`下的`dir`以及`rdbfilename`来指定的。默认是`/var/lib/redis/dump.rdb`。
5. 优点：
    * 存储数据到文件中会进行压缩，文件体积比aof小。
    * 因为存储的是redis具体的值，并且会经过压缩，因此在恢复的时候速度比AOF快。
    * 非常适用于备份。
6. 缺点：
    * RDB在多少时间内发生了多少写操作的时候就会出发同步机制，因为采用压缩机制，RDB在同步的时候都重新保存整个Redis中的数据，因此你一般会设置在最少5分钟才保存一次数据。在这种情况下，一旦服务器故障，会造成5分钟的数据丢失。
    * 在数据保存进RDB的时候，Redis会fork出一个子进程用来同步，在数据量比较大的时候，可能会非常耗时。

#### AOF同步机制：

1. 开启和关闭：默认是关闭的。如果想要开启，那么修改redis.conf中的`appendonly yes`就可以了
2. 同步机制：
    * appendfsync always：每次有数据更新操作，都会同步到文件中。
    * appendfsync everysec：每秒进行一次更新。
    * appendfsync no：使用操作系统的方式进行更新。普遍是30s更新一次。
3. 存储内容：存储的是具体的命令。不会进行压缩。
4. 存储路径：根据`redis.conf`下的`dir`以及`appendfilename`来指定的。默认是`/var/lib/redis/appendonly.aof`。
5. 优点：

    * AOF的策略是每秒钟或者每次发生写操作的时候都会同步，因此即使服务器故障，最多只会丢失1秒的数据。 
    * AOF存储的是Redis命令，并且是直接追加到aof文件后面，因此每次备份的时候只要添加新的数据进去就可以了。
    * 如果AOF文件比较大了，那么Redis会进行重写，只保留最小的命令集合。
6. 缺点：
    * AOF文件因为没有压缩，因此体积比RDB大。 
    * AOF是在每秒或者每次写操作都进行备份，因此如果并发量比较大，效率可能有点慢。
    * AOF文件因为存储的是命令，因此在灾难恢复的时候Redis会重新运行AOF中的命令，速度不及RDB。

### 11. 给redis指定密码

1. 设置密码：在`reids.conf`配置文件中，将`requirepass pasword`取消注释，并且指定你想设置的密码。
2. 使用密码连接reids：
    * 先登录上去，然后再使用`auth password`命令进行授权。
    * 在连接的时候，通过`-a`参数指定密码进行连接。

### 12. 其他机器连接redis

如果想要让其他机器连接本机的redis服务器，那么应该在`redis.conf`配置文件中，指定bind **本机的ip地址**。这样别的机器就能连接成功。不像是网上说的，要指定对方的ip地址。



## 75. Python操作Redis

### 安装

```shell
pip insatll redis
```

### 建立连接

```python
from redis import Redis
xtredis = Redis('192.168.1.200', port='6379', password='123456')
```

### 对字符串进行操作

```python
xtredis.set('username', 'ying')
result = xtredis.get('username')
print(result)

xtredis.delete('username')
result = xtredis.get('username')
print(result)

xtredis.set('username', 'ying')
xtredis.set('username', 'yingjoy')
result = xtredis.get('username')
print(result)
```

### 对列表进行操作

```python
xtredis.lpush('user', 'user1')
xtredis.lpush('user', 'user2')
xtredis.rpush('user', 'user3')
result = xtredis.lrange('user', 0, -1)
print(result)
```

和控制台操作是一样一样的~



### 事务（管道）操作

redis支持事务操作，也就是一些操作只有统一完成，否则失败

```python
pipeline = xtredis.pipeline()
pipeline.set('username', 'ying')
pipeline.set('age', 18)
pipeline.incr('age', 2)
pipeline.execute()

result = xtredis.keys('*')
print(result)
result = xtredis.get('age')
print(result)
----------------------------------
[b'user', b'username', b'age']
b'20'
```



### 发布与订阅

模拟异步发送邮件功能

#### 发送者：

```python
from redis import Redis

xtredis = Redis('192.168.1.200', port='6379', password='123456')

# 发布3条消息
for i in range(3):
    xtredis.publish('email', '{}xxx@qq.com'.format(i))
```

#### 订阅者：

```python
from redis import Redis

xtredis = Redis('192.168.1.200', port='6379', password='123456')

# 订阅
ps = xtredis.pubsub()
ps.subscribe('email')
# 监听
while True:
    # ps.listen() 返回一个生成器
    for item in ps.listen():
        if item['type'] == 'message':
            # 获取邮箱
            data = item['data']
            # bytes 转 str
            print(data.decode())
```

