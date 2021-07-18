#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_dreamfactory_tuan 
Author: Curtin
功能：
Date: 2021/7/17 下午9:40
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
'''
#ck 优先读取【JDCookies.txt】 文件内的ck  再到 ENV的 变量 JD_COOKIE='ck1&ck2' 最后才到脚本内 cookies=ck
cookies = ''
# 设置开团的账号可填用户名 或 pin的值不要; env 设置 export jxgc_kaituan="用户1&用户2"
jxgc_kaituan = ['示例用户1']
#惊喜UA
UserAgent = ''

import os, re, sys
import random
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")
    exit(3)
from urllib.parse import unquote, quote
import json
import time
requests.packages.urllib3.disable_warnings()
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep

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

class getJDCookie(object):
    # 适配各种平台环境ck

    def getckfile(self):
        global v4f
        curf = pwd + 'JDCookies.txt'
        v4f = '/jd/config/config.sh'
        ql_new = '/ql/config/env.sh'
        ql_old = '/ql/config/cookie.sh'
        if os.path.exists(curf):
            with open(curf, "r", encoding="utf-8") as f:
                cks = f.read()
                f.close()
            r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
            cks = r.findall(cks)
            if len(cks) > 0:
                return curf
            else:
                pass
        if os.path.exists(ql_new):
            print("当前环境青龙面板新版")
            return ql_new
        elif os.path.exists(ql_old):
            print("当前环境青龙面板旧版")
            return ql_old
        elif os.path.exists(v4f):
            print("当前环境V4")
            return v4f
        return curf

    # 获取cookie
    def getCookie(self):
        global cookies
        ckfile = self.getckfile()
        try:
            if os.path.exists(ckfile):
                with open(ckfile, "r", encoding="utf-8") as f:
                    cks = f.read()
                    f.close()
                if 'pt_key=' in cks and 'pt_pin=' in cks:
                    r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
                    cks = r.findall(cks)
                    if len(cks) > 0:
                        if 'JDCookies.txt' in ckfile:
                            print("当前获取使用 JDCookies.txt 的cookie")
                        cookies = ''
                        for i in cks:
                            if 'pt_key=xxxx' in i:
                                pass
                            else:
                                cookies += i
                        return
            else:
                with open(pwd + 'JDCookies.txt', "w", encoding="utf-8") as f:
                    cks = "#多账号换行，以下示例：（通过正则获取此文件的ck，理论上可以自定义名字标记ck，也可以随意摆放ck）\n账号1【Curtinlv】cookie1;\n账号2【TopStyle】cookie2;"
                    f.write(cks)
                    f.close()
            if "JD_COOKIE" in os.environ:
                if len(os.environ["JD_COOKIE"]) > 10:
                    cookies = os.environ["JD_COOKIE"]
                    print("已获取并使用Env环境 Cookie")
        except Exception as e:
            print(f"【getCookie Error】{e}")

    # 检测cookie格式是否正确
    def getUserInfo(self, ck, pinName, userNum):
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback=GetJDUserInfoUnion'
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'close',
            'Referer': 'https://home.m.jd.com/myJd/home.action',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'me-api.jd.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'zh-cn'
        }
        try:
            resp = requests.get(url=url, verify=False, headers=headers, timeout=60).text
            r = re.compile(r'GetJDUserInfoUnion.*?\((.*?)\)')
            result = r.findall(resp)
            userInfo = json.loads(result[0])
            nickname = userInfo['data']['userInfo']['baseInfo']['nickname']
            return ck, nickname
        except Exception:
            context = f"账号{userNum}【{pinName}】Cookie 已失效！请重新获取。"
            print(context)
            return ck, False

    def iscookie(self):
        """
        :return: cookiesList,userNameList,pinNameList
        """
        cookiesList = []
        userNameList = []
        pinNameList = []
        if 'pt_key=' in cookies and 'pt_pin=' in cookies:
            r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
            result = r.findall(cookies)
            if len(result) >= 1:
                print("您已配置{}个账号".format(len(result)))
                u = 1
                for i in result:
                    r = re.compile(r"pt_pin=(.*?);")
                    pinName = r.findall(i)
                    pinName = unquote(pinName[0])
                    # 获取账号名
                    ck, nickname = self.getUserInfo(i, pinName, u)
                    if nickname != False:
                        cookiesList.append(ck)
                        userNameList.append(nickname)
                        pinNameList.append(pinName)
                    else:
                        u += 1
                        continue
                    u += 1
                if len(cookiesList) > 0 and len(userNameList) > 0:
                    return cookiesList, userNameList, pinNameList
                else:
                    print("没有可用Cookie，已退出")
                    exit(3)
            else:
                print("cookie 格式错误！...本次操作已退出")
                exit(4)
        else:
            print("cookie 格式错误！...本次操作已退出")
            exit(4)
getCk = getJDCookie()
getCk.getCookie()

# 获取v4环境 特殊处理
try:
    with open(v4f, 'r', encoding='utf-8') as v4f:
        v4Env = v4f.read()
    r = re.compile(r'^export\s(.*?)=[\'\"]?([\w\.\-@#&=_,\[\]\{\}\(\)]{1,})+[\'\"]{0,1}$',
                   re.M | re.S | re.I)
    r = r.findall(v4Env)
    curenv = locals()
    for i in r:
        if i[0] != 'JD_COOKIE':
            curenv[i[0]] = getEnvs(i[1])
except:
    pass

if "jxgc_kaituan" in os.environ:
    if len(os.environ["jxgc_kaituan"]) > 1:
        jxgc_kaituan = os.environ["jxgc_kaituan"]
        if '&' in jxgc_kaituan:
            jxgc_kaituan = jxgc_kaituan.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split('&')
        elif ',' in jxgc_kaituan:
            jxgc_kaituan = jxgc_kaituan.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
        elif '@' in jxgc_kaituan:
            jxgc_kaituan = jxgc_kaituan.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split('@')
        print("已获取并使用Env环境 jxgc_kaituan:", jxgc_kaituan)


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

def userAgent():
    """
    随机生成一个UA
    :return: ua
    """
    if not UserAgent:
        uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
        addressid = ''.join(random.sample('1234567898647', 10))
        iosVer = ''.join(random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
        iosV = iosVer.replace('.', '_')
        iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
        ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
        return f'jdpingou;iPhone;4.11.0;{iosVer};{uuid};network/wifi;model/iPhone{iPhone},1;appBuild/100591;ADID/{ADID};supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/0;hasOCPay/0;supportBestPay/0;session/8;pap/JA2019_3111789;brand/apple;supportJDSHWK/1;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    else:
        return UserAgent
def getResult(text):
    try:
        r = re.compile(r'try\s{jsonp.*?\((.*?)\)', re.M | re.S | re.I)
        r = r.findall(text)
        if len(r) > 0:
            return json.loads(r[0])
        else:
            return text
    except Exception as e:
        print(e)
        return text
def QueryActiveConfig(ck):
    try:
        url = f'https://m.jingxi.com/dreamfactory/tuan/QueryActiveConfig?activeId=T_zZaWP6by9yA1wehxM4mg%3D%3D&tuanId=&_time=1626528863398&_stk=_time%2CactiveId%2CtuanId&_ste=1&h5st=20210717213423401%3B4316088645437162%3B10001%3Btk01w692e1a35a8nelBVM0N0NEliPUhE8RRHmMdPdJCfVENO%2FE71ZoMM98S4V67ihTo7hDW75aJaU5V2XpU99JrsLPEF%3Bfd20eeaf2e88c127d898c14c6c941e80097a01c7d235c405316a08ab70709e20&_={int(round(time.time() * 1000))}&sceneval=2&g_login_type=1&callback=jsonpCBKF&g_ty=ls'
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://st.jingxi.com/pingou/dream_factory/divide.html?activeId=T_zZaWP6by9yA1wehxM4mg==&_close=1&jxsid=',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'm.jingxi.com',
            'User-Agent': 'jdpingou',
            'Accept-Language': 'zh-cn'
        }
        r = requests.get(url, headers=headers, timeout=30, verify=False).text
        data = getResult(r)
        tuanId = data['data']['userTuanInfo']['tuanId']
        activeId = data['data']['userTuanInfo']['activeId']
        isOpenTuan = data['data']['userTuanInfo']['isOpenTuan']
        surplusOpenTuanNum = data['data']['userTuanInfo']['surplusOpenTuanNum']
        encryptPin = data['data']['userInfo']['encryptPin']
        return tuanId, isOpenTuan, surplusOpenTuanNum, encryptPin, activeId
    except Exception as e:
        print(e)

def CreateTuan(ck):
    try:
        url = f'https://m.jingxi.com/dreamfactory/tuan/CreateTuan?activeId=T_zZaWP6by9yA1wehxM4mg%3D%3D&isOpenApp=1&_time=1626528861612&_stk=_time%2CactiveId%2CisOpenApp&_ste=1&h5st=20210717213421615%3B4316088645437162%3B10001%3Btk01w692e1a35a8nelBVM0N0NEliPUhE8RRHmMdPdJCfVENO%2FE71ZoMM98S4V67ihTo7hDW75aJaU5V2XpU99JrsLPEF%3Bfe30749da12b4aab179b7fa95c4f7c20f46fda2cc50228293a47a337f1b3b734&_={int(round(time.time() * 1000))}&sceneval=2&g_login_type=1&callback=jsonpCBKE&g_ty=ls'
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Referer': 'https://st.jingxi.com/pingou/dream_factory/divide.html?activeId=T_zZaWP6by9yA1wehxM4mg==&_close=1&jxsid=',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'm.jingxi.com',
            'User-Agent': 'jdpingou',
            'Accept-Language': 'zh-cn'
        }
        r = requests.get(url, headers=headers, timeout=30, verify=False).text
        getResult(r)
        tuanId, isOpenTuan, surplusOpenTuanNum, encryptPin, activeId = QueryActiveConfig(ck)
        return tuanId, encryptPin, activeId
    except Exception as e:
        print(e)


def JoinTuan(ck, tuanId, encryptPin, activeId, suser, user):
    tuanId = quote(tuanId.encode('utf-8'))
    encryptPin = quote(encryptPin.encode('utf-8'))
    activeId = quote(activeId.encode('utf-8'))
    # print(tuanId, encryptPin, activeId)
    try:
        url = f'https://m.jingxi.com/dreamfactory/tuan/JoinTuan?activeId={activeId}&tuanId={tuanId}&_time=1626528958108&_stk=_time%2CactiveId%2CtuanId&_ste=1&h5st=20210717213558108%3B7117923136170161%3B10001%3Btk01wbabf1c6fa8nVWEzUnhGbkVXu%2BU5JvIH0sBY5KdtN%2FeUVwp%2FzPwCL7k9379OjujqfoLqoyJBK57podKunhi70f1O%3B81b27455ee7e75153e85c3ebb3bb4ada876200faa31d0e792037390b79ce5eff&_=1626528958110&sceneval=2&g_login_type=1&callback=jsonpCBKF&g_ty=ls'
        headers = {
            'Cookie': ck + f'mba_sid=1.1; deviceName=iPhone; deviceOS=iOS; deviceOSVersion=; deviceVersion=4.11.0;_tj_rvurl=https%3A//wq.jd.com/cube/front/activePublish/dream_factory_report/380556.html%3FactiveId%3D{activeId}%26sTuanId%3D{tuanId}%26sPin%3D{encryptPin}%26sType%3D101%26share_ptag%3D%26srv%3Djinshusongjin_https%3A//wq.jd.com/cube/front/activePublish/dream_factory_report/380556.html_jing; jxsid_s_t=; jxsid_s_u=https%3A//st.jingxi.com/pingou/dream_factory/divide.html; cid=4; jxsid=; retina=1; webp=0;',
            'Accept': '*/*',
            'Connection': 'colse',
            'Referer': f'https://st.jingxi.com/pingou/dream_factory/divide.html?activeId={activeId}&sTuanId={tuanId}&sPin={encryptPin}&sType=101&share_ptag=&srv=jinshusongjin_https://wq.jd.com/cube/front/activePublish/dream_factory_report/380556.html_jing',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'm.jingxi.com',
            'User-Agent': userAgent(),
            'Accept-Language': 'zh-cn'
        }
        r = requests.get(url, headers=headers, timeout=30, verify=False).text
        data = getResult(r)
        ret = data['ret']
        if ret == 0:
            msg(f"【{user}】=>【{suser}】:{data['msg']}  加团成功谢谢你~")
            return False
        elif ret == 10209:
            msg(f"【{user}】=>【{suser}】:{data['msg']} 成功完成开团，谢谢你~")
            return True
        elif ret == 10005:
            print(f"【{user}】=>【{suser}】:{data['msg']}")
            return False
        else:
            # print(f"【{user}】=>【{suser}】:{data['msg']}")
            return False
    except Exception as e:
        print(e)

def start():
    scriptName = '### 京喜工厂-开团 ###'
    print(scriptName)
    global cookiesList, userNameList, pinNameList, ckNum, cashCount, cashCountdict
    cookiesList, userNameList, pinNameList = getCk.iscookie()
    for ckname in jxgc_kaituan:
        try:
            ckNum = userNameList.index(ckname)
        except Exception as e:
            try:
                ckNum = pinNameList.index(unquote(ckname))
            except:
                print(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字可填pt_pin的值、也可以填账号名。")
                continue
        userName = userNameList[ckNum]
        for i in range(3):
            print(f"【{userNameList[ckNum]}】开始第{i+1}次开团")
            tuanId, encryptPin, activeId = CreateTuan(cookiesList[ckNum])
            u = 1
            for i in cookiesList:
                if i == cookiesList[ckNum]:
                    u += 1
                    continue
                if JoinTuan(i, tuanId, encryptPin, activeId, suser=userName, user=userNameList[cookiesList.index(i)]):
                    print("已完成")
                    break
                u += 1
    try:
        if '成功完成开团' in msg_info:
            send(scriptName, msg_info)
    except:
        pass
if __name__ == '__main__':
    start()