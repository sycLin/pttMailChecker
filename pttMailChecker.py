#!/usr/bin/python
# -*- coding:utf-8 -*-

import telnetlib
import sys
import time
import datetime

###########
# globals #
###########

host = "ptt.cc"
host_ip = "140.112.172.2"
config_path = __file__[:len(__file__)-2]+"config"
config_dict = {}

####################
# helper functions #
####################

def loadConfig():
	f = open(config_path)
	lineBuf = f.readline()
	while lineBuf != "":
		if lineBuf.startswith('#') or lineBuf == "\n":
			pass
		elif len(lineBuf.split('=')) != 2:
			pass
		else:
			k, v = lineBuf.split('=')
			config_dict[k] = v.rstrip('\n')
		lineBuf = f.readline()
	f.close()

def getAccountInfo():
	if config_dict.get('USERNAME') == None or config_dict.get('PASSWORD') == None:
		loadConfig()
	return config_dict.get('USERNAME'), config_dict.get('PASSWORD')


def main():
	global host
	# record the current time
	now = datetime.datetime.now().timetuple()
	print "%d/%d/%d %s:%s:%s" % (now.tm_year, now.tm_mon, now.tm_mday, str(now.tm_hour).zfill(2), str(now.tm_min).zfill(2), str(now.tm_sec).zfill(2))
	print >> sys.stderr, "%d/%d/%d %s:%s:%s" % (now.tm_year, now.tm_mon, now.tm_mday, str(now.tm_hour).zfill(2), str(now.tm_min).zfill(2), str(now.tm_sec).zfill(2))

	# connect to ptt
	print >> sys.stderr, "creating connection via telnet:", host
	tn = telnetlib.Telnet(host)
	time.sleep(2)
	content = tn.read_very_eager().decode('big5', 'ignore')

	# send account id
	u, p = getAccountInfo()
	if u == None or p == None:
		print >> sys.stderr, "bad configuration..."
		sys.exit(1)
	if u"請輸入代號" not in content:
		print >> sys.stderr, "something wrong: no place to input username"
		# print "dumping content? (Y/N) >",
		# answer = raw_input("")
		# if answer == "Y" or answer == "y":
		# 	print content
		sys.exit(1)
	print >> sys.stderr, "inputting account id"
	tn.write(u+"\r\n")
	time.sleep(2)
	content = tn.read_very_eager().decode('big5', 'ignore')
	# send account password
	if u"請輸入您的密碼" not in content:
		print >> sys.stderr, "something wrong: no place to input password"
		# print "dumping content? (Y/N) >",
		# answer = raw_input("")
		# if answer == "Y" or answer == "y":
		# 	print content
		sys.exit(1)
	print >> sys.stderr, "inputting password"
	tn.write(p+"\r\n")
	time.sleep(3)
	content = tn.read_very_eager().decode('big5', 'ignore')
	# error handling
	if u"密碼不對" in content:
		print >> sys.stderr, "wrong password..."
		sys.exit(1)
	if u"您想刪除其他重複登入的連線嗎" in content:
		print >> sys.stderr, "deleting other connections"
		tn.write('y\r\n')
		time.sleep(5)
		content = tn.read_very_eager().decode('big5', 'ignore')
	while u"按任意鍵繼續" in content:
		print >> sys.stderr, "continue..."
		tn.write('\r\n')
		time.sleep(2)
		content = tn.read_very_eager().decode('big5', 'ignore')
	if u"您要刪除以上錯誤嘗試的記錄嗎" in content:
		print >> sys.stderr, "deleting wrong password records..."
		tn.write('y\r\n')
		time.sleep(3)
		content = tn.read_very_eager().decode('big5', 'ignore')

	# getting into the menu section
	if u"精華公佈欄" in content and u"私人信件區" in content:
		# we are now at menu section
		if u"你有新信件" in content:
			print "%s, you have unread messages!" % (str(u))
			print >> sys.stderr, "%s, you have unread messages!" % (str(u))
		else:
			print "%s, you don't have any unread messages!" % (str(u))
			print >> sys.stderr, "%s, you don't have any unread messages!" % (str(u))
		# logging out
		tn.write('G\r\n')
		tn.write('y\r\n')
		time.sleep(2)
		content = tn.read_very_eager().decode('big5', 'ignore')
		if u"此次停留時間" in content:
			print >> sys.stderr, "logged out successfully"
		else:
			print >> sys.stderr, "failed to log out, forcibly disconnected"
	else:
		print >> sys.stderr, "didn't get into the menu section..."
		# print "dumping content? (Y/N) >",
		# answer = raw_input("")
		# if answer == "Y" or answer == "y":
		# 	print content
		sys.exit(1)



if __name__ == "__main__":
	main()
