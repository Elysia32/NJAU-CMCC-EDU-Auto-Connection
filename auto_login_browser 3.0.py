#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
江苏移动宽带WiFi自动登录脚本
DESIGN BY: @Elysia32 https://github.com/Elysia32
使用前需要安装:
    pip install selenium


"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sys
import argparse
import os

# ==================== 配置区域 ====================
USERNAME = ""  # 手机号，例如: 13800138000
PASSWORD = ""  # 宽带密码

# 认证门户地址
PORTAL_URL = "http://www.msftconnecttest.com/redirect" 
# ==================================================


def find_edge():
    """查找Edge浏览器路径"""
    edge_paths = [
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
    ]

    for path in edge_paths:
        if os.path.exists(path):
            return path
    return None


def create_driver():
    """创建Edge浏览器实例（Windows自带，无需额外驱动）"""
    edge_options = Options()
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--window-size=1920,1080')
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    edge_options.add_experimental_option('useAutomationExtension', False)
    service=Service(r"") #driver绝对路径 如 service=Service(r"C:\path\to\msedgedriver.exe")
    # 查找Edge路径
    edge_path = find_edge()
    if edge_path:
        edge_options.binary_location = edge_path
        print(f"  找到Edge: {edge_path}")
    else:
        print("  警告: 未找到Edge，使用默认路径")

    try:
        # Edge在Windows上有内置驱动支持
        driver = webdriver.Edge(options=edge_options,service=service)
    except Exception as e:
        print(f"  创建浏览器失败: {e}")
        print("  请确保:")
        print("  1. 已安装Microsoft Edge浏览器（Windows 10/11自带）")
        print("  2. 已安装selenium: pip install selenium")
        sys.exit(1)

    # 修改navigator.webdriver属性，绕过自动化检测
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    return driver


def check_network_status(driver):
    """检查网络是否已连接"""
    print("[0/4] 检查网络状态...")
    try:
        driver.get("http://www.baidu.com")
        WebDriverWait(driver, 5).until(
            lambda d: "baidu" in d.current_url.lower()
        )
        print("  网络已连接，无需认证")
        return True
    except:
        print("  需要认证")
        return False


def login_with_browser(driver, username, password):
    """使用浏览器完成认证登录"""
    print("=" * 50)
    print("  NJAU移动宽带WiFi自动登录 (Selenium版)")
    print("=" * 50)
    print()

    # 步骤1: 访问认证门户
    print(f"[1/4] 访问认证门户...")
    driver.get(PORTAL_URL)
    time.sleep(2)

    # 先检查是否有frame，有则直接切换
    print("  检查frame...")
    try:
        # 等待frame出现并切换
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "mainFrame"))
        )
        print("  已切换到mainFrame")
    except TimeoutException:
        # 尝试第一个iframe
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            if iframes:
                driver.switch_to.frame(iframes[0])
                print("  已切换到iframe")
        except Exception:
            pass

    # 在frame中等待用户名输入框
    print("  等待登录页面加载...")

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "UserName"))
        )
        print("  登录页面加载成功")
    except TimeoutException:
        print(f"  错误: 无法找到用户名输入框")
        print(f"  当前URL: {driver.current_url}")
        print(f"  页面标题: {driver.title}")
        return False

    # 步骤2: 填充用户名 - 智能等待输入框可交互
    print(f"[2/4] 输入用户名: {username}")
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "UserName"))
        )
        username_input.clear()
        username_input.send_keys(username)
    except TimeoutException:
        print("  错误: 找不到用户名输入框")
        return False

    # 步骤3: 填充密码 - 智能等待输入框可交互
    print(f"[3/4] 输入密码")
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "PassWord"))
        )
        password_input.clear()
        password_input.send_keys(password)
    except TimeoutException:
        print("  错误: 找不到密码输入框")
        return False

    # 步骤4: 点击登录按钮 - 智能等待按钮可点击
    print(f"[4/4] 点击登录...")
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "loginbutton1"))
        )
        login_button.click()
    except TimeoutException:
        # 尝试其他选择器
        try:
            login_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
            )
            login_button.click()
        except TimeoutException:
            print("  错误: 找不到登录按钮")
            return False

    # 等待认证结果 - 等待登录按钮消失或结果显示
    print("  等待认证结果...")
    try:
        # 等待登录按钮消失（说明已提交表单）
        WebDriverWait(driver, 15).until_not(
            EC.presence_of_element_located((By.ID, "loginbutton1"))
        )
        print("  登录按钮已消失，表单已提交")
    except TimeoutException:
        # 如果登录按钮还存在，检查页面是否有变化
        print("  登录按钮仍在，检查页面是否显示结果...")
        time.sleep(2)

    # 稍微等待页面完全加载
    time.sleep(2)
    current_url = driver.current_url.lower()
    page_title = driver.title.lower()

    # 判断是否认证成功
    success_indicators = ['success', '成功', 'welcome', 'online', 'index.jsp', 'main.jsp']
    fail_indicators = ['fail', '失败', 'error', '错误', 'showNatFail']

    is_success = any(ind in current_url or ind in page_title for ind in success_indicators)
    is_fail = any(ind in current_url or ind in page_title for ind in fail_indicators)

    if is_success and not is_fail:
        print("\n认证成功！")
        return True
    elif is_fail:
        print("\n认证失败，请检查账号密码")
        return False
    else:
        # 尝试验证网络
        try:
            driver.get("http://www.baidu.com")
            if "baidu" in driver.current_url.lower():
                print("\n认证成功！网络已连接")
                return True
        except:
            pass
        print("\n认证状态不明，请手动检查")
        return None


def main(username=None, password=None):
    """主函数"""
    username = username or USERNAME
    password = password or PASSWORD

    if not username or not password:
        print("错误: 未设置用户名或密码")
        sys.exit(1)

    driver = None
    try:
        driver = create_driver()

        # 可选：先检查是否已在线
        # if check_network_status(driver):
        #     print("\n已完成")
        #     return

        # 执行登录
        result = login_with_browser(driver, username, password)

        if result:
            print("\n" + "=" * 50)
            print("登录成功！")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print("登录失败")
            print("=" * 50)

        # 保持浏览器打开一段时间，让用户看到结果
        print("\n浏览器将在10秒后关闭...")
        time.sleep(10)

    except Exception as e:
        print(f"错误: {str(e)}")
    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NJAU移动宽带WiFi自动登录 (Selenium版)')
    parser.add_argument('--username', '-u', help='手机号/用户名')
    parser.add_argument('--password', '-p', help='密码')

    args = parser.parse_args()
    main(username=args.username, password=args.password)
