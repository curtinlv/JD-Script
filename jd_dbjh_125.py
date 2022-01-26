#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / c_lhkk_125 
Author: Curtin
功能：
Date: 2022/1/25 下午8:55
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 20 6,12,15,20 * * *
new Env('大牌集合-瓜分千万豆1.24-2.14')
活动入口：21:/￥63GVM0oHoBMud￥，☂来京东，更超值
'''

import requests
import os
import json
import random
import re
import sys
from time import sleep
import datetime
import time
from urllib.parse import quote
try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本后执行一次，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)

g_name = '大牌集合-瓜分千万豆1.24-2.14'
get_url = 'https://gitee.com/curtinlv/Public/raw/master/kk/125.json'


# 是否发送通知, 关闭通知：export kk_vip_isNotice="false"
isNotice = "true"
# 设置休眠最大时长 ，如60秒，export kk_vip_sleep="60"
kk_vip_sleep = 10

# 如果您有UA可填
UserAgent = ''

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

u ='k6v981/pPDqeC8LcRX3+NVs/ye9oluZX4nOTK56TeMXbR7I2OlzZch4hTs22oCUS'

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
        if aginNum > 30:
            printf("开卡异常，请稍后再试~")
            break
        wait_time(3, 10)
    resp = resp.json()
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
    o = 1
    for v, c in zip(venderIdList, channelList):
        wait_time(0,1)
        act = getShopOpenCardInfo(ck, v, c, headers)
        if act:
            bindWithVender_url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{v}%22%2C%22shopId%22%3A%22{v}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%7D%2C%22writeChildFlag%22%3A0%2C%22activityId%22%3A{act}%2C%22channel%22%3A{c}%7D&client=H5&clientVersion=9.2.0&uuid=88888&'
        else:
            bindWithVender_url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{v}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%7D%2C%22writeChildFlag%22%3A0%2C%22channel%22%3A{c}%7D&client=H5&clientVersion=9.2.0&uuid=88888'
        resp = requests.get(url=bindWithVender_url, headers=headers).json()
        if resp['success']:
            printf(f"\t\t└{resp['message']}")
            if resp['busiCode'] == '0':
                    try:
                        result = resp['result']['giftInfo']['giftList']
                    except:
                        printf(f"\t\t└{resp}")
                        result = []
                    for i in result:
                        print("\t\t\t└{0}:{1} ".format(i['prizeTypeName'], i['discount']))
        else:
            pass
    printf(f"\t您完成开卡任务！")

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
    url = 'http://api.m.jd.com/client.action?functionId=isvObfuscator'
    isvObfuscator_body='body=%7B%22url%22%3A%22https%3A%5C/%5C/jinggengjcq-isv.isvjcloud.com%5C/fronth5%5C/?sid%3Defe8f329e2b6df53831d3b17b669957w%26un_area%3D19_1601_3633_63243%23%5C/pages%5C/unitedCardNew20220124%5C/unitedCardNew20220124?actId%3D29c257bced_220124%22%2C%22id%22%3A%22%22%7D&build=167874&client=apple&clientVersion=10.2.4&d_brand=apple&d_model=iPhone14%2C3&ef=1&ep=%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22screen%22%3A%22%22%2C%22wifiBssid%22%3A%22%3D%22%2C%22osVersion%22%3A%22%3D%3D%22%2C%22area%22%3A%22%22%2C%22openudid%22%3A%22DtVwZtvvZJcmZwPtDtc5DJSmCtZvDzLsCzK2DJG2DtU1EWG5Dzc2ZK%3D%3D%22%2C%22uuid%22%3A%22aQf1ZRdxb2r4ovZ1EJZhcxYlVNZSZz09%22%7D%2C%22ts%22%3A1643115604%2C%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.360buy.jdmobile%22%2C%22ridx%22%3A-1%7D&ext=%7B%22prstate%22%3A%220%22%7D&isBackground=N&joycious=87&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&partner=apple&rfs=0000&scope=01&sign=8ceb02e2fd529ca0f51d61211dc48b78&st=1643116266340&sv=101'
    resp = requests.post(url=url, headers=headers, timeout=30, data=isvObfuscator_body).json()

    if resp['code'] == '0':
        return resp['token']
    else:
        return ''

def relationBind(header, userId, buyerNick, actId, inviterNick, missionType="relationBind", agin=1):
    label = False
    try:
        url = f'https://jinggengjcq-isv.isvjcloud.com/dm/front/openCardNew/complete/mission?mix_nick={buyerNick}'

        body = {
            "jsonRpc": "2.0",
            "params": {
                "commonParameter": {
                    "appkey": "",
                    "m": "POST",
                    "timestamp": int(round(time.time() * 1000)),
                    "userId": userId
                },
                "admJson": {
                    "actId": actId,
                    "missionType": missionType,
                    "inviterNick": inviterNick,
                    "method": "/openCardNew/complete/mission",
                    "userId": userId,
                    "buyerNick": buyerNick
                }
            }
        }
        r = requests.post(url, headers=header, data=json.dumps(body), timeout=30)
        if r.status_code == 200:
            data = r.json()
            if data['success']:
                if data['data']['status'] == 200:
                    printf(f"\t{data['data']['data']['remark']}")
                    label = True
                if data['data']['status'] == 500:
                    if agin > 20:
                        printf(f"[{missionType} post error]: {e}")
                        return label
                    else:
                        wait_time(10, 30)
                        agin += 1
                        return relationBind(header, userId, buyerNick, actId, inviterNick, missionType="relationBind",
                                            agin=agin)
                else:
                    printf(f"\t{data['data']}")
                    label = True
            else:
                printf(f"\t{data['errorMessage']}")
        else:
            printf(f"[{missionType} post error]: {r.status_code} {r.text}")
        return label
    except Exception as e:
        if agin > 20:
            printf(f"[{missionType} post error]: {e}")
            return label
        else:
            wait_time(3, 10)
            agin += 1
            return relationBind(header, userId, buyerNick, actId, inviterNick, missionType="relationBind", agin=agin)

#获取活动状态码
def getact(ck, header,agin=1):
    try:
        url ='https://jinggengjcq-isv.isvjcloud.com/dm/front/openCardNew/activity_load'
        body = {
                "jsonRpc": "2.0",
                "params": {
                    "commonParameter": {
                        "appkey": "",
                        "m": "POST",
                        "timestamp": int(round(time.time() * 1000)),
                        "userId": "10299171"
                    },
                    "admJson": {
                        "actId": "29c257bced_220124",
                        "userId": "10299171",
                        "jdToken": isvObfuscator(ck),
                        "source": "01",
                        "method": "/openCardNew/activity_load",
                        "buyerNick": ""
                    }
                }
            }
        r = requests.post(url, headers=header, data=json.dumps(body), timeout=30)
        userId, actId, nickName, buyerNick = None, None, None, None
        if r.status_code == 200:
            data = r.json()
            if data['success']:
                # printf(json.dumps(data, indent=4, ensure_ascii=False))
                buyerNick = quote(data['data']['data']['buyerNick'])
                userId = data['data']['data']['missionCustomer']['userId']
                actId = data['data']['data']['missionCustomer']['actId']
                nickName = data['data']['data']['missionCustomer']['nickName']
            else:
                printf(json.dumps(data, indent=4, ensure_ascii=False))
        else:
            printf(f"[getact post error]: {r.status_code} {r.text}")

        return userId, actId, nickName, buyerNick
    except Exception as e:
        if agin > 6:
            printf(f"[getact post error]: {e}")
            return
        else:
            wait_time(3, 10)
            agin += 1
            return getact(ck, header, agin=agin)

def checkOpenCard(header, userId, buyerNick, actId, shopId, missionType="openCard",agin=1):
    try:
        url = f'https://jinggengjcq-isv.isvjcloud.com/dm/front/openCardNew/complete/mission?mix_nick={buyerNick}'
        lable = True
        body = {
            "jsonRpc": "2.0",
            "params": {
                "commonParameter": {
                    "appkey": "",
                    "m": "POST",
                    "timestamp": int(round(time.time() * 1000)),
                    "userId": userId
                },
                "admJson": {
                    "actId": actId,
                    "missionType": missionType,
                    "shopId": shopId,
                    "method": "/openCardNew/complete/mission",
                    "userId": userId,
                    "buyerNick": buyerNick
                }
            }
        }
        r = requests.post(url, headers=header, data=json.dumps(body), timeout=30)
        if r.status_code == 200:
            data = r.json()
            if data['success']:
                if data['data']['status'] == 200:
                    remark = data['data']['data']['remark']
                    sendStatus = data['data']['data']['sendStatus']
                    if not sendStatus:
                        lable = False
                    # else:
                    #     printf(f"{json.dumps(data, indent=4, ensure_ascii=False)}")
        else:
            printf(f"[checkOpenCard post error]: {r.status_code} {r.text}")

        return lable
    except Exception as e:
        if agin > 6:
            printf(f"[{missionType} post error]: {e}")
            return
        else:
            wait_time(3, 10)
            agin += 1
            return checkOpenCard(header, userId, buyerNick, actId, shopId, missionType="openCard",agin=agin)
#获取店铺信息
def getShops(header, nick, userId, actId, agin=1):
    try:
        url = f'https://jinggengjcq-isv.isvjcloud.com/dm/front/openCardNew/shopList?mix_nick={nick}'
        body = {
                "jsonRpc": "2.0",
                "params": {
                    "commonParameter": {
                        "appkey": "",
                        "m": "POST",
                        "timestamp": int(round(time.time() * 1000)),
                        "userId": userId
                    },
                    "admJson": {
                        "actId": actId,
                        "userId": userId,
                        "method": "/openCardNew/shopList",
                        "buyerNick": nick
                    }
                }
            }
        r = requests.post(url, headers=header, data=json.dumps(body), timeout=30)
        venderIdList, channelList = [], []
        if r.status_code == 200:
            data = r.json()
            if data['success']:
                cusShops = data['data']['data']['cusShops']
                for i in cusShops:
                    if not i['open']:
                        if checkOpenCard(header, userId, nick, actId, i['userId']):
                            channel = re.findall(r'channel=(\d+)', i['openCardUrl'])
                            if channel:
                                c = channel[0]
                            else:
                                c = '401'
                            venderIdList.append(i['userId'])
                            channelList.append(c)
            else:
                printf(f"getShops ERROR: [{data}]")
        else:
            printf(f"[getShops post error]: {r.status_code} {r.text}")

        return venderIdList, channelList
    except Exception as e:
        if agin > 6:
            printf(f"[getShops post error]: {e}")
            return
        else:
            wait_time(3, 10)
            agin += 1
            return getShops(header, nick, userId, actId, agin=agin)



#关注加购
def mission(header, missionType, userId, buyerNick, actId,agin=1):
    try:
        url = f'https://jinggengjcq-isv.isvjcloud.com/dm/front/openCardNew/complete/mission?mix_nick={buyerNick}'
        body = {
                "jsonRpc": "2.0",
                "params": {
                    "commonParameter": {
                        "appkey": "",
                        "m": "POST",
                        "timestamp": int(round(time.time() * 1000)),
                        "userId": userId
                    },
                    "admJson": {
                        "actId": actId,
                        "missionType": missionType,
                        "method": "/openCardNew/complete/mission",
                        "userId": userId,
                        "buyerNick": buyerNick
                    }
                }
            }
        r = requests.post(url, headers=header, data=json.dumps(body), timeout=30)
        if r.status_code == 200:
            data = r.json()
            if data['success']:
                if data['data']['status'] == 200:
                    printf(f"\t{data['data']['data']['remark']}")
                else:
                    printf(f"\t{data['data']['data']}")
            else:
                printf(f"\t{data['errorMessage']}")
        else:
            printf(f"[{missionType} post error]: {r.status_code} {r.text}")
    except Exception as e:
        if agin > 6:
            printf(f"[{missionType} post error]: {e}")
            return
        else:
            wait_time(3, 10)
            agin += 1
            return mission(header, missionType, userId, buyerNick, actId,agin=agin)

#抽奖
def draw(header, userId, buyerNick, actId, missionType="draw", agin=1):
    try:
        url = f'https://jinggengjcq-isv.isvjcloud.com/dm/front/openCardNew/draw/post?mix_nick={buyerNick}'
        body = {
            "jsonRpc": "2.0",
            "params": {
                "commonParameter": {
                    "appkey": "",
                    "m": "POST",
                    "timestamp": int(round(time.time() * 1000)),
                    "userId": userId
                },
                "admJson": {
                    "actId": actId,
                    "usedGameNum": "2",
                    "dataType": missionType,
                    "method": "/openCardNew/draw/post",
                    "userId": userId,
                    "buyerNick": buyerNick
                }
            }
        }
        r = requests.post(url, headers=header, data=json.dumps(body), timeout=30)
        if r.status_code == 200:
            data = r.json()
            if data['success']:
                if data['data']['status'] == 200:
                    printf(f"\t{data['data']['data']['remark']}")
                else:
                    printf(f"\t{data['data']}")
            else:
                printf(f"\t{data['errorMessage']}")
        else:
            printf(f"[draw post error]: {r.status_code} {r.text}")
    except Exception as e:
        if agin > 6:
            printf(f"[{missionType} post error]: {e}")
            return
        else:
            wait_time(3, 10)
            agin += 1
            return draw(header, userId, buyerNick, actId, missionType="draw", agin=agin)

def gettext(url):
    try:
        resp = requests.get(url, timeout=60).text
        if '该内容无法显示' in resp:
            return gettext(url)
        return resp
    except Exception as e:
        printf(e)

def isUpdate():
    global hdtitle, code, footer
    hdtitle, code, footer = f'{g_name}', 'k6v981/pPDqeC8LcRX3%2BNVs/ye9oluZX4nOTK56TeMXbR7I2OlzZch4hTs22oCUS', 'TG频道 https://t.me/TopStyle2021\n活动入口：'
    try:
        result = gettext(get_url)
        result = json.loads(result)
        hdtitle = result['title']
        isEnable = result['isEnable']
        readme = result['readme']
        code = result['code']
        footer = result['footer']
        if isEnable == 0:
            codeList = code.split('#')
            s = random.randint(0, len(codeList) - 1)
            code = codeList[s]
        else:
            printf(f"{readme}")
            wait_time(30, 60)
    except:
        pass
    return hdtitle, code, footer

def start():
    global one_code,one_name
    hdtitle, code, footer  = isUpdate()
    printf(f"**************************************\n开始【{hdtitle}】{footer}\n**************************************\n")
    one_code = f"{code}"
    one_name = f"Author"
    if datetime.datetime.now() > datetime.datetime.strptime('2022-2-15', "%Y-%m-%d"):
        printf("活动结束\n请删掉脚本")
        exit(3)
    cookieList, nameList = getCk.iscookie()
    a = 1
    for ck, user in zip(cookieList, nameList):
        try:
            printf(f"账号{a}[{user}]")
            header = {
                "Host": "jinggengjcq-isv.isvjcloud.com",
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "Content-Type": "application/json; charset=utf-8",
                "Origin": "https://jinggengjcq-isv.isvjcloud.com",
                "User-Agent": userAgent(),
                "Referer": "https://jinggengjcq-isv.isvjcloud.com/fronth5/?sid=efe8f329e2b6df53831d3b17b669957w&un_area=19_1601_3633_63243",
                "Cookie": ck,
            }
            userId, actId, nickName, buyerNick = getact(ck, header)
            if buyerNick:
                printf(f"Hi, {nickName}。你的助力码[{buyerNick}]")
                if not relationBind(header, userId, buyerNick, actId, one_code):
                    wait_time(60, 300, "网络异常，请休息一会再试")
                    exit(8)
                if a == 1:
                    printf(f"仅账号1助力作者 {one_code}")
                    one_code = f"{buyerNick}"
                    one_name = f"{nickName}"
                else:
                    printf(f"去助力 {one_name}")
                venderIdList, channelList = getShops(header, buyerNick, userId, actId)
                aaa = {"一键关注": "uniteCollectShop", "一键加购": "uniteAddCart"}
                for k in aaa:
                    printf(f"#去完成 {k}")
                    wait_time(2, 3, f"\t{k}")
                    mission(header, aaa[k], userId, buyerNick, actId)
                # 开卡
                printf(f"#去完成开卡任务")
                if len(venderIdList) > 0:
                    bindWithVender(ck, venderIdList, channelList)
                else:
                    printf(f"\t您已经完成过开卡任务！")
                # 抽奖
                for o in range(3):
                    wait_time(3, 5, f"#去抽奖{o+1}")
                    draw(header, userId, buyerNick, actId)
            else:
                printf(f"{user}参加活动失败, 或请检测ck是否正常!")
            a += 1
            wait_time(kk_vip_sleep, kk_vip_sleep+5, "休息一会,")
        except Exception as e:
            printf(f"start error [{user}请检测ck是否正常!] [{e}]")
            a += 1
            continue

if __name__ == '__main__':
    start()