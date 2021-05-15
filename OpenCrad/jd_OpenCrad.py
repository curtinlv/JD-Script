#!/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD_OpenCard
Author: Curtin
功能：JD入会开卡领取京豆
CreateDate: 2021/5/4 下午1:47
UpdateTime: 2021/5/15
'''
version = 'v1.0.5'
readmes = """
# JD入会领豆 - 轻松日撸千豆
##  目录结构
    JD-Script/                  #仓库
    |-- LICENSE
    |-- OpenCrad                # 主目录
    |   |-- jd_OpenCrad.py      # 主代码 （必要）
    |   |-- log                 # 临时目录（可删除）
    |   |-- OpenCardConfig.ini  # 只配置文件（必要）
    |   |-- Readme.md           # 说明
    |   `-- shopid.txt          # shopid存放文件
    `-- README.md

### `【兼容环境】`
    1.Python3.3+ 环境
    2.兼容ios设备软件：Pythonista 3(已测试正常跑，其他软件自行测试)   
    3.Windows exe 

    安装依赖模块 :
    pip3 install requests
    执行：
    python jd_OpenCrad.py
## `【更新记录】`
    2021.5.15：(v1.0.5)
        * 新增远程获取shopid功能
            - isRemoteSid=yes #开启
        * 修改已知Bug
    
    2021.5.9：(v1.0.4 Beta)
        * 优化代码逻辑
        * 打包exe版本测试
    
    2021.5.8：(v1.0.3)
        * 优化记忆功能逻辑：
            - cookiek个数检测
            - shopid个数检测
            - 上一次中断最后记录的用户id检测不存在本次ck里面
            - 临时文件log/memory.json是否存在
            - 以上任意一条命中则记忆接力功能不生效。

    2021.5.7：(v1.0.2)
        * 优化代码逻辑
        * 修复已知Bug

    2021.5.5：(v1.0.1)
        * 新增记忆功能，如中断后下次跑会接着力跑（默认开启）
            - memory= True
        * 新增仅记录shopid，不入会功能（默认关闭）
            - onlyRecord = no
        * 修复已知Bug

    2021.5.4：(v1.0.0)
        * 支持多账号
            - JD_COOKIE=pt_key=xxx;pt_pin=xxx;&pt_key=xxx;pt_pin=xxx; #多账号&分隔
        * 限制京豆数量入会，例如只入50豆以上
            - openCardBean = 50
        * 双线程运行
            - 默认开启，且您没得选择。
        * 记录满足条件的shopid 【record= True】默认开启 （./log 目录可删除）
            - log/可销卡汇总.txt #记录开卡送豆的店铺销卡链接
            - log/shopid-yyyy-mm-dd.txt #记录当天所有入会送豆的shopid
            - log/可销卡用户xxx.txt #记录用户可销卡的店铺

### `【用户参数配置说明】`
### 主配置文件[ OpenCardConfig.ini ] 请保持utf-8默认格式

 变量  | 值  | 说明
 ---- | ----- | ------  
 JD_COOKIE  | pt_key=xxx;pt_pin=xxx;  | 必要(多账号&分隔) 
 openCardBean  | 30 | int，入会送豆满足此值，否则不入会 
 record    | yes或no | 布尔值，是否记录符合条件的shopid(默认yes) 
 onlyRecord  | yes或no |布尔值， yes:仅记录，不入会(默认no) 
 memory  | yes或no | 布尔值，开启记忆功能，接力上一次异常中断位置继续。(默认yes) 
 printlog  | yes或no | 布尔值，yes：只打印部分日志 no:打印所有日志 
 sleepNum  | yes或no | Float，限制速度，单位秒，如果请求过快报错适当调整0.5秒以上 
 isRemoteSid  | yes或no | 布尔值，yes:使用作者远程仓库更新的id，no：使用本地shopid.txt的id 
#### $\color{red}{兼容Env环境（如有配置则优先使用，适合AC、云服务环境等）}$    
        export JD_COOKIE='pt_key=xxx;pt_pin=xxx;' (多账号&分隔)
        export openCardBean=30
        export xxx=xxx

#### Ps:您可以到以下途径获取最新的shopid.txt，定期更新：

###### [GitHub仓库](https://github.com/curtinlv/JD-Script) 
###### [Gitee仓库](https://gitee.com/curtinlv/JD-Script)
###### [TG频道](https://t.me/TopStyle2021)
###### 关注公众号【TopStyle】回复：shopid
![TopStyle](https://gitee.com/curtinlv/img/raw/master/gzhcode.jpg)
# 
    @Last Version: %s

    @Last Time: 2021-05-15

    @Author: Curtin
#### **仅以学习交流为主，请勿商业用途、禁止违反国家法律 ，转载请留个名字，谢谢!** 

# End.
[回到顶部](#readme)
""" % version

################################ 【Main】################################
import time, os, sys, datetime
import requests
import random, string
import re, json,base64
from urllib.parse import unquote
from threading import Thread
from configparser import RawConfigParser

# 定义一些要用到参数
requests.packages.urllib3.disable_warnings()
scriptHeader = """
════════════════════════════════════════
║                                      ║
║     JD入会领豆 - 轻松日撸千豆        ║
║                                      ║
════════════════════════════════════════
@Version: {}""".format(version)
remarks = 'Ps:您可以到以下途径获取最新的shopid.txt，定期更新：\n\n\tGitHub:https://github.com/curtinlv/JD-Script\n\n\tTG频道:https://t.me/TopStyle2021\n\n\t关注公众号【TopStyle】回复：shopid\n\n\n\t\t\t--By Curtin\n'

timestamp = int(round(time.time() * 1000))
today = datetime.datetime.now().strftime('%Y-%m-%d')

pwd = repr(os.getcwd())
pwd = pwd.replace('\'', '')
# 获取用户参数
try:
    configinfo = RawConfigParser()
    try:
        configinfo.read(pwd + "/OpenCardConfig.ini", encoding="UTF-8")
    except Exception as e:
        with open(pwd + "/OpenCardConfig.ini","r",encoding="UTF-8") as config:
            getConfig = config.read().encode('utf-8').decode('utf-8-sig')
        with open(pwd + "/OpenCardConfig.ini","w",encoding="UTF-8") as config:
            config.write(getConfig)
        try:
            configinfo.read(pwd + "/OpenCardConfig.ini", encoding="UTF-8")
        except:
            configinfo.read(pwd + "/OpenCardConfig.ini", encoding="gbk")
    cookies = configinfo.get('main', 'JD_COOKIE')
    openCardBean = configinfo.getint('main', 'openCardBean')
    sleepNum = configinfo.getfloat('main', 'sleepNum')
    record = configinfo.getboolean('main', 'record')
    onlyRecord = configinfo.getboolean('main', 'onlyRecord')
    memory = configinfo.getboolean('main', 'memory')
    printlog = configinfo.getboolean('main', 'printlog')
    isRemoteSid = configinfo.getboolean('main', 'isRemoteSid')
except Exception as e:
    OpenCardConfigLabel = 1
    print("参数配置有误，请检查OpenCardConfig.ini\nError:", e)
    print("尝试从Env环境获取！")

# 获取系统ENV环境参数优先使用 适合Ac、云服务等环境
# JD_COOKIE=cookie （多账号&分隔）
if "JD_COOKIE" in os.environ:
    cookies = os.environ["JD_COOKIE"]
# 只入送豆数量大于此值
if "openCardBean" in os.environ:
    openCardBean = os.environ["openCardBean"]
# 限制速度，单位秒，如果请求过快报错适当调整0.5秒以上
if "sleepNum" in os.environ:
    sleepNum = os.environ["sleepNum"]
# 是否记录符合条件的shopid，输出文件【OpenCardlog/yes_shopid.txt】 False|True
if "record" in os.environ:
    record = os.environ["record"]
# 仅记录，不入会。入会有豆的shopid输出文件【OpenCardlog/all_shopid.txt】,需要record=True且onlyRecord=True才生效。
if "onlyRecord" in os.environ:
    onlyRecord = os.environ["onlyRecord"]
# 开启记忆， 需要record=True且 memory= True 才生效
if "memory" in os.environ:
    memory = os.environ["memory"]
# 判断参数是否存在
try:
    cookies
    openCardBean
    record
    onlyRecord
    memory
    printlog
    isRemoteSid
except NameError as e:
    var_exists = False
    print("[OpenCardConfig.ini] 和 [Env环境] 都无法获取到您的参数或缺少，请配置!\nError:", e)
    time.sleep(60)
    exit(1)
else:
    var_exists = True

# 创建临时目录
if not os.path.exists("./log"):
    os.mkdir("./log")
# 记录功能json
memoryJson = {}


################################### Function ################################

def nowtime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def printinfo(context, label: bool):
    if label == False:
        print(context)


def exitCodeFun(code):
    try:
        exitCode = input()
        print(exitCode)
        exit(code)
    except:
        time.sleep(3)
        exit(code)


# 检测cookie格式是否正确
def iscookie():
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
            for i in result:
                r = re.compile(r"pt_pin=(.*?);")
                pinName = r.findall(i)
                pinName = unquote(pinName[0])
                # 获取用户名
                ck, nickname = getUserInfo(i, pinName)
                if nickname != False:
                    cookiesList.append(ck)
                    userNameList.append(nickname)
                    pinNameList.append(pinName)
                else:
                    continue
            if len(cookiesList) > 0 and len(userNameList) > 0:
                return cookiesList, userNameList, pinNameList
            else:
                print("没有可用Cookie，已退出")
                exitCodeFun(3)
        else:
            print("cookie 格式错误！...本次操作已退出")
            exitCodeFun(4)
    else:
        print("cookie 格式错误！...本次操作已退出")
        exitCodeFun(4)

# 检查是否有更新版本

def gettext(url):
    try:
        resp = requests.get(url,timeout=60).text
        if '该内容无法显示' in resp:
            gettext(url)
        return resp
    except Exception as e:
        print(e)

def isUpdate():
    url = base64.decodebytes(
        b"aHR0cHM6Ly9naXRlZS5jb20vY3VydGlubHYvUHVibGljL3Jhdy9tYXN0ZXIvT3BlbkNyYWQvdXBkYXRlLmpzb24=")
    try:
        result = gettext(url)
        result = json.loads(result)
        isEnable = result['isEnable']
        uPversion = result['version']
        info = result['info']
        readme1 = result['readme1']
        readme2 = result['readme2']
        readme3 = result['readme3']
        if isEnable > 50 and isEnable < 150:
            if version != uPversion:
                print(f"\n{info}，\n\n当前最新版本：【{uPversion}】\n")
                print(f"{readme1}{readme2}{readme3}")
                time.sleep(300)
                exit(666)
            else:
                print(f"\n{readme1}{readme2}{readme3}")
        else:
            print(readme1)
            print("!!! 无法使用，请联系作者。CurtinLV")
            time.sleep(300)
            exit(666)

    except:
        print("请检查您的环境是否正常！")
        time.sleep(10)
        exit(666)

def getUserInfo(ck, pinName):
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
        print(f"用户【{pinName}】Cookie 已失效！请重新获取。")
        return ck, False


# 设置Headers
def setHeaders(cookie, intype):
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
        return headers
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
        return headers
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
        return headers


# 记录符合件的shopid到本地文件保存 当前目录：OpenCardlog/shopid-yyyy-mm-dd.txt 或 log-yyyy-mm-dd.txt
def outfile(filename, context, iscover):
    """
    :param filename: 文件名 默认txt格式
    :param context: 写入内容
    :param iscover: 是否覆盖 False or True
    :return:
    """
    if record == True:
        try:
            if iscover == False:
                with open(pwd + "/log/{0}".format(filename), "a+", encoding="utf-8") as f1:
                    f1.write("{}\n".format(context))
            elif iscover == True:
                with open(pwd + "/{0}".format(filename), "w+", encoding="utf-8") as f1:
                    f1.write("{}".format(context))
        except Exception as e:
            print(e)


# 记忆功能 默认双线程
def memoryFun(startNum, threadNum, usernameLabel, username, getallbean, userCount):
    global memoryJson
    if memory == True:
        if usernameLabel == True:
            memoryJson['allShopidNum'] = endShopidNum
            memoryJson['currUser{}'.format(threadNum)] = username
            memoryJson['t{}_startNum'.format(threadNum)] = startNum
            memoryJson['allUserCount'] = userCount
        elif usernameLabel == False:
            try:
                memoryJson['{}'.format(username)]
                memoryJson['{}'.format(username)] += getallbean
            except:
                memoryJson['{}'.format(username)] = getallbean

        else:
            pass
        try:
            if os.path.exists(pwd + "/log"):
                with open(pwd + "/log/memory.json", "w", encoding="utf-8") as f:
                    json.dump(memoryJson, f, indent=4)
            else:
                pass
        except Exception as e:
            print(e)


# 获取记忆配置
def getMemory():
    """
    :return: memoryJson
    """
    if os.path.exists(pwd + "/log/memory.json"):
        with open(pwd + "/log/memory.json", "r", encoding="utf-8") as f:
            memoryJson = json.load(f)
            if len(memoryJson) > 0:
                return memoryJson
    else:
        pass

def rmCount():
    if os.path.exists(pwd + "/log/入会汇总.txt"):
        os.remove(pwd + "/log/入会汇总.txt")

# 判断是否启用记忆功能
def isMemory(memorylabel, startNum1, startNum2, midNum, endNum, pinNameList):
    """
    :param memorylabel: 记忆标签
    :param startNum1: 线程1默认开始位置
    :param startNum2: 线程2默认开始位置
    :param midNum:  线程1默认结束位置
    :param endNum: 线程2默认结束位置
    :return: startNum1, startNum2, memorylabel
    """
    if memory == True and memorylabel == 0:
        try:
            memoryJson = getMemory()
            if memoryJson['allShopidNum'] == endNum:
                currUserLabel = 0

                if memoryJson['allUserCount'] == allUserCount:
                    for u in pinNameList:
                        if memoryJson['currUser1'] == u:
                            currUserLabel += 1
                        elif memoryJson['currUser2'] == u:
                            currUserLabel += 1
                    if currUserLabel > 1:
                        print("通知：检测到您配置的CK有变更，本次记忆功能不生效。")
                        rmCount()
                        return startNum1, startNum2, memorylabel
                    if memoryJson['t1_startNum'] + 1 == midNum and memoryJson['t2_startNum'] + 1 == endNum:
                        print(
                            f"\n上次已完成所有shopid，\n\nPs:您可以关注公众号或TG频道获取最新shopid。\n公众号: TopStyle\n电报TG:https://t.me/TopStyle2021\n\n请输入 0 或 1\n0 : 退出。\n1 : 重新跑一次，以防有漏")
                        try:
                            getyourNum = int(input("正在等待您的选择："))
                            if getyourNum == 1:
                                print("Ok,那就重新跑一次~")
                                rmCount()
                                memorylabel = 1
                                return startNum1, startNum2, memorylabel
                            elif getyourNum == 0:
                                print("Ok,已退出~")
                                time.sleep(10)
                                exit(0)
                        except:
                            # print("Error: 您的输入有误！已退出。")
                            exitCodeFun(3)
                    else:
                        if memoryJson['t1_startNum']:
                            startNum1 = memoryJson['t1_startNum']
                            print(f"已启用记忆功能 memory= True，线程1从第【{startNum1}】店铺开始")
                        if memoryJson['t2_startNum']:
                            startNum2 = memoryJson['t2_startNum']
                            print(f"已启用记忆功能 memory= True，线程2从第【{startNum2}】店铺开始")
                        memorylabel = 1
                        return startNum1, startNum2, memorylabel
                else:
                    print("通知：检测到您配置的CK有变更，本次记忆功能不生效。")
                    rmCount()
                    return startNum1, startNum2, memorylabel
            else:
                print("通知：检测到shopid有更新，本次记忆功能不生效。")
                rmCount()
                memorylabel = 1
                return startNum1, startNum2, memorylabel
        except Exception as e:
            memorylabel = 1
            return startNum1, startNum2, memorylabel


# 获取VenderId
def getVenderId(shopId, headers):
    """
    :param shopId:
    :param headers
    :return: venderId
    """
    url = 'https://shop.m.jd.com/?shopId={0}'.format(shopId)
    resp = requests.get(url=url, verify=False, headers=headers, timeout=60)
    resulttext = resp.text
    r = re.compile(r'venderId: \'(\d+)\'')
    venderId = r.findall(resulttext)
    return venderId[0]


# 查询礼包
def getShopOpenCardInfo(venderId, headers, shopid, userName):
    """
    :param venderId:
    :param headers:
    :return: activityId,getBean 或 返回 0:没豆 1:有豆已是会员 2:记录模式（不入会）
    """
    num1 = string.digits
    v_num1 = ''.join(random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 1)) + ''.join(
        random.sample(num1, 4))  # 随机生成一窜4位数字
    url = 'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body=%7B%22venderId%22%3A%22{2}%22%2C%22channel%22%3A406%7D&client=H5&clientVersion=9.2.0&uuid=&jsonp=jsonp_{0}_{1}'.format(
        timestamp, v_num1, venderId)
    resp = requests.get(url=url, verify=False, headers=headers, timeout=60)
    time.sleep(sleepNum)
    resulttxt = resp.text
    r = re.compile(r'jsonp_.*?\((.*?)\)\;', re.M | re.S | re.I)
    result = r.findall(resulttxt)
    cardInfo = json.loads(result[0])
    venderCardName = cardInfo['result']['shopMemberCardInfo']['venderCardName']  # 店铺名称
    printinfo(f"\t╰查询入会礼包【{venderCardName}】{shopid}", printlog)
    openCardStatus = cardInfo['result']['userInfo']['openCardStatus']  # 是否会员
    interestsRuleList = cardInfo['result']['interestsRuleList']
    if interestsRuleList == None:
        printinfo("\t\t╰Oh,该店礼包已被领光了~", printlog)
        return 0, 0
    try:
        if len(interestsRuleList) > 0:
            for i in interestsRuleList:
                if "京豆" in i['prizeName']:
                    getBean = int(i['discountString'])
                    activityId = i['interestsInfo']['activityId']
                    context = "{0}".format(shopid)
                    outfile(f"shopid-{today}.txt", context, False)  # 记录所有送豆的shopid
                    in_url='https://shop.m.jd.com/?shopId={}'.format(shopid)
                    url = 'https://shopmember.m.jd.com/member/memberCloseAccount?venderId={}'.format(venderId)
                    context = "[{0}]:入会{2}豆店铺【{1}】\n\t加入会员:{4}\n\t解绑会员:{3}".format(nowtime(), venderCardName, getBean, url,in_url)  # 记录
                    outfile("入会汇总.txt", context, False)
                    if getBean >= openCardBean:  # 判断豆是否符合您的需求
                        print(f"\t╰{venderCardName}:入会赠送【{getBean}豆】，可入会")
                        context = "{0}".format(shopid)
                        outfile(f"入会{openCardBean}豆以上的shopid-{today}.txt", context, False)
                        if onlyRecord == True:
                            print("已开启仅记录，不入会。")
                            return 2, 2
                        if openCardStatus == 1:
                            url = 'https://shopmember.m.jd.com/member/memberCloseAccount?venderId={}'.format(venderId)
                            print("\t\t╰[账号：{0}]:您已经是本店会员，请注销会员卡24小时后再来~\n注销链接:{1}".format(userName, url))
                            context = "[{3}]:入会{1}豆，{0}销卡：{2}".format(venderCardName, getBean, url, nowtime())
                            outfile("可退会账号【{0}】.txt".format(userName), context, False)
                            return 1, 1
                        return activityId, getBean
                    else:
                        print(f'\t\t╰{venderCardName}:入会送【{getBean}】豆少于【{openCardBean}豆】,不入...')
                        if onlyRecord == True:
                            print("已开启仅记录，不入会。")
                            return 2, 2
                        return 0, openCardStatus

                else:
                    pass
            printinfo("\t\t╰Oh~ 该店入会京豆已被领光了", printlog)
            return 0, 0
        else:
            return 0, 0
    except Exception as e:
        print(e)


# 开卡
def bindWithVender(venderId, shopId, activityId, channel, headers):
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
    qq_num = ''.join(random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 1)) + ''.join(
        random.sample(num1, 8)) + "@qq.com"
    url = 'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=bindWithVender&body=%7B%22venderId%22%3A%22{4}%22%2C%22shopId%22%3A%22{7}%22%2C%22bindByVerifyCodeFlag%22%3A1%2C%22registerExtend%22%3A%7B%22v_sex%22%3A%22%E6%9C%AA%E7%9F%A5%22%2C%22v_name%22%3A%22{0}%22%2C%22v_birthday%22%3A%221990-03-18%22%2C%22v_email%22%3A%22{6}%22%7D%2C%22writeChildFlag%22%3A0%2C%22activityId%22%3A{5}%2C%22channel%22%3A{3}%7D&client=H5&clientVersion=9.2.0&uuid=&jsonp=jsonp_{1}_{2}'.format(
        v_name, timestamp, v_num1, channel, venderId, activityId, qq_num, shopId)
    try:
        respon = requests.get(url=url, verify=False, headers=headers, timeout=60)
        result = respon.text
        return result
    except Exception as e:
        print(e)


# 获取开卡结果
def getResult(resulttxt, userName, user_num):
    r = re.compile(r'jsonp_.*?\((.*?)\)\;', re.M | re.S | re.I)
    result = r.findall(resulttxt)
    for i in result:
        result_data = json.loads(i)
        busiCode = result_data['busiCode']
        if busiCode == '0':
            message = result_data['message']
            try:
                result = result_data['result']['giftInfo']['giftList']
                print(f"\t\t╰用户{user_num}【{userName}】:{message}")
                for i in result:
                    print("\t\t\t╰{0}:{1} ".format(i['prizeTypeName'], i['discount']))
            except:
                print(f'\t\t╰用户{user_num}【{userName}】:{message}')
            return busiCode
        else:
            print("\t\t╰用户{0}【{1}】:{2}".format(user_num, userName, result_data['message']))
            return busiCode


def getRemoteShopid():
    url = base64.decodebytes(
        b"aHR0cHM6Ly9naXRlZS5jb20vY3VydGlubHYvUHVibGljL3Jhdy9tYXN0ZXIvT3BlbkNyYWQvc2hvcGlkLnR4dA==")
    try:
        rShopid= gettext(url)
        rShopid=rShopid.split("\n")
        return rShopid
    except:
        print("无法从远程获取shopid")
        exitCodeFun(999)

# 读取shopid.txt
def getShopID():

    shopid_path = os.path.join(os.path.split(sys.argv[0])[0], "shopid.txt")
    try:
        with open(shopid_path, "r", encoding="utf-8") as f:
            shopid = f.read()
            if len(shopid) > 0:
                shopid = shopid.split("\n")
                return shopid
            else:
                print("Error:请检查shopid.txt文件是否正常！\n")
                exitCodeFun(2)
    except Exception as e:
        print("Error:请检查shopid.txt文件是否正常！\n", e)
        exitCodeFun(2)

# 进度条
def progress_bar(start, end, threadNum):
    print("\r", end="")
    if threadNum == 2:
        start2 = start - midNum
        end2 = end - midNum
        print("\n###[{1}]:线程{2}【当前进度: {0}%】\n".format(round(start2 / end2 * 100, 2), nowtime(), threadNum))
    elif threadNum == 1:
        print("\n###[{1}]:线程{2}【当前进度: {0}%】\n".format(round(start / end * 100, 2), nowtime(), threadNum))
    sys.stdout.flush()


# 为多线程准备
def OpenVipCrad(startNum: int, endNum: int, shopids, cookies, userNames, pinNameList, threadNum):
    for i in range(startNum, endNum):
        user_num = 1
        activityIdLabel = 0
        for ck, userName, pinName in zip(cookies, userNames, pinNameList):
            if i % 10 == 0 and i != 0:
                progress_bar(i, endNum, threadNum)
            try:
                if len(shopids[i]) > 0:
                    headers_b = setHeaders(ck, "mall")  # 获取请求头
                    venderId = getVenderId(shopids[i], headers_b)  # 获取venderId
                    time.sleep(sleepNum)  # 根据用户需求是否限制请求速度
                    # 新增记忆功能
                    memoryFun(i, threadNum, True, pinName, 0, allUserCount)
                    if activityIdLabel == 0:
                        headers_a = setHeaders(ck, "mh5")
                        activityId, getBean = getShopOpenCardInfo(venderId, headers_a, shopids[i], userName)  # 获取入会礼包结果
                    #  activityId,getBean 或 返回 0:没豆 1:有豆已是会员 2:记录模式（不入会）
                    time.sleep(sleepNum)  # 根据用户需求是否限制请求速度
                    if activityId == 0 or activityId == 2:
                        break
                    elif activityId == 1:
                        user_num += 1
                        continue
                    elif activityId > 10:
                        activityIdLabel = 1
                        headers = setHeaders(ck, "JDApp")
                        result = bindWithVender(venderId, shopids[i], activityId, 208, headers)
                        busiCode = getResult(result, userName, user_num)
                        if busiCode == '0':
                            memoryFun(i, threadNum, False, pinName, getBean, allUserCount)
                            memoryJson = getMemory()
                            print(f"用户{user_num}:【{userName}】累计获得：{memoryJson['{}'.format(pinName)]} 京豆")
                            time.sleep(sleepNum)
                    else:
                        break
            except Exception as e:
                user_num += 1
                print(e)
                continue
            user_num += 1
    time.sleep(1)
    progress_bar(endNum, endNum, threadNum)

# start
def start():
    print(scriptHeader)
    outfile("Readme.md", readmes, True)
    isUpdate()
    global endShopidNum, midNum, allUserCount
    if isRemoteSid:
        print("已启用远程获取shopid")
        allShopid = getRemoteShopid()
    else:
        print("从本地shopid.txt获取shopid")
        allShopid = getShopID()
    allShopid = list(set(allShopid))
    endShopidNum = len(allShopid)
    midNum = int(endShopidNum / 2)
    print("获取到店铺数量:", endShopidNum)
    print(f"您已设置入会条件：{openCardBean} 京豆")
    print("获取用户...")
    cookies, userNames, pinNameList = iscookie()
    allUserCount = len(cookies)
    print("共{}个有效账号".format(allUserCount))
    memorylabel = 0
    startNum1 = 0
    startNum2 = midNum
    starttime = time.perf_counter()  # 记录时间开始
    if endShopidNum > 1:
        # 如果启用记忆功能，则获取上一次记忆位置
        startNum1, startNum2, memorylabel = isMemory(memorylabel, startNum1, startNum2, midNum, endShopidNum,
                                                     pinNameList)
        # 多线程部分
        threads = []
        t1 = Thread(target=OpenVipCrad, args=(startNum1, startNum2, allShopid, cookies, userNames, pinNameList, 1))
        threads.append(t1)
        t2 = Thread(target=OpenVipCrad, args=(startNum2, endShopidNum, allShopid, cookies, userNames, pinNameList, 2))
        threads.append(t2)
        try:
            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()
            isSuccess = True
        except:
            isSuccess = False
    elif endShopidNum == 1:
        startNum1, startNum2, memorylabel = isMemory(memorylabel, startNum1, startNum2, midNum, endShopidNum,
                                                     pinNameList)
        OpenVipCrad(startNum1, endShopidNum, allShopid, cookies, userNames, 1)
        isSuccess = True
    else:
        print("获取到shopid数量为0")
        exitCodeFun(9)
    endtime = time.perf_counter()  # 记录时间结束
    if os.path.exists(pwd + "/log/memory.json"):
        memoryJson = getMemory()
        n = 1
        for name,pinname in zip(userNames,pinNameList):
            try:
                userCountBean = memoryJson['pinname']
                print(f"用户{n}:【{name}】:本次累计获得：{userCountBean}豆")
            except:
                print(f"用户{n}:【{name}】:本次累计获得：0 豆")
            n += 1

    time.sleep(1)
    print("--- 入会总耗时 : %.03f 秒 seconds ---" % (endtime - starttime))
    print("{0}\n{1}\n{2}".format("*" * 60, scriptHeader, remarks))
    exitCodeFun(0)

if __name__ == '__main__':
    start()
