#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / 测试_test
Author: Curtin
功能：邀请5人得60豆（每天最多10次600豆），被邀请完成开卡30豆，一次性任务。ck1助力Author，其他助力ck1
Date: 2021/11/14 下午6:21
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 30 6,12,15,20 11-17 11 *
new Env('品牌联合开卡 11.11-11.17');
活动入口：16:/#A5eHpAAyC12xuX%，☂
'''
import requests
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

if datetime.datetime.now() > datetime.datetime.strptime('2021-11-18', "%Y-%m-%d"):
    print("品牌联合开卡 11.11-11.17---活动结束\n请删掉脚本：jd_kk_test.py")
    exit(3)

UserAgent = ''
activityId='96475ceebdf0418ab524c9bc68a789e8'
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

    body = 'body={"url":"https:\/\/cjhydz-isv.isvjcloud.com","id":""}&build=167863&client=apple&clientVersion=10.2.2&d_brand=apple&d_model=iPhone14,3&ef=1&eid=&ep={"ciphertype":5,"cipher":{"screen":"CJS4DMeyDzc4","wifiBssid":"","osVersion":"CJUkCG==","area":"","openudid":"DtVwZtvvZJcmZwPtDtc5DJSmCtZvDzLsCzK2DJG2DtU1EWG5Dzc2ZK==","uuid":""},"ts":1636884530,"hdid":"","version":"1.0.3","appname":"com.360buy.jdmobile","ridx":-1}&ext={"prstate":"0"}&isBackground=N&joycious=67&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&partner=apple&rfs=0000&scope=10&sign=0a635010067282017044162e187af9a7&st=1636884564653&sv=112&uemps=0-0'

    resp = requests.post(url=url, headers=headers, data=body).json()
    if resp['code'] == '0':
        return resp['token']
    else:
        return ''


def buildheaders(ck):
    url = 'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index/5986361?activityId=96475ceebdf0418ab524c9bc68a789e8&inviter=kNwcKz+y+wjfE/yhJf7Ph2cLh8yR0FTTtPtNBwC7New+Y72eTaNK0sHryLjn2YvU&inviterImg=http://storage.360buyimg.com/i.imageUpload/31333435303133353830315f7031363134333838323331343238_mid.jpg&inviterNickName=Curtinlv&shareuserid4minipg=kNwcKz%2By%2BwjfE%2FyhJf7Ph2cLh8yR0FTTtPtNBwC7New%2BY72eTaNK0sHryLjn2YvU&shopid=599119&lng=113.367448&lat=23.112787&sid=6ed3dcfe7c0bb6992246a5771fac1aaw&un_area=19_1601_3633_63243'
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': ck,
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'cjhydz-isv.isvjcloud.com',
        'User-Agent': userAgent(),
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
    resp = requests.get(url, headers)
    LZ_TOKEN = re.findall(r'(LZ_TOKEN_KEY=.*?;).*?(LZ_TOKEN_VALUE=.*?;)', resp.headers['Set-Cookie'])
    return LZ_TOKEN[0][0]+LZ_TOKEN[0][1]

def getMyPing(ck):
    sleep(1)
    cookie = buildheaders(ck)
    token = isvObfuscator(ck)
    url = 'https://cjhydz-isv.isvjcloud.com/customer/getMyPing'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhydz-isv.isvjcloud.com',
        'User-Agent': userAgent(),
        'Cookie': cookie,
        'Host': 'cjhydz-isv.isvjcloud.com',
        'Referer': 'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index/5986361?activityId=96475ceebdf0418ab524c9bc68a789e8&',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept': 'application/json'
    }
    body = f'userId=599119&token={token}&fromType=APP&riskType=1'
    resp = requests.post(url=url, headers=headers, data=body)
    try:
        pin = resp.json()['data']['pin']
        secretPin = resp.json()['data']['secretPin']
        userid = resp.json()['data']['id']
        yunMidImageUrl = resp.json()['data']['yunMidImageUrl']
    except Exception as e:
        print("建议请稍等再试~", e)
        sys.exit(1)
    LZ_TOKEN_KEY = re.findall(r'(LZ_TOKEN_KEY=.*?;)', resp.headers['Set-Cookie'])[0]
    LZ_TOKEN_VALUE = re.findall(r'(LZ_TOKEN_VALUE=.*?;)', resp.headers['Set-Cookie'])[0]
    AUTH_C_USER = re.findall(r'(AUTH_C_USER=.*?;)', resp.headers['Set-Cookie'])[0]
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cjhydz-isv.isvjcloud.com',
        'User-Agent': userAgent(),
        'Cookie': LZ_TOKEN_KEY+LZ_TOKEN_VALUE+AUTH_C_USER+'APP_ABBR=CJHY;__jd_ref_cls=Mnpm_ComponentApplied;',
        'Host': 'cjhydz-isv.isvjcloud.com',
        'Referer': 'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index/5986361?activityId=96475ceebdf0418ab524c9bc68a789e8&',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept': 'application/json'
    }
    return headers, pin, secretPin, userid, yunMidImageUrl

def accessLog(headers, body):
    url = 'https://cjhydz-isv.isvjcloud.com/common/accessLog'
    resp = requests.post(url=url, headers=headers, data=quote(body))
    if resp.status_code == 200:
        print('\t└accessLog ---> success')
    else:
        print('\t└accessLog ---> error')

def getOpenCardAllStatuesNew(ck):
    headers, pin, secretPin, userid, yunMidImageUrl = getMyPing(ck)
    url = 'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/getOpenCardAllStatuesNew'
    body = f'activityId={activityId}&pin={secretPin}&isInvited=1'
    resp = requests.post(url=url, headers=headers, data=body).json()
    if resp['result']:
        shoplist = resp['data']['list']
        venderIdList = []
        shopIdList = []
        channelList = []
        shopNameList = []
        for i in shoplist:
            if not i['statue']:
                openCardLink = i['openCardLink']
                shopid = re.findall(r'shopId=(\d+)', openCardLink)[0]
                venderId = re.findall(r'venderId=(\d+)', openCardLink)[0]
                channel = re.findall(r'channel=(\d+)', openCardLink)[0]
                shopIdList.append(shopid)
                venderIdList.append(venderId)
                channelList.append(channel)
                shopNameList.append(i['shopName'])
    return shopIdList, venderIdList, channelList, shopNameList


def getShopOpenCardInfo(headers, venderId, channe):
    url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body=%7B%22venderId%22%3A%22{venderId}%22%2C%22payUpShop%22%3Atrue%2C%22channel%22%3A{channe}%7D&client=H5&clientVersion=9.2.0&uuid=88888'
    resp = requests.get(url=url, headers=headers).json()
    if resp['result']['interestsRuleList']:
        activityId = resp['result']['interestsRuleList'][0]['interestsInfo']['activityId']
        return activityId
    else:
        return None

def bindWithVender(ck, inviterNickName, inviter):
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
    shopIdList, venderIdList, channelList, shopNameList= getOpenCardAllStatuesNew(ck)
    for shopId,venderId,channe,shopName in zip(shopIdList, venderIdList, channelList, shopNameList):
        shopcard_url = f'https://shopmember.m.jd.com/shopcard/?venderId={venderId}&shopId={shopId}&channel={channe}&returnUrl=https%3A%2F%2Fcjhydz-isv.isvjcloud.com%2FmicroDz%2Finvite%2Factivity%2Fwx%2Fview%2Findex%2F5986361%3FactivityId%3D{activityId}%26inviter%3D{inviter}%26inviterImg%3D%26inviterNickName%3D{inviterNickName}%26shareuserid4minipg%3D{inviter}%26shopid%3D599119%26lng%3D113.%26lat%3D23.%26sid%3D%26un_area%3D'
        requests.get(url=shopcard_url, headers=headers)
        sleep(1)
        shopactivityId = getShopOpenCardInfo(headers, venderId, channe)
        print("shopactivityId:", shopactivityId)
        sleep(1)
        bindWithVender_url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{venderId}%22%2C%22shopId%22%3A%22{shopId}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%7D%2C%22writeChildFlag%22%3A0%2C%22activityId%22%3A{shopactivityId}%2C%22channel%22%3A{channe}%7D&client=H5&clientVersion=9.2.0&uuid=88888&'
        resp = requests.get(url=bindWithVender_url, headers=headers).json()
        print(f"\t└去开卡【{shopName}】")
        if resp['success']:
            print(f"\t\t└{resp['message']}")
        else:
            pass
    print(f"\t└完成开卡获得30豆，京东明显查询【微定制-邀请瓜分京豆】。")


def getActivityInfo(ck):
    headers, pin, secretPin, userid, yunMidImageUrl = getMyPing(ck)
    url = 'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/getActivityInfo'
    body = f'activityId={activityId}'
    resp = requests.post(url, headers=headers, data=body).json()
    # print(resp)
def isInvited(ck):
    headers, pin, secretPin, userid, yunMidImageUrl = getMyPing(ck)
    url = 'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/isInvited'
    body = f'activityId={activityId}&pin={secretPin}'
    resp = requests.post(url=url, headers=headers, data=body).json()
    print(resp)
    # exit(3)
    # print(resp)

def inviteRecord(headers, inviter):
    url = 'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/inviteRecord'
    body = f'activityId={activityId}&inviter={inviter}&pageNo=1&pageSize=15&type=0'
    resp = requests.post(url=url, headers=headers, data=body).json()
    # print(resp)


def acceptInvite(headers, pin, secretPin, inviter, inviterNick, yunMidImageUrl):
    inviteRecord(headers, inviter)
    body = f'venderId=&code=99&pin={pin}&activityId={activityId}&pageUrl=https%3A%2F%2Fcjhydz-isv.isvjcloud.com%2FmicroDz%2Finvite%2Factivity%2Fwx%2Fview%2Findex%2F5986361%3FactivityId%3D{activityId}%26inviter%3D{inviter}%26inviterImg%3D%26inviterNickName%3D{inviterNick}%26shareuserid4minipg%3D{inviter}%26shopid%3D599119%26lng%3D%26lat%3D%26sid%3D%26un_area%3D&subType='
    accessLog(headers, body)
    url = 'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/acceptInvite'
    body1 = f'activityId={activityId}&inviter={inviter}&inviterImg=&inviterNick={quote(inviterNick)}&invitee={secretPin}&inviteeImg={yunMidImageUrl}&inviteeNick={quote(pin)}'
    headers['Referer'] = f'https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index/5986361?activityId={activityId}&inviter={inviter}&inviterImg=&inviterNickName={inviterNick}&shareuserid4minipg={inviter}&shopid=599119&lng=113.&lat=23.&sid=6ed3dcfe7c0bb6992246a5771fac1aaw&un_area=19_1601_3633_63243'
    resp = requests.post(url=url, headers=headers, data=body1).json()
    print(f"\t└{resp['errorMessage']}")


def miniProgramShareInfo(ck):
    headers, pin, secretPin, userid, yunMidImageUrl = getMyPing(ck)
    url = 'https://cjhydz-isv.isvjcloud.com/miniProgramShareInfo/getInfo?activityId=96475ceebdf0418ab524c9bc68a789e8'
    resp = requests.get(url=url, headers=headers).json()
    # print(resp)

def getSimpleActInfoVo(ck):
    headers, pin, secretPin, userid, yunMidImageUrl = getMyPing(ck)
    url = 'https://cjhydz-isv.isvjcloud.com/customer/getSimpleActInfoVo'
    body = f'activityId={activityId}'
    resp = requests.post(url=url, headers=headers, data=body).json()
    # print(resp)

def getSystemConfig(ck):
    headers, pin, secretPin, userid, yunMidImageUrl = getMyPing(ck)
    url = 'https://cjhydz-isv.isvjcloud.com/wxCommonInfo/getSystemConfig'
    body = f'activityId={activityId}'
    resp = requests.post(url=url, headers=headers, data=body).json()
    # print(resp)
def start():
    global MasterPin, Mastersecret
    cookieList, nameList = getCk.iscookie()
    a = 1
    try:
        for ck, user in zip(cookieList, nameList):
            headers, pin, secret, userid, yunMidImageUrl = getMyPing(ck)
            print(f"## 用户{a}【{user}】")
            getSystemConfig(ck)
            getSimpleActInfoVo(ck)
            getActivityInfo(ck)
            isInvited(ck)
            if a == 1:
                MasterPin = pin
                Mastersecret = secret
                print(f"用户{a}[{pin}]>>助力>>>[Curtinlv]")
                acceptInvite(headers, MasterPin, Mastersecret, '2vlPNpSNPs2zwEu+07zbf8+iQEinB57W5aMO3vKdRy0Jah8sXZOcx4hozgiV81Rt697ulbLIDOIodMQ2RvALQQ==', 'Curtinlv', yunMidImageUrl)
                bindWithVender(ck, MasterPin, Mastersecret)
                a += 1
                sleep(60)
                continue
            print(f"用户{a}[{pin}]>>助力>>>[{MasterPin}]")
            acceptInvite(headers, pin, secret, Mastersecret, MasterPin, yunMidImageUrl)
            body = f'venderId=&code=99&pin={secret}%253D%253D&activityId={activityId}&pageUrl=https%3A%2F%2Fcjhydz-isv.isvjcloud.com%2FmicroDz%2Finvite%2Factivity%2Fwx%2Fview%2Findex%2F5986361%3FactivityId%3D{activityId}%26inviter%3D{Mastersecret}%26inviterImg%3Dhttp%3A%2F%2Fstorage.360buyimg.com%2Fi.imageUpload%2F31333435303133353830315f7031363134333838323331343238_mid.jpg%26inviterNickName%3D{MasterPin}%26shareuserid4minipg%3D{Mastersecret}%26shopid%3D599119%26lng%3D113.%26lat%3D23.%26sid%3D%26un_area%3D&subType='
            accessLog(headers,body)
            bindWithVender(ck, MasterPin, Mastersecret)
            sleep(60)
            a += 1
    except Exception as e:
        pass
if __name__ == '__main__':
   try:
       start()
   except:
       print("网络异常，请稍等再试~\n")