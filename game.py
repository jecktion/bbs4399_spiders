# -*- coding: utf-8 -*-
# 此程序用来抓取 的数据
import requests
import time
import random
import re
from multiprocessing.dummy import Pool
import csv
import json
import sys
from fake_useragent import UserAgent, FakeUserAgentError


class Spider(object):
	def __init__(self):
		# self.date = '2000-10-01'
		try:
			self.ua = UserAgent(use_cache_server=False).random
		except FakeUserAgentError:
			pass
		self.cookie = 'smidV2=2018073111042584f5bed5f954ebe37a599675bd6d429e005530598407badc0; _4399tongji_vid=153300626559291; _ga=GA1.2.1501981606.1533020133; Hm_lvt_1b08922f2d6095855a3530341e9b66ca=1533006177,1533521681; Pnick=%E9%83%BD%E5%B0%89%E5%AE%9C%E6%B0%91%E6%9E%9A%E5%B3%B0; Pauth=2775326258%7C18260027173%7Cbb845bc7c7075b70c7347376b7a5dc82%7C1537974594%7C0%7C5d79f08c88b98efa1bdee83069341853%7C; User=%E9%83%BD%E5%B0%89%E5%AE%9C%E6%B0%91%E6%9E%9A%E5%B3%B0%7C2775326258%7C18260027173%7C8e31d60fb7866b3f7b861e29d4a16d2a41d0331b; _4399tongji_st=1537974596; Hm_lvt_5c9e5e1fa99c3821422bf61e662d4ea5=1537974597; Hm_lpvt_5c9e5e1fa99c3821422bf61e662d4ea5=1537974597; Hm_lvt_da0bce75c9049bf4056836b34215ec4c=1537974597; Hm_lpvt_da0bce75c9049bf4056836b34215ec4c=1537974597; ad_forums=1'
	
	def get_headers(self):
		user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
		               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
		               'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
		               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
		               'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
		               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
		               'Opera/9.52 (Windows NT 5.0; U; en)',
		               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.2pre) Gecko/2008071405 GranParadiso/3.0.2pre',
		               'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.0 Safari/534.3',
		               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.4 Safari/532.0',
		               'Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.7.39 Version/11.00']
		user_agent = random.choice(user_agents)
		headers = {'Host': 'bbs.4399.cn', 'Connection': 'keep-alive',
		           'User-Agent': user_agent,
		           'Referer': 'http://bbs.4399.cn/forums-mtag-82137-page-2',
		           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		           'Accept-Encoding': 'gzip, deflate, br',
		           'Accept-Language': 'zh-CN,zh;q=0.8',
		           'Cookie': self.cookie
		           }
		return headers

	def p_time(self, stmp):  # 将时间戳转化为时间
		stmp = float(str(stmp)[:10])
		timeArray = time.localtime(stmp)
		otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		return otherStyleTime

	def replace(self, x):
		# 去除img标签,7位长空格
		removeImg = re.compile('<img.*?>| {7}|')
		# 删除超链接标签
		removeAddr = re.compile('<a.*?>|</a>')
		# 把换行的标签换为\n
		replaceLine = re.compile('<tr>|<div>|</div>|</p>')
		# 将表格制表<td>替换为\t
		replaceTD = re.compile('<td>')
		# 把段落开头换为\n加空两格
		replacePara = re.compile('<p.*?>')
		# 将换行符或双换行符替换为\n
		replaceBR = re.compile('<br><br>|<br>')
		# 将其余标签剔除
		removeExtraTag = re.compile('<.*?>', re.S)
		# 将&#x27;替换成'
		replacex27 = re.compile('&#x27;')
		# 将&gt;替换成>
		replacegt = re.compile('&gt;|&gt')
		# 将&lt;替换成<
		replacelt = re.compile('&lt;|&lt')
		# 将&nbsp换成''
		replacenbsp = re.compile('&nbsp;')
		# 将&#177;换成±
		replace177 = re.compile('&#177;')
		replace1 = re.compile(' {2,}')
		x = re.sub(removeImg, "", x)
		x = re.sub(removeAddr, "", x)
		x = re.sub(replaceLine, "\n", x)
		x = re.sub(replaceTD, "\t", x)
		x = re.sub(replacePara, "", x)
		x = re.sub(replaceBR, "\n", x)
		x = re.sub(removeExtraTag, "", x)
		x = re.sub(replacex27, '\'', x)
		x = re.sub(replacegt, '>', x)
		x = re.sub(replacelt, '<', x)
		x = re.sub(replacenbsp, '', x)
		x = re.sub(replace177, u'±', x)
		x = re.sub(replace1, '', x)
		x = re.sub('\n', '', x)
		return x.strip()
	
	def GetProxies(self):
		# 代理服务器
		proxyHost = "http-dyn.abuyun.com"
		proxyPort = "9020"
		# 代理隧道验证信息
		proxyUser = "HI18001I69T86X6D"
		proxyPass = "D74721661025B57D"
		proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
			"host": proxyHost,
			"port": proxyPort,
			"user": proxyUser,
			"pass": proxyPass,
		}
		proxies = {
			"http": proxyMeta,
			"https": proxyMeta,
		}
		return proxies

	def get_comments(self, ss):  # 获取某一页游戏评论
		game_url, product_number, plat_number, page = ss
		print 'page:',page
		p0 = re.compile('http[s]?://bbs\.4399\.cn/forums-mtag-(\d+)')
		game_id = re.findall(p0, game_url)[0]
		url = 'https://bbs.4399.cn/forums-mtag-%s-page-%d' % (game_id, page)
		retry = 5
		while 1:
			try:
				text = requests.get(url, headers=self.get_headers(), proxies=self.GetProxies(),timeout=10).content.decode('utf-8', 'ignore')
				p = re.compile(
					u'<li data-id="(\d+?)">.*?target="_blank">(.*?)</a>.*?<span class="date">(.*?)</span>.*?<p class="text">(.*?)</p>.*?<span class="hot">热度\((\d+?)\)</span>.*?<span class="comment">(\d+?)</span>',
					re.S)
				items = re.findall(p, text)
				results = []
				for item in items:
					# print '|'.join(item)
					nick_name = item[1]
					cmt_date = item[2]
					if u'-' not in cmt_date:
						continue
					# if cmt_date < self.date:
					# 	continue
					cmt_time = cmt_date + ' ' + '00:00:00'
					comments = item[3]
					like_cnt = item[4]
					cmt_reply_cnt = item[5]
					long_comment = '0'
					last_modify_date = self.p_time(time.time())
					src_url = game_url
					tmp = [product_number, plat_number, nick_name, cmt_date, cmt_time, comments, like_cnt,
					       cmt_reply_cnt, long_comment, last_modify_date, src_url]
					print '|'.join(tmp)
					results.append([x.encode('gbk', 'ignore') for x in tmp])
				return results
			except Exception as e:
				retry -= 1
				if retry == 0:
					print e
					return None
				else:
					continue
	
	def get_total_page(self, game_url):  # 获取网址的总页数
		p0 = re.compile('http[s]?://bbs\.4399\.cn/forums-mtag-(\d+)')
		game_id = re.findall(p0, game_url)[0]
		url = 'http://bbs.4399.cn/forums-mtag-%s-page-1' % game_id
		retry = 5
		while 1:
			try:
				text = requests.get(url, headers=self.get_headers(), proxies=self.GetProxies(), timeout=10).content.decode('utf-8', 'ignore')
				p0 = re.compile(u'共 (.*?) 页')
				total_page = re.findall(p0, text)[1]
				return total_page
			except:
				retry -= 1
				if retry == 0:
					return None
				else:
					continue

	def get_all(self, game_url, product_number, plat_number):  # 获取所有内容
		totalpage = self.get_total_page(game_url)
		if totalpage is None:
			with open('error.txt', 'a') as f:
				tmp = [game_url, product_number, plat_number]
				f.write('|'.join(tmp).encode('gbk', 'ignore') + '\n')
			return None
		else:
			print u'%s 共有 %s 页' % (product_number, totalpage)
			if int(totalpage) > 1000:
				totalpage = '1000'
			ss = []
			for page in range(1, int(totalpage) + 1):
				ss.append([game_url, product_number, plat_number, page])
			pool = Pool(3)
			items = pool.map(self.get_comments, ss)
			pool.close()
			pool.join()
			mm = []
			for item in items:
				if item is not None:
					mm.extend(item)
			with open('data_comments_5.csv', 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerows(mm)


if __name__ == "__main__":
	# 4399需要登陆，你这边注册一个4399的账号，登陆一次，然后获取cookie换掉self.cookie就可以运行程序了
	# 4399需要登陆，你这边注册一个4399的账号，登陆一次，然后获取cookie换掉self.cookie就可以运行程序了
	# 4399需要登陆，你这边注册一个4399的账号，登陆一次，然后获取cookie换掉self.cookie就可以运行程序了
	# 4399需要登陆，你这边注册一个4399的账号，登陆一次，然后获取cookie换掉self.cookie就可以运行程序了
	spider = Spider()
	s1 = []
	with open('data.csv') as f:
		tmp = csv.reader(f)
		for i in tmp:
			if 'http' in i[2]:
				s1.append([i[2], i[0], 'P28'])
	for j in s1:
		print j[1],j[0]
		if j[1] in ['F0000254']:
			spider.get_all(j[0], j[1], j[2])
