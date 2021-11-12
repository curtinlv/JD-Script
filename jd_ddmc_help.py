#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_ddmc_help 
Author: Curtinr
功能：东东萌宠-助力
Date: 2021/11/08 下午9:30
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 1 0,23 * * *
new Env('东东萌宠-助力');
'''

# 是否按ck顺序助力, true: 按顺序助力 false：按指定用户助力，默认true
ddmc_isOrder="true"
# 助力名单(当ddmc_isOrder="false" 才生效), ENV 环境设置 export ddmc_help="Curtinlv&用户2&用户3"
ddmc_help = ["Curtinlv", "用户x", "用户3"]
#是否开启通知，Ture：发送通知，False：不发送
isNotice=True
# UA 可自定义你的, 默认随机生成UA。
UserAgent = ''

import os, sys
import random
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")
    exit(3)
try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)
from urllib.parse import unquote
##############
requests.packages.urllib3.disable_warnings()
# requests.packages.urllib3.disable_warnings()
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
host_api = 'https://api.m.jd.com/client.action'
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


if "ddmc_isOrder" in os.environ:
    if len(os.environ["ddmc_isOrder"]) > 1:
        ddmc_isOrder = os.environ["ddmc_isOrder"]
if "ddmc_help" in os.environ:
    if len(os.environ["ddmc_help"]) > 1:
        ddmc_help = os.environ["ddmc_help"]
        if '&' in ddmc_help:
            ddmc_help = ddmc_help.split('&')
        print("已获取并使用Env环境 ddmc_help:", ddmc_help)
if not isinstance(ddmc_help, list):
    ddmc_help = ddmc_help.split(" ")



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
        'request-from': 'native',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://h5.m.jd.com',
        'User-Agent': userAgent(),
        'Cookie': ck,
        'Host': 'api.m.jd.com',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/WiXHzdNRVxmQQdEpLo4Z4yvsiFy/index.html?',
        'Accept-Language': 'zh-cn',
        'Accept': 'application/json, text/plain, */*'
    }
    return headers

def getShareCode(ck):
    try:
        body = 'functionId=initPetTown&body={"version":1}&client=wh5&clientVersion=1.0.0'
        resp = requests.post(url=host_api, headers=buildHeaders(ck), data=body, timeout=10).json()
        return resp['result']['shareCode']
    except:
        return 'MTE1NDAxNzgwMDAwMDAwNDM4ODc1MjU='

def getHelpAddedBonus(ck):
    try:
        body='functionId=getHelpAddedBonus&body={}&client=wh5&clientVersion=1.0.0'
        resp = requests.post(url=host_api, headers=buildHeaders(ck), data=body, timeout=10).json()
        if resp['resultCode'] == '0':
            msg(f"\t\t└👌领取额外奖励：{resp['result']['reward']}g, 当前：{resp['result']['foodAmount']}g")
        else:
            msg(f"\t\t└👌领取额外奖励：{resp['message']}")
    except:
        pass

def ddmc(ck, shareCode, user):
    try:
        body = 'functionId=slaveHelp&body={"shareCode":"' + shareCode + '"}&client=wh5&clientVersion=1.0.0'
        resp = requests.post(url=host_api, headers=buildHeaders(ck), data=body, timeout=10).json()
        if resp['resultCode'] == '0':
            if resp['result']['helpStatus'] == 0:
                print(f"\t└[{user}] 助力结果：{resp['message']}")
            if resp['result']['helpStatus'] == 2:
                return True
            else:
                return False
        else:
            return False
    except:
        pass

def start():
    try:
        scriptName = '### 东东萌宠-助力 ###'
        print(scriptName)
        cookiesList, userNameList = getCk.iscookie()
        if ddmc_isOrder == "true":
            for ck, master in zip(cookiesList, userNameList):
                print(f"### ☺️开始助力 {master}")
                sharecode = getShareCode(ck)
                for c, user in zip(cookiesList, userNameList):
                    if master == user:
                        print(f"\t└😓{user} 不能助力自己，跳过~")
                        continue
                    if ddmc(c, sharecode,user):
                        msg(f"☺️[{master}]已完成助力~")
                        getHelpAddedBonus(ck)
                        break
        elif ddmc_isOrder == "false":
            if not ddmc_help:
                print("您未配置助力的账号，\n助力账号名称：可填用户名 或 pin的值不要; \nenv 设置 export qmkhb_help=\"Curtinlv&用户2\"  多账号&分隔\n本次退出。")
                sys.exit(0)
            for ckname in ddmc_help:
                try:
                    ckNum = userNameList.index(ckname)
                except Exception as e:
                    try:
                        ckNum = userNameList.index(unquote(ckname))
                    except:
                        msg(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                        continue
                master = userNameList[ckNum]
                sharecode = getShareCode(cookiesList[ckNum])
                print(f"### ☺️开始助力 {master}")
                for c, user in zip(cookiesList, userNameList):
                    if master == user:
                        print(f"\t└😓{user} 不能助力自己，跳过~")
                        continue
                    if ddmc(c, sharecode, user):
                        msg(f"☺️[{master}]已完成助力~")
                        getHelpAddedBonus(cookiesList[ckNum])
                        break
        if isNotice:
            send(scriptName, msg_info)
        else:
            print("\n", scriptName, "\n", msg_info)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    start()
