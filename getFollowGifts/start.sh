#!/usr/bin/env bash
## 使用Env环境执行方式
## 执行命令 ：sh start.sh
## 2021.6.6
## By Curtin
## 定时任务：
## 0 8 * * * sh /你存放脚本的本地绝对路径/start.sh
##
#########################################
#主脚本路径。默认和主脚本同级目录
cd `dirname $0`
curpwd=`pwd`
scriptPath="${curpwd}/jd_getFollowGift.py"
################### ↓↓↓【以下需要配置的参数，代替配置文件OpenCradConfig.ini】↓↓↓ ###################
#京东cookie 格式：pt_key=xxx;pt_pin=xxx; & pt_key=xxx;pt_pin=xxx; (多账号&分隔)
export JD_COOKIE=''

############【通知参数】############
####### TG 机器人 #######
# TG token
export TG_BOT_TOKEN=
# UserId
export TG_USER_ID=

##### 如果你的网络能正常打开TG 以下参数不用配置 ↓↓↓
# TG_API_HOST
export TG_API_HOST=
# TG代理ip 和端口
export TG_PROXY_IP=
# TG代理端口
export TG_PROXY_PORT=
############################### ↑↑↑
######## 【微信 推送加】#####
# token
export PUSH_PLUS_TOKEN=
#Bark 推送
export BARK=
##################

################### ↑↑↑↑ 你需要填的参数到此结束 ↑↑↑↑ ##############################
######### 以下不用配置，默认就好 ##########################

_printTime(){
  echo "[`date +"%F %T"`]: $1"
}

##################↓↓↓↓↓↓ 获取v4-bot用户cookie↓↓↓↓↓↓ ###################################
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
fixCookie(){
    local cookieElement=($(sed 's/;/ /g' <<<$1))
    echo "${cookieElement[1]};${cookieElement[0]};"
    _printTime ""
}

if [ -f "$JD_DIR/config/config.sh" ];then
    source $JD_DIR/config/config.sh
    # 支持参数传入 start-v4.sh 1 就是玩第一个账号
    if [[ $# -eq 0 ]]; then
        export JD_COOKIE=$(getCookie ${OpenCardUserList[@]})
    elif [[ $# -eq 1 ]]; then
        export JD_COOKIE=$(getCookieNum $1)
    else
        _printTime "参数错误脚本退出!"
        exit 1
    fi
fi
##################↑↑↑↑↑ 获取v4-bot用户cookie↑↑↑↑↑ ####################################################
##############################3
logfile=${BASH_SOURCE%/*}/run_jd_getFollowGift.log


PID=`ps -ef | grep "python3 ${scriptPath}" | grep -v grep| awk '{print $2}'`
if [ ! -z $PID ];then
        _printTime "已在后台运行 PID：$PID 如需要终止执行命令：kill $PID"
        _printTime "查看运行日志: tail -f ${logfile}"
else
        _printTime "开始执行关注有礼领豆...."
        echo "" >${logfile} #清空日志
        nohup python3 ${scriptPath} >> ${logfile} 2>&1 &
        sleep 5
        PID=`ps -ef | grep "python3 ${scriptPath}" | grep -v grep| awk '{print $2}'`
        if [ -z ${PID} ];then
                _printTime "执行失败!"
                _printTime "请检查日志: tail -f ${logfile}"
        else
                _printTime "执行成功，已放在后台运行 PID：$PID"
                _printTime "查看运行日志: tail -f ${logfile}"
        fi
fi
