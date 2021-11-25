#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / 测试
Author: Curtin
功能：邀请1人得20豆（每人最多20次100豆），被邀请完成开卡70+豆，一次性任务。ck1助力Author，其他助力ck1
Date: 2021/11/23 下午20:10
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 30 0,6,12,15,20 23-30 11 *
new Env('奢宠会员-瓜分万元大奖 11.23-11.30')
活动入口：
'''
import requests
import os
import json
import random, string
import re
import sys
from time import sleep
import datetime
import time
from urllib.parse import quote, unquote, quote_plus
try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本后执行一次，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)

# 是否发送通知
isNotice = "true"
def printf(*args):
    text = ''
    for i in args:
        text += i
    print(text)
    sys.stdout.flush()
    
if datetime.datetime.now() > datetime.datetime.strptime('2021-12-01', "%Y-%m-%d"):
    printf("奢宠会员 11.1-11.30---活动结束\n请删掉脚本：jd_kk_shechong.py")
    exit(3)

UserAgent = ''
activityId='dzkmladn20211123A'

countbean = {}
allList = []
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
        iosVer = ''.join(random.sample(["14.5.1", "msg14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
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

    body = 'body={"url":"https:\/\/lzdz1-isv.isvjcloud.com","id":""}&build=167870&client=apple&clientVersion=10.2.4&d_brand=apple&d_model=iPhone10,3&ef=1&eid=&ep={"ciphertype":5,"cipher":{"screen":"CJOyDIeyDNC2","wifiBssid":"","osVersion":"CJGkCm==","area":"","openudid":"ENK5DNK5Y2TuDWTsEQOmZwO4ZwZwDNOzDzrtCWPwZJunYtqmDzVrZK==","uuid":"aQf1ZRdxb2r4ovZ1EJZhcxYlVNZSZz09"},"ts":1637642895,"hdid":"=","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1}&ext={"prstate":"0"}&isBackground=N&joycious=93&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&partner=TF&rfs=0000&scope=10&sign=cbc51d94bb4d6efdac7b6af9dc3637a1&st=1637642927932&sv=101&uemps=0-0&'

    resp = requests.post(url=url, headers=headers, timeout=30, data=body).json()
    if resp['code'] == '0':
        return resp['token']
    else:
        return ''


def buildheaders(ck, shareUuid, shareuserid4minipg):
    sid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
    url = f'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/activity/4963678?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg={shareuserid4minipg}&shopid=1000004123&sid={sid}&un_area='
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': ck,
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'lzdz1-isv.isvjcloud.com',
        'User-Agent': userAgent(),
        'Accept-Language': 'zh-cn'
    }
    resp = requests.get(url, headers)
    LZ_TOKEN = re.findall(r'(LZ_TOKEN_KEY=.*?;).*?(LZ_TOKEN_VALUE=.*?;)', resp.headers['Set-Cookie'])
    return LZ_TOKEN[0][0]+LZ_TOKEN[0][1]

def getMyPing(shareUuid, shareuserid4minipg, cookie, token):
    sid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
    url = 'https://lzdz1-isv.isvjcloud.com/customer/getMyPing'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://lzdz1-isv.isvjcloud.com',
        'User-Agent': userAgent(),
        'Cookie': cookie,
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Referer': f'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/activity/4963678?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg={shareuserid4minipg}&shopid=1000004123&sid={sid}&un_area=',
        'Accept-Language': 'zh-cn',
        'Accept': 'application/json'
    }
    body = f'userId=1000004123&token={token}&fromType=APP'
    resp = requests.post(url=url, headers=headers, timeout=30, data=body)
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
            'Origin': 'https://lzdz1-isv.isvjcloud.com',
            'User-Agent': userAgent(),
            'Cookie': LZ_TOKEN_KEY+LZ_TOKEN_VALUE + AUTH_C_USER + '__jd_ref_cls=Mnpm_ComponentApplied; mba_muid=16376427422281457677509.801.1637642928827; mba_sid=801.14; __jda=60969652.16376427422281457677509.1637642742.1637642742.1637642742.1; __jdb=60969652.5.16376427422281457677509|1.1637642742; __jdc=60969652; __jdv=60969652%7Ckong%7Ct_2011739974_%7Cjingfen%7C394dd4aa2cef4f9cbf65939ceda8cc4c%7C1637577535593; pre_seq=7; pre_session=809409cbd5bb8a0fa8fff41378c1afe91b8075ad|2225',
            'Host': 'lzdz1-isv.isvjcloud.com',
            'Referer': f'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/activity/4963678?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg={shareuserid4minipg}&shopid=1000004123&sid={sid}&un_area=19_1601_3633_63243',            'Accept-Language': 'zh-cn',
            'Accept': 'application/json'
        }
        return headers, nickname, secretPin, AUTH_C_USER
    except Exception as e:
        # printf("建议请稍等再试~", e)
        return False, False, False

def accessLog(headers,pin, shareUuid, shareuserid4minipg, AUTH_C_USER):
    sid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
    accbody = f'venderId=1000004123&code=99&pin={quote(pin)}&activityId={activityId}&pageUrl=https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/activity/4963678?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg={quote(shareuserid4minipg)}&shopid=1000004123&sid=&un_area=&subType=app&adSource=null'
    url = 'https://lzdz1-isv.isvjcloud.com/common/accessLogWithAD'
    resp = requests.post(url=url, headers=headers, timeout=30, data=accbody)
    if resp.status_code == 200:
        LZ_TOKEN_KEY = re.findall(r'(LZ_TOKEN_KEY=.*?;)', resp.headers['Set-Cookie'])[0]
        LZ_TOKEN_VALUE = re.findall(r'(LZ_TOKEN_VALUE=.*?;)', resp.headers['Set-Cookie'])[0]
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://lzdz1-isv.isvjcloud.com',
            'User-Agent': userAgent(),
            'Cookie': LZ_TOKEN_KEY + LZ_TOKEN_VALUE + AUTH_C_USER,
            'Host': 'lzdz1-isv.isvjcloud.com',
            'Referer': f'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/activity/4963678?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg={shareuserid4minipg}&shopid=1000004123&sid={sid}&un_area=',
            'Accept-Language': 'zh-cn',
            'Accept': 'application/json'
            # 'Content-Length': '295'
        }
        printf('\t└accessLog ---> success')
        return headers
    else:
        printf('\t└accessLog ---> error')


def activityContent(header, pin, shareUuid, pinImg, nick):
    url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/activityContent'
    try:
        pinImg =  quote_plus(pinImg)
    except:
        pinImg = ''
    body = f'activityId={activityId}&pin={quote(pin)}&pinImg={pinImg}&nick={quote(nick)}&cjyxPin=&cjhyPin=&shareUuid={shareUuid}'
    resp = requests.post(url=url, headers=header, data=body).json()
    try:
        # printf(json.dumps(resp, indent=4, ensure_ascii=False))
        actorUuid = resp['data']['actorUuid']
        shareTitle = resp['data']['shareTitle']
        return actorUuid, shareTitle
    except:
        return None, None

def getUserInfo(header, pin):
    url = 'https://lzdz1-isv.isvjcloud.com/wxActionCommon/getUserInfo'
    body = 'pin=' + quote(pin)
    resp = requests.post(url=url, headers=header, data=body).json()
    yunMidImageUrl = resp['data']['yunMidImageUrl']
    nickname = resp['data']['nickname']
    secretPin = resp['data']['secretPin']
    return yunMidImageUrl, secretPin, nickname

def checkOpenCard(header, actorUuid,shareUuid, pin):
    url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/checkOpenCard'
    body = f'activityId={activityId}&actorUuid={actorUuid}&shareUuid={shareUuid}&pin={quote(pin)}'
    resp = requests.post(url=url, headers=header, data=body).json()
    # printf(json.dumps(resp, indent=4, ensure_ascii=False))
    openCard1 = resp['data']['openCard1']
    openCard2 = resp['data']['openCard2']
    score1 = resp['data']['score1']
    score2 = resp['data']['score2']
    venderIdList=[]
    channelList=[]
    if not openCard1:
        cardList1 = resp['data']['cardList1']
        for i in cardList1:
            if i['status'] == 0:
                toUrl = i['toUrl']
                venderId = re.findall(r'venderId=(\d+)', toUrl)[0]
                channel = re.findall(r'channel=(\d+)', toUrl)[0]
                venderIdList.append(venderId)
                channelList.append(channel)
    if not openCard2:
        cardList2 = resp['data']['cardList2']
        for i in cardList2:
            if i['status'] == 0:
                toUrl = i['toUrl']
                venderId =  re.findall(r'venderId=(\d+)', toUrl)[0]
                channel =  re.findall(r'channel=(\d+)', toUrl)[0]
                venderIdList.append(venderId)
                channelList.append(channel)
    return venderIdList, channelList, score1, score2


def saveTask(header, pin, actorUuid, user):
    global countbean
    url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/saveTask'
    body = f'activityId={activityId}&pin={quote(pin)}&actorUuid={actorUuid}&taskType=2&taskValue=100015195341'
    printf("#去完成加购任务~")
    resp = requests.post(url=url, headers=header, data=body).json()
    # printf(resp)
    if resp['result']:
        bean = resp['data']['addBeanNum']
        printf(f"\t☺️加购获得: {bean} 豆 ")
        try:
            countbean[user] += resp['data']['addBeanNum']
        except:
            countbean[user] = resp['data']['addBeanNum']
    else:
        printf(f"\t😆{resp['errorMessage']}")
def drawContent(header, pin):
    url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/openCardcommon/drawContent'
    body = f'activityId={activityId}&pin={quote(pin)}'
    resp = requests.post(url=url, headers=header, data=body)

def startDraw(header, actorUuid, pin, user, num):
    global countbean
    try:
        drawContent(header, pin)
        sleep(1)
        url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/startDraw'
        body = f'activityId={activityId}&actorUuid={actorUuid}&pin={quote(pin)}&type={num+1}'
        resp = requests.post(url=url, headers=header, data=body)
        resp = resp.json()
        if resp['result']:
            if resp['data']['drawOk']:
                printf(f"\t☺️抽奖获得: {resp['data']['name']} ️")
                try:
                    countbean[user] += 30
                except:
                    countbean[user] = 30
            else:
                printf(f"\t😭抽奖获得: {resp['data']['name']} ")
        else:
            printf(f"\t😆{resp['errorMessage']}")
    except:
        pass

#
def followShop(header, actorUuid, pin, shareUuid, user):
    global countbean
    url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/dz/openCard/followShop'
    body = f'activityId={activityId}&pin={quote(pin)}&actorUuid={actorUuid}&taskType=23&taskValue=1000004123&shareUuid={shareUuid}'
    printf("#去完成关注任务~")
    resp = requests.post(url=url, headers=header, data=body).json()
    # printf(resp)
    if resp['result']:
        if resp['data']['sendStatus']:
            printf(f"\t☺️关注获得: {resp['data']['addBeanNum']} 豆️")
            try:
                countbean[user] += resp['data']['addBeanNum']
            except:
                countbean[user] = resp['data']['addBeanNum']
        else:
            printf(f"\t😭关注获得: {resp['data']['addBeanNum']} 豆 ")
    else:
        printf(f"\t😆{resp['errorMessage']}")

def insertCrmPageVisit(header, pin, num):
    url = 'https://lzdz1-isv.isvjcloud.com/crm/pageVisit/insertCrmPageVisit'
    body = f'venderId=1000004123&elementId=%E5%8E%BB%E5%BC%80%E{num}%8D%A15&pageId=dzkmladn20211123A&pin={quote(pin)}'
    resp = requests.post(url=url, headers=header, data=body)
    if resp.status_code == 200:
        printf(f'\t└模拟点击去开卡{num+1} ---> success')
    else:
        printf(f'\t└模拟点击去开卡{num+1} ---> error')

def getShopOpenCardInfo(ck, venderId, channe, headers):
    url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body=%7B%22venderId%22%3A%22{venderId}%22%2C%22payUpShop%22%3Atrue%2C%22channel%22%3A{channe}%7D&client=H5&clientVersion=9.2.0&uuid=88888'
    sleep(0.5)
    resp = requests.get(url=url, headers=headers).json()
    venderCardName = resp['result']['shopMemberCardInfo']['venderCardName']  # 店铺名称
    printf(f'\t去开卡：{venderCardName}')
    if resp['result']['interestsRuleList']:
        activityId = resp['result']['interestsRuleList'][0]['interestsInfo']['activityId']
        return activityId
    else:
        return None

def bindWithVender(ck, venderIdList, channelList):
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
    for v, c in zip(venderIdList, channelList):
        act = getShopOpenCardInfo(ck, v, c, headers)
        if act:
            bindWithVender_url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{v}%22%2C%22shopId%22%3A%22{v}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%7D%2C%22writeChildFlag%22%3A0%2C%22activityId%22%3A{act}%2C%22channel%22%3A{c}%7D&client=H5&clientVersion=9.2.0&uuid=88888&'
        else:
            bindWithVender_url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{v}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%7D%2C%22writeChildFlag%22%3A0%2C%22channel%22%3A{c}%7D&client=H5&clientVersion=9.2.0&uuid=88888'
        resp = requests.get(url=bindWithVender_url, headers=headers).json()
        if resp['success']:
            printf(f"\t\t└{resp['message']}")
        else:
            pass


def getCode():
    try:
        url = 'https://gitee.com/curtinlv/Public/raw/master/code.txt'
        response = requests.get(url)
        code = response.text
        if response.status_code == 200 and len(code) > 30:
            return code
        else:
            return 'wqdHuFdMJj0bcG7ysk0r8mwklxRrP5C78lmKjh9Mn4avAmNuF4i+OHS9NlRdtagP'
    except:
        return 'wqdHuFdMJj0bcG7ysk0r8mwklxRrP5C78lmKjh9Mn4avAmNuF4i+OHS9NlRdtagP'

def gettext(url):
    try:
        resp = requests.get(url, timeout=60).text
        if '该内容无法显示' in resp:
            return gettext(url)
        return resp
    except Exception as e:
        printf(e)

def isUpdate():
    global hdtitle, isEnable, readme, code, footer
    url = 'https://gitee.com/curtinlv/Public/raw/master/kk/shechong.json'
    try:
        result = gettext(url)
        result = json.loads(result)
        hdtitle = result['title']
        isEnable = result['isEnable']
        readme = result['readme']
        code = result['code']
        footer = result['footer']
        if isEnable == 0:
            code = code.split('#')
            s = random.randint(0, len(code) - 1)
            return True, hdtitle, readme, code[s], footer
        else:
            return False, hdtitle, readme, code, footer
    except:
        return False, '奢宠会员-瓜分万元大奖 11.23-11.30', '', 'bc5f8aab60ad47ab8249c5a58c3e00d5&wqdHuFdMJj0bcG7ysk0r8mwklxRrP5C78lmKjh9Mn4avAmNuF4i+OHS9NlRdtagP', '\n开源免费使用 https://github.com/curtinlv/JD-Script\nTG频道 https://t.me/TopStyle2021'

def getDrawRecordHasCoupon(headers, pin, actorUuid, user):
    # try:
    url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/openCardcommon/getDrawRecordHasCoupon'
    body = f'activityId={activityId}&pin={quote(pin)}&actorUuid={actorUuid}'
    resp = requests.post(url=url, headers=headers, timeout=30, data=body).json()
    allcount = {}
    if resp['result']:
        data = resp['data']
        a = 0
        for i in data:
            if a == 0:
                a = 1
                allcount['id'] = user
            # printf(i)
            # printf(json.dumps(i, indent=4, ensure_ascii=False))
            if '京豆' in i['infoName']:
                beanNum = re.findall(r'(\d+)', i['infoName'])[0]
                try:
                    allcount[i['value'] + '京豆'] += int(beanNum)
                except:
                    allcount[i['value'] + '京豆'] = int(beanNum)
            else:
                try:
                    allcount['礼品'] += '###' + i['infoName']
                except:
                    allcount['礼品'] = i['infoName']
        allList.append(allcount)
    # except:
    #     pass


def start():
    global shareuserid4minipg, Masternickname, shareUuid
    isok, hdtitle, readme, code, footer = isUpdate()
    if not isok and readme:
        printf(readme)
        exit(0)
    printf(f"开始：【{hdtitle}】")
    shareUuid = code.split("&")[0]
    shareuserid4minipg = code.split("&")[1]
    cookieList, nameList = getCk.iscookie()
    a = 1
    # try:
    for ck, user in zip(cookieList, nameList):
        printf(f"##☺️用户{a}【{user}】")
        try:
            cookie = buildheaders(ck, shareUuid, shareuserid4minipg)
            sleep(0.2)
            token = isvObfuscator(ck)
        except:
            printf(f"️##😭用户{a}【{user}】获取token异常, ip有可能给限制了~")
            a += 1
            continue
        sleep(0.1)
        try:
            header, nickname, pin, AUTH_C_USER = getMyPing(shareUuid, shareuserid4minipg, cookie, token)
        except:
            printf(f"️##😭用户{a}【{user}】暂无法参加活动~")
            a += 1
            continue
        try:
            sleep(0.3)
            yunMidImageUrl, pin, nickname = getUserInfo(header, pin)
            sleep(0.3)
            header = accessLog(header, pin, shareUuid, shareuserid4minipg, AUTH_C_USER)
            sleep(0.3)
            actorUuid, shareTitle = activityContent(header, pin, shareUuid, yunMidImageUrl, nickname)
            # 关注
            sleep(0.3)
            followShop(header, actorUuid, pin, shareUuid, user)
            # 加购
            sleep(0.3)
            saveTask(header, pin, actorUuid, user)
            printf("#去完成开卡任务~")
            # 开卡
            venderIdList, channelList, score1, score2 = checkOpenCard(header, actorUuid, shareUuid, pin)
            if len(venderIdList) > 0:
                for i in range(10):
                    sleep(1)
                    insertCrmPageVisit(header, pin, i)
                bindWithVender(ck, venderIdList, channelList)
                printf("#去抽奖~")
                for i in range(2):
                    sleep(5)
                    startDraw(header, actorUuid, pin, user, i)
            else:
                printf("\t😆任务已完成!")
            for i in range(2):
                startDraw(header, actorUuid, pin, user, i)
            if a == 1:
                printf(f"用户{a}[{nickname}]>助力>>[Author]{shareUuid}")
                shareuserid4minipg = pin
                shareUuid = actorUuid
                Masternickname = nickname
                a += 1
                continue
            printf(f"用户{a}[{nickname}]>>助力>>>[{Masternickname}]{shareUuid}")
            a += 1
        except:
            continue
    # 抽奖
    a = 1
    shareUuid = 'bc5f8aab60ad47ab8249c5a58c3e00d5'
    shareuserid4minipg = 'wqdHuFdMJj0bcG7ysk0r8mwklxRrP5C78lmKjh9Mn4avAmNuF4i+OHS9NlRdtagP'
    for ck, user in zip(cookieList, nameList):
        printf(f"##☺️用户{a}【{user}】")
        try:
            cookie = buildheaders(ck, shareUuid, shareuserid4minipg)
            sleep(0.2)
            token = isvObfuscator(ck)
        except:
            printf(f"️##😭用户{a}【{user}】获取token异常, ip有可能给限制了~")
            a += 1
            continue
        sleep(0.1)
        try:
            header, nickname, pin, AUTH_C_USER = getMyPing(shareUuid, shareuserid4minipg, cookie, token)
        except:
            printf(f"️##😭用户{a}【{user}】暂无法参加活动~")
            a += 1
            continue
        sleep(0.3)
        try:
            yunMidImageUrl, pin, nickname = getUserInfo(header, pin)
            header = accessLog(header, pin, shareUuid, shareuserid4minipg, AUTH_C_USER)
            actorUuid, shareTitle = activityContent(header, pin, shareUuid, yunMidImageUrl, nickname)
            getDrawRecordHasCoupon(header, pin, actorUuid, user)
            venderIdList, channelList, score1, score2 = checkOpenCard(header, actorUuid, shareUuid, pin)
            bindWithVender(ck, venderIdList, channelList)
            for i in range(2):
                startDraw(header, actorUuid, pin, user, i)
            if a == 1:
                shareUuid = actorUuid
                shareuserid4minipg = pin
            a += 1
        except:
            continue
    msg("*" * 40)
    msg("### 【本次】")
    allbean = 0
    for k in countbean:
        msg(f"用户[{k}], 获得京豆:{countbean[k]}")
        allbean += countbean[k]
    msg("*" * 40)
    msg("### 【累计】")
    allUserBean = 0
    for c in allList:
        usetBean = 0
        try:
            msg(f"用户{nameList.index(c['id']) + 1} [{c['id']}]累计获得京豆:")
            for i in c:
                if i == 'id':
                    continue
                msg(f"\t└{i}: {c[i]}")
                if '京豆' in i:
                    usetBean += c[i]
                    allUserBean += c[i]
            msg(f"\t└累计获得京豆: {usetBean}")
        except:
            continue
        msg('-' * 20)
    msg(f"本次总获得: {allbean} 京豆")
    msg(f"累计总获得: {allUserBean} 京豆")
    msg("*" * 40)
    msg(footer)
    if isNotice == "true":
        send(hdtitle, msg_info)

if __name__ == '__main__':
    start()