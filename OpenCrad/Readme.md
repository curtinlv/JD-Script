# JD入会领豆 - 轻松日撸千豆
##  目录结构
    JD-Script/                  #仓库
    |-- LICENSE
    |-- OpenCrad                # 主目录
    |   |-- jd_OpenCrad.py      # 主代码 （必要）
    |   |-- log                 # 临时目录（可删除）
    |   |-- OpenCardConfig.ini  # 只配置文件（必要）
    |   |-- Readme.md           # 说明
    |   `-- shopid.txt          # shopid存放文件（必要）
    `-- README.md

### `【兼容环境】`
    1.Python3.3+ 环境
    2.兼容ios设备软件：Pythonista 3(已测试正常跑，其他软件自行测试)   
    3.Windows exe

    安装依赖模块 :
    pip3 install requests
    pip3 install configparser
    执行：
    python jd_OpenCrad.py
## `【更新记录】`

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
    
    2021.5.5：(v1.0.1)
        * 新增记忆功能，如中断后下次跑会接着力跑（默认开启）
            - memory= True
        * 新增仅记录shopid，不入会功能（默认关闭）
            - onlyRecord = no
        * 修复已知Bug
    
    2021.5.7：(v1.0.2)
        * 优化代码逻辑
        * 修复已知Bug
    
    2021.5.8：(v1.0.3)
        * 优化记忆功能逻辑：
            - cookiek个数检测
            - shopid个数检测
            - 上一次中断最后记录的用户id检测不存在本次ck里面
            - 临时文件log/memory.json是否存在
            - 以上任意一条命中则记忆接力功能不生效。

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
    @Last Version: v1.0.3
    
    @Last Time: 2021-05-09
    
    @Author: Curtin
#### **仅以学习交流为主，请勿商业用途或违反国家法律 ，转载请注明出处，谢谢!** 

# End.
[回到顶部](#readme)