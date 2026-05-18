# NJAU/NAU CMCC-EDU-Auto-Connection
NJAU开机自动连接中国移动校园网  
！！！**仅用于个人学习，所有操作也仅是简化登录过程，并无其他不良影响**！！！
## 用request库经历多次失败后，改用selenium库
😭😭😭力竭了，搞不明白ParamStr参数的生成，经过多次观察，这个参数有时候会变，有时候不会变，我的2.0脚本get到的参数有时候跟抓到的参数也不一样，没招了  
## 使用教程
1.下载auto_login_browser 3.0.py，安装selenium库  
2.配置py文件里的用户名和密码，即手机号和宽带密码  
3.进 https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ 下载对应版本的浏览器驱动（浏览器更新之后，不知道不同版本的driver能不能用），查看当前edge版本：右上角···->帮助和反馈->关于MS EDGE  
4.解压驱动，把msedgedriver.exe绝对路径放到57行的service参数中  
5.设置开机自启  
## 开机自启：
创建一个bat文件（直接放py文件有概率不运行，可能是计算机不知道启动方式？），内容为  
> @echo off  
python "xxx"  

(xxx为绝对路径)  
Win+R调出运行，输入" shell:common startup "打开启动文件夹，把bat文件放入即可  
## 2.0增加了页面元素检测，防止网速慢未加载出页面就提前加载指令  
## 3.0修复以下内容：
1.一开始从菜鸟编程看到“从 Selenium 4 开始，在浏览器驱动的管理方式上发生了变化：Selenium 4 尝试自动检测系统中安装的浏览器版本，并下载相应的驱动程序，这意味着用户不再需要手动下载和设置驱动程序路径，除非他们需要特定版本的驱动程序。”，直接用的driver = webdriver.Edge()获取，结果有以下报错  
> 1.“There was an error managing msedgedriver (error sending request for url (https://msedgedriver.microsoft.com/LATEST_RELEASE_148_WINDOWS)); using driver found in the cache”，后面仔细一想，没有网怎么自动检测并下载...于是改为手动下载driver  
> 2.每天url里面的wlanuserip参数会变（真阴），所以改为http://www.msftconnecttest.com/redirect  直接重定向进登录页  



# 以下内容为request库的一顿暴改，没怎么学网络这块，拼尽全力无法战胜，当个乐子看
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
