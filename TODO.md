### TODO

1. 总体

    - 确定需要添加的API

2. 树莓派端

    - 工程结构，把*常量*和*配置变量*分开

    - 增加不同显示模式的切换（视频流、抓取输出信号）

    - 增加对于不同下载线的支持

    - 编写树莓派安装脚本

    - 改用format格式化字符串

3. 服务器端

    - 重构工程结构，将网站API、与树莓派连接的Socket以及与网页连接的WebSocket分离

    - 增加系统管理员交互方式（命令行或简易网页）

4. 浏览器端

    - 整合登录页面和交互页面，统一采用React框架。

    - 增加多树莓派支持

    - 增加不同反馈方式

---

## 工程简介

### 1. 树莓派端

#### 整体思路

树莓派端的主要思路是通过Socket与服务器通信，接收服务器发送的json数据，并执行相应的操作。因此工程结构也相对简单，`main.py`第32行`read_until`函数用于接收服务器发送的数据，当读取到一个完整的json时就调用`on_read`函数处理数据，同时调用`read_until`等待下一个json数据。

#### 细节

1. 在`exotic_fpga.py`中使用了程序`djtgcfg`，见[Adept 2](https://reference.digilentinc.com/reference/software/adept/start?redirect=1id=digilent_adept_2#software_downloads)。

2. 在`exotic_rpi.py`中，对于GPIO的控制是通过`gpio`这一工具实现的，相关信息见[The GPIO utility](http://wiringpi.com/the-gpio-utility/)。

### 2. 服务器端

#### 说明

`server.bak`文件夹下是前一版服务器代码，`server`文件夹是目前正在重构的服务器代码。目前重构完成度还很低，所以主要可以参考原先的代码。

#### 整体结构

服务器端可分为三个主要部分：

（1）网站API：该部分主要负责网页相关的请求例如登录、登出、注册等，工程中的大部分`XxxHandler`均属此类。

（2）WebSocket：该部分主要实现浏览器与服务器之间的即时通信，在工程中主要对应`LiveHandler.py`中的`LiveShowHandler`。

（3）Socket服务器：该部分用于与树莓派建立连接并进行通信，在工程中主要对应`FPGAServer.py`文件。

### 3. 浏览器端

#### 技术栈

本项目中使用到的主要技术为[React](https://facebook.github.io/react/)、[Redux](http://redux.js.org/)。这种框架对于单页应用比较合适，但是学习曲线比较陡，其中涉及到的库比较多。建议通过以下教程进行学习：[Full-Stack Redux Tutorial](http://teropa.info/blog/2015/09/10/full-stack-redux-tutorial.html)。在教程中主要关注`React`、`Redux`、`Webpack`、`Babel`、`ES2015`。

#### 工程结构

前端页面主要位于`server.bak/static/src`（重构前）和`server/media/src`（重构后）下。目前工程运行方式如下：

```bash
# ./server
python app.py  # 启动服务器，访问localhost:6060即可看到页面。

# ./server/media
npm install    # 安装依赖，这一步可能需要很久，必要的时候需要采用代理、国内镜像、cnpm等措施
npm start      # 开始构建，文件修改后会实时生成新的文件，在浏览器中刷新即可看到效果
```

