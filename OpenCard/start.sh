#!/usr/bin/env bash
## 使用Env环境执行方式，OpenCardConfig.ini配置文件参数不会生效。
## 执行命令 ：sh start.sh
## 2021.5.23
## By Curtin
## 定时任务：
## 0 8 * * * sh /你存放脚本的本地绝对路径/start.sh
##
#########################################
#主脚本路径。默认和主脚本同级目录
scriptPath='jd_OpenCard.py'
################### ↓↓↓【以下需要配置的参数，代替配置文件OpenCardConfig.ini】↓↓↓ ###################
#京东cookie 格式：pt_key=xxx;pt_pin=xxx; & pt_key=xxx;pt_pin=xxx; (多账号&分隔)
export JD_COOKIE='你的京东Cookie放这里，单引号保留'

#只入送豆数量大于此值
export openCardBean=5

#False|True 是否记录符合条件的shopid，输出文件【log/shopid-yyyy-mm-dd.txt】
export record=True

#True:仅记录，不入会; False:记录且还要入会。同时需要record=True才生效。
export onlyRecord=False

#True 或 False  开启记忆功能，接力上一次异常中断位置继续。
export memory=True

#True：只打印部分日志 False:打印所有日志
export printlog=False

#限制速度，单位秒，如果请求过快报错适当调整0.5秒以上
export sleepNum=0

#是否启用远程shopid，True:使用作者远程仓库更新的id，False：使用本地shopid.txt的id
export isRemoteSid=True

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
####### 【企业微信推 推送方法： http://note.youdao.com/s/HMiudGkb 】
export QYWX_AM=""
###### Bark  推送 iOS用户下载App获取码
export BARK=""

################### ↑↑↑↑ 你需要填的参数到此结束 ↑↑↑↑ ##############################
######### 以下不用配置，默认就好 ##########################
cd `dirname $0`
workpath=`pwd`
logfile=${workpath}/run_OpenCard.log
_printTime(){
  echo "[`date +"%F %T"`]: $1"
}
PID=`ps -ef | grep "python3 ${scriptPath}" | grep -v grep| awk '{print $2}'`
if [ ! -z $PID ];then
	_printTime "已在后台运行 PID：$PID 如需要终止执行命令：kill $PID"
	_printTime "查看运行日志: tail -f ${logfile}"
else
	_printTime "开始执行入会领豆...."
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

