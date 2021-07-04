#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_cash
Author: Curtin
功能：签到领现金-助力
Date: 2021/7/4 上午09:35
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
'''

#ck 优先读取【JDCookies.txt】 文件内的ck  再到 ENV的 变量 JD_COOKIE='ck1&ck2' 最后才到脚本内 cookies=ck
cookies = ''
# 设置被助力的账号可填用户名 或 pin的值不要;
cash_zlzh = ['Your JD_User', '买买买']

### 推送参数设置
# TG 机器人token
TG_BOT_TOKEN = ''
# TG用户id
TG_USER_ID = ''
# TG代理ip
TG_PROXY_IP = ''
# TG代理端口
TG_PROXY_PORT = ''
# TG 代理api
TG_API_HOST = ''
# 微信推送加+
PUSH_PLUS_TOKEN = ''

# 建议调整一下的参数
# UA 可自定义你的，注意格式: 【 jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1 】
UserAgent = ''
# 限制速度 （秒）
sleepNum = 0.1

import os, re, sys
import random
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
from urllib.parse import unquote, quote
import json
import time
requests.packages.urllib3.disable_warnings()

pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
t = time.time()
aNum = 0
cashCount = 0
cashCountdict = {}
message_info = ''''''

def message(str_msg):
    global message_info
    print(str_msg)
    message_info = "{}\n{}".format(message_info, str_msg)
    sys.stdout.flush()

class getJDCookie(object):
    # 适配各种平台环境ck
    def getckfile(self):
        if os.path.exists(pwd + 'JDCookies.txt'):
            return pwd + 'JDCookies.txt'
        elif os.path.exists('/ql/config/env.sh'):
            print("当前环境青龙面板新版")
            return '/ql/config/env.sh'
        elif os.path.exists('/ql/config/cookie.sh'):
            print("当前环境青龙面板旧版")
            return '/ql/config/env.sh'
        elif os.path.exists('/jd/config/config.sh'):
            print("当前环境V4")
            return '/jd/config/config.sh'
        elif os.path.exists(pwd + 'JDCookies.txt'):
            return pwd + 'JDCookies.txt'
        return pwd + 'JDCookies.txt'

    # 获取cookie
    def getCookie(self):
        global cookies
        ckfile = self.getckfile()
        try:
            if os.path.exists(ckfile):
                with open(ckfile, "r", encoding="utf-8") as f:
                    cks = f.read()
                    f.close()
                if 'pt_key=' in cks and 'pt_pin=' in cks:
                    r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
                    cks = r.findall(cks)
                    if len(cks) > 0:
                        if 'JDCookies.txt' in ckfile:
                            print("当前获取使用 JDCookies.txt 的cookie")
                        cookies = ''
                        for i in cks:
                            cookies += i
                        return
            else:
                with open(pwd + 'JDCookies.txt', "w", encoding="utf-8") as f:
                    cks = "#多账号换行，以下示例：（通过正则获取此文件的ck，理论上可以自定义名字标记ck，也可以随意摆放ck）\n账号1【Curtinlv】cookie1;\n账号2【TopStyle】cookie2;"
                    f.write(cks)
                    f.close()
            if "JD_COOKIE" in os.environ:
                if len(os.environ["JD_COOKIE"]) > 10:
                    cookies = os.environ["JD_COOKIE"]
                    print("已获取并使用Env环境 Cookie")
        except Exception as e:
            print(f"【getCookie Error】{e}")

    # 检测cookie格式是否正确
    def getUserInfo(self, ck, pinName, userNum):
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback=GetJDUserInfoUnion'
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'close',
            'Referer': 'https://home.m.jd.com/myJd/home.action',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'me-api.jd.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'zh-cn'
        }
        try:
            resp = requests.get(url=url, verify=False, headers=headers, timeout=60).text
            r = re.compile(r'GetJDUserInfoUnion.*?\((.*?)\)')
            result = r.findall(resp)
            userInfo = json.loads(result[0])
            nickname = userInfo['data']['userInfo']['baseInfo']['nickname']
            return ck, nickname
        except Exception:
            context = f"账号{userNum}【{pinName}】Cookie 已失效！请重新获取。"
            print(context)
            return ck, False

    def iscookie(self):
        """
        :return: cookiesList,userNameList,pinNameList
        """
        cookiesList = []
        userNameList = []
        pinNameList = []
        if 'pt_key=' in cookies and 'pt_pin=' in cookies:
            r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
            result = r.findall(cookies)
            if len(result) >= 1:
                print("您已配置{}个账号".format(len(result)))
                u = 1
                for i in result:
                    r = re.compile(r"pt_pin=(.*?);")
                    pinName = r.findall(i)
                    pinName = unquote(pinName[0])
                    # 获取账号名
                    ck, nickname = self.getUserInfo(i, pinName, u)
                    if nickname != False:
                        cookiesList.append(ck)
                        userNameList.append(nickname)
                        pinNameList.append(pinName)
                    else:
                        u += 1
                        continue
                    u += 1
                if len(cookiesList) > 0 and len(userNameList) > 0:
                    return cookiesList, userNameList, pinNameList
                else:
                    print("没有可用Cookie，已退出")
                    exit(3)
            else:
                print("cookie 格式错误！...本次操作已退出")
                exit(4)
        else:
            print("cookie 格式错误！...本次操作已退出")
            exit(4)
getCk = getJDCookie()
getCk.getCookie()

if "cash_zlzh" in os.environ:
    if len(os.environ["cash_zlzh"]) > 1:
        cash_zlzh = os.environ["cash_zlzh"]
        cash_zlzh = cash_zlzh.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
        print("已获取并使用Env环境 cash_zlzh:", cash_zlzh)
# 获取TG_BOT_TOKEN
if "TG_BOT_TOKEN" in os.environ:
    if len(os.environ["TG_BOT_TOKEN"]) > 1:
        TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
        print("已获取并使用Env环境 TG_BOT_TOKEN")
# 获取TG_USER_ID
if "TG_USER_ID" in os.environ:
    if len(os.environ["TG_USER_ID"]) > 1:
        TG_USER_ID = os.environ["TG_USER_ID"]
        print("已获取并使用Env环境 TG_USER_ID")
# 获取代理ip
if "TG_PROXY_IP" in os.environ:
    if len(os.environ["TG_PROXY_IP"]) > 1:
        TG_PROXY_IP = os.environ["TG_PROXY_IP"]
        print("已获取并使用Env环境 TG_PROXY_IP")
# 获取TG 代理端口
if "TG_PROXY_PORT" in os.environ:
    if len(os.environ["TG_PROXY_PORT"]) > 1:
        TG_PROXY_PORT = os.environ["TG_PROXY_PORT"]
        print("已获取并使用Env环境 TG_PROXY_PORT")
    elif not TG_PROXY_PORT:
        TG_PROXY_PORT = ''
# 获取TG TG_API_HOST
if "TG_API_HOST" in os.environ:
    if len(os.environ["TG_API_HOST"]) > 1:
        TG_API_HOST = os.environ["TG_API_HOST"]
        print("已获取并使用Env环境 TG_API_HOST")
# 获取pushplus+ PUSH_PLUS_TOKEN
if "PUSH_PLUS_TOKEN" in os.environ:
    if len(os.environ["PUSH_PLUS_TOKEN"]) > 1:
        PUSH_PLUS_TOKEN = os.environ["PUSH_PLUS_TOKEN"]
        print("已获取并使用Env环境 PUSH_PLUS_TOKEN")

# 获取通知，
notify_mode = []
if PUSH_PLUS_TOKEN:
    notify_mode.append('pushplus')
if TG_BOT_TOKEN and TG_USER_ID:
    notify_mode.append('telegram_bot')

# tg通知
def telegram_bot(title, content):
    try:
        print("\n")
        bot_token = TG_BOT_TOKEN
        user_id = TG_USER_ID
        if not bot_token or not user_id:
            print("tg服务的bot_token或者user_id未设置!!\n取消推送")
            return
        print("tg服务启动")
        if TG_API_HOST:
            url = f"{TG_API_HOST}/bot{TG_BOT_TOKEN}/sendMessage"
        else:
            url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'chat_id': str(TG_USER_ID), 'text': f'{title}\n\n{content}', 'disable_web_page_preview': 'true'}
        proxies = None
        if TG_PROXY_IP and TG_PROXY_PORT:
            proxyStr = "http://{}:{}".format(TG_PROXY_IP, TG_PROXY_PORT)
            proxies = {"http": proxyStr, "https": proxyStr}
        try:
            response = requests.post(url=url, headers=headers, params=payload, proxies=proxies).json()
        except:
            print('推送失败！')
        if response['ok']:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)

# push推送
def pushplus_bot(title, content):
    try:
        print("\n")
        if not PUSH_PLUS_TOKEN:
            print("PUSHPLUS服务的token未设置!!\n取消推送")
            return
        print("PUSHPLUS服务启动")
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSH_PLUS_TOKEN,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)

def send(title, content):
    """
    使用 bark, telegram bot, dingding bot, serverJ 发送手机推送
    :param title:
    :param content:
    :return:
    """
    footer = '开源免费使用：https://github.com/curtinlv/JD-Script'
    content = content + "\n" + footer
    for i in notify_mode:

        if i == 'telegram_bot':
            if TG_BOT_TOKEN and TG_USER_ID:
                telegram_bot(title=title, content=content)
            else:
                print('未启用 telegram机器人')
            continue
        elif i == 'pushplus':
            if PUSH_PLUS_TOKEN:
                pushplus_bot(title=title, content=content)
            else:
                print('未启用 PUSHPLUS机器人')
            continue
        else:
            print('此类推送方式不存在')

def userAgent():
    """
    随机生成一个UA
    jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1
    :return: ua
    """
    if not UserAgent:
        uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
        addressid = ''.join(random.sample('1234567898647', 10))
        iosVer = ''.join(random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
        iosV = iosVer.replace('.', '_')
        iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
        ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
        return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'
    else:
        return UserAgent

def buildHeader(ck):
    headers = {
        'Origin': 'https://h5.m.jd.com',
        'Cookie': ck,
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://h5.m.jd.com/babelDiy/Zeus/GzY6gTjVg1zqnQRnmWfMKC4PsT1/index.html?lng=&lat=&sid=&un_area=',
        'Host': 'api.m.jd.com',
        'User-Agent': userAgent(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    return headers

def getShareCode(header):
    global aNum
    try:
        url = 'https://api.m.jd.com/client.action?functionId=cash_getJDMobShareInfo&body=%7B%22source%22%3A2%7D&appid=CashReward&client=m&clientVersion=9.2.8'
        resp = requests.post(url=url, headers=header,  verify=False, timeout=30).json()
        if resp['data']['bizMsg'] == 'success' and resp['data']['success']:
            inviteCode = resp['data']['result']['inviteCode']
            shareDate = resp['data']['result']['shareDate']
            aNum = 0
            return inviteCode, shareDate
        else:
            print("获取互助码失败！")
            return 0, 0
    except Exception as e:
        if aNum < 5:
            aNum += 1
            return getShareCode(header)
        else:
            aNum = 0
            print("获取互助码失败！", e)
            return 0, 0

def helpCode(header, inviteCode, shareDate, uNUm, user, name):
    try:
        url = f'https://api.m.jd.com/client.action?functionId=cash_mob_assist&body=%7B%22source%22%3A3%2C%22inviteCode%22%3A%22{inviteCode}%22%2C%22shareDate%22%3A%22{shareDate}%22%7D&appid=CashReward&client=m&clientVersion=9.2.8'
        resp = requests.post(url=url, headers=header,  verify=False, timeout=30).json()
        if resp['data']['success']:
            print(f'用户{uNUm}【{user}】助力【{name}】{resp["data"]["bizMsg"]} -> 您也获得{resp["data"]["result"]["cashStr"]}现金')
        else:
            print(f'用户{uNUm}【{user}】助力【{name}】{resp["data"]["bizMsg"]}')
    except Exception as e:
        print("helpCode Error", e)
        print(f'用户{uNUm}【{user}】助力【{name}】报错了！')

def cash_exchangePage(ck):
    try:
        iosVer = ''.join(random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
        url = 'https://api.m.jd.com/client.action?functionId=cash_exchangePage'
        header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': ck,
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Host': 'api.m.jd.com',
            'User-Agent': f'JD4iPhone/167724 (iPhone; iOS {iosVer}; Scale/3.00)',
            'Referer': '',
            'Accept-Language': 'zh-Hans-CN;q=1'
        }
        body = f'body=%7B%7D&build=167724&client=apple&clientVersion=10.0.6&d_brand=apple&d_model=iPhone13%2C4&eid=&isBackground=N&joycious=82&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&openudid=809409cbd5bb8a0fa8fff41378c1afe91b8075ad&osVersion={iosVer}&partner=apple&rfs=0000&scope=10&screen=1125%2A2436&sign=5b8aa440653bb1fcbad0f0ff71671cae&st=1625368739358&sv=122&uemps=0-0&uts=&uuid=&wifiBssid=unknown'
        response = requests.post(url=url, headers=header, data=body, verify=False, timeout=30).json()
        return response['data']['result']['totalMoney']
    except Exception as e:
        print("cash_exchangePage Error", e)
        return 0

def start():
    print("### 签到领现金-助力 ###")
    global cookiesList, userNameList, pinNameList, ckNum, cashCount, cashCountdict
    cookiesList, userNameList, pinNameList = getCk.iscookie()
    for ckname in cash_zlzh:
        try:
            ckNum = userNameList.index(ckname)
        except Exception as e:
            try:
                ckNum = pinNameList.index(ckname)
            except:
                print(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                continue

        print(f"### 开始助力账号【{userNameList[int(ckNum)]}】###")
        inviteCode, shareDate = getShareCode(buildHeader(cookiesList[ckNum]))
        if inviteCode == 0:
            print(f"## {userNameList[int(ckNum)]}  获取互助码失败。请稍后再试！")
            continue
        u = 0
        for i in cookiesList:
            if i == cookiesList[ckNum]:
                u += 1
                continue
            helpCode(buildHeader(i), inviteCode, shareDate, u+1, userNameList[u], userNameList[ckNum])
            time.sleep(sleepNum)
            u += 1
        totalMoney = cash_exchangePage(cookiesList[ckNum])
        cashCount += totalMoney
        cashCountdict[userNameList[ckNum]] = totalMoney

    message("\n-------------------------")
    for i in cashCountdict.keys():
        message(f"账号【{i}】当前现金: ￥{cashCountdict[i]}")
    message("## 总累计获得 ￥%.2f" % cashCount)
    send("### 签到领现金-助力 ###", message_info)


if __name__ == '__main__':
    start()
