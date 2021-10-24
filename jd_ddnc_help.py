#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_ddnc_help_list 
Author: Curtin
功能：东东农场-仅助力使用
Date: 2021/10/23 下午4:15
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 0 0 * * *
new Env('东东农场-助力');
'''
# 是否按ck顺序助力, true: 按顺序助力 false：按指定用户助力，默认true
ddnc_isOrder="true"
# 东东农场助力名单(当ddnc_isOrder="false" 才生效), ENV 环境设置 export ddnc_help_list="Curtinlv&用户2&用户3"
ddnc_help_list = ["Curtinlv", "用户2", "用户3"]
#是否开启通知，Ture：发送通知，False：不发送
isNotice=True
# UA 可自定义你的, 默认随机生成UA。
UserAgent = ''

import os, re, sys
import random
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")
    exit(3)
from urllib.parse import unquote
# requests.packages.urllib3.disable_warnings()
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep


def userAgent():
    """
    随机生成一个UA
    jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1
    :return: ua
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.15(0x18000f29) NetType/WIFI Language/zh_CN'

    """
    uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
    addressid = ''.join(random.sample('1234567898647', 10))
    iosVer = ''.join(random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
    iosV = iosVer.replace('.', '_')
    iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
    ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(
        random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
        random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
    if not UserAgent:
        return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'
    else:
        return UserAgent
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
if "ddnc_isOrder" in os.environ:
    if len(os.environ["ddnc_isOrder"]) > 1:
        ddnc_isOrder = os.environ["ddnc_isOrder"]
if "ddnc_help_list" in os.environ:
    if len(os.environ["ddnc_help_list"]) > 1:
        ddnc_help_list = os.environ["ddnc_help_list"]
        if '&' in ddnc_help_list:
            ddnc_help_list = ddnc_help_list.split('&')
        print("已获取并使用Env环境 ddnc_help_list:", ddnc_help_list)
if not isinstance(ddnc_help_list, list):
    ddnc_help_list = ddnc_help_list.split(" ")


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

def buildHeaders(ck):
    headers = {
        'Cookie': ck,
        'content-type': 'application/json',
        'Connection': 'keep-alive',
        'Referer': '',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'Host': 'api.m.jd.com',
        'User-Agent': userAgent()
    }
    return headers

def awardInviteFriendForFarm(ck):
    url = f'https://api.m.jd.com/client.action?functionId=awardInviteFriendForFarm&body=%7B%7D&appid=wh5'
    response = requests.get(url=url, headers=buildHeaders(ck), timeout=10).json()
    print(response)
def getShareCode(ck):
    url = f'https://api.m.jd.com/client.action?functionId=initForFarm&body=%7B%22shareCode%22%3A%22%22%2C%22imageUrl%22%3A%22%22%2C%22nickName%22%3A%22%22%2C%22version%22%3A14%2C%22channel%22%3A2%2C%22babelChannel%22%3A3%7D&appid=wh5'
    response = requests.get(url=url, headers=buildHeaders(ck), timeout=10).json()
    return response['farmUserPro']['shareCode']

def ddnc_help(ck, nickname, shareCode, masterName):
    try:
        url = f'https://api.m.jd.com/client.action?functionId=initForFarm&body=%7B%22shareCode%22%3A%22{shareCode}%22%2C%22imageUrl%22%3A%22%22%2C%22nickName%22%3A%22%22%2C%22version%22%3A14%2C%22channel%22%3A2%2C%22babelChannel%22%3A3%7D&appid=wh5'
        response = requests.get(url=url, headers=buildHeaders(ck), timeout=10).json()
        # print(response['farmUserPro'])
        # print("\n")
        # print(response['helpResult'])
        # print("\n")
        # masterUserName = response['helpResult']['masterUserInfo']['nickName']
        help_result = response['helpResult']['code']
        if help_result == "0":
            print(f"\t└👌{nickname} 助力成功～")
        elif help_result == "8":
            print(f"\t└😆{nickname} 已没有助力机会~  ")
        elif help_result == "10":
            msg(f"\t└☺️ {masterName} 今天好友助力已满～")
            # awardInviteFriendForFarm(ck)
            return True
        else:
            print(f"\t└😄 {nickname} 助力 {masterName} ")

        return False
    except Exception as e:
        print(f"{nickname} 助力失败～", e)
        return False

def start():
    try:
        scriptName = '### 东东农场-助力 ###'
        print(scriptName)
        global cookiesList, userNameList, pinNameList, ckNum
        cookiesList, userNameList, pinNameList = getCk.iscookie()
        if ddnc_isOrder == "true":
            for ck,user in zip(cookiesList,userNameList):
                msg(f"开始助力 {user}")
                try:
                    shareCode = getShareCode(ck)
                except Exception as e:
                    print(e)
                    continue
                for ck, nickname in zip(cookiesList, userNameList):
                    if nickname == user:
                        print(f"\t└😓{user} 不能助力自己，跳过~")
                        continue
                    result = ddnc_help(ck, nickname, shareCode, user)
                    if result:
                        break
        elif ddnc_isOrder == "false":
            if not ddnc_help_list:
                print("您未配置助力的账号，\n助力账号名称：可填用户名 或 pin的值不要; \nenv 设置 export ddnc_help_list=\"Curtinlv&用户2\"  多账号&分隔\n本次退出。")
                sys.exit(0)
            for ckname in ddnc_help_list:
                try:
                    ckNum = userNameList.index(ckname)
                except Exception as e:
                    try:
                        ckNum = pinNameList.index(unquote(ckname))
                    except:
                        msg(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                        continue
                masterName = userNameList[ckNum]
                shareCode = getShareCode(cookiesList[ckNum])
                msg(f"开始助力 {masterName}")
                for ck, nickname in zip(cookiesList, userNameList):
                    if nickname == masterName:
                        print(f"\t└😓{masterName} 不能助力自己，跳过~")
                        continue
                    result = ddnc_help(ck, nickname, shareCode, masterName)
                    if result:
                        break
        else:
            print("请检查ddnc_isOrder 变量参数是否正确填写。")
        if isNotice:
            send(scriptName, msg_info)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    start()

