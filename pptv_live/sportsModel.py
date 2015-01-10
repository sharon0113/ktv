# -*- coding: utf-8 -*-

class sportsModel(object):

	def __init__(self, cursor):
		super(sportsModel, self).__init__()
		self.cursor = cursor

	def add_item(self, name, category, date, state="precast", starttime="00:00:01", endtime="23:59:59"):
		execute_String = "INSERT m3u8sports(name, date, category, state, starttime, endtime) VALUE(%s, %s, %s, %s, %s, %s)"
		self.cursor.execute(execute_String, (name, date, category, state, starttime, endtime))
		execute_String = "select max(vid) from m3u8sports"
		self.cursor.execute(execute_String)
		result = self.cursor.fetchone()
		try:
			result = result[0]
			currentUrl = "http://http://121.41.85.39/m3u8/"+"m3u8/"+date+"-"+str(result)+".m3u"
			execute_String = "UPDATE m3u8sports set url= %s where vid = %s"
			self.cursor.execute(execute_String, (currentUrl, result))
		except Exception, e:
			print e
			print "501 write resource database error"
			result = 0
		return result
	
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







