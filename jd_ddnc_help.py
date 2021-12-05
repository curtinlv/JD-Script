#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_ddnc_help_list 
Author: Curtin
功能：东东农场-仅助力使用
Date: 2021/11/08 下午8:20
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

count = {}

import os, sys
import random
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")
    exit(3)
from urllib.parse import unquote
import time
try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)
requests.packages.urllib3.disable_warnings()
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
def farmA(ck):
    url1 = 'https://api.m.jd.com/client.action?functionId=farmAssistInit&body=%7B%22version%22%3A14%2C%22channel%22%3A1%2C%22babelChannel%22%3A%22120%22%7D&appid=wh5'
    resp = requests.get(url1, headers=buildHeaders(ck), timeout=10).json()
    if resp['status'] == 2:
        return True
    else:
        return False
def getSuccess(ck, user):
    global count
    url = 'https://api.m.jd.com/client.action?functionId=receiveStageEnergy&body=%7B%22version%22%3A14%2C%22channel%22%3A1%2C%22babelChannel%22%3A%22120%22%7D&appid=wh5'
    resp = requests.get(url,  headers=buildHeaders(ck), timeout=10).json()
    if resp['code'] == '0':
        print(f"☺️{user}, 收货水滴【{resp['amount']}g】")
        try:
            count[user] += resp['amount']
        except:
            count[user] = resp['amount']
    # print(resp)

def getShareCode(ck):
    url = f'https://api.m.jd.com/client.action?functionId=initForFarm&body=%7B%22shareCode%22%3A%22%22%2C%22imageUrl%22%3A%22%22%2C%22nickName%22%3A%22%22%2C%22version%22%3A14%2C%22channel%22%3A2%2C%22babelChannel%22%3A3%7D&appid=wh5'
    response = requests.get(url=url, headers=buildHeaders(ck), timeout=10).json()
    return response['farmUserPro']['shareCode']

def ddnc_help(ck, nickname, shareCode, masterName):
    try:
        url = f'https://api.m.jd.com/client.action?functionId=initForFarm&body=%7B%22shareCode%22%3A%22{shareCode}%22%2C%22imageUrl%22%3A%22%22%2C%22nickName%22%3A%22%22%2C%22version%22%3A14%2C%22channel%22%3A2%2C%22babelChannel%22%3A3%7D&appid=wh5'
        response = requests.get(url=url, headers=buildHeaders(ck), timeout=10).json()
        help_result = response['helpResult']['code']
        if help_result == "0":
            print(f"\t└👌{nickname} 助力成功～")
        elif help_result == "8":
            print(f"\t└😆{nickname} 已没有助力机会~  ")
        elif help_result == "10":
            msg(f"\t└☺️ {masterName} 今天好友助力已满～")
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
        global cookiesList, userNameList, ckNum
        cookiesList, userNameList = getCk.iscookie()
        if ddnc_isOrder == "true":
            for ck,user in zip(cookiesList,userNameList):
                try:
                    m_ck = ck
                    print(f"开始助力 {user}")
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
                        if farmA(m_ck):
                            getSuccess(m_ck, user)
                        if result:
                            for n in range(4):
                                if farmA(m_ck):
                                    time.sleep(2)
                                    getSuccess(m_ck, user)
                            break
                except:
                    continue

        elif ddnc_isOrder == "false":
            if not ddnc_help_list:
                print("您未配置助力的账号，\n助力账号名称：可填用户名 或 pin的值不要; \nenv 设置 export ddnc_help_list=\"Curtinlv&用户2\"  多账号&分隔\n本次退出。")
                sys.exit(0)
            for ckname in ddnc_help_list:
                try:
                    ckNum = userNameList.index(ckname)
                except Exception as e:
                    try:
                        ckNum = userNameList.index(unquote(ckname))
                    except:
                        msg(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                        continue
                masterName = userNameList[ckNum]
                shareCode = getShareCode(cookiesList[ckNum])
                print(f"开始助力 {masterName}")
                for ck, nickname in zip(cookiesList, userNameList):
                    try:
                        if nickname == masterName:
                            print(f"\t└😓{masterName} 不能助力自己，跳过~")
                            continue
                        result = ddnc_help(ck, nickname, shareCode, masterName)
                        if farmA(cookiesList[ckNum]):
                            getSuccess(cookiesList[ckNum], masterName)
                        if result:
                            for n in range(4):
                                if farmA(cookiesList[ckNum]):
                                    time.sleep(2)
                                    getSuccess(cookiesList[ckNum], masterName)
                            break
                    except:
                        continue
        else:
            print("😓请检查ddnc_isOrder 变量参数是否正确填写。")
        msg("*"*30)
        for i in count:
            msg(f"💧账号【{i}】本次助力收获水滴:{count[i]}g 💧")
        msg("*" * 30)
        if isNotice:
            send(scriptName, msg_info)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    start()

