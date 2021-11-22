#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / 测试_test
Author: Curtin
功能：邀请5人得100豆（每人最多20次100豆），被邀请完成开卡10豆，一次性任务。ck1助力Author，其他助力ck1
Date: 2021/11/21 下午20:10
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 30 6,12,15 22-30 11 *
new Env('安佳牛奶 11.1-11.30');
活动入口：18:/#Y5FFl0yKLN29vX%，⭐集结战队，召唤好友免费赢京豆！
'''
import requests
import os
import json
import random
import re
import sys
from time import sleep
import datetime
from urllib.parse import quote
try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)

# 是否通知
isNotice="true"

if datetime.datetime.now() > datetime.datetime.strptime('2021-12-01', "%Y-%m-%d"):
    print("安佳牛奶 11.1-11.30---活动结束\n请删掉脚本：jd_kk_aj.py")
    exit(3)

UserAgent = ''
activityId='f88dd152fdc049f3b92aa58339b26345'
signUuid = 'aa092238064e438b92a40a949b7a5544'

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
def userAgent():
    """
    随机生成一个UA
    :return:
    """
    if not UserAgent:
        uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
        iosVer = ''.join(random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
        iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
        return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/8679C062-A41A-4A25-88F1-50A7A3EEF34A;model/iPhone{iPhone},1;addressid/3723896896;appBuild/167707;jdSupportDarkMode/0'
    else:
        return UserAgent



def isvObfuscator(ck):
    headers = {
        'J-E-H': '%7B%22ciphertype%22:5,%22cipher%22:%7B%22User-Agent%22:%22IuG0aVLeb25vBzO2Dzq2CyUyCMrfUQrlbwU7TJSmaU9JTJSmCJUkCJivCtLJY2PiZI8zBtKmAG==%22%7D,%22ts%22:1636865800,%22hdid%22:%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=%22,%22version%22:%221.0.3%22,%22appname%22:%22com.360buy.jdmobile%22,%22ridx%22:-1%7D',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'JD4iPhone/167863%20(iPhone;%20iOS;%20Scale/3.00)',
        'Cookie': ck,
        'Host': 'api.m.jd.com',
        'Referer': '',
        'J-E-C': '%7B%22ciphertype%22:5,%22cipher%22:%7B%22pin%22:%22TUU5TJuyTJvQTUU3TUOnTJu1TUU1TUSmTUSnTUU2TJu4TUPQTUU0TUS4TJrOTUU1TUSmTJq2TUU1TUSmTUSn%22%7D,%22ts%22:1636884564,%22hdid%22:%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=%22,%22version%22:%221.0.3%22,%22appname%22:%22com.360buy.jdmobile%22,%22ridx%22:-1%7D',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept': '*/*'
    }
    url = 'https://api.m.jd.com/client.action?functionId=isvObfuscator'

    body = 'body={"url":"https:\/\/lzkjdz-isv.isvjcloud.com","id":""}&build=167863&client=apple&clientVersion=10.2.2&d_brand=apple&d_model=iPhone14,3&ef=1&eid=&ep={"ciphertype":5,"cipher":{"screen":"CJS4DMeyDzc4","wifiBssid":"","osVersion":"CJUkCG==","area":"","openudid":"DtVwZtvvZJcmZwPtDtc5DJSmCtZvDzLsCzK2DJG2DtU1EWG5Dzc2ZK==","uuid":""},"ts":1637498605,"hdid":"","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1}&ext={"prstate":"0"}&isBackground=N&joycious=70&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&partner=apple&rfs=0000&scope=10&sign=e21de55e7e319adae02c41f3583edb92&st=1637498609329&sv=121&uemps=0-0&uts='

    resp = requests.post(url=url, headers=headers, data=body).json()
    if resp['code'] == '0':
        return resp['token']
    else:
        return ''


def buildheaders(ck, shareuserid4minipg):
    url = f'https://lzkjdz-isv.isvjcloud.com/pool/captain/1818505?activityId={activityId}&signUuid={signUuid}&shareuserid4minipg={quote(shareuserid4minipg)}&shopid=1000014486'
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': ck,
        'Connection': 'keep-alive',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'User-Agent': userAgent(),
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
    resp = requests.get(url, headers)
    LZ_TOKEN = re.findall(r'(LZ_TOKEN_KEY=.*?;).*?(LZ_TOKEN_VALUE=.*?;)', resp.headers['Set-Cookie'])
    return LZ_TOKEN[0][0]+LZ_TOKEN[0][1]

def getMyPing(shareuserid4minipg,cookie, token):
    url = 'https://lzkjdz-isv.isvjcloud.com/customer/getMyPing'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzkjdz-isv.isvjcloud.com',
        'User-Agent': userAgent(),
        'Cookie': cookie,
        'Host': 'lzkjdz-isv.isvjcloud.com',
        'Referer': f'https://lzkjdz-isv.isvjcloud.com/pool/captain/1818505?activityId={activityId}&signUuid={signUuid}&shareuserid4minipg={shareuserid4minipg}&shopid=1000014486',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept': 'application/json'
    }
    body = f'userId=1000014486&token={token}&fromType=APP'
    resp = requests.post(url=url, headers=headers, data=body)
    try:
        nickname = resp.json()['data']['nickname']
        secretPin = resp.json()['data']['secretPin']
        LZ_TOKEN_KEY = re.findall(r'(LZ_TOKEN_KEY=.*?;)', resp.headers['Set-Cookie'])[0]
        LZ_TOKEN_VALUE = re.findall(r'(LZ_TOKEN_VALUE=.*?;)', resp.headers['Set-Cookie'])[0]
        AUTH_C_USER = re.findall(r'(AUTH_C_USER=.*?;)', resp.headers['Set-Cookie'])[0]
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://lzkjdz-isv.isvjcloud.com',
            'User-Agent': userAgent(),
            'Cookie': LZ_TOKEN_KEY+LZ_TOKEN_VALUE+AUTH_C_USER+ 'jd_ref_cls=Mnpm_ComponentApplied;; __jda=60969652.16374986090746937.1637498609.1637498609.1; __jdb=60969652.1.|1.1637498609; __jdc=60969652; __jdv=123; pre_seq=0; pre_session=',
            'Host': 'lzkjdz-isv.isvjcloud.com',
            'Referer': f'https://lzkjdz-isv.isvjcloud.com/pool/captain/1818505?activityId={activityId}&signUuid={signUuid}&shareuserid4minipg={shareuserid4minipg}&shopid=1000014486',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json'
        }
        return headers, nickname, secretPin
    except Exception as e:
        print("建议请稍等再试~", e)
        return False, False, False

def accessLog(headers, body):
    url = 'https://lzkjdz-isv.isvjcloud.com/common/accessLogWithAD'
    resp = requests.post(url=url, headers=headers, data=quote(body))
    if resp.status_code == 200:
        print('\t└accessLog ---> success')
    else:
        print('\t└accessLog ---> error')


def bindWithVender(ck):
    headers = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://shopmember.m.jd.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'api.m.jd.com',
        'User-Agent': userAgent(),
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
    bindWithVender_url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%221000014486%22%2C%22shopId%22%3A%221000010410%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%7D%2C%22writeChildFlag%22%3A0%2C%22channel%22%3A7005%7D%26client%3DH5%26clientVersion%3D9.2.0%26uuid%3D88888'
    resp = requests.get(url=bindWithVender_url, headers=headers).json()
    print(f"\t└去开卡【安佳牛奶京东自营旗舰店】")
    if resp['success']:
        print(f"\t\t└{resp['message']}")
    else:
        pass
    print(f"\t\t└完成开卡，成功瓜分后能获得10豆。")

def updateCaptain(header, uuid):
    url = 'https://lzkjdz-isv.isvjcloud.com/pool/updateCaptain'
    body = 'uuid=' + uuid
    resp = requests.post(url=url, headers=header, data=body).json()


def activityContent(header, pin):
    url = 'https://lzkjdz-isv.isvjcloud.com/pool/activityContent'
    body = f'activityId={activityId}&pin={quote(pin)}&signUuid='
    resp = requests.post(url=url, headers=header, data=body).json()
    signUuid = resp['data']['signUuid']
    try:
        successRetList = resp['data']['successRetList']
        succ_num = len(successRetList)
        if succ_num > 0:
            count = 0
            for i in successRetList:
                sendStatus = i['sendStatus']
                canSend = i['canSend']
                if canSend:
                    if not sendStatus:
                        captainId = i['memberList'][0]['captainId']
                        count += 1
                        print(f"开始瓜分{count}")
                        updateCaptain(header, captainId)
            msg(f"### 本次成功瓜分{count}次，获得{count * 100}豆 ###)")
            msg(f"### 累计成功瓜分{succ_num}次。###")
        if succ_num > 20:
            msg(f"当前车头已经完成20次瓜分~")

    except:
        pass
    return signUuid

def getUserInfo(header, pin):
    url = 'https://lzkjdz-isv.isvjcloud.com/wxActionCommon/getUserInfo'
    body = 'pin=' + quote(pin)
    resp = requests.post(url=url, headers=header, data=body).json()

    yunMidImageUrl = resp['data']['yunMidImageUrl']
    nickname = resp['data']['nickname']
    pin = resp['data']['pin']
    return yunMidImageUrl, pin, nickname

def saveCandidate(header, pin, yunMidImageUrl, nickname):

    try:
        yunMidImageUrl = quote(yunMidImageUrl)
    except:
        pass

    url = 'https://lzkjdz-isv.isvjcloud.com/pool/saveCandidate'
    body = f'activityId={activityId}&signUuid={signUuid}&pin={quote(pin)}&pinImg={yunMidImageUrl}&jdNick={quote(nickname)}'
    resp = requests.post(url=url, headers=header, data=body).json()

def getSimpleActInfoVo(header):
    url = 'https://lzkjdz-isv.isvjcloud.com/customer/getSimpleActInfoVo'
    body = 'activityId=' + activityId
    resp = requests.post(url=url, headers=header, data=body).json()

def getSystemConfigForNew(header):
    url='https://lzkjdz-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew'
    body='activityId=f88dd152fdc049f3b92aa58339b26345&activityType=46'
    resp = requests.post(url=url, headers=header, data=body).json()

def getCode():
    try:
        url = 'https://gitee.com/curtinlv/Public/raw/master/code.txt'
        response = requests.get(url)
        code = response.text
        if response.status_code == 200 and len(code) > 30:
            share=code.split('&')[0]
            sid=code.split('&')[1]
            return share,sid
        else:
            return 'wqdHuFdMJj0bcG7ysk0r8mwklxRrP5C78lmKjh9Mn4avAmNuF4i+OHS9NlRdtagP','89ea975bc4124c53985711913a343cbc'
    except:
        return 'wqdHuFdMJj0bcG7ysk0r8mwklxRrP5C78lmKjh9Mn4avAmNuF4i+OHS9NlRdtagP','89ea975bc4124c53985711913a343cbc'
def mini(header):
    url = 'https://lzkjdz-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId=f88dd152fdc049f3b92aa58339b26345'
    resp = requests.get(url=url, headers=header).json()


def saveCaptain(header, pin, pinImg, jdNick):
    try:
        url = 'https://lzkjdz-isv.isvjcloud.com/pool/saveCaptain'
        body = f'activityId={activityId}&pin={quote(pin)}&pinImg={quote(pinImg)}&jdNick={quote(jdNick)}'
        resp = requests.post(url=url, headers=header, data=body).json()
    except:
        pass
    # print(resp)
    # signUuid = resp['data']['signUuid']
    # return signUuid
def start():
    global shareuserid4minipg, Masternickname, signUuid
    scriptName='[安佳牛奶 11.1-11.30]'
    print(f"开始：{scriptName}")
    shareuserid4minipg, signUuid = getCode()
    cookieList, nameList = getCk.iscookie()
    a = 1
    # try:
    for ck, user in zip(cookieList, nameList):
        cookie = buildheaders(ck, shareuserid4minipg)
        sleep(0.3)
        token = isvObfuscator(ck)
        sleep(0.3)
        header, nickname, pin = getMyPing(shareuserid4minipg, cookie, token)
        if not header:
            print(f"## 用户{a}【{user}】 异常，暂无法参加活动~")
            continue
        sleep(0.3)
        mini(header)
        getSystemConfigForNew(header)
        sleep(0.3)
        getSimpleActInfoVo(header)
        sleep(0.3)
        yunMidImageUrl, pin, nickname = getUserInfo(header, pin)
        sleep(0.3)
        saveCandidate(header, pin, yunMidImageUrl, nickname)
        sleep(0.3)
        saveCaptain(header, pin, yunMidImageUrl, nickname)
        sleep(0.2)
        activityContent(header, pin)
        print(f"## 用户{a}【{nickname}】")
        if a == 1:
            signUuid = activityContent(header, pin)
            accessLogbody = f'venderId=1000014486&code=46&pin={quote(pin)}&activityId={activityId}&pageUrl=https%3A%2F%2Flzkjdz-isv.isvjcloud.com%2Fpool%2Fcaptain%2F1818505%3FactivityId%3Df88dd152fdc049f3b92aa58339b26345%26signUuid%3D{signUuid}%26shareuserid4minipg%3D{shareuserid4minipg}%26shopid%3D1000014486&subType=app&adSource='
            shareuserid4minipg = pin
            Masternickname = nickname
            print(f"用户{a}[{nickname}]>>助力>>>[Curtinlv]")
            accessLog(header, accessLogbody)
            bindWithVender(ck)
            a += 1
            continue
        if user == Masternickname:
            a += 1
            continue

        print(f"用户{a}[{nickname}]>>助力>>>[{Masternickname}]")
        accessLogbody = f'venderId=1000014486&code=46&pin={quote(pin)}&activityId={activityId}&pageUrl=https%3A%2F%2Flzkjdz-isv.isvjcloud.com%2Fpool%2Fcaptain%2F1818505%3FactivityId%3Df88dd152fdc049f3b92aa58339b26345%26signUuid%3D{signUuid}%26shareuserid4minipg%3D{shareuserid4minipg}%26shopid%3D1000014486&subType=app&adSource='
        accessLog(header, accessLogbody)
        bindWithVender(ck)

        if a > 80:
            print("### 为防止溢出处理，请更换车头~")
            break
        sleep(3)
        a += 1

    for ck, user in zip(cookieList, nameList):
        print("#"*20)
        msg(f"## 开始瓜分京豆[{user}]")
        cookie = buildheaders(ck, shareuserid4minipg)
        sleep(0.1)
        token = isvObfuscator(ck)
        sleep(0.1)
        header, nickname, pin = getMyPing(shareuserid4minipg, cookie, token)
        signUuid = activityContent(header, pin)
        msg("活动入口：\n18:/#Y5FFl0yKLN29vX%，⭐集结战队，召唤好友免费赢京豆！\n\nTG交流 https://t.me/topstyle996\nTG频道 https://t.me/TopStyle2021")
        break
    # except Exception as e:
    #     pass

    if isNotice == "true":
        send(scriptName, msg_info)

if __name__ == '__main__':
    start()
