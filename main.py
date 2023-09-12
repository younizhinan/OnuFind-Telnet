#-*- coding: utf-8 -*-
#!/usr/bin/python 
import logging
from logging.handlers import RotatingFileHandler
import xtelnet
from queue import Queue
import threading
import time
from _datetime import datetime
import re
import os
from conf import *

#创建一个事件对象
thread_event = threading.Event()
#创建结果列表
result = []
#创建进程列表
threads = []
#定义日志位置
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
title = ".\\Logs\\"+ "Log-" + now + ".txt"
logging.basicConfig(filename=title, level = logging.INFO)

#定义连接与操作
def telnet(ip, username, passwd, cmd):
	global result
	# res = []
	try:
		tn = xtelnet.session()
		tn.connect(ip, username, passwd, p=23, timeout = 5)
		output = tn.execute(cmd).split("\n")
		#匹配Onu x/x/x:x
		pattern = r'Onu\d{1,}/\d{1,}/\d{1,}:\d{1,}'
		#进程锁，防止多个进程同时写入
		lock.acquire()
		for i in output:
			i = i.replace('\r', '').replace('\n', '')
			match_obj = re.findall(pattern, i)
			# if match_obj:
			# 	res.append("%s - %s"% (ip, match_obj[-1]))
			if match_obj:
				result.append("%s - %s"% (ip, match_obj[-1]))
			logging.info('%s - %s' % (ip, i))
		print("正在%s上查询"% ip)
		lock.release()
		# if res:
		# 	for i in res:
		# 		print("找到结果: %s"% i)
	except Exception as e:
		lock.acquire()
		logging.error('%s - %s' % (ip, e))
		print('%s - %s' % (ip, e))
		lock.release()

if __name__ == '__main__':
	lock = threading.Lock()
	#匹配H-H-H的MAC格式
	pattern = r'^[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}$'
	mac = input("请输入要查询的MAC(H-H-H):")
	match_obj = re.findall(pattern, mac)
	if len(match_obj) != 0:
		mac = match_obj[-1]
	else:
		while len(match_obj) == 0:
			mac = input("请输入正确格式的MAC地址:")
			match_obj = re.findall(pattern, mac)
		mac = match_obj[-1]
	cmd = "display onu mac-address " + str(mac)
	print("开始查询...")
	for key in swip:
		ip = swip[key]
		a = threading.Thread(target=telnet, args=(ip, username, passwd, cmd))
		a.start()
		threads.append(a)
	#等待所有子线程结束才继续运行主线程
	for a in threads:
		a.join()
	if result:
		print("##########################")
		print("找到%s个结果:"% len(result))
		for i in result:
			print(" %s "% i)
		print("##########################")
	else:
		print("##########################")
		print("未找到结果")
		print("##########################")
	print("日志文件已保存至%s"% title)
	input("输入Enter退出...")


		