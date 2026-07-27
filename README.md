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

