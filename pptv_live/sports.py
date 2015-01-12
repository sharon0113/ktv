from datetime import datetime
from django.http import HttpResponse
from utils import Jsonify
from sportsModel import sportsModel
from django.db import connection
from PPTVSportsSpider import PPTVSpider

ROOT = "/mnt/m3u8/"

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
		with open(url) as fp:
			content = fp.read()
	else:
		content = ""
	return HttpResponse(content, content_type="application/vnd.apple.mpegurl")
def read_ts(request):
	cursor=  connection.cursor()
	vid = request.GET.get("vid", 0)
	date =  request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	start = request.GET.get("start", 0)
	during = request.GET.get("during", 10)
	currentFeature = "start="+str(start)+"&during="+str(during)
	path = ROOT+"ts/"+date+"-"+str(vid)+"-"+currentFeature+".ts"
	with open(path,'rb') as fp:
		content = fp.read()
		return HttpResponse(content, content_type="video/MP2T")
	# fp = open(, "r")
	# return Jsonify(content)
