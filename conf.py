#-*- coding: utf-8 -*-
#!/usr/bin/python
#要执行操作的交换机管理
import re
import os
import openpyxl

#创建字典
swip = {}

#打开文档
workbook = openpyxl.load_workbook('./设备列表.xlsx')

#获取工作表
sheet = workbook['Sheet1']
for row in sheet.iter_rows(values_only=True):
	swip[row[0]] = row[1]
lastkey = list(swip)[-1]

#交换机用户名密码    
username = "wasu"  #用户名
passwd = "wasu@123"    #密码
threads = [30]   #多线程