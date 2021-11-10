#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / msg 
Author: Curtin
功能：通知服务
Date: 2021/11/7 下午6:46
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021


# 调用方法：
    from msg import msg
    #启动通知服务
    msg().main()

    # 发信息 msg打印控制台同时会记录日志在message()，后面统一发送
    msg(" Hello ! ")
    print(" test ")  # 不会记录
    msg(" My name is Curtin ")

    # 发送到通知服务（如tg机器人、企业微信等）
    message = msg().message()
    send("标题", message)

'''
import requests
import os, sys


## 获取通知服务
class msg(object):
    def __init__(self, m=None):
        if m != None:
            self.str_msg = m
            print(self.str_msg)
            self.message()
        else:
            self.str_msg = None
    def message(self):
        global msg_info
        try:
            if self.str_msg:
                msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            if self.str_msg:
                msg_info = "{}".format(self.str_msg)
            else:
                msg_info = ""
        sys.stdout.flush()
        if msg_info:
            return msg_info
        else:
            return ""
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://ghproxy.com/https://raw.githubusercontent.com/curtinlv/JD-Script/main/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass
    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")


if __name__ == '__main__':
    # 启动通知服务
    msg().main()

    # msg打印控制台同时会记录日志在message()，后面统一发送
    print("\n打印在控制台的信息:")
    msg("Hello ! ")
    print("Test ")  # 不会记录
    msg("My name is Curtin. ")

    # 发送到通知服务（如tg机器人、企业微信等）
    message = msg().message()
    send("标题", message)
    print("\n发送到通知服务的信息:")
    print(message)
