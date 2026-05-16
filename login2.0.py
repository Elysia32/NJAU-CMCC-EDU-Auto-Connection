import requests
import re
import time
BASE_URL = "http://wlan.jsyd139.com"
LOGIN_URL = "http://wlan.jsyd139.com/authServlet"
def get_param_str():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0"
    }
    init_response=requests.get("xxx",headers=headers) #替换成登录页面的url
    Param=re.findall('<frame name="mainFrame" src="style/default_szlan/index.jsp.?paramStr=(.*?)" noresize scrolling="auto">',init_response.text)
    re_response=requests.get(f"http://wlan.jsyd139.com/style/default_szlan/index.jsp?paramStr={Param[0]}",headers=headers)
    real_param=re.findall('<input type="hidden" name="paramStr" id="paramStr" value="(.*?)" />',re_response.text)
    return real_param[0]
LOGIN_DATA = {
    "paramStr": f"{get_param_str()}",
    "UserType": "",
    "province": "",
    "pwdType": "1",
    "serviceType": "xxx",
    "isCookie": "true",
    "cookieType": "-1",
    "UserName": "xxx",
    "PassWord": "xxx",
}

def login():
    try:
        print(f"正在登录{LOGIN_URL}...")
        session = requests.Session()  #存cookie
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": f"{BASE_URL}/",
            "Content-Type": "application/x-www-form-urlencoded",
        })

        response = session.post(LOGIN_URL, data=LOGIN_DATA, timeout=3)
        response.encoding = 'gbk'
        return response
    except requests.exceptions.ReadTimeout:
        pass
    except Exception:
        pass
def check_network():
    try:
        requests.get("http://www.baidu.com", timeout=5)
        return True
    except:
        return False

if __name__ == "__main__":
    count=0
    while(True):
        response = login()
        time.sleep(1)
        count+=1
        if check_network():
            print("登录成功")
            break
        if count>5:
            print("登录失败")
            break

    