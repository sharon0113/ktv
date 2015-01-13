from datetime import datetime
from django.db import connection
from PPTVSportsSpider import PPTVSportsSpider
import urllib2

PORT = "http://127.0.0.1:8000/"
ROOT = "/mnt/m3u8/"

lastDate = "2015-01-11"
currentDate = "2015-01-11"

timer = set({})
infoList = []
cursor = connection.cursor()

while(True):
	lastDate = currentDate
	currentDate = datetime.now().strftime("%Y-%m-%d")
	currentTime = datetime.now().strftime("%H:%M")
	#part only newday execute
	if currentDate != lastDate:
		print "new day "+ currentDate + "started"
		timer = set({})
		request = PPTVSportsSpider(cursor).getPrecastList(currentDate)
		try:
			result = urllib2.urlopen(request)
		except Exception, e:
			print e
			print "101 day initialization error"
		if result:
			jsonList = result.loads(result)
			for json in jsonList:
				timer.add(json["starttime"])
		else:
			print "there is no live today: "+currentDate
	#part every loop to examine
	if currentTime in timer:
		#TO-DO
		currentInfoList = sportsModel(cursor).getUrlByTime(currentTime)
		for info in currentInfoList:
			infoList.append[info]

	#part every loop to execute
	for info in infoList:
		request = urllib2.Request(info["analyseUrl"], headers={
			"user-agent": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
			})
		try:
			video = urllib2.open(request)
		except Exception, e:
			print e
			print "102 video has stopped"
			#TO-EXAMINE
			infoList = infoList.remove(info)
		videoContent = video.read()
		#be consistent with DB
		fp = open("videoName.ts", "w")
		fp.write(videoContent)
		fp.close()
		fp = open("m3u8Name.m3u", "r+")
		fp.write(info["url"])
		fp.close()
		



	







	






 