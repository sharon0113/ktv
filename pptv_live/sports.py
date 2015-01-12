from datetime import datetime
from utils import Jsonify
from sportsModel import sportsModel
from django.db import connection
from PPTVSportsSpider import PPTVSpider

ROOT = "/m3u8/"

def get_list(request):
	cursor = connection.cursor()
	date = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	result = sportsModel(cursor).one_day_list(date)
	return Jsonify(result)
def spider(request):
	cursor = connection.cursor()
	date = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	result = PPTVSpider(cursor).runSpider(date)
	return Jsonify(result)
def read_m3u8(request):
	cursor = connection.cursor()
	vid = request.GET.get("vid", 0)
	url = sportsModel(cursor).get_url(vid)
	if url:
		fp = open("/m3u8/"+url, "r")
		content = fp.read()
	else:
		content = ""
	return Jsonify(content)
def read_ts(request):
	cursor=  connection.cursor()
	vid = request.GET.get("vid", 0)
	date =  request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	start = request.GET.get("start", 0)
	during = request.GET.get("during", 10)
	currentFeature = "start="+str(start)+"&during="+str(during)
	fp = open(ROOT+"ts/"+date+"-"+str(vid)+"-"+currentFeature+".ts", "r")
	content = fp.read()
	return Jsonify(content)
