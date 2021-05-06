#!/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: test / JD_OpenCard
Author: Curtin
功能：JD入会开卡领取京豆
CreateDate: 2021/5/4 下午1:47
updateTime: 2021/5/6
version: v1.0.2

################################ 【更新记录】################################
环境Python3、兼容ios设备Pythonista 3(已测试正常跑，其他软件自行测试)、
依赖 pip install requests
！！！ 仅以学习为主，请勿商业用途，转载请注明出处，谢谢。

2021.5.4：
    * 支持多账号
    * 限制京豆数量入会，例如只入50豆以上
    * 双线程运行
    * 记录满足条件的shopid 【record= True】默认开启
2021.5.5:
    * 新增记忆功能，如中断后下次跑会接着力跑【memory= True】默认开启
2021.5.6
    * 更改参数配置方式 OpenCardConfig.ini（为了方便后续打包exe）
    * 修复已知Bug

################################ 【用户参数配置说明】################################
编辑文件OpenCardConfig.ini 请保持utf-8 默认格式：
    JD_COOKIE='pt_key=xxx;pt_pin=xxx;' (多账号&分隔)
    openCardBean=30
    xxx=xxx
或
env环境：
    export JD_COOKIE='pt_key=xxx;pt_pin=xxx;' (多账号&分隔)
    export openCardBean=30
    export xxx=xxx
'''
################################ 【定义参数】2021.5.6 更改参数配置方式 以下参数无效 ####################
# #cookie (多账号&分隔)
# cookies='pt_key=xxx;pt_pin=xxx;'
# #只入送豆数量大于此值
# openCardBean = 30
# #限制速度，单位秒，如果请求过快报错适当调整0.5秒以上
# sleepNum=0
# #False|True 是否记录符合条件的shopid，输出文件【OpenCardlog/yes_shopid.txt】
# record = True
# #仅记录，不入会。入会有豆的shopid输出文件【OpenCardlog/all_shopid.txt】,需要record=True且onlyRecord=True才生效。
# onlyRecord = False
# #开启记忆， 需要record=True且 memory= True 才生效。
# memory= True
#
################################ 【Main】################################
import time,os,sys,datetime
import requests
import random,string
import re,json
from urllib.parse import unquote
import threading
import configparser
#定义一些必要参数
requests.packages.urllib3.disable_warnings()
script_name='JD入会领取豆-PyScript'
timestamp=int(round(time.time() * 1000))
today = datetime.datetime.now().strftime('%Y-%m-%d')
pwd = repr(os.getcwd())
pwd = pwd.replace('\'','')
#获取用户参数
try:
    configinfo = configparser.RawConfigParser()
    configinfo.read(pwd + "/OpenCardConfig.ini")
    cookies = configinfo.get('main', 'JD_COOKIE')
    openCardBean = configinfo.getint('main', 'openCardBean')
    sleepNum = configinfo.getfloat('main', 'sleepNum')
    record = configinfo.getboolean('main', 'record')
    onlyRecord = configinfo.getboolean('main', 'onlyRecord')
    memory = configinfo.getboolean('main', 'memory')
except Exception as e:
    OpenCardConfigLabel = 1
    print("参数配置有误，请检查OpenCardConfig.ini\nError:",e)
    print("尝试从Env环境获取！")

#获取系统ENV环境参数优先使用 适合Ac、云服务等环境
# JD_COOKIE=cookie （多账号&分隔）
if "JD_COOKIE" in os.environ:
    cookies = os.environ["JD_COOKIE"]
#只入送豆数量大于此值
if "openCardBean" in os.environ:
    openCardBean = os.environ["openCardBean"]
#限制速度，单位秒，如果请求过快报错适当调整0.5秒以上
if "sleepNum" in os.environ:
    sleepNum = os.environ["sleepNum"]
#是否记录符合条件的shopid，输出文件【OpenCardlog/yes_shopid.txt】 False|True
if "record" in os.environ:
    record = os.environ["record"]
#仅记录，不入会。入会有豆的shopid输出文件【OpenCardlog/all_shopid.txt】,需要record=True且onlyRecord=True才生效。
if "onlyRecord" in os.environ:
    onlyRecord = os.environ["onlyRecord"]
#开启记忆， 需要record=True且 memory= True 才生效
if "memory" in os.environ:
    memory = os.environ["memory"]
#判断参数是否存在
try:
    cookies
    openCardBean
    record
    onlyRecord
    memory
except NameError as e:
    var_exists = False
    print("[OpenCardConfig.ini] 和 [Env环境] 都无法获取到您的参数或缺少，请配置!\nError:",e)
    exit(1)
else:
    var_exists = True

#创建临时目录
if not os.path.exists("./log"):
    os.mkdir("./log")
#记录功能json
memoryJson = {}

################################### Function ################################
#检测cookie格式是否正确
def iscookie():
    cookiesList = []
    if 'pt_key=' in cookies and 'pt_pin=' in cookies:
        r = re.compile(r"pt_key=.*?pt_pin=.*?;" ,  re.M | re.S | re.I)
        result = r.findall(cookies)
        if len(result) == 1:
            cookiesList.append(result[0])
            return cookiesList
        elif len(result)>1:
            return result
        else:
            print("cookie 格式错误！...本次操作已退出")
            exit(1)
    else:
        print("cookie 格式错误！...本次操作已退出")
        exit(9)

#设置Headers
def setHeaders(cookie,intype):
    try:
        r = re.compile(r"pt_pin=(.*?);")
        userName = r.findall(cookie)
        userName = unquote(userName[0])
        if intype == 'mall':
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Host": "shop.m.jd.com",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
                "Accept-Language": "zh-cn",
                "Accept-Encoding": "gzip, deflate, br",
                # "Connection": "keep-alive"
                "Connection": "close"
            }
            return headers, userName
        elif intype == 'JDApp':
            headers = {
                'Cookie': cookie,
                'Accept': "*/*",
                'Connection': "close",
                'Referer': "https://shopmember.m.jd.com/shopcard/?",
                'Accept-Encoding': "gzip, deflate, br",
                'Host': "api.m.jd.com",
                'User-Agent': "jdapp;iPhone;9.4.8;14.3;809409cbd5bb8a0fa8fff41378c1afe91b8075ad;network/wifi;ADID/201EDE7F-5111-49E8-9F0D-CCF9677CD6FE;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone13,4;addressid/;supportBestPay/0;appBuild/167629;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
                'Accept-Language': "zh-cn"
            }
            return headers,userName
        elif intype == 'mh5':
            headers = {
                'Cookie': cookie,
                'Accept': "*/*",
                'Connection': "close",
                'Referer': "https://shopmember.m.jd.com/shopcard/?",
                'Accept-Encoding': "gzip, deflate, br",
                'Host': "api.m.jd.com",
                'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
                'Accept-Language': "zh-cn"

            }
            return headers, userName
    except Exception as e:
        print(e,"cookie格式有误！")
        exit(2)



#记录符合件的shopid到本地文件保存 当前目录：OpenCardlog/shopid-yyyy-mm-dd.txt 或 log-yyyy-mm-dd.txt
def outfile(filename,context,iscover):
    """
    :param filename: 文件名 默认txt格式
    :param context: 写入内容
    :param iscover: 是否覆盖 False or True
    :return:
    """
    if record == True:
        try:
            if iscover == False:
                with open(pwd + "/log/{0}".format(filename),"a+" ,encoding="utf-8") as f1:
                    f1.write("{}\n".format(context))
            elif iscover == True:
                with open(pwd + "/log/{0}".format(filename),"w+" ,encoding="utf-8") as f1:
                    f1.write("{}".format(context))
        except Exception as e:
            print(e)

#记忆功能 默认双线程
def memoryFun(userName,startNum,threadNum):
    global memoryJson
    if memory == True:
        memoryJson['userName'] = userName
        memoryJson['allShopidNum'] = vip_info_all
        memoryJson['t{}_startNum'.format(threadNum)] = startNum
        try:
            if os.path.exists(pwd + "/log"):
                with open(pwd + "/log/memory.json", "w", encoding="utf-8") as f:
                    json.dump(memoryJson, f, indent=4)
            else:
                pass
        except Exception as e:
            print(e)
#获取记忆配置
def getMemory():
    """
    :return: memoryJson
    """
    if os.path.exists(pwd + "/log/memory.json"):
        with open(pwd +"/log/memory.json","r",encoding="utf-8") as f:
            memoryJson = json.load(f)
            if len(memoryJson) > 0:
                return memoryJson
    else:
        pass

#获取VenderId
def getVenderId(shopId,headers):
   """
   :param shopId:
   :param headers
   :return: venderId
   """
   url = 'https://shop.m.jd.com/?shopId={0}'.format(shopId)
   resp = requests.get(url=url,verify=False, headers=headers , timeout=30)
   resulttext=resp.text
   r = re.compile(r'venderId: \'(\d+)\'')
   venderId = r.findall(resulttext)
   return venderId[0]

#查询礼包
def getShopOpenCardInfo(venderId,headers,shopid,userName):
    """
    :param venderId:
    :param headers:
    :return: activityId,getBean
    """
    #新增记忆
    num1 = string.digits
    v_num1 = ''.join(random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 1)) + ''.join(
        random.sample(num1, 4))
    url='https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body=%7B%22venderId%22%3A%22{2}%22%2C%22channel%22%3A406%7D&client=H5&clientVersion=9.2.0&uuid=&jsonp=jsonp_{0}_{1}'.format(timestamp,v_num1,venderId)
    resp = requests.get(url=url,verify=False, headers=headers , timeout=30)
    time.sleep(sleepNum)
    resulttxt = resp.text
    r = re.compile(r'jsonp_.*?\((.*?)\)\;', re.M | re.S | re.I)
    result = r.findall(resulttxt)
    cardInfo=json.loads(result[0])
    venderCardName =  cardInfo['result']['shopMemberCardInfo']['venderCardName'] # 店铺名称
    print(f"\t╰查询入会礼包【{venderCardName}】{shopid}")
    openCardStatus = cardInfo['result']['userInfo']['openCardStatus'] # 是否会员
    interestsRuleList = cardInfo['result']['interestsRuleList']
    if interestsRuleList == None:
        print("\t\t╰Oh,该店礼包已被领光了~")
        return 0,openCardStatus
    try:
        if len(interestsRuleList) > 0:
            for i in interestsRuleList:
                if "京豆" in i['prizeName']:
                    getBean = int(i['discountString'])
                    activityId = i['interestsInfo']['activityId']
                    context = "{0} {1}豆 {2}".format(shopid, getBean,venderCardName)
                    outfile("all_shopid.txt", context,False)
                    if getBean >= openCardBean:
                        print(f"\t\t╰入会赠送【{getBean}豆】，可入会")
                        if onlyRecord == True:
                            print("已开启仅记录，不入会。")
                            return 0, openCardStatus
                        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        context = "{0}:shopid:{1},店铺:{2},京豆:{3}".format(nowtime,shopid, venderCardName, getBean)
                        outfile("log.txt",context,False)
                        context = "{0}".format(shopid)
                        outfile("{}_yes_shopid.txt".format(userName),context,False)
                        if openCardStatus == 1:
                            url='https://shopmember.m.jd.com/member/memberCloseAccount?venderId={}'.format(venderId)
                            print("\t\t╰您已经是本店会员，请注销会员卡后再来运行~\n注销链接:{}".format(url))
                            context = "{0}:入会{1}豆:注销链接：{2}".format(venderCardName, getBean, url)
                            outfile("可注销会员卡用户【{0}】.txt".format(userName),context,False)
                            return 0, openCardStatus
                        return activityId,getBean
                    else:
                        print(f'\t\t╰入会赠送【{getBean}豆】少于【{openCardBean}豆】，不入会，跳过...')
                        if onlyRecord == True:
                            print("已开启仅记录，不入会。")
                            return 0, openCardStatus
                        return 0,openCardStatus
                else:
                    pass
                print("\t\t╰Oh~ 该店入会京豆已被领光了")
                return 0,openCardStatus

    except Exception as e:
        print(e)


#开卡
def bindWithVender(venderId,shopId,activityId,channel,headers):
    """

    :param venderId:
    :param shopId:
    :param activityId:
    :param channel:
    :param headers:
    :return: result : 开卡结果
    """
    num = string.ascii_letters + string.digits
    v_name = ''.join(random.sample(num, 10))
    num1 = string.digits
    v_num1 = ''.join(random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 1)) + ''.join(random.sample(num1, 4))
    qq_num = ''.join(random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 1)) + ''.join(random.sample(num1, 8)) + "@qq.com"
    url = 'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{4}%22%2C%22shopId%22%3A%22{7}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%22v_sex%22%3A%22%E6%9C%AA%E7%9F%A5%22%2C%22v_name%22%3A%22{0}%22%2C%22v_birthday%22%3A%221990-03-18%22%2C%22v_email%22%3A%22{6}%22%7D%2C%22writeChildFlag%22%3A0%2C%22activityId%22%3A{5}%2C%22channel%22%3A{3}%7D&client=H5&clientVersion=9.2.0&uuid=&jsonp=jsonp_{1}_{2}'.format(v_name, timestamp, v_num1, channel, venderId, activityId,qq_num,shopId)
    try:
        respon = requests.get(url=url,verify=False, headers=headers , timeout=30)
        result = respon.text
        return result
    except Exception as e:
        print(e)


#获取开卡结果
def getResult(resulttxt):
    r = re.compile(r'jsonp_.*?\((.*?)\)\;', re.M | re.S | re.I)
    result = r.findall(resulttxt)
    for i in result:
        result_data = json.loads(i)
        busiCode = result_data['busiCode']
        if busiCode == '0':
            message = result_data['message']
            try:
                result = result_data['result']['giftInfo']['giftList']
                print(f"\t\t╰{message}")
                for i in result:
                    print("\t\t\t╰{0}:{1} ".format(i['prizeTypeName'],i['discount']))
            except:
                print(f'\t\t╰{message}')
            return busiCode
        else:
            print("\t\t╰{}".format(result_data['message']))
            return busiCode
#读取shopid.txt
def getShopID():
    shopid_path = os.path.join(os.path.split(sys.argv[0])[0], "shopid.txt")
    try:
        with open(shopid_path , "r", encoding="utf-8" ) as f:
            shopid = f.read()
            if len(shopid) >0:
                shopid = shopid.split("\n")
                return shopid
            else:
                print("Error:请检查shopid.txt文件是否正常！\n")
                exit(9)
    except Exception as e:
        print("Error:请检查shopid.txt文件是否正常！\n",e)
        exit(9)

#进度条
def progress_bar(start,end):
    print("\r", end="")
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("### {1}【当前进度: {0}%】".format(round(start/end*100,2),nowtime))
    sys.stdout.flush()

#子线程
def threadfor(user_num,ck,vip_info,start,stop,thread_num):
    getAllbeanCount = 0
    headers_a, userName = setHeaders(ck, "mh5")
    if thread_num == 1:
        print(f"用户{user_num}：【{userName}】")
    for i in range(start,stop):
        try:
            headers_b, userName = setHeaders(ck, "mall")
            if len(vip_info[i]) > 0:
                venderId = getVenderId(vip_info[i], headers_b)
                time.sleep(sleepNum)
                #新增记忆功能
                memoryFun(userName,i,thread_num)
                activityId, getBean = getShopOpenCardInfo(venderId, headers_a,vip_info[i],userName)
                time.sleep(sleepNum)
                if activityId != 0:
                    headers, userName = setHeaders(ck, "JDApp")
                    result = bindWithVender(venderId, vip_info[i], activityId, 208, headers)
                    busiCode = getResult(result)
                    if busiCode == '0':
                        getAllbeanCount += getBean
                        print(f"累计获得：{getAllbeanCount} 京豆")
                        if thread_num == 1:
                            progress_bar(i, stop)
                        time.sleep(sleepNum)
                if i % 20 == 0 and thread_num == 1 and i != 0:
                    progress_bar(i, stop)
        except Exception as e:
            # pass
            print(e)
    if thread_num == 1:
        time.sleep(1)
        print(f"用户{user_num}：【{userName}】，本次总累计获得：{getAllbeanCount} 京豆")
        progress_bar(stop, stop)

#start
def start():
    global vip_info_all
    print(f"【{script_name} by Curtin】")
    vip_info = getShopID()
    vip_info_all = len(vip_info)
    vip_info_mid = int(vip_info_all / 2)
    print("获取到店铺数量", vip_info_all)
    print(f"您已设置入会条件：{openCardBean} 京豆")
    user_num = 1
    cookies = iscookie()
    print("共{}个账号".format(len(cookies)))
    memorylabel=0
    for ck in cookies:
        startNum1 = 0
        startNum2 = vip_info_mid
        headers_a, userName = setHeaders(ck, "mh5")
        #如果启用记忆功能，则获取上一次记忆位置
        if memory == True and memorylabel == 0:
            try:
                memoryJson = getMemory()
                if memoryJson['allShopidNum'] == vip_info_all:
                    if memoryJson['userName'] == userName:
                        memorylabel = 1
                        if memoryJson['t1_startNum']:
                            startNum1=memoryJson['t1_startNum']
                            print(f"已启用记忆功能 memory= True，用户{userName},线程1从【{startNum1}】个店铺开始")
                        if memoryJson['t2_startNum']:
                            startNum2=memoryJson['t2_startNum']
                            print(f"已启用记忆功能 memory= True，用户{userName},线程2从【{startNum2}】个店铺开始")
                        if memoryJson['t1_startNum']+1 == vip_info_mid and memoryJson['t2_startNum']+1 == vip_info_all:
                            print(f"\n账号【{userName}】上次已完成所有shopid，请输入\n0 : 跳过,继续跑下一个账号\n1 : 重新跑一次\n\n 【Ps:或到作者GitHub获取新的shopid.txt】\n")
                            try:
                                getmemoryNum=int(input("正在等待您的选择："))
                                if getmemoryNum == 1:
                                    print("那就重新跑一次~")
                                    startNum1 = 0
                                    startNum2 = vip_info_mid
                                elif getmemoryNum == 0:
                                    print("继续跑下一个账号~")
                                    if len(cookies) == 1:
                                        print("您只配置了一个账号~ 程序已退出...")
                                    return 1
                            except:
                                print("您的输入有误！默认跳过继续跑下一个账号")
                                continue
                    else:
                        print(f"已启用记忆功能 memory= True，跳过用户{userName}，为多账号准备。")
                        user_num += 1
                        continue
                else:
                    print("检测到shopid.txt文件有更新，本次记忆功能不生效。")
                    memorylabel = 1
            except Exception as e:
                memorylabel = 1
        starttime = time.perf_counter() #记录时间开始
        # 多线程部分
        if vip_info_all > 1:
            threads = []
            t1 = threading.Thread(target=threadfor, args=(user_num, ck, vip_info, startNum1, vip_info_mid,1))
            threads.append(t1)
            t2 = threading.Thread(target=threadfor, args=(user_num, ck, vip_info, startNum2, vip_info_all,2))
            threads.append(t2)

            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()
        elif vip_info_all == 1:
            threadfor(user_num,ck,vip_info,0,vip_info_all,3)
        else:
            print("获取到shopid数量为0")
            exit(8)

        endtime = time.perf_counter()  # 记录时间结束
        time.sleep(3)
        print("--- 入会总耗时 : %.03f 秒 seconds ---" % (endtime - starttime))
        outfile("log.txt","--- 入会总耗时 : %.03f 秒 seconds ---" % (endtime - starttime),False)
        user_num += 1
    if os.path.exists(pwd +"/log/memory.json"):
        print("\n已跑完所有账号，清除记忆缓存")
        os.remove(pwd + "/log/memory.json")
if __name__ == '__main__':
    start()
