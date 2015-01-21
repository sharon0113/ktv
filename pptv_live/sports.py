from datetime import datetime
from django.http import HttpResponse
from utils import Jsonify
from sportsModel import sportsModel, liveModel
from django.db import connection
from PPTVSportsSpider import PPTVSpider
import logging
from time import sleep
logger = logging.getLogger('appserver')

ROOT = "/mnt/m3u8/"
M3U8NEWPATH = "/mnt/m3u8live/m3u8New/"
TSPATH = "/mnt/m3u8live/ts/"

def get_list(request):
	date = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	result = sportsModel().one_day_list(date)
	return Jsonify(result)

def spider(request):
	cursor = connection.cursor()
	date = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	result = PPTVSpider(cursor).runSpider(date)
	return Jsonify(result)

def read_m3u8(request):
	vid = request.GET.get("vid", 0)
	url = sportsModel().get_url(vid)
	if url:
		with open(url) as fp:
			content = fp.read()
	else:
		content = ""
	return HttpResponse(content, content_type="application/vnd.apple.mpegurl")

def read_live_m3u8(request):
	vid = request.GET.get("vid", 0)
	date = datetime.now().strftime("%Y-%m-%d")
	path = M3U8NEWPATH+date+"-"+str(vid)+".m3u"
	while(True):
		logger.debug("############DEBUG############")
		logger.debug("request for m3u8"+path+"at:  "+datetime.now().strftime("%T"))
		logger.debug("############DEBUG############")
		try:
			with open(path) as fp:
				content = fp.read()
			return HttpResponse(content, content_type="application/vnd.apple.mpegurl")
		except Exception, e:
			debug.logger(e)
			debug.logger("301 can't get ts file")
			sleep(1)
			continue

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

def read_live_ts(request):
	vid = request.GET.get("vid", "0")
	tsCode = request.GET.get("tsCode", "00000X")
	date =  request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	path = TSPATH+date+"-"+str(vid)+"-"+tsCode+".ts"
	logger.debug(datetime.now().strftime("%T"))
	while(True):
		logger.debug("############DEBUG############")
		logger.debug("request for ts"+path+"at:  "+datetime.now().strftime("%T"))
		logger.debug("############DEBUG############")
		try:
			with open(path,'rb') as fp:
				content = fp.read()
			return HttpResponse(content, content_type="video/MP2T")
		except Exception, e:
			debug.logger(e)
			debug.logger("301 can't get ts file")
			sleep(1)
			continue


def get_precast(request):
	cursor=  connection.cursor()
	date =  request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	result = PPTVSpider(cursor).getPrecastList(date)
	return Jsonify(result)

def get_current_live(request):
	date =  request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	infoList = liveModel().getLiveList(date)
	return Jsonify(infoList)
	
