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
一开始的"isCookie"参数依照原请求包中填的False一直不通过，借助AI分析后改成True才可以（具体原因未知😰）

## 使用教程
### 1.下载login.py文件，并安装request库
### 2.先手动进一次登录页面，抓取自己的请求参数
