from datetime import datetime
from django.db import connection
from PPTVSportsSpider import PPTVSportsSpider
from Downloader import M3u8LiveDownloader
import urllib2
from time import sleep
from daemonize import Daemonize

PORT = "http://127.0.0.1:8000/"
ROOT = "/mnt/m3u8/"

lastDate = "2015-01-12"
currentDate = "2015-01-13"
InfoList = {}
cursor = connection.cursor()

def runTimer():
	while(True):
		print "run it in "+datetime.now().strftime("%T")
		starttime = datetime.now()
		lastDate = currentDate
		currentDate = datetime.now().strftime("%Y-%m-%d")
		currentTime = datetime.now().strftime("%H:%M")
		#part only newday execute
		if currentDate != lastDate:
			print "new day "+ currentDate + "started"
		#part every loop to examine
		liveList = PPTVSportsSpider(cursor).getLiveList(currentDate)
		currentInfolist = {}
		for liveUrl in liveList:
			if liveUrl in InfoList.keys():
				currentInfolist[liveUrl] = InfoList[liveUrl]
			else:
				currentInfolist[liveUrl] = set([])
				InfoList[liveUrl] = currentInfolist[liveUrl]
			currentSet = M3u8LiveDownloader(liveUrl, currentInfolist[liveUrl]).runDownloader()
			InfoList[liveUrl] = currentSet
		endtime = datetime.now()
		delta = (endtime - starttime).total_seconds()
		delta = int(delta)
		if delta < 120:
			remains = 120 - delta
			sleep(remains)
		else:
			print "WARNING: while loop runs over 2 seconds."

if __name__=='__main__':
	pid="timer.pid"
	
	keep_fds = [fh.stream.fileno()]
	# servermain()
	daemon = Daemonize(app="jobs", pid=pid, action=runTimer,keep_fds=keep_fds)
	daemon.start()
	
		



	







	






 