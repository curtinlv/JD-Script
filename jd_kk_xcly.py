#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / 测试
Author: Curtin
功能：自动完成所有任务，如没完成，多跑几次，账号一助力Curtinlv，其余助力账号一
Date: 2022/1/15 05:30
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 20 10,21 * 1-2 *
new Env('新春礼遇 数倍加码1.12-2.10')
活动入口：
https://lzdz1-isv.isvjcloud.com/dingzhi/trainingcamp/interaction/activity/8655764?activityId=dz2201100000406501&shareUuid=4ef5a0ee24ee4909844bbc176bd10951&adsource=null&shareuserid4minipg=wqdHuFdMJj0bcG7ysk0r8mwklxRrP5C78lmKjh9Mn4avAmNuF4i+OHS9NlRdtagP&shopid=1000004123
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

g_name = '新春礼遇 数倍加码1.12-2.10'
get_url = 'https://gitee.com/curtinlv/Public/raw/master/kk/xcly.json'

# 是否发送通知, 关闭通知：export kk_vip_isNotice="false"
isNotice = "true"
# 设置休眠最大时长 ，如60秒，export kk_vip_sleep="60"
kk_vip_sleep = 30

allUserBean = {}

if "isNotice" in os.environ:
    if len(os.environ["kk_vip_isNotice"]) > 1:
        isNotice = os.environ["kk_vip_isNotice"]

if "kk_vip_sleep" in os.environ:
    if len(os.environ["kk_vip_sleep"]) > 1:
        kk_vip_sleep = float(os.environ["kk_vip_sleep"])


# 如果您有UA可填
UserAgent = ''
activityId='dz2201100000406501'
activityshopid='1000004123'
jdActivityId='10713953'
random_num = '8655764'

master_shareUuid = '4ef5a0ee24ee4909844bbc176bd10951'
master_shareuserid4minipg = 'wqdHuFdMJj0bcG7ysk0r8mwklxRrP5C78lmKjh9Mn4avAmNuF4i+OHS9NlRdtagP'

# url
main_host='https://lzdz1-isv.isvjcloud.com'

#1 getpin
getMyPing_url = 'https://lzdz1-isv.isvjcloud.com/customer/getMyPing'
#2 getUserInfo
getUserInfo_url = 'https://lzdz1-isv.isvjcloud.com/wxActionCommon/getUserInfo'
#3
accessLogWithAD_url = 'https://lzdz1-isv.isvjcloud.com/common/accessLogWithAD'
pageUrl = 'https://lzdz1-isv.isvjcloud.com/dingzhi/trainingcamp/interaction/activity/'
#4 活动活动详情
activityContent_url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/trainingcamp/interaction/activityContent'
#5
drawContent_url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/drawContent'
#6
initOpenCard_url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/trainingcamp/interaction/initOpenCard' # 检测开卡状态
#7
getSystemConfigForNew = 'https://lzdz1-isv.isvjcloud.com/wxCommonInfo/getSystemConfigForNew'
# 'https://lzdz1-isv.isvjcloud.com/dingzhi/trainingcamp/interaction/activity/8655764?activityId=dz2201100000406501&shareUuid=f4d822efc99942bdbfc6807a1fb03a6c'
#8 获取品牌id
getCardMaterial_url = 'https://crmsam.jd.com/union/getCardMaterial?activityId=&token='

#9 我的奖品
getDrawRecordHasCoupon_url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/taskact/common/getDrawRecordHasCoupon'

#11 访问记录
insertCrmPageVisit_url = 'https://lzdz1-isv.isvjcloud.com/crm/pageVisit/insertCrmPageVisit'
#12 抽奖
draw_url = 'https://lzdz1-isv.isvjcloud.com/dingzhi/opencard/draw'

# token
isvObfuscator_body = f'body=%7B%22url%22%3A%22https%3A%5C/%5C/lzdz1-isv.isvjcloud.com%22%2C%22id%22%3A%22%22%7D&build=167870&client=apple&clientVersion=10.2.4&d_brand=apple&d_model=iPhone10%2C3&ef=1&&ep=%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22screen%22%3A%22CJOyDIeyDNC2%22%2C%22wifiBssid%22%3A%22{random_num}%3D%22%2C%22osVersion%22%3A%22CJGkCm%3D%3D%22%2C%22area%22%3A%22{random_num}%22%2C%22openudid%22%3A%22ENK5DNK5Y2TuDWTsEQOmZwO4ZwZwDNOzDzrtCWPwZJunYtqmDzVrZK%3D%3D%22%2C%22uuid%22%3A%22%22%7D%2C%22ts%22%3A1642199846%2C%22hdid%22%3A%22%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.360buy.jdmobile%22%2C%22ridx%22%3A-1%7D&ext=%7B%22prstate%22%3A%220%22%7D&isBackground=N&joycious=87&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&partner=TF&rfs=0000&scope=01&sign=bb5a801e8990acd4da57a06525ff711e&st=1642205022716&sv=120&'
# 获取请求头
buildheaders_url = f'https://lzdz1-isv.isvjcloud.com/dingzhi/trainingcamp/interaction/activity/{random_num}?activityId={activityId}&shareUuid={master_shareUuid}&adsource=null&shareuserid4minipg={master_shareuserid4minipg}&shopid={activityshopid}'


def printf(*args):
    text = ''
    for i in args:
        text += str(i)
    print(text)
    sys.stdout.flush()

def wait_time(a, b, msg=None):
    s1 = random.randint(a,b)
    s2 = random.randint(3,9)
    time_s = float(f'{s1}.{s2}')
    if msg:
        printf(f"{msg}\t等待时间：{time_s}s")
    time.sleep(time_s)


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
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'JD4iPhone/167870%20(iPhone;%20iOS;%20Scale/3.00)',
        'Cookie': ck,
        'Host': 'api.m.jd.com',
        'Referer': '',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept': '*/*'
    }
    url = 'https://api.m.jd.com/client.action?functionId=isvObfuscator'

    resp = requests.post(url=url, headers=headers, timeout=30, data=isvObfuscator_body).json()
    if resp['code'] == '0':
        return resp['token']
    else:
        return ''


def buildheaders(ck, shareUuid, shareuserid4minipg):
    sid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
    url = f'https://lzdz1-isv.isvjcloud.com/dingzhi/trainingcamp/interaction/activity/{random_num}?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg={shareuserid4minipg}&shopid={activityshopid}'
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

def getMyPing(cookie, token):
    sid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
    url = getMyPing_url
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': main_host,
        'User-Agent': userAgent(),
        'Cookie': cookie,
        'Host': 'lzdz1-isv.isvjcloud.com',
        'Referer': buildheaders_url,
        'Accept-Language': 'zh-cn',
        'Accept': 'application/json'
    }
    body = f'userId={activityshopid}&token={token}&fromType=APP'
    resp = requests.post(url=url, headers=headers, timeout=30, data=body)
    try:
        nickname = resp.json()['data']['nickname']
        secretPin = resp.json()['data']['secretPin']
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://lzdz1-isv.isvjcloud.com',
            'User-Agent': userAgent(),
            'Cookie': cookie,
            'Host': 'lzdz1-isv.isvjcloud.com',
            'Referer': buildheaders_url,
            'Accept-Language': 'zh-cn',
            'Accept': 'application/json'
        }
        return headers, nickname, secretPin
    except Exception as e:
        # printf("建议请稍等再试~", e)
        return False, False, False

def accessLog(headers,pin, shareUuid, shareuserid4minipg):
    try:
        sid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
        # accbody = f'venderId={activityshopid}&code=99&pin={quote(pin)}&activityId={activityId}&pageUrl={pageUrl}{random_num}?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg={quote(shareuserid4minipg)}&shopid={activityshopid}&sid=&un_area=&subType=app&adSource=null'
        accbody = f'venderId={activityshopid}&code=99&pin={quote(pin)}&activityId={activityId}&pageUrl=https%3A%2F%2Flzdz1-isv.isvjcloud.com%2Fdingzhi%2Fcustomized%2Fcommon%2Factivity%3FactivityId={activityId}&sid={sid}&un_area=&subType=app&adSource='
        url = accessLogWithAD_url
        resp = requests.post(url=url, headers=headers, timeout=30, data=accbody)
        if resp.status_code == 200:
            LZ_TOKEN = re.findall(r'(LZ_TOKEN_KEY=.*?;).*?(LZ_TOKEN_VALUE=.*?;)', resp.headers['Set-Cookie'])
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://lzdz1-isv.isvjcloud.com',
                'User-Agent': userAgent(),
                'Cookie': LZ_TOKEN[0][0] + LZ_TOKEN[0][1],
                'Host': 'lzdz1-isv.isvjcloud.com',
                'Referer': buildheaders_url,
                'Accept-Language': 'zh-cn',
                'Accept': 'application/json'
            }
            return headers
        else:
            return headers
    except Exception as e:
        printf(e)
        return headers



# 访问记录
def insertCrmPageVisit(header, pin,shop_value):
    url = insertCrmPageVisit_url
    body = f'venderId={activityshopid}&elementId={shop_value}&pageId={activityId}&pin={quote(pin)}'
    resp = requests.post(url=url, headers=header, timeout=30, data=body)
    if resp.status_code == 200:
        resp = resp.json()
        if resp['result']:
            printf(f"insertCrmPageVisit ok")
    else:
        pass



def activityContent(header, pin, shareUuid, pinImg, nick, shareuserid4minipg, agin=1):
    url = activityContent_url
    try:
        pinImg = quote_plus(pinImg)
    except:
        pinImg = ''
    body = f'activityId={activityId}&pin={quote(pin)}&pinImg={pinImg}&nick={quote(nick)}&cjyxPin=&cjhyPin=&shareUuid={shareUuid}'
    header['Cookie'] += f'AUTH_C_USER={quote(pin)};'
    header['Referer'] = f'https://lzdz1-isv.isvjcloud.com/dingzhi/trainingcamp/interaction/activity/{random_num}?activityId={activityId}&shareUuid={shareUuid}&adsource=null&shareuserid4minipg={quote(shareuserid4minipg)}&shopid={activityshopid}&'
    try:
        resp = requests.post(url=url, headers=header, data=body)
        if resp.status_code == 200:
            resp = resp.json()
            actorUuid = resp['data']['actorUuid']
            shareTitle = resp['data']['shareTitle']
            return actorUuid, shareTitle
        else:
            printf(f"activityContent req [{resp.text}]")
            return 0, ''
    except Exception as e:
        if agin > 6:
            return 0, ''
        else:
            wait_time(30, 60, f"获取助力码失败，尝试重新获取{agin}")
            agin += 1
            return activityContent(header, pin, shareUuid, pinImg, nick, shareuserid4minipg, agin=agin)
        # printf(f"activityContent {e}")



def getUserInfo(header, pin):
    url = getUserInfo_url
    body = 'pin=' + quote(pin)
    resp = requests.post(url=url, headers=header, data=body).json()
    yunMidImageUrl = resp['data']['yunMidImageUrl']
    nickname = resp['data']['nickname']
    secretPin = resp['data']['secretPin']
    return yunMidImageUrl, secretPin, nickname

def drawContent(header, pin):
    url = drawContent_url
    body = f'activityId={activityId}&pin={quote(pin)}'
    resp = requests.post(url=url, headers=header, data=body).json()

def initOpenCard(header, pin, actorUuid, shareUuid):
    url = initOpenCard_url
    body = f'activityId={activityId}&pin={quote(pin)}&actorUuid={actorUuid}&shareUuid={shareUuid}'
    all_token = []
    # try:
    resp = requests.post(url=url, headers=header, data=body)
    if resp.status_code == 200:
        resp = resp.json()
        # printf(json.dumps(resp, indent=4, ensure_ascii=False))
        if resp['result']:
            data = resp['data']
            AllOpenCard_status = []
            for d in data:
                if 'AllOpenCard' in d:
                    if not data[d]:
                        # 截取未完成开卡的
                        tmp = "{}".format(d)
                        id = tmp.split('AllOpenCard')[0]
                        AllOpenCard_status.append(id)
            if data['beans'] > 0:
                printf(f"\t完成开卡获得京豆{data['beans']}")
            for i in AllOpenCard_status:
                for e in data:
                    if f'{i}OpenCardUrl' == e:
                        t = re.findall(r'https://crmsam\.jd\.com/union/index\.html\?token=(.*?)&url=', data[e])
                        if len(t)>0:
                            all_token.append(t[0])
            return all_token
        else:
            printf(resp['errorMessage'])
            return all_token
    else:
        printf(resp.status_code, resp.text)
        return all_token
    # except Exception as e:
    #     printf(f"initOpenCard[{e}]")
    #     return all_token



# 我的奖品
def getDrawRecordHasCoupon(header, pin, actorUuid,user):
    global allUserBean
    url = getDrawRecordHasCoupon_url
    body = f'activityId={activityId}&pin={quote(pin)}&actorUuid={actorUuid}'
    try:
        resp = requests.post(url=url, headers=header, data=body)
        if resp.status_code == 200:
            resp = resp.json()
            if resp['result']:
                # print(resp)
                recordList = resp['data']
                if recordList:
                    for i in recordList:
                        if '京豆' in i['infoName']:
                            beanNum = re.findall(r'(\d+)', i['infoName'])[0]
                            try:
                                allUserBean[f"{user}"] += int(beanNum)
                            except:
                                allUserBean[f"{user}"] = int(beanNum)
                        else:
                            try:
                                allUserBean[f'{user}_yes'] += '+' + i['infoName']
                            except:
                                allUserBean[f'{user}_yes'] = i['infoName']
            else:
                # printf(f"\t😭 没中奖~ [{resp['data']['name']} ]")
                print(resp.text)
    except Exception as e:
        printf(f"getDrawRecordHasCoupon [{e}]")




def getShopOpenCardInfo(ck, venderId, channe, headers):
    url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body=%7B%22venderId%22%3A%22{venderId}%22%2C%22payUpShop%22%3Atrue%2C%22channel%22%3A{channe}%7D&client=H5&clientVersion=9.2.0&uuid=88888'
    sleep(0.5)
    # resp = requests.get(url=url, headers=headers).json()
    aginNum = 0
    while True:
        resp = requests.get(url=url, headers=headers)
        if resp.status_code == 200:
            break
        aginNum += 1
        if aginNum > 20:
            printf("开卡异常，请稍后再试~")
            break
        wait_time(3, 10, "店铺信息获取失败")
    resp = resp.json()
    venderCardName = resp['result']['shopMemberCardInfo']['venderCardName']  # 店铺名称
    printf(f'\t去开卡：{venderCardName}')
    if resp['result']['interestsRuleList']:
        activityId = resp['result']['interestsRuleList'][0]['interestsInfo']['activityId']
        return activityId
    else:
        return None
def getCardMaterial(ck, token):
    try:
        brandIds = []
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://shopmember.m.jd.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type':	'application/json;charset=UTF-8',
            'Host': 'crmsam.jd.com',
            'User-Agent': userAgent(),
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'referer': f'https://crmsam.jd.com/union/index.html?token={token}&url=https%3A%2F%2Flzdz1-isv.isvjcloud.com%2Fdingzhi%2Ftrainingcamp%2Finteraction%2Factivity%2F{random_num}%3FactivityId%3D{activityId}%26shareUuid%3D{master_shareUuid}'
        }
        url = getCardMaterial_url + token
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            resp = resp.json()
            if '查询成功' in resp['message']:
                data = resp['data']
                for i in data:
                    brandIds.append(i['brandId'])
            return brandIds

        else:
            printf(f"{resp.text}")
            return brandIds
    except Exception as e:
        print(f"getCardMaterial [{e}]")
        return brandIds

def submitBindCards(ck, brandsIds, pin, header, token):
    url = 'https://crmsam.jd.com/union/submitBindCards'
    headers = {
        'Cookie': ck,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://shopmember.m.jd.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'crmsam.jd.com',
        'User-Agent': userAgent(),
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'referer': f'https://crmsam.jd.com/union/index.html?token={token}&url=https%3A%2F%2Flzdz1-isv.isvjcloud.com%2Fdingzhi%2Ftrainingcamp%2Finteraction%2Factivity%2F{random_num}%3FactivityId%3D{activityId}%26shareUuid%3D{master_shareUuid}'
    }
    body = {
        "phone": None,
        "smsCode": None,
        "brandsIds": brandsIds,
        "bindChannel": False,
        "activityId": "",
        "token": token
    }
    resp = requests.post(url, headers=headers, data=json.dumps(body))
    if resp.status_code == 200:
        if resp.json()['message'] == 'SUCCESS':
            data = resp.json()['data']
            for i in data:
                printf(i)
        else:
            printf(f"开卡失败~")
    else:
        printf(resp.status_code)
        printf(resp.text)




def bindWithVender(ck, venderIdList, channelList,pin,header):
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
        insertCrmPageVisit(header, pin, "%E5%8E%BB%E5%BC%80%E5%8D%A1")
        wait_time(0,1)
        act = getShopOpenCardInfo(ck, v, c, headers)
        if act:
            bindWithVender_url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{v}%22%2C%22shopId%22%3A%22{v}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%7D%2C%22writeChildFlag%22%3A0%2C%22activityId%22%3A{act}%2C%22channel%22%3A{c}%7D&client=H5&clientVersion=9.2.0&uuid=88888&'
        else:
            bindWithVender_url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{v}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%7D%2C%22writeChildFlag%22%3A0%2C%22channel%22%3A{c}%7D&client=H5&clientVersion=9.2.0&uuid=88888'
        resp = requests.get(url=bindWithVender_url, headers=headers).json()
        if resp['success']:
            printf(f"\t\t└{resp['message']}, [{resp}]")
        else:
            pass


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

    try:
        result = gettext(get_url)
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
        return False, f'{g_name}', '', f'{master_shareUuid}&{master_shareuserid4minipg}', 'TG频道 https://t.me/TopStyle2021\n活动入口：20:/#239s57fgLQaxO@，嚯！囤大牌年货，赢惊喜大奖'




def start():
    global shareuserid4minipg, Masternickname, one_shareUuid, one_shareuserid4minipg, one_name
    if datetime.datetime.now() > datetime.datetime.strptime('2022-2-11', "%Y-%m-%d"):
        printf("活动结束\n请删掉脚本")
        exit(3)
    isok, hdtitle, readme, code, footer = isUpdate()
    if not isok and readme:
        printf(readme)
        exit(0)
    printf(f"开始：【{hdtitle}】")
    one_name = '仅账号一助力 Curtin，其他全部助力账号一'
    one_shareUuid = code.split("&")[0]
    one_shareuserid4minipg = code.split("&")[1]
    cookieList, nameList = getCk.iscookie()
    a = 1
    for ck, user in zip(cookieList, nameList):
        try:
            printf(f"##☺️账号{a}[{user}]，您好!")
            printf(f"\t└助力：[{one_name}] 助力码：{one_shareUuid}")
            try:
                cookie = buildheaders(ck, one_shareUuid, one_shareuserid4minipg)
                wait_time(1, 1)
                token = isvObfuscator(ck)
            except:
                printf(f"️##😭账号{a}【{user}】获取token异常, ip有可能给限制了~")
                a += 1
                continue
            wait_time(1, 2)
            try:
                header, nickname, pin = getMyPing(cookie, token)
            except:
                printf(f"️##😭账号{a}【{user}】暂无法参加活动~")
                a += 1
                continue
            wait_time(1, 3)
            # try:
            yunMidImageUrl, pin, nickname = getUserInfo(header, pin)
            wait_time(1, 3)
            header = accessLog(header, pin, one_shareUuid, one_shareuserid4minipg)
            wait_time(1, 2)
            actorUuid, shareTitle = activityContent(header, pin, one_shareUuid, yunMidImageUrl, nickname,one_shareuserid4minipg)
            # 开卡
            printf("#去完成开卡任务~")
            wait_time(1, 2)
            alltoken = initOpenCard(header, pin, actorUuid, one_shareUuid)
            wait_time(1, 3)
            if len(alltoken) > 0:
                for i in alltoken:
                    brandsIds = getCardMaterial(ck, i)
                    if len(brandsIds) > 0:
                        wait_time(3, 6, "一键开卡")
                        submitBindCards(ck, brandsIds, pin, header, i)
            else:
                wait_time(2, 3, "\t已完成全部开卡")
            if a == 1:
                if actorUuid == 0:
                    printf("账号一获取助力码失败~，请重新尝试运行。")
                    exit(1)
                one_shareUuid = actorUuid
                one_shareuserid4minipg = pin
                one_name = user
            if not a == len(cookieList):
                a += 1
                wait_time(kk_vip_sleep, kk_vip_sleep, "###休息一会")
        except Exception as e:
            printf(f"ERROR MAIN {e}")
            if a == 1:
                exit(0)
            a += 1
            continue
#################################
    a = 1
    printf("\n【收获统计】")
    userList = []
    one_shareUuid = master_shareUuid
    one_shareuserid4minipg = master_shareuserid4minipg
    for ck, user in zip(cookieList, nameList):
        try:
            try:
                cookie = buildheaders(ck, one_shareUuid, one_shareuserid4minipg)
                wait_time(0, 1)
                token = isvObfuscator(ck)
            except:
                printf(f"️##😭账号{a}【{user}】获取token异常, ip有可能给限制了~")
                a += 1
                continue
            wait_time(0, 1)
            try:
                header, nickname, pin = getMyPing(cookie, token)
            except:
                printf(f"️##😭账号{a}【{user}】暂无法参加活动~")
                a += 1
                continue
            wait_time(1, 2)
            actorUuid, shareTitle = activityContent(header, pin, one_shareUuid, '', nickname, one_shareuserid4minipg)
            # 奖品
            getDrawRecordHasCoupon(header, pin, actorUuid, user)
            userList.append(user)
            if a == 1:
                one_shareUuid = actorUuid
                one_shareuserid4minipg = pin
                one_name = user
            a += 1
        except Exception as e:
            printf(f"抽奖统计 {e}")
            a += 1
            continue

    msg("*" * 40)
    allBean = 0
    allJiangpin = ""
    n = 0
    a = 1
    for u in userList:
        try:
            msg(f"账号{a}[{u}]")
            for m in allUserBean:
                if m == u:
                    msg(f"\t\t└获得京豆: {allUserBean[u]}")
                    allBean += allUserBean[u]
                if m == f'{u}_yes':
                    msg(f"\t\t└获得奖品: {allUserBean[f'{u}_yes']}")
                    allJiangpin += "+" + allUserBean[f'{u}_yes']
            a += 1
            n += 1
        except:
            a += 1
            n += 1
            continue
    if allBean > 0:
        msg(f"总获得京豆: {allBean} ")
    if allJiangpin:
        msg(f"总获得奖品: {allJiangpin}")
    msg("*" * 40)
    msg(footer)
    if isNotice == "true":
        send(shareTitle, msg_info)

if __name__ == '__main__':
    start()