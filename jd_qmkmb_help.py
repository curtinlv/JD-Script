#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_qmkmb_help 
Author: Curtin
功能：全民开红包-助力  入口：京豆app-领券中心-锦鲤红包
Date: 2021/11/08 下午4:48
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 0 0,23 * * *
new Env('全民开红包-助力');
'''

# 是否按ck顺序助力, true: 按顺序助力 false：按指定用户助力，默认true
qmkhb_isOrder="true"
# 助力名单(当qmkhb_isOrder="false" 才生效), ENV 环境设置 export qmkhb_help="Curtinlv&用户2&用户3"
qmkhb_help = ["Curtinlv", "用户2", "用户3"]
#是否开启通知，Ture：发送通知，False：不发送
isNotice=True
# UA 可自定义你的, 默认随机生成UA。
UserAgent = ''
print("待修复")
exit(0)
import os, re, sys
import random, time
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")
    exit(3)
from urllib.parse import unquote
##############
try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_cookie.py")
    sys.exit(3)
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep

###
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

if "qmkhb_isOrder" in os.environ:
    if len(os.environ["qmkhb_isOrder"]) > 1:
        qmkhb_isOrder = os.environ["qmkhb_isOrder"]
if "qmkhb_help" in os.environ:
    if len(os.environ["qmkhb_help"]) > 1:
        qmkhb_help = os.environ["qmkhb_help"]
        if '&' in qmkhb_help:
            qmkhb_help = qmkhb_help.split('&')
        print("已获取并使用Env环境 qmkhb_help:", qmkhb_help)
if not isinstance(qmkhb_help, list):
    qmkhb_help = qmkhb_help.split(" ")



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
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://happy.m.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': ck,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'User-Agent': userAgent(),
        'Referer': '',
        'Accept-Language': 'zh-cn'
    }
    return headers

def getrid(ck):
    try:
        url = f'https://api.m.jd.com/api?appid=jinlihongbao&functionId=h5activityIndex&loginType=2&client=jinlihongbao&t={round(time.time() * 1000)}&clientVersion=10.2.2&osVersion=-1'
        body = 'body=%7B%22isjdapp%22%3A1%7D'
        resp = requests.post(url=url, headers=buildHeaders(ck), data=body).json()
        rid = resp['data']['result']['redpacketInfo']['id']
        packetTotalSum = resp['data']['result']['redpacketInfo']['packetTotalSum']
        return rid, packetTotalSum
    except Exception as e:
        print(e)
        return '374536093', None

def friendhelp(ck, rid, nickname):
    try:
        t = round(time.time() * 1000)
        url = f'https://api.m.jd.com/api?appid=jinlihongbao&functionId=jinli_h5assist&loginType=2&client=jinlihongbao&t={t}&clientVersion=10.2.0&osVersion=-1'
        body = f'body=%7B%22redPacketId%22:%22{rid}%22,%22followShop%22:1,%20%22random%22:%20%22%22,%20%22log%22:%20%22%22,%20%22sceneid%22:%20%22JLHBhPageh5%22%7D'
        resp = requests.post(url=url, headers=buildHeaders(ck), data=body, timeout=10).json()
        result = resp['data']['result']['statusDesc']
        print(f"\t└😆用户【{nickname}】{result}")
    except Exception as e:
        print(e)
def start():
    try:
        scriptName = '### 全民开红包-助力 ###'
        print(scriptName)
        cookiesList, userNameList = getCk.iscookie()
        if qmkhb_isOrder == "true":
            for ck, user in zip(cookiesList, userNameList):
                print(f"### ☺️开始助力 {user}")
                try:
                    rid, total = getrid(ck)
                except Exception as e:
                    print(e)
                    continue
                for k, nickname in zip(cookiesList, userNameList):
                    if nickname == user:
                        print(f"\t└😓{user} 不能助力自己，跳过~")
                        continue
                    friendhelp(k, rid, nickname)
            msg("### 👌统计：")
            for i,u in zip(cookiesList,userNameList):
                rid, total = getrid(i)
                msg(f"账户🧧[{u}]:本场收益红包:{total}")
            msg("\n【活动入口】：京豆app-领券中心-锦鲤红包。")
        elif qmkhb_isOrder == "false":
            if not qmkhb_help:
                print("您未配置助力的账号，\n助力账号名称：可填用户名 或 pin的值不要; \nenv 设置 export qmkhb_help=\"Curtinlv&用户2\"  多账号&分隔\n本次退出。")
                sys.exit(0)
            msg("### 👌统计：")
            for ckname in qmkhb_help:
                try:
                    ckNum = userNameList.index(ckname)
                except Exception as e:
                    try:
                        ckNum = userNameList.index(unquote(ckname))
                    except:
                        msg(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                        continue
                masterName = userNameList[ckNum]
                rid, total = getrid(cookiesList[ckNum])
                print(f"### ☺️开始助力 {masterName}")
                for ck, nickname in zip(cookiesList, userNameList):
                    if nickname == masterName:
                        print(f"\t└😓{masterName} 不能助力自己，跳过~")
                        continue
                    friendhelp(ck, rid, nickname)
                rid, total = getrid(cookiesList[ckNum])
                msg(f"账户🧧[{masterName}]:本场收益红包:{total}")
            msg("\n【活动入口】：京豆app-领券中心-锦鲤红包。")
        else:
            print("请检查qmkhb_isOrder 变量参数是否正确填写。")
        if isNotice:
            send(scriptName, msg_info)
        else:
            print("\n", scriptName, "\n", msg_info)
    except Exception as e:
        print("start",e)

if __name__ == '__main__':
    start()