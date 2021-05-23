
# JD入会领豆小程序
![JD入会领豆小程序](https://raw.githubusercontent.com/curtinlv/JD-Script/main/OpenCrad/resultCount.png)
  
## 使用方法
#### [手机用户（参考） https://mp.weixin.qq.com/s/ih6aOURXWM-iKrhvMyR3mw](https://mp.weixin.qq.com/s/ih6aOURXWM-iKrhvMyR3mw)
#### [PC用户 （参考） https://mp.weixin.qq.com/s/JmLxAecZAlEc4L2sZWnn1A](https://mp.weixin.qq.com/s/JmLxAecZAlEc4L2sZWnn1A)

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
    2.兼容ios设备软件：Pythonista 3、Pyto(已测试正常跑，其他软件自行测试)   
    3.Windows exe 

    安装依赖模块 :
    pip3 install requests
    执行：
    python3 jd_OpenCrad.py
## `【更新记录】`
    2021.5.23：(v1.1.1)
        * 修复一些问题及优化一些代码
        * 修复Env环境读取变量问题
        * 新增 start.sh 运行脚本（可Env环境使用）
            - 运行方式 sh start.sh
            1.适合定时任务或不想依赖ini配置文件。 
            2.支持单号跑多开，如
               cp start.sh start_2.sh
               sh start_2.sh  #只跑里面配置的参数，如cookie
            3.定时任务（参考）：
               0 8 * * * sh /home/curtin/JD-Script/OpenCrad/start.sh
               2 8 * * * sh /home/curtin/JD-Script/OpenCrad/start_1.sh
    2021.5.21：(v1.1.0)
        * 修复一些问题及优化一些代码：
            - 修复最后统计显示为0，新增开卡个数统计
            - 修复记忆功能一些bug
            - 等等一些小问题
        * 新增机器人通知
            - 开启远程shopid、配合crontab 坐等收豆
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
            - 上一次中断最后记录的账号id检测不存在本次ck里面
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
            - log/可销卡账号xxx.txt #记录账号可销卡的店铺

### `【账号参数配置说明】`
### 主配置文件[ OpenCardConfig.ini ] 请保持utf-8默认格式

 变量  | 值  | 说明
 ---- | ----- | ------  
 JD_COOKIE  | pt_key=xxx;pt_pin=xxx;  | 必要(多账号&分隔) 
 openCardBean  | 30 | int，入会送豆满足此值，否则不入会 
 record    | False或True | 布尔值，是否记录符合条件的shopid(默认True) 
 onlyRecord  | False或True |布尔值， True:仅记录，不入会(默认False) 
 memory  | False或True | 布尔值，开启记忆功能，接力上一次异常中断位置继续。(默认yes) 
 printlog  | False或True | 布尔值，True：只打印部分日志 False:打印所有日志 
 sleepNum  | False或True | Float，限制速度，单位秒，如果请求过快报错适当调整0.5秒以上 
 isRemoteSid  | False或True | 布尔值，True:使用作者远程仓库更新的id，False：使用本地shopid.txt的id 
#### 兼容Env环境（如有配置则优先使用，适合AC、云服务环境等）    
        export JD_COOKIE='pt_key=xxx;pt_pin=xxx;' (多账号&分隔)
        export openCardBean=30
        export xxx=xxx

#### Ps:您可以到以下途径获取最新的shopid.txt，定期更新：

###### [GitHub仓库 https://github.com/curtinlv/JD-Script](https://github.com/curtinlv/JD-Script) 
###### [Gitee仓库 https://gitee.com/curtinlv/JD-Script](https://gitee.com/curtinlv/JD-Script)
###### [TG频道 https://t.me/TopStyle2021](https://t.me/TopStyle2021)
###### [TG群 https://t.me/topStyle996](https://t.me/topStyle996)
###### 关注公众号【TopStyle】回复：shopid
![TopStyle](https://gitee.com/curtinlv/img/raw/master/gzhcode.jpg)
# 
    @Last Version: v1.1.1

    @Last Time: 2021-05-22 18:02

    @Author: Curtin
#### **仅以学习交流为主，请勿商业用途、禁止违反国家法律 ，转载请留个名字，谢谢!** 

# End.
[回到顶部](#readme)
