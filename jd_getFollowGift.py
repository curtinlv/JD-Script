#!/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_getFollowGift 
Author: Curtin
功能：
Date: 2021/6/6 上午7:57
建议cron: 0 9 * * *
new Env('关注有礼');

2022-1-9:
    1、修复bug
2021-11-08：
    1、修复cookie检测接口
'''
##################################

#######################################
version = 'v1.1.0'
readmes = """
# JD 关注有礼

##  目录结构
    JD-Script/                  #主仓库
    |-- getFollowGifts                # 主目录
    |   |-- jd_getFollowGift.py       # 主代码 （必要）
    |   |-- JDCookies.txt             # 存放JD cookie，一行一个ck
    |   |-- Readme.md                 # 说明书
    |   `-- start.sh                  # shell脚本（非必要）
    `-- README.md


### `【兼容环境】`
    1.Python3.6+ 环境
    2.兼容ios设备软件：Pythonista 3、Pyto(已测试正常跑，其他软件自行测试)   
    3.Windows exe 

    安装依赖模块 :
    pip3 install requests
    执行：
    python3 jd_getFollowGift.py


## `【更新记录】`
    2021.6.6：（v1.0.0 Beta）
        * Test


###### [GitHub仓库 https://github.com/curtinlv/JD-Script](https://github.com/curtinlv/JD-Script) 
###### [TG频道 https://t.me/TopStyle2021](https://t.me/TopStyle2021)
###### [TG群 https://t.me/topStyle996](https://t.me/topStyle996)
###### 关注公众号【TopStyle】
![TopStyle](https://gitee.com/curtinlv/img/raw/master/gzhcode.jpg)
# 
    @Last Version: %s

    @Last Time: 2021-06-06 07:57

    @Author: Curtin
#### **仅以学习交流为主，请勿商业用途、禁止违反国家法律 ，转载请留个名字，谢谢!** 

# End.
[回到顶部](#readme)
""" % version

################################ 【Main】################################
import time, os, sys, datetime
import requests
import re, json, base64
from urllib.parse import unquote, quote_plus

try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)

# 获取当前工作目录
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep

# 定义一些要用到参数
requests.packages.urllib3.disable_warnings()
scriptHeader = """


════════════════════════════════════════
║                                      ║
║      JD   关   注   有   礼           ║
║                                      ║
════════════════════════════════════════
@Version: {}""".format(version)
remarks = '\n\n\tTG交流 : https://t.me/topstyle996\n\n\tTG频道 : https://t.me/TopStyle2021\n\n\t公众号 : TopStyle\n\n\t\t\t--By Curtin\n'
######JD Cookie (多账号&分隔)




#######
notify_mode = []
message_info = ''''''
usergetGiftinfo = {}


## 获取通知服务
class msg(object):
    def __init__(self, m):
        self.str_msg = m
        self.msg()
    def msg(self):
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

def exitCodeFun(code):
    try:
        # exitCode = input()
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            print("进程睡眠10分钟后自动退出。")
            time.sleep(600)
        exit(code)
    except:
        time.sleep(3)
        exit(code)

def nowtime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')





# 检查是否有更新版本

def gettext(url):
    try:
        resp = requests.get(url, timeout=60).text
        if '该内容无法显示' in resp or '违规' in resp:
            return gettext(url)
        return resp
    except Exception as e:
        print(e)


def isUpdate():
    global footer,readme,uPversion,scriptName
    url = base64.decodebytes(
        b"aHR0cHM6Ly9naXRlZS5jb20vY3VydGlubHYvUHVibGljL3Jhdy9tYXN0ZXIvRm9sbG93R2lmdHMvdXBkYXRlLmpzb24=")
    try:
        result = gettext(url)
        result = json.loads(result)
        scriptName = result['name']
        isEnable = result['isEnable']
        uPversion = result['version']
        info = result['info']
        readme = result['readme']
        pError = result['m']
        footer = result['footer']
        getWait = result['s']
        if isEnable > 50 and isEnable < 150:
            if version != uPversion:
                print(f"\n当前最新版本：【{uPversion}】\n\n{info}\n")
                msg(f"{readme}")
                exitCodeFun(888)
            else:
                msg(f"{readme}")
                time.sleep(getWait)
        else:
            print(pError)
            exitCodeFun(888)

    except:
        msg("请检查您的环境/版本是否正常！")
        exitCodeFun(888)

def outfile(filename, context):
    with open(filename, "w+", encoding="utf-8") as f1:
        f1.write(context)
        f1.close()


def getRemoteShopid():
    url = base64.decodebytes(
        b"aHR0cHM6Ly9naXRlZS5jb20vY3VydGlubHYvUHVibGljL3Jhdy9tYXN0ZXIvRm9sbG93R2lmdHMvc2hvcGlkLnR4dA==")
    try:
        rShopid = gettext(url)
        rShopid = rShopid.split("\n")
        return rShopid
    except:
        print("无法从远程获取shopid")
        exitCodeFun(999)
def createShopidList():
    global shopidNum ,shopidList
    shopidList = []
    shopids = getRemoteShopid()
    shopidNum = len(shopids) - 1
    for i in range(shopidNum):
        shopid = shopids[i]
        shopid = eval(shopid)
        shopidList.append(shopid)
def memoryFun(pinName,bean):
    global usergetGiftinfo
    try:
        try:

            usergetGiftinfo['{}'.format(pinName)]
            usergetGiftinfo['{}'.format(pinName)] += bean
        except:
            usergetGiftinfo['{}'.format(pinName)] = bean
    except Exception as e:
        print(e)

def buildBody(data):
    shopid = data['shopid']
    venderId = data['venderId']
    activityId = data['activityId']
    signbody = data['signbody']
    openudid = data['openudid']
    body = 'body={"follow":0,"shopId":"' + shopid + '","activityId":"' + activityId + '","sourceRpc":"shop_app_home_window","venderId":"'+ venderId + '"}&build=&client=apple&clientVersion=10.2.4&d_brand=apple&d_model=iPhone10,3&ef=1&eid=&ep={"ciphertype":5,"cipher":{"openudid":"' + openudid + '"}}&ext={"prstate":"0"}&joycious=66&lang=zh_CN&partner=TF&' + signbody

    return body

def drawShopGift(cookie, data):
    try:
        url = 'https://api.m.jd.com/client.action?functionId=drawShopGift'
        body = data
        headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'JD4iPhone/167870%20(iPhone;%20iOS;%20Scale/3.00)',
            'Cookie': cookie,
            'Host': 'api.m.jd.com',
            'Referer': '',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'Accept': '*/*'
        }
        n = 1
        while True:
            response = requests.post(url, headers=headers, data=body, timeout=60)
            if response.status_code != 403:
                break
            else:
                if n == 6:
                    break
                n += 1
                print("狗东限制ip，休眠60秒...")
                sys.stdout.flush()
                time.sleep(60)
        if 'isSuccess' in response.text:
            return response.json()
        else:
            return 9
    except Exception as e:
        return 9
def getGiftresult(result, nickname, pinName, uNum):
    try:
        if result['isSuccess']:
            if result['result']:
                followDesc = result['result']['followDesc']
                giftDesc = result['result']['giftDesc']
                print(f"\t└账号{uNum}【{nickname}】{followDesc}>{giftDesc}")
                if result['result']['giftCode'] == '200':
                    try:
                        alreadyReceivedGifts = result['result']['alreadyReceivedGifts']
                        for g in alreadyReceivedGifts:
                            if g['prizeType'] == 4:
                                bean = g['redWord']
                                memoryFun(pinName, int(bean))
                            print(f"\t\t└获得{g['rearWord']}:{g['redWord']}")
                    except:
                        pass
    except Exception as e:
        print(f"getGiftresult Error {e}")


def start():
    print(scriptHeader)
    isUpdate()
    outfile("Readme.md", readmes)
    cookiesList, userNameList = getCk.iscookie()
    userNum = len(cookiesList)
    msg(f"开始：{scriptName}")
    createShopidList()
    msg(f"获取到店铺：{shopidNum}")
    starttime = time.perf_counter()  # 记录时间开始
    for i in shopidList:
        body = buildBody(i)
        print(f"关注店铺【{i['shopid']}】")
        uNum = 1
        for ck, nickname in zip(cookiesList, userNameList):
            result = drawShopGift(ck, body)
            time.sleep(1.5)
            if result != 9:
                getGiftresult(result, nickname, nickname, uNum)
            else:
                uNum += 1
                break
            uNum += 1
    endtime = time.perf_counter()  # 记录时间结束
    msg("\n###【本次统计 {}】###\n".format(nowtime()))
    all_get_bean = 0
    n = 1
    for name, pinname in zip(userNameList, userNameList):
        try:
            userCountBean = usergetGiftinfo['{}'.format(pinname)]
            msg(f"账号{n}:【{name}】\n\t└收获 {userCountBean} 京豆")
            all_get_bean += userCountBean
        except Exception as e:
            msg(f"账号{n}:【{name}】\n\t└收获 0 京豆")
        n += 1
    msg(f"\n本次总累计获得：{all_get_bean} 京豆")
    msg("\n------- 总耗时 : %.03f 秒 seconds -------" % (endtime - starttime))
    print("{0}\n{1}\n{2}".format("*" * 30, scriptHeader, remarks))
    send(f"【{scriptName}】", message_info)
    exitCodeFun(0)

if __name__ == '__main__':
    start()
