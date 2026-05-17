# NJAU/NAU CMCC-EDU-Auto-Connection
NJAU开机自动连接中国移动校园网  
！！！**仅用于个人学习，所有操作也仅是简化登录过程，并无其他不良影响**！！！
## 经历多次失败后，用cc写了一个selenium脚本，直接模拟用户操作
😭😭😭力竭了，搞不明白ParamStr参数的生成，经过多次观察，这个参数有时候会变，有时候不会变，我的2.0脚本get到的参数有时候跟抓到的参数也不一样，没招了  
只能说AI牛逼，一开始请求不通直接调用selenium库，认证过程一气呵成  
只需要下载auto_login_browser2.0.py就可以了，改一下里面的用户名，密码和url就可以用了  
## 2.0增加了页面元素检测，防止网速慢未加载出页面就提前加载指令

# 以下内容为自己的探索历程，拼尽全力无法战胜，当个乐子看
## 前言
电脑每次开机都需要从浏览器登录CMCC-EDU校园网，过程繁琐，遂写此登录脚本

## 开发过程
### 1.使用开发者工具(F12)抓包，找到POST请求数据
数据包携带如下参数
> "paramStr": "xxx",  
"UserType": "",  
"province": "",  
"pwdType": "1",  
"serviceType": "xxx",  
"isCookie": "true",  
"cookieType": "-1",  
"UserName": "xxx",  
"PassWord": "xxx",
### 2.用request库模仿数据包直接发送
一开始的"isCookie"参数依照原请求包中填的False一直不通过，借助AI分析后改成True才可以（具体原因未知😰，可能要保存登录信息才行）
### 3. 1.0版本遇到的问题
第一版的paramstr参数是直接获取的，但第二天我发现参数变了，我又抓了几次包发现这个是随机生成的，生成方法如下（个人猜测：
> 1.先通过登录页网址+ip参数获取第一个paramstr，即脚本中的init_response参数  
> 2.再通过请求 "http://wlan.jsyd139.com/style/default_szlan/index.jsp?paramStr=xxx" ，把第一个paramstr放到后面然后获取真正的paramstr
### 4.相较于第一版的改进
> 1.动态获取paramstr  
> 2.利用try-except隐藏了超时报错（登录成功之后原请求会卡死，直到timeout，这边直接隐藏  
> 3.摒弃了超时检测，改为网络状态检测，通过get百度的网址来获得状态  
> 4.每次检测时间为9s左右，共检测5次，一般来说第一次就可以成功，后面的没啥用，如果第一次失败后面的也不太可能成功😁

## 使用教程2.0
### 1.下载login2.0.py文件，并安装request库
### 2.先手动进一次登录页面，抓取自己的请求参数
![image](https://github.com/Elysia32/NJAU-CMCC-EDU-Auto-Connection/blob/main/param.png)
在登录页面按F12打开开发者工具，点击网络，F5刷新，找到带有ParamStr字样的数据包，转到响应页，根据里面的内容修改py文件的"xxx"（引号不要删)，包括pwdType，UserName和PassWord，其他参数不用改
### 3.把登录页的地址复制到init_response的xxx中（抓取paramstr）
### 3.先在有网的情况下测试一下有无“登录成功”的return，有的话一般就没问题
### 4.设置开机自启
Win+R调出运行，输入" shell:common startup "打开启动文件夹，把修改好的login.py文件拖入即可（记得把py文件默认打开方式改为python)

## 使用教程1.0
### 1.下载login.py文件，并安装request库
### 2.先手动进一次登录页面，抓取自己的请求参数
![image](https://github.com/Elysia32/NJAU-CMCC-EDU-Auto-Connection/blob/main/param.png)
在登录页面按F12打开开发者工具，点击网络，F5刷新，找到带有ParamStr字样的数据包，转到响应页，根据里面的内容修改py文件的"xxx"（引号不要删)，包括ParamStr，pwdType，UserName和PassWord，其他参数不用改
### 3.先在有网的情况下测试一下有无“登录成功”的return，有的话一般就没问题
### 4.设置开机自启
Win+R调出运行，输入" shell:common startup "打开启动文件夹，把修改好的login.py文件拖入即可（记得把py文件默认打开方式改为python)  

## 其实还有一种方法，设置一个自动任务，通过拨号的方式连接CMCC
### 1.去拨号界面新建一个拨号 用户名填手机号，密码就是密码，名字随便起
### 2.去任务计划程序里创建一个自动任务，触发器添加以下几个
> 1.启动时  
> 2.工作站解锁时  
> 3.登录时  
> 4.发生事件时 -日志:System，源：Rasman，事件 ID:20268（有时候会掉线，这个用来检测掉线，然后再自动连接
### 3.操作按照这个填写
> 启动程序  名称为rasdial 添加参数填 "xxxx 手机号 密码"->其中xxxx为拨号界面创建的拨号名称

个人感觉哈，拨号的网速比wifi慢，不知道为什么
