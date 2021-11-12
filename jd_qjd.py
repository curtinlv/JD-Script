#!/usr/bin/env python3
# -*- coding: utf-8 -*
#全民抢京豆（8.6-8.16)
'''
项目名称: JD-Script / jd_qjd
Author: Curtin
功能：全民抢京豆（10.29-11.12）：https://h5.m.jd.com/rn/3MQXMdRUTeat9xqBSZDSCCAE9Eqz/index.html?has_native=0
    满160豆需要20人助力，每个用户目前只能助力2次不同的用户。
Date: 2021/7/3 上午10:02
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
update: 2021.11.08 20:21
建议cron: 0 0 * 10,11 *  python3 jd_qjd.py
new Env('全民抢京豆 10.29-11.12');
* 修复了助力活动不存在、增加了随机UA（如果未定义ua则启用随机UA）
* 新增推送
* 修复0点不能开团
* 兼容pin为中文转码编码
'''
# print("全民抢京豆(10.29-11.12）--活动已结束\nTG交流 https://t.me/topstyle996\nTG频道 https://t.me/TopStyle2021")
# exit(0)
#ck 优先读取【JDCookies.txt】 文件内的ck  再到 ENV的 变量 JD_COOKIE='ck1&ck2' 最后才到脚本内 cookies=ck
cookies=''
qjd_zlzh=['Curtinlv', '买买买']
#是否开启通知，ture：发送通知，false：不发送 。如关闭通知：export qjd_isNotice="false"
qjd_isNotice="true"

#####

# 建议调整一下的参数
# UA 可自定义你的，默认随机
UserAgent = ''
# 限制速度 （秒）
sleepNum = 0.1

import os, re, sys
import random, string
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
from urllib.parse import unquote
import json
import time
try:
    from jd_cookie import getJDCookie
    getCk = getJDCookie()
except:
    print("请先下载依赖脚本，\n下载链接：https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/jd_tool_dl.py")
    sys.exit(3)
requests.packages.urllib3.disable_warnings()
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
t = time.time()
aNum = 0
beanCount = 0
userCount = {}
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

def getEnvs(label):
    try:
        if label == 'True' or label == 'yes' or label == 'true' or label == 'Yes':
            return True
        elif label == 'False' or label == 'no' or label == 'false' or label == 'No':
            return False
    except Exception as e:
        pass
    try:
        if '.' in label:
            return float(label)
        elif '&' in label:
            return label.split('&')
        elif '@' in label:
            return label.split('@')
        else:
            return int(label)
    except:
        return label


if "qjd_zlzh" in os.environ:
    if len(os.environ["qjd_zlzh"]) > 1:
        qjd_zlzh = os.environ["qjd_zlzh"]
        qjd_zlzh = qjd_zlzh.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
        print("已获取并使用Env环境 qjd_zlzh:", qjd_zlzh)
if "qjd_isNotice" in os.environ:
    if len(os.environ["qjd_isNotice"]) > 1:
        qjd_isNotice = os.environ["qjd_isNotice"]

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

def getShareCode(ck):
    global aNum
    try:
        v_num1 = ''.join(random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 1)) + ''.join(random.sample(string.digits, 4))
        url1 = f'https://api.m.jd.com/client.action?functionId=signGroupHit&body=%7B%22activeType%22%3A2%7D&appid=ld&client=apple&clientVersion=10.0.6&networkType=wifi&osVersion=14.3&uuid=&jsonp=jsonp_' + str(int(round(t * 1000))) + '_' + v_num1
        url = 'https://api.m.jd.com/client.action?functionId=signBeanGroupStageIndex&body=%7B%22monitor_refer%22%3A%22%22%2C%22rnVersion%22%3A%223.9%22%2C%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22monitor_source%22%3A%22bean_m_bean_index%22%7D&appid=ld&client=apple&clientVersion=&networkType=&osVersion=&uuid=&jsonp=jsonp_' + str(int(round(t * 1000))) + '_' + v_num1
        head = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://h5.m.jd.com/rn/3MQXMdRUTeat9xqBSZDSCCAE9Eqz/index.html?has_native=0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'api.m.jd.com',
            # 'User-Agent': 'Mozilla/5.0 (iPhone CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
            'User-Agent': userAgent(),
            'Accept-Language': 'zh-cn'
        }
        requests.get(url1,  headers=head, verify=False, timeout=30)
        resp = requests.get(url=url, headers=head, verify=False, timeout=30).text
        r = re.compile(r'jsonp_.*?\((.*?)\)\;', re.M | re.S | re.I)
        result = r.findall(resp)
        jsonp = json.loads(result[0])
        try:
            groupCode = jsonp['data']['groupCode']
            shareCode = jsonp['data']['shareCode']
            activityId = jsonp['data']['activityMsg']['activityId']
            sumBeanNumStr = int(jsonp['data']['sumBeanNumStr'])
        except:
            if aNum < 5:
                aNum += 1
                return getShareCode(ck)
            else:
                groupCode = 0
                shareCode = 0
                sumBeanNumStr = 0
                aNum = 0
                activityId = 0
        aNum = 0
        return groupCode, shareCode, sumBeanNumStr, activityId
    except Exception as e:
        print(f"getShareCode Error", e)

def helpCode(ck, groupCode, shareCode,u, unum, user, activityId):
    try:
        v_num1 = ''.join(random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 1)) + ''.join(random.sample(string.digits, 4))
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': f'https://h5.m.jd.com/rn/42yjy8na6pFsq1cx9MJQ5aTgu3kX/index.html?jklActivityId=115&source=SignSuccess&jklGroupCode={groupCode}&ad_od=1&jklShareCode={shareCode}',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'api.m.jd.com',
            'User-Agent': userAgent(),
            'Accept-Language': 'zh-cn'
        }
        url = 'https://api.m.jd.com/client.action?functionId=signGroupHelp&body=%7B%22activeType%22%3A2%2C%22groupCode%22%3A%22' + str(groupCode) + '%22%2C%22shareCode%22%3A%22' + shareCode + f'%22%2C%22activeId%22%3A%22{activityId}%22%2C%22source%22%3A%22guest%22%7D&appid=ld&client=apple&clientVersion=10.0.4&networkType=wifi&osVersion=13.7&uuid=&openudid=&jsonp=jsonp_{int(round(t * 1000))}_{v_num1}'
        resp = requests.get(url=url, headers=headers, verify=False, timeout=30).text
        r = re.compile(r'jsonp_.*?\((.*?)\)\;', re.M | re.S | re.I)
        result = r.findall(resp)
        jsonp = json.loads(result[0])
        helpToast = jsonp['data']['helpToast']
        pageFlag = jsonp['data']['pageFlag']
        if pageFlag == 0:
            print(f"账号{unum}【{u}】助力失败! 原因：{helpToast}")
            if '满' in helpToast:
                print(f"## 恭喜账号【{user}】团已满，今日累计获得160豆")
                return True
            return False
        else:
            if '火' in helpToast:
                print(f"账号{unum}【{u}】助力失败! 原因：{helpToast}")
            else:
                print(f"账号{unum}【{u}】{helpToast} , 您也获得1豆哦~")
            return False
    except Exception as e:
        print(f"helpCode Error ", e)

def start():
    scriptName='### 全民抢京豆-助力 ###'
    print(scriptName)
    global cookiesList, userNameList, ckNum, beanCount, userCount
    cookiesList, userNameList = getCk.iscookie()
    for ckname in qjd_zlzh:
        try:
            ckNum = userNameList.index(ckname)
        except Exception as e:
            try:
                ckNum = userNameList.index(unquote(ckname))
            except:
                print(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                continue

        print(f"### 开始助力账号【{userNameList[int(ckNum)]}】###")
        groupCode, shareCode, sumBeanNumStr, activityId = getShareCode(cookiesList[ckNum])
        if groupCode == 0:
            msg(f"## {userNameList[int(ckNum)]}  获取互助码失败。请手动分享后再试~ 。")
            continue
        u = 0
        for i in cookiesList:
            if i == cookiesList[ckNum]:
                u += 1
                continue
            result = helpCode(i, groupCode, shareCode, userNameList[u], u+1, userNameList[int(ckNum)], activityId)
            time.sleep(sleepNum)
            if result:
                break
            u += 1
        groupCode, shareCode, sumBeanNumStr, activityId = getShareCode(cookiesList[ckNum])
        userCount[f'{userNameList[ckNum]}'] = sumBeanNumStr
        beanCount += sumBeanNumStr
    print("\n-------------------------")
    for i in userCount.keys():
        msg(f"账号【{i}】已抢京豆: {userCount[i]}")
    msg(f"## 今日累计获得 {beanCount} 京豆")
    try:
        if qjd_isNotice == "true":
            send(scriptName, msg_info)
    except:
        pass


if __name__ == '__main__':
    start()
