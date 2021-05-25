#!/usr/bin/env bash
## 使用Env环境执行方式，OpenCradConfig.ini配置文件参数不会生效。
## 执行命令 ：bash start.sh
## 2021.5.25
## By Curtin
## 定时任务：
## 0 8 * * * bash /你存放脚本的本地绝对路径/start.sh
##
#########################################
source $JD_DIR/config/config.sh
logdir="/jd/log/OpenCrad"
[[ -d ${logdir} ]] || mkdir -p ${logdir}

## function
_printTime(){
  echo -e "[$(date +"%F %T")]: $1"
}

clearLog(){
    _printTime "清理24小时前日志"
    find $logdir -mtime 1 -name '*log' -exec rm -f {} \;
}

# 修复有些大佬用浏览器获取 cookie 的时候顺序错导致 python 脚本报错
fixCookie(){
    local cookieElement=($(sed 's/;/ /g' <<<$1))
    echo "${cookieElement[1]};${cookieElement[0]};"
    _printTime ""
}

# 随机 cookie
randomCookie(){
    echo $(sed 's/\s/\n/g' <<<$@ | shuf)
}

getCookie(){
    local NUM
    [[ ${OpenCardRandomCK} == "true" ]] && NUM=($(randomCookie $@)) || NUM=$@
    local jdCookie
    local tmpCookie
    if ! echo "${NUM[@]}" | sed 's/\s//g' | grep -q '^[[:digit:]]*$' ; then
        _printTime "错误！ OpenCardUserList 只能输入数字\n$(echo "${NUM[@]}" | sed 's/\s//')"
        exit 1
    fi
    for i in ${NUM[@]}; do
        tmpCookie=$(eval echo '$Cookie'$i)
        [[ ${tmpCookie} == "" ]] && _printTime "Cookie$i 为空,跳过不执行！" && break
        # 如果 pt_pin 开始的需要调转为 pt_key 开头
        grep -q '^pt_pin.*' <<<${tmpCookie} && tmpCookie=$(fixCookie ${tmpCookie})
        [[ ${jdCookie} == "" ]] && jdCookie="${tmpCookie}" || jdCookie="${jdCookie} & ${tmpCookie}"
    done
    echo "${jdCookie}"
}

# 获取指定账号的 Cookie
getCookieNum(){
    echo $(eval echo '$Cookie'$1)
}


#主脚本路径。V4 建议在 config.sh 文件添加 OwnRawFile 
scriptPath='/jd/own/raw/jd_OpenCard.py'
################### ↓↓↓【以下需要配置的参数，代替配置文件OpenCradConfig.ini】↓↓↓ ###################
#京东cookie 格式：pt_key=xxx;pt_pin=xxx; & pt_key=xxx;pt_pin=xxx; (多账号&分隔)

# 支持参数传入 start-v4.sh 1 就是玩第一个账号
if [[ $# -eq 0 ]]; then
    export JD_COOKIE=$(getCookie ${OpenCardUserList[@]})
elif [[ $# -eq 1 ]]; then
    export JD_COOKIE=$(getCookieNum $1)
else
    _printTime "参数错误脚本退出!"
    exit 1
fi
#只入送豆数量大于此值
[[ -z ${openCardBean} ]] && export openCardBean=5

#False|True 是否记录符合条件的shopid，输出文件【log/shopid-yyyy-mm-dd.txt】
[[ -z ${record} ]] && export record=True

#True:仅记录，不入会; False:记录且还要入会。同时需要record=True才生效。
[[ -z ${onlyRecord} ]] && export onlyRecord=False

#True 或 False  开启记忆功能，接力上一次异常中断位置继续。
[[ -z ${memory} ]] && export memory=True

#True：只打印部分日志 False:打印所有日志
[[ -z ${printlog} ]] && export printlog=False

#限制速度，单位秒，如果请求过快报错适当调整0.5秒以上
[[ -z ${sleepNum} ]] && export sleepNum=0

#是否启用远程shopid，True:使用作者远程仓库更新的id，False：使用本地shopid.txt的id
[[ -z ${isRemoteSid} ]] && export isRemoteSid=True

############【通知参数】############

####### TG 机器人 #######
# TG token
[[ -z ${TG_BOT_TOKEN} ]] && export TG_BOT_TOKEN=
# UserId
[[ -z ${TG_USER_ID} ]] && export TG_USER_ID=

##### 如果你的网络能正常打开TG 以下参数不用配置 ↓↓↓
# TG_API_HOST
[[ -z ${TG_API_HOST} ]] && export TG_API_HOST=
# TG代理ip 和端口
[[ -z ${TG_PROXY_IP} ]] && export TG_PROXY_IP=
# TG代理端口
[[ -z ${TG_PROXY_PORT} ]] && export TG_PROXY_PORT=
############################### ↑↑↑

######## 【微信 推送加】#####
# token
[[ -z ${PUSH_PLUS_TOKEN} ]] && export PUSH_PLUS_TOKEN=
##################

################### ↑↑↑↑ 你需要填的参数到此结束 ↑↑↑↑ ##############################
######### 以下不用配置，默认就好 ##########################
logfile="${logdir}/$(date '+%Y-%m-%d-%H-%M-%S').log"

PID=$(ps | grep "python3 ${scriptPath}" | grep -v grep| awk '{print $1}')
if [ ! -z $PID ];then
    _printTime "已在后台运行 PID：$PID 如需要终止执行命令：kill $PID"
    _printTime "查看运行日志: tail -f ${logfile}"
else
    _printTime "开始执行入会领豆...."
    nohup python3 ${scriptPath} 2>&1 > ${logfile} &
    PID=$!
    echo > /tmp/openCard_$PID
    sleep 5
    if ! ps | grep -q $PID ;then
        _printTime "执行失败!"
        _printTime "请检查日志: tail -f ${logfile}"
    else
        _printTime "执行成功，已放在后台运行 PID：$PID"
        _printTime "查看运行日志: tail -f ${logfile}"
    fi
fi

clearLog
