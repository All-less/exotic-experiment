# 快速使用

1. socket端口可以通过访问[/api/status](http://exotic.lmin.me/api/status)获得。

2. 树莓派端需要进行身份验证后才能收发信息

  验证方式为使用socket发送验证包，需要两个字段设备id及其验证码。
  当前默认有一个设备id为fpga的设备存储于数据库中，使用有管理员权限的账号登录[/api/admin/query?device_id=fpga](http://exotic.lmin.me/api/admin/query?device_id=fpga)即可获取。同时，使用管理员权限访问[/api/admin/add](http://exotic.lmin.me/api/admin/add)可以添加新的设备id。

3. 推流使用rtmp协议

# 信息格式

通信使用json格式，信息分为服务器控制信息以及数据交换信息。

## 控制信息

控制信息为含有action且为0的json对象，而另一个字段behave表明所需要干的事情。

``` json
{
    "action" : 0,
    "behave" : "do something"
}
```

其中behave字段当前有如下几种值：

* acquire

  客户端发出，获取所连接的莓派的操作权限

* release

  客户端发出，释放所连接的树莓派的操作权限

* liver_leave

  服务器端发出，表明树莓派的连接断开

* user_change

  服务器端发出，表明树莓派操作权限转移

  附属字段change，为当前操作者的昵称，可为空(null)，表示无人操作。

* file_upload

  服务器端发出，表明文件成功上传。

  附属字段info，为一个关于文件信息的json对象。

  在这个对象中，有三个字段，valid表明文件是否可用，name表示上传的文件名，size表示上传的文件大小

* file_program

  树莓派端发出，服务器转发，客户端接收。表示文件已经成功下载板子。

* authorization

  树莓派端发出，服务器截取，用于验证连接的身份。

  必须含有两个字段：

  * device_id，树莓派的设备id
  * auth_key，与设备id对应的识别码

  服务器的返回结果中不会含有action，而是使用status字段表示状态。

  status为0时，表示验证成功。此时，在json对象中还会有三个字段：

  * index，当前树莓派分配的索引号
  * filelink，树莓派下载文件时所用的url
  * webport， 服务器所使用的web端口号

  status为1表示验证失败。

值得一提的是，来自于浏览器端的所有action为0的json对象会被拦截，既不会被发送到树莓派端，也不会被广播至其他的浏览器端。

## 数据信息

数据信息的格式不固定，服务器会默认广播大部分的信息。所以，该数据格式需要前端小哥和树莓派端小哥商量后最终定稿。下面所写的是当前浏览器端demo以及树莓派端demo所用的数据格式。

首先，每个数据包均含有action字段，并根据action字段的不同，有不同的含义。

* action = 1, key down

  表示某个键盘按键被按下，带有字段code，表示被按下按键的编码。([键码（KeyCode）](http://xiaotao-2010.iteye.com/blog/1818668))

* action = 2, key up

  表示某个按键被放开，带有字段code，表示被按下按键的编码。

* action = 3, switch press

  表示某个开关被按下，带有字段id，表示开关的id。

# 树莓派端demo使用

该demo程序接收4个命令行参数：

* argv[1]，host，表示目标服务器的地址
* argv[2]，port，表明socket连接的端口
* argv[3]，device_id，表明设备ID
* argv[4]，auth_key，表示设备识别码

前两个用于定位服务器位置，后两个用于身份验证。

在连接上服务器之后，可以在命令行下输入命令即可。部分格式的命令会被转义，大部分的命令会直接发送至服务器。

转义命令格式如下：

* auth

  发送身份验证包至所连接的服务器

* keyup keycode

  会发送一个按下keycode所代表按键的信息至服务器

* keydown keycode

  发送一个按键弹起的信息

* switch id

  发送一个开关被反置的消息至服务器

# 服务器使用

在使用之前，需要确保含有tornado的包。

## 配置

使用命令

``` shell
python config.py
```

可以获取到所有服务器的配置参数，与直接运行服务器时的参数一致。可以使用该文件进行配置调整。

可调整参数及其默认值如下：

``` json
{
    "config": null,
    "database": "exotic.db",
    "webport": 8080,
    "socketport": 8081,
    "cookie_secret": "XmuwPAt8wHdnik4Xvc3GXmbXLifVmPZYhoc9Tx4x1iZ",
    "_user": "user",
    "_nickname": "nickname",
    "_password": "password",
    "_identity": "identity",
    "filesize": 1048576,
    "unauthsize": 32,
}
```

* config

  配置覆盖文件，在命令行下指定--config=xx.py 会直接运行目标文件中的命令并使用内部定义的所有数据。而后续再写入的所有配置信息会覆盖重复出现的字段。

* database

  数据库文件，指定所使用的sqlite3数据库文件

* webport

  浏览器端口，浏览器通过这个端口访问web服务器，websocket也是这个端口

* socketport

  socket端口，树莓派通过这个端口与服务器进行通信

* cookie_secret

  cookie加密键，tornado用于加密cookie的字符串

* _user, _nickname, _password, _identity

  对应cookie的名字

* filesize

  文件大小，表明客户端所能上传的最大文件大小，大于这个数目的会被服务器拒绝

* unauthsize

  未授权客户端的个数，多余这个个数，服务器会主动将最早连入的设备连接断开

## 使用

1. 使用models.py初始化数据库

  ``` shell
  python models.py --config=config_override.py
  ```

2. 运行服务器端程序

  ``` shell
  python server.py --config=config_override.py
  ```

3. 开始使用

  使用client.py连入服务器，使用浏览器连入服务器即可。

# url详解

下方所有的$1均表示连入设备的索引值，为验证成功后由服务器发送的index值

* /

  用户主页的位置，只接受get请求。主页上显示当前连入的设备及其信息。

* /live/($1)/

  每个连入设备所独有的界面，用于与设备进行交互。

* /live/($1)/file/($2)

  $2为对该设备所属的文件进行的行为，未指定即默认显示文件的对应信息。当前有一个行为，download表示下载文件。

  对应每个连入设备在服务器端缓存的用户上传的文件

* /socket/live/($1)

  对应每个设备的websocket连接地址

* /api/livelist

  与主页上的所有信息对应，为json格式

* /api/status

  服务器暴露的一些信息，当前仅为socketport即socket端口

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
