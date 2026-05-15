import requests

BASE_URL = "http://wlan.jsyd139.com"
LOGIN_URL = "http://wlan.jsyd139.com/authServlet"

LOGIN_DATA = {
    "paramStr": "xxx",
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
    print(f"正在登录{LOGIN_URL}...")
    session = requests.Session()  #存cookie
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"{BASE_URL}/",
        "Content-Type": "application/x-www-form-urlencoded",
    })

    response = session.post(LOGIN_URL, data=LOGIN_DATA, timeout=10)
    response.encoding = 'gbk'
    return response

if __name__ == "__main__":
    for i in range(0,3):
        response = login()
        if "success" in response.text.lower() or "登录成功" in response.text:
            print("登录成功")
            break
        else:
            print("登录失败")
            break
