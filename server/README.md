# 快速使用

1. socket端口可以通过访问 /api/status 获得。

2. 树莓派端需要进行身份验证后才能收发信息

  验证方式为使用socket发送验证包，需要两个字段设备id及其验证码。

  在client.py中为了简便，可以使用命令行3、4号参数指定device_id以及auth_key，并输入auth发送验证包。

  运行models.py后默认有一个设备id为test的设备存储于数据库中，使用有管理员权限的账号登录  /api/admin/query?device_id=test 即可获取。同时，使用管理员权限访问 /api/admin/add 可以添加新的设备id。

3. 推流使用rtmp协议

  推流命令与地址后续有详细介绍。

  如果要本地测试，需要自己搭建RTMP服务器，具体方法参考[大作业 - 2 rtmp服务器配置](http://www.jianshu.com/p/6b2bebf7a731)。server.py只作为信息中转站，目前没有处理RTMP流的能力。

  梯子转发ffmpeg的流似乎会出很多问题，不推荐通过梯子推流。

# 消息格式

通信使用json格式，消息分为控制消息、状态消息，操作消息，信息消息以及其他。

服务器接受控制消息并返回状态消息，同时在某些情况下会发出信息消息。

除去一些特殊情况，服务器默认广播所有从树莓派端发送来的消息，同时屏蔽所有非操作者发送来的消息。操作者发送的消息将会被发往树莓派端。

## 控制消息

控制消息为含有type且为0的json对象，而另一个字段action表明所需要干的事情。

其中服务器有响应的action字段，有如下几种值：

* acquire

  浏览器端发出，获取所连接的莓派的操作权限

  操作成功后服务器会发出操作者变化的信息消息

* release

  浏览器端发出，释放所连接的树莓派的操作权限

  操作成功后服务器会发出操作者变化的信息消息

* broadcast

  浏览器端发出，表示这条消息将会被广播至所有用户。

  服务器接受到这种消息的时候，会在其内填入两个字段后再进行全浏览器端广播：

  * nickname，表示发送人的昵称
  * timestamp，表示服务器端接收的时间戳

* authorize

  树莓派端发出，用于验证连接的身份。

  必须含有两个字段：

  * device_id，树莓派的设备id
  * auth_key，与设备id对应的识别码

  服务器返回一个状态消息，表示验证成功或失败。

值得一提的是，不论是从树莓派端还是浏览器端发送来的其余的所有type为0的json对象也都会被拦截，既不会被发送到树莓派端，也不会被广播至其他的浏览器端。

## 状态消息

状态消息是type为1的消息，有字段status表示状态。

status字段有如下的值：

* authorized

  服务器发出，树莓派端接收。表示树莓派身份验证成功。此时，除了type，status字段，在json对象中还会有几个字段：

  * index，当前树莓派分配的索引号
  * filelink，树莓派下载文件时所用的url
  * webport， 服务器所使用的web端口号
  * rtmp_host，rtmp服务器位置
  * rtmp_push_port，rtmp服务器的推流端口
  * stream_name，推流的流名字

* auth_fail

  服务器发出，树莓派端接收。表示树莓派身份验证失败。

* file_upload

  服务器端发出，浏览器端树莓派端接收，表明文件成功上传。

  附属字段info，为一个关于文件信息的json对象。

  在这个对象中，有三个字段，valid表明文件是否可用，name表示上传的文件名，size表示上传的文件大小

## 操作消息

操作消息是type为2的消息，含有operation字段。服务器不会主动发出这类消息。

## 信息消息

信息消息是type为3的消息，含有字段info。

服务器会发出两种信息消息，其info字段分别为：

* user_changed

  服务器发出，浏览器端树莓派端接收，表示当前树莓派操作者变化。

  带有字段user，表示当前树莓派的操作者，可为空(null)，表示无人操作。

* fpga_disconnected

  服务器发出，浏览器端接收，表示相关联的树莓派端断开连接。

# 树莓派端demo使用

该demo程序接收5个命令行参数：

* argv[1]，host，表示目标服务器的地址
* argv[2]，port，表明socket连接的端口
* argv[3]，device_id，表明设备ID
* argv[4]，auth_key，表示设备识别码
* argv[5]，separator，表示socket消息分隔符

1、2用于定位服务器位置，3、4用于身份验证，5用于消息发送。

在树莓派连入服务器之后，需要一次身份验证命令将身份信息发往服务器端进行验证。处于无身份的状态在服务器链接过多的时候会被优先断开。

在身份验证成功后，服务器会发送一个json对象，表示当前连入的相关信息，下方就是一个例子。

``` json
{
    "status": 0,
    "index": 0,
    "rtmpHost": "localhost",
    "rtmpPushPort": 6666,
    "streamName": "0",
    "webport": 8080,
    "filelink": "/live/0/file/download"
}
```

* status表示此次的身份验证成功
* index表示当前树莓派在服务器的索引值
* rtmpHost, rtmpPushPort, streamName 在下文服务器配置处详细叙述，与rtmp推流有关
* webport为web服务器的端口号，用于下载文件
* filelink为web文件下载的url

在连接上服务器并验证身份之后，可以在命令行下输入命令即可。部分格式的命令会被转义，大部分的命令会直接发送至服务器。

转义命令格式如下：

* auth

  发送身份验证包至所连接的服务器

* keypress keycode

  会发送一个按下keycode所代表按键的信息至服务器([键码（KeyCode）](http://xiaotao-2010.iteye.com/blog/1818668))

* switchon id

  发送一个开关打开的消息

* switchoff id

  发送一个开关关闭的消息

* buttonpress id

  发送一个按钮按下的消息

* buttonrelease id

  发送一个按钮弹起的消息

* exit

  退出client.py

# 服务器使用

在使用之前，需要确保含有tornado的包。可以使用pip命令安装所有的依赖。

``` shell
pip install -r requirement.txt
```

## 配置

### 配置调试

使用命令

``` shell
python config.py
```

可以获取到所有服务器的配置参数，与直接运行服务器时的参数一致。可以使用该文件进行配置调整。

可调整参数及其默认值如下：

``` json
options =  {
    "config": null,

    "_user": "user",
    "_identity": "identity",
    "_password": "password",
    "_nickname": "nickname",

    "webport": 8080,
    "filesize": 1048576,
    "cookie_secret": "XmuwPAt8wHdnik4Xvc3GXmbXLifVmPZYhoc9Tx4x1iZ",
    "database": "exotic.db",
    "messageInterval": 2,

    "socketport": 8081,
    "unauthsize": 32,
    "separator": "\n",

    "rtmpHost": "localhost",
    "rtmpPushPort": 6666,
    "rtmpPullPort": 1935,
    "rtmpAppName": "live",

    "userCountSend": false,
    "sendPeriod": 5000,
    "sendHost": "localhost",
    "sendPort": 8080,
    "sendURL": "/api/report",
    "device_id": 10000,
    "auth_key": "None",
}

```

### 配置解析

本工程使用Tornado的options.parse_command_line()解析。该函数有一些特性在此先说明。

在命令行的解析过程中，命令行参数允许重复出现，同时后续出现的参数会覆盖先前输入的同名参数。

而如同config这样指定配置文件的参数，会在遇到的那一刻将配置文件内的所有项目执行完毕并赋值。后续的命令行参数会在此后继续进行解析。当然，依然是后续的覆盖先行的。

### 配置文件

* config

  配置覆盖文件，在命令行下指定--config=xx.py 会直接运行目标文件中的命令并使用内部定义的所有数据。而后续再写入的所有配置信息会覆盖重复出现的字段。

  可以重复出现多次--config，每次遇到都会执行一次目标文件，取最新的结果作为最终配置。

### 服务器自身配置

* _user, _nickname, _password, _identity

  对应cookie的名字

* webport

  浏览器端口，浏览器通过这个端口访问web服务器，websocket也是这个端口

* cookie_secret

  cookie加密键，tornado用于加密cookie的字符串

* filesize

  文件大小，表明客户端所能上传的最大文件大小，大于这个数目的会被服务器拒绝

* database

  数据库文件，指定所使用的sqlite3数据库文件

* messageInterval

  每个用户发送消息的冷却时间

### Socket 相关配置

* socketport

  socket端口，树莓派通过这个端口与服务器进行通信

* unauthsize

  未授权客户端的个数，多于这个个数，服务器会主动将最早连入的设备连接断开

* separator

  socket下交流所用的信息间分隔符，以分隔符分割信息。

### RTMP 相关配置

* rtmpHost

  RTMP服务器的地址，浏览器端及树莓派端均需求，可以是网址或者IP

* rtmpPushPort

  RTMP服务器推流的端口，用于树莓派端推流。

* rtmpPullPort

  RTMP服务器拉流的端口，用户浏览器端拉流。

* rtmpAppName

  RTMP服务器所使用的appname，用于组成拉流的URL。

对于**浏览器端**，拉流的URI为
``` url
rtmp://rtmpHost:rtmpPullPort/rtmpAppName/streamName
```
其中，所有项均会由服务器给出。streamName由服务器根据某些规则计算得到，其余项均为配置。

对于**树莓派端**，推流的命令为
``` shell
ffmpeg -i ... -f flv -metadata streamName="streamName" tcp://rtmpHost:rtmpPushPort
```
其中，所有项均会由服务器给出。streamName由服务器根据某些规则计算得到，其余项均为配置。

### 中心服务器相关配置

* userCountSend

  是否发送当前在线用户数据到指定url

* sendPeriod

  发送频率，单位为ms

* sendHost, sendPort, sendURL

  发送的主机、端口及URL，默认发送给自己

* device_id, auth_key

  发送时附带上的身份识别信息

以上信息结合起来就是，如果设置了userCountSend字段为真，服务器会以sendPeriod为间隔向 http://sendHost:sendPort/sendURL 这个地址发送数据包，数据包如下：
``` json
{
    "auth_id" : "auth_id",
    "auth_key" : "auth_key",
    "device_id" : "auth_id",
    "userCount" : 在线人数
}
```

## 使用

0. 使用config_override.py

  config_override.py主要用法是覆盖默认配置。当然在命令行下输入也是可以的，但是每次都输入不仅烦还有可能出错，所以推荐还是使用配置文件写入。

  配置文件所用的就是python语法，将某个字段直接赋值即可。

  一个配置文件可以是这样的一个文件

  ``` python
socketport = 9007
webport = 8007
unauthsize = 4
rtmpHost = "localhost"
rtmpPushPort = 6666
rtmpPullPort = 1935
rtmpAppName = "live"
  ```

  此时可以使用

  ``` shell
python config.py --config=config_override.py
  ```

  查看配置

1. 使用models.py初始化数据库

  ``` shell
  python models.py --config=config_override.py
  ```

2. 运行服务器端程序

  ``` shell
  python server.py --config=config_override.py
  ```

3. 开始使用

  使用client.py连入服务器并通过身份验证后，使用浏览器连入服务器即可。

# url详解

下方所有的$1均表示连入设备的索引值，为验证成功后由服务器发送的index值

* /

  用户主页的位置，只接受get请求。主页上显示当前连入的设备及其信息。

* /live/($1)/

  每个连入设备所独有的界面，用于与设备进行交互。

* /live/($1)/file/($2)

  下载该设备所属的文件中类型为$2的文件。

* /socket/live/($1)

  对应每个设备的websocket连接地址

* /api/livelist

  与主页上的所有信息对应，为json格式

* /api/status

  服务器暴露的一些信息，当前仅为socketport即socket端口

* /api/report

  用以接受在线用户数据的url，对于用户无用，只是以此测试发送成功与否

* /api/admin/query

  需要管理员权限，接受get请求，在请求参数中指明device_id则返回对应的auth_key

* /api/admin/add, /admin/add

  需要管理员权限，接受post以及get请求。

  * get请求下显示一个浏览器端的请求页面，并在点击提交后转入post页面。
  * post请求下根据传入的device_id生成auth_key。

* /register

  接受post以及get请求

  * get请求显示注册页面，按要求填写字段后提交转入post页面。
  * post请求对传入的参数进行验证，如果合法则存入数据库并设置相关cookie

* /login

  接受post以及get请求

  * get请求显示登录页面，填写对应字段后提交转入post页面。
  * post请求对传入的参数进行验证，合法则设置cookie

* /logout

  接受get请求

  请求之后页面上所有的cookie被清除，用户登出。
