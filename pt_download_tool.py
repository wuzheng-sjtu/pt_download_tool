#-*- coding:utf-8 -*-
__author__ = 'Zheng Wu'
__version__ = '1.0'

# This is a auto download tool for pt.sjtu.edu.cn

from splinter import Browser
import urllib2
import re
import os
import sys
import time
import webbrowser

def name_transform(row_string):
	# 寻找需要转义的字符并在其前面加上‘\’
	row_string = row_string.replace(' ','\ ')
	row_string = row_string.replace('[','\[')
	row_string = row_string.replace(']','\]')
	row_string = row_string.replace("'","\'")
	row_string = row_string.replace("(","\(")
	row_string = row_string.replace(")","\)")
	return row_string


reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv)!=3:
	print 'Error! Download directory or browser download default directory is not specified!\n'
	exit()
else:
	download_dir = sys.argv[1]
	if os.path.exists(download_dir):
		pass
	else:
		print 'the specfied directory does not exist, creating it for you ...\n'
		os.system('mkdir -p '+download_dir)

default_dir = sys.argv[2]
search_cont = raw_input('Please enter the content you want to search:\n')

# log in 
url = 'https://pt.sjtu.edu.cn/'
browser=Browser('chrome')
browser.visit(url)
time.sleep(15)

# enter the search page
search_url = 'https://pt.sjtu.edu.cn/torrents.php?incldead=0&spstate=0&inclbookmarked=0&picktype=0&search=' + search_cont +'&search_area=0&search_mode=0' 
browser.visit(search_url)
time.sleep(2)
now_html = browser.html

# use re to crawl the target torrent url
pattern = re.compile(r'<a target="_blank" href="(.*?)">')
for append_url in re.findall(pattern, now_html):
	torrent_url = url + append_url
	webbrowser.open(torrent_url)
	#获取刚刚下载所得的种子并将其移动到指定文件夹
	l = os.listdir(default_dir)
	l.sort(key=lambda fn: os.path.getmtime(default_dir+fn) if not os.path.isdir(default_dir+fn) else 0)
	newfile = os.path.join(default_dir,l[-1])
	newfile = name_transform(newfile)
	os.system(r'mv '+newfile+' '+os.path.join(download_dir,append_url[-6:]+'.torrent'))
	print ('mv '+newfile+' '+os.path.join(download_dir,append_url[-6:]+'.torrent'))
	os.system(r'btc add -f '+os.path.join(download_dir,append_url[-6:]+'.torrent'))
	print ('btc add -f '+os.path.join(download_dir,append_url[-6:]+'.torrent'))
	time.sleep(10)

date_row = time.strftime("%Y-%m-%d %X",time.localtime())
date_short = date_row[:-5]
minute = int(date_row[-5:-3])
#将近5min内下载的种子进行下载
for i in range(5):
	date_match = date_short+'0'*(minute-i<10)+str(minute-i)
	os.system('btc list | btc filter --key date_added "'+date_match+'*" | btc download --directory '+download_dir)

