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
cron: 0 0 9-21 1 *
new Env('城城分现金助力(1.9-1.21)');
update 2022.1.9
'''
## 助力账号名称：可填用户名 或 pin的值不要; env 设置 export ccfxj_help="Curtinlv&用户2"  多账号&分隔
ccfxj_help=["Curtinlv", ]
#是否开启通知，Ture：发送通知，False：不发送
isNotice="true"
# UA 可自定义你的，注意格式: 【 jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1 】
UserAgent = ''
ccfxj_isOrder="true"

countM = {}
outCK = []

import os, re, sys
import random
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
from urllib.parse import unquote

try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)

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


if "ccfxj_isOrder" in os.environ:
    if len(os.environ["ccfxj_isOrder"]) > 1:
        ccfxj_isOrder = os.environ["ccfxj_isOrder"]
if "isNotice" in os.environ:
    if len(os.environ["isNotice"]) > 1:
        isNotice = os.environ["isNotice"]

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
        'User-Agent': 'jdapp;iPhone;10.2.4;;;M/5.0;appBuild/167870;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22ENK5DNK5Y2TuDWTsEQOmZwO4ZwZwDNOzDzrtCWPwZJunYtqmDzVrZK%3D%3D%22%2C%22sv%22%3A%22CJGkCm%3D%3D%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1641688257%2C%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.360buy.jdmobile%22%2C%22ridx%22%3A-1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;',
        'Referer': 'https://bunearth.m.jd.com/babelDiy/Zeus/x4pWW6pvDwW7DjxMmBbnzoub8J/index.html?inviteId=oev_XKwNZWFLYxOrCpeJ977LiD9Y&encryptedPin=RnFgy28NOT3fwtQUrIByXZNawkwqxlr3&sid=221a60c654ad1bc111e2fdee34aaa7cw&un_area=19_1607_6736_62140',
        'Accept-Language': 'zh-cn'
    }
    return headers

def getInviteId(ck):
    try:
        url = 'https://api.m.jd.com/client.action'
        body = 'functionId=city_getHomeDatav1&body={"lbsCity":"19","realLbsCity":"1601","inviteId":"","headImg":"","userName":"","taskChannel":"1","location":"113.,23.","safeStr":""}&client=wh5&clientVersion=1.0.0'
        resp = requests.post(url=url, headers=buid_header(ck), data=body, timeout=30).json()
        userActBaseInfo = resp['data']['result']['userActBaseInfo']
        mainInfos = resp['data']['result']['mainInfos']
        inviteId = userActBaseInfo['inviteId']
        poolMoney = userActBaseInfo['poolMoney']
        cityCodeList, roundNumList = [], []
        for i in mainInfos:
            cityCodeList.append(i['cityCode'])
            roundNumList.append(i['roundNum'])
        return inviteId, poolMoney, cityCodeList, roundNumList
    except:
        return "", "0", [], []

def zhuli(ck, inviteId, user):
    global outCK
    url = 'https://api.m.jd.com/client.action'
    body = 'functionId=city_getHomeDatav1&body={"lbsCity":"19","realLbsCity":"1601","inviteId":"' + inviteId + '","headImg":"","userName":"","taskChannel":"1","location":"113.,23.","safeStr":"{}"}&client=wh5&clientVersion=1.0.0&uuid='
    resp = requests.post(url=url, headers=buid_header(ck), data=body, timeout=30).json()
    import json
    try:
        m = resp['data']['result']['toasts'][0]['msg']
        status = resp['data']['result']['toasts'][0]['status']
        if status == "3":
            outCK.append(ck)
    except:
        print(f"\t{user}--助力失败")


def city_receiveCash(ck):
    try:
        invid, poolMoney, cityCodeList, roundNumList = getInviteId(ck)
        for roundNum in roundNumList:
            url = 'https://api.m.jd.com/client.action'
            body = 'functionId=city_receiveCash&body={"cashType":1,"roundNum":' + str(roundNum) + '}&client=wh5&clientVersion=1.0.0&uuid='
            resp = requests.post(url=url, headers=buid_header(ck), data=body, timeout=30).json()
    except:
        pass

def delckValue(z_cookiesList, z_userNameList):
    for i in outCK:
        try:
            ckNum = cookiesList.index(i)
            print(f"\t{z_userNameList[ckNum]} 已没有助力机会。")
            z_cookiesList.pop(ckNum)
            z_userNameList.pop(ckNum)
        except:
            continue
    return z_cookiesList, z_userNameList


def start():
    scriptName = '### 城城分现金-助力 ###'
    print(scriptName)
    global cookiesList, userNameList, pinNameList, ckNum
    cookiesList, userNameList = getCk.iscookie()
    z_cookiesList,z_userNameList = [], []
    for c,u in zip(cookiesList,userNameList):
        z_cookiesList.append(c)
        z_userNameList.append(u)
    if ccfxj_isOrder == "true":
        for ck, user in zip(cookiesList, userNameList):
            m_ck = ck
            try:
                invid, poolMoney, cityCodeList, roundNumList = getInviteId(m_ck)
            except:
                print(f"账号异常【{user}】，无法获取助力码，请手动分享~")
                continue
            print(f"### 开始助力 {user}\t当前金额 {poolMoney}\t助力码 {invid}")
            z_cookiesList, z_userNameList = delckValue(z_cookiesList, z_userNameList)
            for ck, user_a in zip(z_cookiesList, z_userNameList):
                if user == user_a:
                    continue
                zhuli(ck, invid, user_a)
            city_receiveCash(m_ck)
    else:
        count_ck, count_u = [], []
        if not ccfxj_help:
            print("您未配置助力的账号，\n助力账号名称：可填用户名 或 pin的值不要; \nenv 设置 export ccfxj_help=\"Curtinlv&用户2\"  多账号&分隔\n本次退出。")
            sys.exit(0)
        for ckname in ccfxj_help:
            try:
                ckNum = userNameList.index(ckname)
            except Exception as e:
                try:
                    ckNum = userNameList.index(unquote(ckname))
                except:
                    print(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                    continue
            userName = userNameList[ckNum]
            try:
                invid, poolMoney, cityCodeList, roundNumList = getInviteId(cookiesList[ckNum])
            except:
                print(f"账号异常【{ckname}】，无法获取助力码，请手动分享~")
                continue
            msg(f"### 本次助力车头：{userName}")
            count_ck.append(cookiesList[ckNum])
            count_u.append(ckname)
            z_cookiesList, z_userNameList = delckValue(z_cookiesList, z_userNameList)
            for ck,user in zip(z_cookiesList,z_userNameList):
                if userName == user:
                    continue
                zhuli(ck, invid, user)
            city_receiveCash(cookiesList[ckNum])
    msg("城城分现金当前余额：")
    msg("*"*40)
    if ccfxj_isOrder == "true":
        for ck,user in zip(cookiesList,userNameList):
            invid, poolMoney, cityCodeList, roundNumList = getInviteId(ck)
            msg(f"用户[{user}]\t待提现{poolMoney}")
    else:
        for ck,user in zip(count_ck,count_u):
            invid, poolMoney, cityCodeList, roundNumList = getInviteId(ck)
            msg(f"用户[{user}]\t待提现{poolMoney}")
    msg("*" * 40)
    msg("\n***************\n城城分现金入口：\n25:/￥81H1VBRi2hU6z%☆")
    if isNotice == "true":
        send(scriptName, msg_info)

if __name__ == '__main__':
    start()