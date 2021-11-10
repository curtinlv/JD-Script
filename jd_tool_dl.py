#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
Author: Curtin
功能：脚本依赖下载
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021
cron: 0 5 * * *
new Env('脚本依赖下载 for Curtinlv 仓库');
'''

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")
    exit(3)
import os
def getTool(toolName, a=0):
    if a == 0:
        a += 1
    try:
        url = 'https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/' + toolName
        response = requests.get(url)
        if response.status_code == 404:
            print(f"[{toolName}] 下载连接有误！")
            print(f"下载失败：[{toolName}]")
            return
        if 'urtinlv' in response.text:
            with open(toolName, "w+", encoding="utf-8") as f:
                f.write(response.text)
                print(f"已添加依赖：{toolName}")
        else:
            if a < 5:
                a += 1
                return getTool(toolName, a)
            else:
                print(f"下载失败：{toolName}")
    except:
        if a < 5:
            a += 1
            return getTool(toolName, a)
        else:
            print(f"下载失败：{toolName}")

if __name__ == '__main__':
    file_name = ['jd_cookie.py', 'msg.py', 'sendNotify.py']
    for f in file_name:
        if os.path.exists(f):
            os.remove(f)
        print(f"开始下载依赖：{f}")
        getTool(f)

