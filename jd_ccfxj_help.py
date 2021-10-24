#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_ccfxj_help 
Author: Curtin
功能：城城分现金助力 活动入口：15.0:/￥WAAD60EE92byb0%，☃そ點①點ひ领哯唫！
Date: 2021/10/20 下午8:59
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
说明：仅测试使用，目前只助力，需要手动领取提现。
cron: 0 0 * * *
new Env('城城分现金助力-助力.py');
'''
## 助力账号名称：可填用户名 或 pin的值不要; env 设置 export ccfxj_help="Curtinlv&用户2"  多账号&分隔
ccfxj_help=["Curtinlv", ]
#是否开启通知，Ture：发送通知，False：不发送
isNotice=True
# UA 可自定义你的，注意格式: 【 jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1 】
UserAgent = ''

import os, re, sys
import random
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
from urllib.parse import unquote
# requests.packages.urllib3.disable_warnings()
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
addressid = ''.join(random.sample('1234567898647', 10))
iosVer = ''.join(random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
iosV = iosVer.replace('.', '_')
iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(
    random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
    random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
###


class getJDCookie(object):
    # 适配各种平台环境ck

    def getckfile(self):
        global v4f
        curf = pwd + 'JDCookies.txt'
        v4f = '/jd/config/config.sh'
        ql_new = '/ql/config/env.sh'
        ql_old = '/ql/config/cookie.sh'
        if os.path.exists(curf):
            with open(curf, "r", encoding="utf-8") as f:
                cks = f.read()
                f.close()
            r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
            cks = r.findall(cks)
            if len(cks) > 0:
                return curf
            else:
                pass
        if os.path.exists(ql_new):
            print("当前环境青龙面板新版")
            return ql_new
        elif os.path.exists(ql_old):
            print("当前环境青龙面板旧版")
            return ql_old
        elif os.path.exists(v4f):
            print("当前环境V4")
            return v4f
        return curf

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
                            if 'pt_key=xxxx' in i:
                                pass
                            else:
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
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback='
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
            if sys.platform == 'ios':
                requests.packages.urllib3.disable_warnings()
                resp = requests.get(url=url, verify=False, headers=headers, timeout=60).json()
            else:
                resp = requests.get(url=url, headers=headers, timeout=60).json()
            if resp['retcode'] == "0":
                nickname = resp['data']['userInfo']['baseInfo']['nickname']
                return ck, nickname
            else:
                context = f"账号{userNum}【{pinName}】Cookie 已失效！请重新获取。"
                print(context)
                return ck, False
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

if "ccfxj_help" in os.environ:
    if len(os.environ["ccfxj_help"]) > 1:
        ccfxj_help = os.environ["ccfxj_help"]
        if '&' in ccfxj_help:
            ccfxj_help = ccfxj_help.split('&')
        print("已获取并使用Env环境 ccfxj_help:", ccfxj_help)
if not isinstance(ccfxj_help, list):
    ccfxj_help = ccfxj_help.split(" ")

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

## 获取通知服务
class msg(object):
    def __init__(self, m):
        self.str_msg = m
        self.message()
    def message(self):
        global msg_info
        print(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass
    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")
        ###################
msg("").main()
##############

def buid_header(ck):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://bunearth.m.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': ck,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'User-Agent': userAgent(),
        'Referer': 'https://bunearth.m.jd.com/babelDiy/Zeus/x4pWW6pvDwW7DjxMmBbnzoub8J/index.html?inviteId=&encryptedPin=&lng=113.&lat=23.&sid=&un_area=',
        'Accept-Language': 'zh-cn'
    }
    return headers

def getInviteId(ck):
    url = 'https://api.m.jd.com/client.action'
    body = 'functionId=city_getHomeData&body={"lbsCity":"19","realLbsCity":"1601","inviteId":"","headImg":"","userName":"","taskChannel":"1"}&client=wh5&clientVersion=1.0.0&uuid=' + uuid
    resp = requests.post(url=url, headers=buid_header(ck), data=body, timeout=30).json()
    userActBaseInfo = resp['data']['result']['userActBaseInfo']
    inviteId = userActBaseInfo['inviteId']
    poolMoney = userActBaseInfo['poolMoney']
    msg(f"当前助力池：{poolMoney} 元")
    return inviteId, poolMoney

def zhuli(ck, inviteId, user):
    url = 'https://api.m.jd.com/client.action'
    body = 'functionId=city_getHomeData&body={"lbsCity":"19","realLbsCity":"1601","inviteId":"' + inviteId + '","headImg":"","userName":"","taskChannel":"1"}&client=wh5&clientVersion=1.0.0&uuid=' + uuid
    resp = requests.post(url=url, headers=buid_header(ck), data=body, timeout=30).json()
    try:
        m = resp['data']['result']['toasts'][0]['msg']
        print(f"{user}--{m}")
    except:
        print(f"{user}--助力失败")


def start():
    scriptName = '### 城城分现金-助力 ###'
    print(scriptName)
    global cookiesList, userNameList, pinNameList, ckNum
    cookiesList, userNameList, pinNameList = getCk.iscookie()
    if not  ccfxj_help:
        print("您未配置助力的账号，\n助力账号名称：可填用户名 或 pin的值不要; \nenv 设置 export ccfxj_help=\"Curtinlv&用户2\"  多账号&分隔\n本次退出。")
        sys.exit(0)
    for ckname in ccfxj_help:
        try:
            ckNum = userNameList.index(ckname)
        except Exception as e:
            try:
                ckNum = pinNameList.index(unquote(ckname))
            except:
                print(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                continue
        userName = userNameList[ckNum]
        invid, poolMoney = getInviteId(cookiesList[ckNum])
        msg(f"### 本次助力车头：{userName}")
        for ck,user in zip(cookiesList,userNameList):
            zhuli(ck, invid, user)

    invid, poolMoney = getInviteId(cookiesList[ckNum])
    msg("\n***************\n城城分现金入口：\n15.0:/￥WAAD60EE92byb0%，☃そ點①點ひ领哯唫！")
    if isNotice:
        send(scriptName, msg_info)

if __name__ == '__main__':
    start()