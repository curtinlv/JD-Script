#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_zddd_Help
Author: Curtin
功能：种豆得豆-助力
Date: 2021/11/08 下午8:20
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 0 0 * * *
new Env('种豆得豆-助力.py');
'''

# 种豆得豆助力码 ENV环境变量设置 export PLANT_BEAN_SHARECODES="code1&code2&code3"
zddd_code = ["htk72lxpnunzixkrhxvd4gjj3a3h7wlwy7o5jii", ]

# UA 可自定义你的，注意格式: 【 jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1 】
UserAgent = ''

import os, re, sys
import random
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)
from urllib.parse import unquote
# requests.packages.urllib3.disable_warnings()
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
requests.packages.urllib3.disable_warnings()
###
uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
addressid = ''.join(random.sample('1234567898647', 10))
iosVer = ''.join(random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
iosV = iosVer.replace('.', '_')
iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(
    random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
    random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
###
if "PLANT_BEAN_SHARECODES" in os.environ:
    if len(os.environ["PLANT_BEAN_SHARECODES"]) > 1:
        zddd_code = os.environ["PLANT_BEAN_SHARECODES"]
        if '&' in zddd_code:
            zddd_code = zddd_code.split('&')
        elif '@' in zddd_code:
            zddd_code = zddd_code.split('@')
        print("已获取并使用Env环境 zddd_code:", zddd_code)
if not isinstance(zddd_code, list):
    zddd_code = zddd_code.split(" ")


def userAgent():
    """
    随机生成一个UA
    jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1
    :return: ua
    """
    if not UserAgent:
        return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'
    else:
        return UserAgent


def zhuli(ck, username, code):
    url = f'https://api.m.jd.com/client.action?functionId=plantBeanIndex&body=%7B%22plantUuid%22%3A%22{code}%22%2C%22monitor_source%22%3A%22plant_m_plant_index%22%2C%22monitor_refer%22%3A%22%22%2C%22version%22%3A%229.2.4.0%22%7D&appid=ld&client=apple&clientVersion=10.1.4&networkType=wifi&osVersion={iosVer}&uuid={uuid}'
    headers = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': f'https://plantearth.m.jd.com/plantBean/index?source=jingkoulingzhuli&plantUuid={code}&mpin=&lng=113&lat=&sid=&un_area=',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'api.m.jd.com',
        'User-Agent': userAgent(),
        'Accept-Language': 'zh-cn'
    }
    try:
        resp = requests.get(url=url, headers=headers,  timeout=30)
        if resp.json()['data']:
            print(username, "助力完成~")
    except:
        print(username, "助力失败~")

def start():
    cookiesList, userNameList = getCk.iscookie()
    for ck, username in zip(cookiesList, userNameList):
        for code in zddd_code:
            zhuli(ck, username, code)

if __name__ == '__main__':
    start()
