# -*- coding: utf-8 -*-
from django.db import connection
PORT = "http://127.0.0.1:8000/"

class sportsModel(object):

	def __init__(self):
		super(sportsModel, self).__init__()
		self.cursor = connection.cursor

	def add_item(self, name, category, date, state="finish", starttime="00:00", endtime="23:59"):
		execute_String = "INSERT INTO m3u8sports(name, `date`, category, state, starttime, endtime) VALUES(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\',\' {5}\')".format(name, date, category, state, starttime, endtime)
		try:
			self.cursor.execute(execute_String)
		except Exception, e:
			print e
			print "501 write resource database error"
		vid = self.cursor.lastrowid
		try:
			innerUrl = "/mnt/m3u8/m3u8New/"+date+"-"+str(vid)+".m3u"
			currentUrl = "http://121.41.85.39/pptvlive/readm3u8"+str(vid)+".m3u?vid="+str(vid)
			execute_String = "UPDATE m3u8sports set inurl= %s, url= %s where vid = %s"
			self.cursor.execute(execute_String, (innerUrl, currentUrl, vid))
		except Exception, e:
			print e
			print "501 url update error"
			vid = 0

		return vid
	
	def one_day_list(self, date):
		execute_String = "SELECT name, category, starttime, url FROM m3u8sports where date = %s"
		self.cursor.execute(execute_String, (date, ))
		itemList = self.cursor.fetchall()
		jsonList = []
		for item in itemList:
			currentJson = {}
			currentJson["name"] = item[0]
			currentJson["category"] = item[1]
			currentJson["starttime"] = item[2]
			currentJson["url"] = item[3]
			jsonList.append(currentJson)
		return jsonList

	def get_url(self, vid):
		execute_String = "SELECT inurl from m3u8sports where vid = %s"
		self.cursor.execute(execute_String, (vid, ))
		url = self.cursor.fetchone()
		if url:
			url = url[0]
		else:
			url = ""
		return url

class liveModel(object):

	def __init__(self, cursor):
		super(liveModel, self).__init__()
		self.cursor = connection.cursor

	def addLiveItem(self, name, date, url, state="live"):
		execute_String = "INSERT INTO m3u8live(name, `date`, category, state, url) VALUES(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')".format(name, date, category, state, url)
		try:
			self.cursor.execute(execute_String)
		except Exception, e:
			print e
			print "501 write resource database error"
		vid = self.cursor.lastrowid
		try:
			interface = PORT+"read_m3u8_live"+str(vid)+".m3u?vid="+str(vid)
			execute_String = "UPDATE m3u8live SET interface = %s  WHERE vid = %s"
			self.cursor.execute(execute_String, (interface, vid))
		except Exception, e:
			print e
			print "501 url update error"
			vid = 0

		return vid







