#!/usr/bin/env bash
################### ↓↓↓【以下需要配置的参数，代替配置文件OpenCradConfig.ini】↓↓↓ ###################
#京东cookie 格式：pt_key=xxx;pt_pin=xxx; & pt_key=xxx;pt_pin=xxx; (多账号&分隔)
[[ -z JD_COOKIE ]] && export JD_COOKIE=''

############【通知参数】############
####### TG 机器人 #######
# TG token
[[ -z TG_BOT_TOKEN ]] && export TG_BOT_TOKEN=
# UserId
[[ -z TG_USER_ID ]] && export TG_USER_ID=

##### 如果你的网络能正常打开TG 以下参数不用配置 ↓↓↓ #####
# TG_API_HOST
[[ -z TG_API_HOST ]] && export TG_API_HOST=
# TG代理ip 和端口
[[ -z TG_PROXY_IP ]] && export TG_PROXY_IP=
# TG代理端口
[[ -z TG_PROXY_PORT ]] && export TG_PROXY_PORT=
############################### ↓↓↓ 【微信 推送加】 #####
# token
[[ -z PUSH_PLUS_TOKEN ]] && export PUSH_PLUS_TOKEN=
#Bark 推送
[[ -z BARK ]] && export BARK=
# 企业微信推送
[[ -z QYWX_AM ]] && export QYWX_AM=
##################

################### ↑↑↑↑ 你需要填的参数到此结束 ↑↑↑↑ ##############################
######### 以下不用配置，默认就好 ##########################

# 脚本绝对路径
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_NAME=${SCRIPT_PATH##*/}
SHELL_FOLDER="${SCRIPT_PATH%/*}"
# python 脚本目录名称数组
PYTHON_SCRIPT_NAME=()
# python 脚本绝对路径数组
PYTHON_SCRIPT_PATH=()

info() { echo -e "[`date +"%F %T"`] [info] $*"; }
warn() { echo -e "[`date +"%F %T"`] [warn] $*"; }
error(){
    echo -e "[`date +"%F %T"`] [error] $*"
    echo
    help
    exit 1
}

# 脚本帮助
help(){
    echo "${SCRIPT_NAME} 脚本使用说明."
    echo "    使用语法1: ${SCRIPT_NAME} OpenCard getFollowGifts"
    echo "    使用语法2: ${SCRIPT_NAME} -c 1 OpenCard getFollowGifts"
    echo "    使用语法3: ${SCRIPT_NAME} -r <python 脚本绝对路径1> -r <python 脚本绝对路径2>"
    echo "    使用语法4: ${SCRIPT_NAME} -r <脚本同一目录python脚本名字> -r <python 脚本绝对路径>"
    echo "    选项:"
    echo "          -c        (--cookie_num) <num>                 V4 专用参数，跑单独的 cookie"
    echo "          -r        (--run_script) <pythonScriptPath>    指定 python 脚本文件绝对路径或当前目录下python脚本名字"
}

# 根据脚本当前目录获得 python 脚本路径
getPythonScriptPath(){
    local name=$1
    local dir="${SHELL_FOLDER}/${name}"
    [[ ! -d ${dir} ]] && echo "false" && return
    local path=$(ls ${dir}/*.py | xargs realpath 2> /dev/null)
    local path_num=$(wc -l  <<<"${path}")
    if [[ ${path_num} == 1 ]]; then
        echo ${path}
    else
        echo "false"
    fi
}

# v4 检查是否 v4 环境
is_v4(){
    [[ -f $JD_DIR/config/config.sh ]] && return 0 || return 1
}

# 获取指定账号的 Cookie
getCookieNum(){
    export JD_COOKIE=$(eval echo '$Cookie'$1)
}

# 修复有些大佬用浏览器获取 cookie 的时候顺序错导致 python 脚本报错
fixCookie(){
    local cookieElement=($(sed 's/;/ /g' <<<$1))
    echo "${cookieElement[1]};${cookieElement[0]};"
}

# 随机 cookie
randomCookie(){
    echo $(sed 's/\s/\n/g' <<<$@ | shuf)
}

# 获取传入
getCookie(){
    local NUM
    [[ ${OpenCardRandomCK} == "true" ]] && NUM=($(randomCookie $@)) || NUM=$@
    local jdCookie
    local tmpCookie
    if ! echo "${NUM[@]}" | sed 's/\s//g' | grep -q '^[[:digit:]]*$' ; then
        error "错误！ OpenCardUserList 只能输入数字\n$(echo "${NUM[@]}" | sed 's/\s//')"
    fi
    for i in ${NUM[@]}; do
        tmpCookie=$(eval echo '$Cookie'$i)
        [[ ${tmpCookie} == "" ]] && warn "Cookie$i 为空,跳过不执行！" && break
        # 如果 pt_pin 开始的需要调转为 pt_key 开头
        grep -q '^pt_pin.*' <<<${tmpCookie} && tmpCookie=$(fixCookie ${tmpCookie})
        [[ ${jdCookie} == "" ]] && jdCookie="${tmpCookie}" || jdCookie="${jdCookie} & ${tmpCookie}"
    done
    export JD_COOKIE="${jdCookie}"
}

# v4 环境获取 cookie
getV4Cookie(){
    source $JD_DIR/config/config.sh
    # 支持参数传入，如果 V4_COOKIE_NUM 定义了数字就只跑这个数字的 Cookie
    if [[ -z ${V4_COOKIE_NUM} ]]; then
        getCookie ${OpenCardUserList[@]}
    else
        getCookieNum ${V4_COOKIE_NUM}
    fi
}

# 根据不同环境声明不同日志路径
# getLogPath 脚本目录
getLogPath(){
    local scriptName=$1
    local logDir
    local logPath
    if is_v4 ; then
        logDir="$JD_DIR/log/${scriptName}"
        logPath="${logDir}/$(date '+%Y-%m-%d-%H-%M-%S').log"
    elif is_ql ; then
        logDir="$QL_DIR/log/${scriptName}"
        logPath="${logDir}/$(date '+%Y-%m-%d-%H-%M-%S').log"
    else
        logDir=$SHELL_FOLDER/curtinlv_JD-Script_log
        logPath="${logDir}/${scriptName}.log"
    fi
    [[ ! -d ${logDir} ]] && mkdir -p ${logDir}
    info "日志文件存储路径为： ${logPath}"
    LOG_FILE=${logPath}
}

# 执行 Python 脚本，支持传入多个脚本
## 使用方法 runPythonScript ./OpenCard/jd_OpenCard.py ./getFollowGifts/jd_getFollowGift.py
runPythonScript(){
    local scriptPath
    local scriptName
    for value in $*; do
        if [[ -f ${value} ]]; then
            scriptPath="${value}"
            scriptName=$(awk -F '.' '{print $1}' <<<${value##*/})
        elif [[ -f $(getPythonScriptPath ${value}) ]]; then
            scriptPath=$(getPythonScriptPath ${value})
            scriptName=$(awk -F '.' '{print $1}' <<<${scriptPath##*/})
        else
            warn "未找到 ${value} 跳过执行！"
            continue
        fi
        info "######## 开始执行 ${scriptName} ########"
        # 日志默认存放在脚本根目录,每次执行被覆盖
        getLogPath ${scriptName}
        nohup python3 ${scriptPath} 2>&1 > ${LOG_FILE} &
        PID=$!
        info "等待 python 脚本执行。"
        sleep 5
        if ! ps | grep -v grep | grep -q $PID ;then
            warn "执行失败!"
            warn "请检查日志: \n$(cat ${LOG_FILE})"
        else
            info "执行成功，已放在后台运行 PID：$PID"
            info "查看运行日志: tail -f ${LOG_FILE}"
        fi
        info "######## 执行结束 ${scriptName} ########"
        echo ""
    done
}

# 解析脚本传入参数
getOption(){
    [[ $# -eq 0 ]] && help && exit
    while [[ $# -gt 0 ]]; do
        case $1 in
            # -c 参数，只支持 V4 环境，可以指定哪个 cookie 跑脚本
            "-c"|"--cookie_num")
                is_v4 || is_ql || error "-c 参数只支持 v4 环境下使用"
                shift
                if ! grep -q '^[[:digit:]]*$' <<<"${1}"; then
                    error "--cookie 只能传入数字\n $(help)"
                fi
                V4_COOKIE_NUM=$1
                ;;
            # -r 参数，可以指定脚本的路径
            "-r"|"--run_script")
                shift
                if [[ -f $1 ]]; then
                    PYTHON_SCRIPT_PATH+=($(realpath $1))
                elif [[ -f "${SHELL_FOLDER}/${1##*/}" ]]; then
                    PYTHON_SCRIPT_PATH+=($(realpath ${SHELL_FOLDER}/${1##*/}))
                else
                    warn "脚本路径：$1 当前脚本不存在，跳过不执行！"
                fi
                ;;
            # 输出脚本帮助
            "-h"|"--help")
                help && exit;;
            # 其余均属于 python 脚本文件夹名
            *)
                if [[ $(getPythonScriptPath $1) != "false" ]]; then
                    PYTHON_SCRIPT_NAME+=($1)
                else
                    warn "当前脚本目录找不到 $1，跳过不执行！"
                fi
                ;;
        esac
        shift
    done
    [[ ${#PYTHON_SCRIPT_NAME[@]} -eq 0 ]] && \
        [[ ${#PYTHON_SCRIPT_PATH[@]} -eq 0 ]] && \
        error "没有找到可用的脚本！"
}

# 检查是否为青龙环境
is_ql(){
    [[ -f /ql/config/config.sh ]] && return 0 || return 1
}

getQlCookie(){
    # 获取青龙的  cookie
    loadCookie(){
        local i=1
        for cookie in $(cat /ql/config/cookie.sh); do
            cookie=$(sed 's/=/\\=/g' <<<$cookie)
            cookie=$(sed 's/;/\\;/g' <<<$cookie)
            eval Cookie$i=$cookie
            (( i++ ))
        done
    }

    # 获取微信推送 TG 推送等配置
    source /ql/config/config.sh
    loadCookie
    if [[ -z ${V4_COOKIE_NUM} ]]; then
        getCookie ${OpenCardUserList[@]}
    else
        getCookieNum ${V4_COOKIE_NUM}
    fi
}

# Main
# 解析脚本传入参数
getOption $*

# 检查是否 V4 环境，加载 v4 config.sh
if is_v4; then
    getV4Cookie
fi

# 检查是否青龙环境，加载青龙配置
if is_ql; then
    getQlCookie
fi

[[ ${#PYTHON_SCRIPT_NAME[@]} -ne 0 ]] && runPythonScript ${PYTHON_SCRIPT_NAME[@]}
[[ ${#PYTHON_SCRIPT_PATH[@]} -ne 0 ]] && runPythonScript ${PYTHON_SCRIPT_PATH[@]}