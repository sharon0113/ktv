from datetime import datetime
from utils import Jsonify
from sportsModel import sportsModel
from django.db import connection
from PPTVSportsSpider import PPTVSpider


def get_list(request):
	cursor = connection.cursor()
	date = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	result = sportsModel(cursor).one_day_list(date)
	return Jsonify(result)
def spider(request):
	cursor = connection.cursor()
	date = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
	PPTVSpider(cursor).runSpider(date)
