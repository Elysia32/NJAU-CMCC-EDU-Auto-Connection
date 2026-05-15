# NJAU/NAU CMCC-EDU-Auto-Connection
NJAU开机自动连接中国移动校园网
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

## 使用教程
### 1.下载login.py文件，并安装request库
### 2.先手动进一次登录页面，抓取自己的请求参数
![image](https://github.com/Elysia32/NJAU-CMCC-EDU-Auto-Connection/blob/main/param.png)
在登录页面按F12打开开发者工具，点击网络，F5刷新，找到带有ParamStr字样的数据包，转到响应页，根据里面的内容修改py文件的"xxx"（引号不要删)，包括ParamStr，pwdType，UserName和PassWord，其他参数不用改
### 3.先在有网的情况下测试一下有无“登录成功”的return，有的话一般就没问题
### 4.设置开机自启
Win+R调出运行，输入" shell:common startup "打开启动文件夹，把修改好的login.py文件拖入即可（记得把py文件默认打开方式改为python)
