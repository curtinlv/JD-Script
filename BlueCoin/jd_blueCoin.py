#!/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: test / jd_blueCoin
Author: Curtin
功能：东东超市商品兑换
Date: 2021/4/17 上午11:22

2021-4-22:
* 支持 Pythonista 3
* 解决开着圈x跑异常，解决控制台输出红字

2021-4-24:
* 时间优化

2021-04-26：
* 增加多线程并发
'''
################【参数】######################
#您的ck格式：pt_key=xxx;pt_pin=xxx; (多账号&分隔)
cookies=''
#【填写您要兑换的商品】
coinToBeans='京豆包'
#轮次
startMaxNum=30
#多线程并发，相当于每秒点击兑换次数...适当调整，手机会发烫
dd_thread=30

#开始抢兑时间
starttime='23:59:59.00000000'
#结束时间
endtime='00:00:30.00000000'

###############################################
import time,datetime
import requests,re
from urllib.parse import quote, unquote
import threading
import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requests.packages.urllib3.disable_warnings()

timestamp=int(round(time.time() * 1000))
script_name='东东超市商品兑换-Python'
title=''
prizeId=''
blueCost=''
inStock=''

today = datetime.datetime.now().strftime('%Y-%m-%d')
tomorrow=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

class TaskThread(threading.Thread):
    """
    处理task相关的线程类
    """
    def __init__(self, func, args=()):
        super(TaskThread, self).__init__()
        self.func = func  # 要执行的task类型
        self.args = args  # 要传入的参数

    def run(self):
        # 线程类实例调用start()方法将执行run()方法,这里定义具体要做的异步任务
        # print("start func {}".format(self.func.__name__))  # 打印task名字　用方法名.__name__
        self.result = self.func(*self.args)  # 将任务执行结果赋值给self.result变量

    def get_result(self):
        # 改方法返回task函数的执行结果,方法名不是非要get_result
        try:
            return self.result
        except Exception as ex:
            print(ex)
            return "ERROR"


def iscookie():
    if 'pt_key=' in cookies and 'pt_pin=' in cookies:
        r = re.compile(r"pt_key=.*?pt_pin=.*?;" ,  re.M | re.S | re.I)
        result = r.findall(cookies)
        if len(result) == 1:
            return result[0]
        elif len(result)>1:
            return result
        else:
            print("cookie 格式错误！...本次操作已退出")
            exit(1)
    else:
        print("cookie 格式错误！...本次操作已退出")
        exit(9)

def setHeaders(cookie):
    try:
        r = re.compile(r"pt_pin=(.*?);")
        userName = r.findall(cookie)
        userName = unquote(userName[0])
    except Exception as e:
        print(e,"cookie格式有误！")
        exit(2)
    headers = {
        'Origin': 'https://jdsupermarket.jd.com',
        'Cookie': cookie,
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://jdsupermarket.jd.com/game/?tt={}'.format(timestamp-314),
        'Host': 'api.m.jd.com',
        'User-Agent': 'jdapp;iPhone;9.4.8;14.3;809409cbd5bb8a0fa8fff41378c1afe91b8075ad;network/wifi;ADID/201EDE7F-5111-49E8-9F0D-CCF9677CD6FE;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone13,4;addressid/2455696156;supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-cn'
    }
    return headers,userName

#查询东东超市蓝币数量
def getBlueCoinInfo(headers):
    try:
        url='https://api.m.jd.com/api?appid=jdsupermarket&functionId=smtg_newHome&clientVersion=8.0.0&client=m&body=%7B%22channel%22:%2218%22%7D&t={0}'.format(timestamp)
        respon = requests.get(url=url, verify=False, headers=headers)
        result = respon.json()
        totalBlue=result['data']['result']['totalBlue']
        shopName=result['data']['result']['shopName']
        return totalBlue,shopName
    except Exception as e:
        print(e)

#查询所有用户蓝币、等级
def getAllUserInfo():
    id_num = 1
    for ck in cookies:
        headers,userName = setHeaders(ck)
        try:
            totalBlue,shopName = getBlueCoinInfo(headers)
            url = 'https://api.m.jd.com/api?appid=jdsupermarket&functionId=smtg_receiveCoin&clientVersion=8.0.0&client=m&body=%7B%22type%22:4,%22channel%22:%2218%22%7D&t={0}'.format(timestamp)
            respon = requests.get(url=url, verify=False,  headers=headers)
            result = respon.json()
            level = result['data']['result']['level']
            print("【用户{4}:{5}】: {0} {3}\n【等级】: {1}\n【蓝币】: {2}万\n------------------".format(shopName, level, totalBlue / 10000,totalBlue, id_num,userName))
        except Exception as e:
            # print(e)
            print(f"账号{id_num}【{userName}】异常请检查ck是否正常~")
        id_num += 1
#查询商品
def smtg_queryPrize(headers, coinToBeans):
    url = 'https://api.m.jd.com/api?appid=jdsupermarket&functionId=smt_queryPrizeAreas&clientVersion=8.0.0&client=m&body=%7B%22channel%22:%2218%22%7D&t={}'.format(timestamp)
    try:
        respone = requests.get(url=url, verify=False, headers=headers)
        result = respone.json()
        allAreas = result['data']['result']['areas']
        for alist in allAreas:
            for x in alist['prizes']:
                if coinToBeans in x['name']:
                    if alist['areaId'] != 6:
                        skuId = x['skuId']
                    else:
                        skuId = 0
                    title = x['name']
                    prizeId = x['prizeId']
                    blueCost = x['cost']
                    status = x['status']
                    return title, prizeId, blueCost, status, skuId
        # print("请检查设置的兑换商品名称是否正确？")
        # return 0, 0, 0, 0, 0
    except Exception as e:
        print(e)


#判断设置的商品是否存在 存在则返回 商品标题、prizeId、蓝币价格、是否有货
def isCoinToBeans(coinToBeans,headers):
    global title, prizeId
    if coinToBeans.strip() != '':
        try:
            title, prizeId, blueCost, inStock, skuId = smtg_queryPrize(headers,coinToBeans)
            return title, prizeId, blueCost, inStock, skuId
        except Exception as e:
            print(e)
            pass
    else:
        print("1.请检查设置的兑换商品名称是否正确?")
#抢兑换
def smtg_obtainPrize(prizeId,headers):
    timestamp = int(round(time.time() * 1000))
    url = 'https://api.m.jd.com/api?appid=jdsupermarket&functionId=smtg_obtainPrize&clientVersion=8.0.0&client=m&body=%7B%22prizeId%22:%22{0}%22,%22channel%22:%221%22%7D&t={1}'.format(prizeId, timestamp)
    try:
        respon = requests.post(url=url, verify=False, headers=headers)
        result=respon.json()
        success=result['data']['success']
        bizMsg = result['data']['bizMsg']
        if success == True:
            print(result)
            print("╰{0}...恭喜兑换成功！".format(bizMsg))
            return 0
        else:
            print(f"\t╰{bizMsg}")
            return 999
    except Exception as e:
        print(e)


def issmtg_obtainPrize(headers,userName,user_num,maxNum):

    try:
        maxNum=int(maxNum)
        title, prizeId, blueCost, inStock, skuId = isCoinToBeans(coinToBeans,headers)
        totalBlue, shopName = getBlueCoinInfo(headers)
        if totalBlue > blueCost:
            qgtime = '{} {}'.format(today, starttime)
            qgendtime = '{} {}'.format(tomorrow, endtime)
            num=1
            nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f8')
            print(f"当前时间[{nowtime}]\n开始时间[{qgtime}]\n正在等待，请勿终止退出...")
            while True:
                nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f8')
                if nowtime > qgtime:
                    print(f"账号{user_num}：{userName} 第{num}次尝试...")
                    t_num = range(dd_thread)
                    threads = []
                    for t in t_num:
                        thread = TaskThread(smtg_obtainPrize, args=(prizeId, headers))
                        threads.append(thread)
                        thread.start()
                    for thread in threads:
                        thread.join()
                        result = thread.get_result()
                        if result == 0:
                            print(f"账号{user_num}：{userName} 成功兑换【{title}】")
                            return 0
                    if nowtime > qgendtime:
                        title, prizeId, blueCost, inStock, skuId = isCoinToBeans(coinToBeans, headers)
                        if inStock == 2:
                            print("\n{1}:【{0}】 当前没货了......".format(title, userName))
                            exit(1)
                    elif num > maxNum:
                        break
                    num += 1

                else:
                    pass

        else:
            print("[{3}]:你的蓝币{0}w不足够兑换【{1}】, 需要{2}w".format(totalBlue/10000,title,blueCost/10000,userName))
    except Exception as e:
        print(e)

def checkUser(cookies): #返回符合条件的ck list
    if isinstance(cookies,list):
        pass
    elif isinstance(cookies,str):
        cookies = [cookies,]
    else:
        print("cookie 类型有误")
        exit(2)
    cookieList=[]
    user_num=1
    for i in cookies:
        headers,userName = setHeaders(i)
        try:
            totalBlue, shopName = getBlueCoinInfo(headers)
            title,prizeId,blueCost,inStock, skuId = isCoinToBeans(coinToBeans,headers)
            totalBlueW = totalBlue / 10000
            if user_num == 1:
                print("您已设置兑换的商品：【{0}】 需要{1}w蓝币".format(title, blueCost / 10000))
                print("********** 首先检测您是否有钱呀 ********** ")
            if totalBlue > blueCost:
                cookieList.append(i)
                print(f"账号{user_num}:【{userName}】蓝币:{totalBlueW}万...yes")
            else:
                print(f"账号{user_num}:【{userName}】蓝币:{totalBlueW}万...no")
        except Exception as e:
            print(f"账号{user_num}:【{userName}】，该用户异常，查不到商品关键词【{coinToBeans}】")
        user_num+=1

    if len(cookieList) >0:
        print("共有{0}个账号符合兑换条件".format(len(cookieList)))
        return cookieList
    else:
        print("共有{0}个账号符合兑换条件...已退出，请继续加油赚够钱再来~".format(len(cookieList)))
        exit(0)

#Start
def start():
    print(f"###### 启动并发线程 【Thread-{dd_thread}】")
    cookies = iscookie()
    cookies = checkUser(cookies)
    run_num=1
    while True:
        print(f"\n【准备开始第{run_num} 轮...】\n")
        user_num=1
        for i in cookies:
            headers,userName = setHeaders(i)
            issmtg_obtainPrize(headers, userName, user_num, maxNum=0)
            user_num+=1
        if run_num > startMaxNum:
            print("已结束")
            break
        run_num+=1

if __name__ == '__main__':
    print("【{}】".format(script_name))
    start()
