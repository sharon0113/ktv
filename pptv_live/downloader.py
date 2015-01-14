# -*- coding: utf-8 -*-

import urllib2
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from django.db import connection
import os
import re

ROOT = "/mnt/m3u8live/"
PORT = "http://121.41.85.39/"
date = datetime.now().strftime("%Y-%m-%d")
M3U8PATH = "/mnt/m3u8live/m3u8/"
M3U8SUBPATH = "/mnt/m3u8live/m3u8Sub/"
M3U8NEWPATH = "/mnt/m3u8live/m3u8New/"
TSPATH = "/mnt/m3u8live/ts/"

class M3u8LiveDownloader(object):

	def __init__(self, url, downloadSet):
		super(M3u8LiveDownloader, self).__init__()
		date = datetime.now().strftime("%Y-%m-%d")
		self.liveUrl = url
		self.cursor = connection.cursor()
		request = urllib2.Request(self.liveUrl, headers={
			"user-agent": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
			})
		webPage = urllib2.urlopen(request)
		pageContent = webPage.read()
		pageContent=pageContent.replace(" ", "").replace("\t", "").replace("\n", "")
		regex = r"<scripttype=\"text/javascript\">varwebcfg={.*};</script>"
		pattern = re.compile(regex)
		matcher = pattern.search(pageContent)
		if matcher:
			soup = BeautifulSoup(matcher.group())
			webcfg = matcher.group().replace(" ", "").replace("\t", "").replace("\n", "")
			idPattern = re.compile(r"\"id\":[0-9]*")
			idValue = idPattern.search(webcfg).group()
			idValue = idValue.split(":")[1]
			kkPattern = re.compile(r"\"ctx\":\"[A-Za-z0-9%]*%3D[A-Za-z0-9-]*\"")
			kkValue = kkPattern.search(webcfg).group()
			kkValueGroup=kkValue.split("3D")
			kkValue = kkValueGroup[len(kkValueGroup)-1].strip("\"")
			self.m3u8Url = "http://web-play.pptv.com/web-m3u8-"+idValue+".m3u8?type=m3u8.web.pad&playback=0&kk="+kkValue+"&o=v.pptv.com&rcc_id=0"
		else:
			print "NOT MATCHED"
			self.m3u8Url = "urlNotExisted"
		self.name = date+"-Video:NAME_UNKNOWN"
		sportsModel(cursor).addLiveItem(self.name, date, self.liveUrl)
		self.vid = self.cursor.lastrowid
		self.vid = "101"
		self.tsDownloadSet = downloadSet

	def runDownloader(self):
		print "Downloader initializing..."
		request = urllib2.Request(self.m3u8Url, headers={
			"user-agent": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
			})
		m3u8Page = urllib2.urlopen(request)
		m3u8Content = m3u8Page.read()
		print "Downloading m3u8 level 1..."
		fp = open(M3U8PATH+date+"-"+str(self.vid)+".m3u", "w")
		fp.write(m3u8Content)
		fp.close()
		m3u8SubPattern = re.compile(r"http://[0-9.:]*/live/[0-9\/]*/[a-zA-Z0-9]*\.m3u8\?playback=[0-9]*&rcc_id=[0-9]*&pre=[a-zA-Z0-9]*&o=[a-z]*\.pptv\.com&type=m3u8\.web\.pad&kk=[a-zA-Z0-9-]*&chid=[0-9]*&k=[a-zA-Z0-9-%_]*")
		m3u8SubList = m3u8SubPattern.findall(m3u8Content)
		print str(len(m3u8SubList)) + " m3u8 urls successfully fetched, start downloading first m3u8 level 2 file..."
		resultPointer = open(M3U8NEWPATH+date+"-"+str(self.vid)+".m3u", "w") 
		resultPointer.write("""#EXTM3U\n#EXT-X-TARGETDURATION:5\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:284222306\n""")
		resultPointer.close()
		tsCount = 0
		for m3u8SubUrl in m3u8SubList:
			try:
				portPattern = re.compile(r"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*:[0-9]*")
				matcher = portPattern.search(m3u8SubUrl)
				if matcher:
					ipAddress = matcher.group()
					ipCode = ipAddress.replace(":","").replace(".","")
				else:
					ipAddress = "0.0.0.0:80"
					ipCode = "000080"
				currentRequest = urllib2.Request(m3u8SubUrl, headers={
				"user-agent": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
				})
				m3u8SubPage = urllib2.urlopen(currentRequest)
				m3u8SubContent = m3u8SubPage.read()
				fp = open(M3U8SUBPATH+date+"-"+str(self.vid)+"-"+ipCode+".m3u", "w")
				fp.write(m3u8SubContent)
				fp.close()
				tsPattern = re.compile(r"/live/[a-zA-Z0-9]*/[0-9]*.ts\?pre=ikan&o=[a-z]*.pptv.com&playback=[0-9]*&k=[a-zA-Z0-9-]*&segment=[a-zA-Z0-9_]*&type=m3u8\.web\.pad&chid=[0-9]*&kk=[a-zA-Z0-9-]*&rcc_id=[0-9]*")
				tsList = tsPattern.findall(m3u8SubContent)
				print "m3u8 level 2 successfully downloaded, "+str(len(tsList))+" ts files in total"
				for tsUrl in tsList:
					url = "http://"+ ipAddress+ tsUrl
					codePattern = re.compile(r"[0-9]*\.ts")
					matcher = codePattern.search(tsUrl)
					if matcher:
						tsCode = matcher.group().replace(".ts", "")
					else:
						tsCode = "00000X"
					if tsCode not in self.tsDownloadSet:
						request = urllib2.Request(url, headers={
							"user-agent": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
							})
						print "Downloading "+url
						tsPage = urllib2.urlopen(request)
						tsContent = tsPage.read()
						fp = open(TSPATH+date+"-"+str(self.vid)+"-"+tsCode+".ts", "w")
						fp.write(tsContent)
						fp.close()
						tsCount += 1
						self.tsDownloadSet.add(tsCode)
					else:
						print str(tsCode) +"alreadyDownloaded, pass it"
					resultPointer = open(M3U8NEWPATH+date+"-"+str(self.vid)+".m3u", "a+") 
					resultPointer.write("""#EXTINF:5,\n"""+PORT+"read_ts_live"+str(self.vid)+".ts?tsCode="+tsCode+"&vid="+str(self.vid)+"\n")
					resultPointer.close()
				break
			except Exception,e:
				print e
				print "202 sub m3u9 process error, try another one."
				continue
		print "Congratulations, download finished, "+str(tsCount)+" downloaded."
		return {"state":True, "downloadSet":self.tsDownloadSet}

		


