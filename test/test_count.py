# !/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Tao Jiang'
from mongo_connect import *
import logging
import constant

log = logging.getLogger("CountThread")


def test_count(min_time, max_time):
	"""
	统计简历导入条数
	:param min_time:
	:param max_time:
	:return:
	"""
	dest_conn = connect(database=constant.db_dest_db, collection=constant.db_dest_collection, host=constant.db_dest_ip,
						port=constant.db_dest_port, user=constant.db_dest_user, password=constant.db_dest_pass)
	try:
		# 判断连接是否正常，连接失败抛出异常
		if dest_conn is None:
			raise pymongo.errors.ServerSelectionTimeoutError

		# 统计当前时间段内简历条数：
		count = dest_conn.count({"crawled_time": {"$gte": min_time, "$lt": max_time}})
		log.info(u"当前时间段内查找到的简历总数据条数是：" + str(count))

		count = dest_conn.count({"crawled_time": {"$gte": min_time, "$lt": max_time}, "flag": "0"})
		log.info(u"当前时间段内查找到的简历flag 为 0 时条数是：" + str(count))

		count = dest_conn.count({"crawled_time": {"$gte": min_time, "$lt": max_time}, "flag": "1"})
		log.info(u"当前时间段内查找到的简历flag 为 1 时条数是：" + str(count))

		count = dest_conn.count({"crawled_time": {"$gte": min_time, "$lt": max_time}, "status": "0"})
		log.info(u"当前时间段内查找到的简历status 为 0时的条数是：" + str(count))

		count = dest_conn.count({"crawled_time": {"$gte": min_time, "$lt": max_time}, "status": "1"})
		log.info(u"当前时间段内查找到的简历status 为 1条数是：" + str(count))

		count = dest_conn.count({"crawled_time": {"$gte": min_time, "$lt": max_time}, "status": "2"})
		log.info(u"当前时间段内查找到的简历status 为 2条数是：" + str(count))
	# 捕获mongo 连接超时 异常
	except pymongo.errors.ServerSelectionTimeoutError, e:
		log.error(u"数据库连接超时， 异常信息： %s" % e.message)
	except:
		log.error(u"统计简历条数错误")
