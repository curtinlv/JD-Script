#!/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / getJDCookie 
@Author: Curtin
功能：
Date: 2021/5/9 下午5:53
'''

print('''
******************************************
获取京东cookie工具_v1.2

Author: Curtin

Date: 2021-01-24 17:43

UpdateTime：2021-06-20 10:55

# GitHub https://github.com/curtinlv
# TG交流 https://t.me/topstyle996
# TG频道 https://t.me/TopStyle2021 
# 关注公众号【TopStyle】
 
 Ps:需依赖谷歌浏览Chrome 和 驱动 chromedriver  ，版本要求一致！
 谷歌浏览Chrome : https://www.google.cn/chrome/
 驱动链接: http://npm.taobao.org/mirrors/chromedriver/  (下载放在脚本同目录下)
 
******************************************
''')
import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json, os, sys

# 加启动配置
chrome_options = webdriver.ChromeOptions()
# 打开chrome浏览器
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
#chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])#禁止打印日志
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])#跟上面只能选一个
# chrome_options.add_argument('--start-maximized')#最大化
chrome_options.add_argument('--incognito')#无痕隐身模式
chrome_options.add_argument("disable-cache")#禁用缓存
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('log-level=3')#INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
# chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"')


def exitWait():
    getYourCode = input("请按回车键自动退出。")
    exit(0)
try:
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        driver = webdriver.Chrome(options=chrome_options, executable_path=r'./chromedriver.exe')
    else:
        driver = webdriver.Chrome(options=chrome_options, executable_path=r'./chromedriver')
    driver.set_window_size(375, 812)
except:
    print('报错了!请检查你的环境是否安装谷歌Chrome浏览器！或者驱动【chromedriver.exe】版本是否和Chrome浏览器版本一致！\n驱动更新链接：http://npm.taobao.org/mirrors/chromedriver/')
    exitWait()
    exit(9)



def jd_login():

    driver.get('https://bean.m.jd.com/bean/signIndex.action')
    print('【请使用验证码方式登录您的账号，此次登录模拟手机登录，不会记录您任何信息，获取的cookie最长有效期为30天。】')
    try:
        if WebDriverWait(driver, 600, poll_frequency=0.2, ignored_exceptions=None).until(EC.title_is(u"签到日历")):
            '''判断title,返回布尔值'''
            nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('{} : 登录成功'.format(nowtime))

    except:
        print('超时退出')
        exitWait()
        exit(2)

def get_cookie():
    jd_cookies = driver.get_cookies()
    try:
        with open('cookies_tmp.txt','w') as fp:
            json.dump(jd_cookies, fp)
    except:
        print('保存cookie失败！')
    try:
        with open('cookies_tmp.txt','r') as fp:
            cookies = json.load(fp)
            for cookie in cookies:
                if cookie['name'] == "pt_key":
                    pt_key ='{}={};'.format(cookie['name'], cookie['value'])
                elif cookie['name'] == "pt_pin":
                    pt_pin = '{}={};'.format(cookie['name'], cookie['value'])
            try:
                pt_key
                pt_pin
                result = pt_key + pt_pin
            except:
                pass
        print(result)
        with open('JDCookies.txt','w+') as fp:
            fp.write(result)
            print('获取到cookie,已保存在文件[JDCookies.txt]')
            os.remove('cookies_tmp.txt')
    except:
       print('读取cookie失败！')
    driver.close()


if __name__ == '__main__':
    try:
        jd_login()
        get_cookie()
    except:
        pass
    finally:
        exitWait()
