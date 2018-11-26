#!/usr/bin/python3
# author:shujiangle

import subprocess
import re
from subprocess import Popen, PIPE
import os,sys,re
import time
from pyecharts import Bar


# 获取主机名
def get_hostname():
    print("\033[1;35m", end="")
    hostnames = os.popen("hostname").read().strip()
    print("你的主机名是: %s"%hostnames)
    # 获取主机现在时间
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print("主机的当前时间：%s"%now_time)

    # 获取主机运行时间
    times = os.popen("uptime").read().strip()
    times1 = re.findall(r"up(.*)days|min",times)
    times2 = re.findall(r"min|days,.*,(.*)user",times)
    times3 = re.findall(r"average:\s+(.*),\s+(.*),\s+(.*)",times)
    print("主机登录天数：%s"%(times1[0].strip()))
    print("主机的当前登录用户：%s"%(times2[0].strip()))
    print("主机1分钟负载：%s,5分钟负载：%s, 15分钟负载：%s"%(times3[0][0],times3[0][1],times3[0][2]))
    print("\033[0m", end="")

# 获取空间使用率
def get_space_use():
    ret = subprocess.run("df -h", shell=True, stdout=subprocess.PIPE)
    space_free=ret.stdout.decode("utf-8")
    space_free=re.findall(r"\d+\%\s+\/.*", space_free)
    space_free_num=[i.split("%")[0] for i in space_free]
    space_free_dir=[i.split()[-1] for i in space_free]
    # for i in range(len(space_free_dir)):
    #     print("\033[1;32m", end="")
    #     print("%s目录的使用率%s"%(space_free_dir[i], space_free_num[i]))
    #     print("\033[0m", end="")
    # return [space_free_dir, space_free_num]
    if os.path.exists("/root/PYTHON-STUDY/get_use/get_space_num.txt"):
        os.remove("/root/PYTHON-STUDY/get_use/get_space_num.txt")
    for i in range(len(space_free_dir)):
        print("\033[1;32m", end="")
        # print("%s目录的使用率%s"%(space_free_dir[i], space_free_num[i]))
        f = open("/root/PYTHON-STUDY/get_use/get_space_num.txt", "a")
        f.write("%s %s\n"%(space_free_dir[i], space_free_num[i]))
        # 关闭打开的文件
        f.close()
        print("\033[0m", end="")
    return [space_free_dir, space_free_num]


# 把数据生成图表
def get_pic():
    f = open("/root/PYTHON-STUDY/get_use/get_space_num.txt", "r")
    a = f.readlines()
    f.close()
    a = [i.strip("\n") for i in a]
    a1 = a[0].split()
    a2 = a[1].split()
    a3 = a[2].split()
    a4 = a[3].split()
    a5 = a[4].split()
    a6 = a[-1].split()
    v = [a1[1],a2[1],a3[1],a4[1],a5[1],a6[1]]
    # attr = "%s,%s,%s,%s,%s,%s"%(a1[0],a2[0],a3[0],a4[0],a5[0],a6[0])
    # print(attr)
    attr = [a1[0],a2[0],a3[0],a4[0],a5[0],a6[0]]
    v1 = [int(v1) for v1 in v]
    bar = Bar("空间使用率展示图")
    bar.add("", attr, v1, bar_category_gap=0)
    bar.render("/date/www/nginx/html/index.html")
# 获取服务器的ip地址
def get_ip():
    ip = subprocess.run("ifconfig", shell=True, stdout=subprocess.PIPE)
    ip = ip.stdout.decode()
    ip_name = re.findall(r"(.*):\s+flag", ip)
    ip_num1 = re.findall(r"inet\s+(.*)\s+netmask", ip)
    ip_num1 = [i.strip() for i in ip_num1]
    ip_num2 = re.findall(r"netmask\s+(.*)broadcast", ip)
    ip_num2 = [i.strip() for i in ip_num2]
    ip_num3 = re.findall(r"broadcast\s+(.*)", ip)
    ip_num4 = re.findall(r"ether\s+(.*)\s+txqueuelen", ip)
    ip_num4 = [i.strip() for i in ip_num4]
    print("\033[1;33m", end="")
    for k1 in range(len(ip_name)-1):
        print("%s网卡的ip地址是%s：子网掩码是%s: 广播地址是：%s 网卡的mac地址：%s"%(ip_name[k1], ip_num1[k1], ip_num2[k1],ip_num3[k1],ip_num4[k1]))
    print("%s网卡的ip地址是%s：子网掩码是%s:"%(ip_name[-1], ip_num1[-1], ip_num2[-1]))
    print("\033[0m", end="")



if __name__ == '__main__':
    # get_hostname()
    get_space_use()
    get_pic()
    # get_ip()
