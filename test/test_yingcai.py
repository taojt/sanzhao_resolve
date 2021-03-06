# !/usr/bin/python
# -*- coding:utf-8 -*-

from handling_resume.handling_yingcai import handling_yingcai
from convert_time import *
from mongo_connect import *
import logging
import constant

log = logging.getLogger("YingcaiThread")


def test_yingcai(min_time, max_time):
	"""
	导入解析英才简历方法
	:param min_time:
	:param max_time:
	:return:
	"""
	src_conn = connect(database=constant.db_yingcai, collection=constant.db_yingcai_collection, host=constant.db_src_ip,
					   port=constant.db_src_port,
					   user=constant.db_src_user, password=constant.db_src_pass)
	dest_conn = connect(database=constant.db_dest_db, collection=constant.db_dest_collection, host=constant.db_dest_ip,
						port=constant.db_dest_port, user=constant.db_dest_user, password=constant.db_dest_pass)
	page = 0
	page_size = 1000
	temp = 0
	all_temp = 0
	start = datetime.datetime.now()
	try:
		# 检测mongo 连接是否正确，不正确抛出异常
		if src_conn is None:
			raise pymongo.errors.ServerSelectionTimeoutError
		# 统计当前时间段内简历条数：
		count = src_conn.count({"crawled_time": {"$gte": min_time, "$lt": max_time}})
		log.info(u"当前时间段内查找到的英才简历条数是：" + str(count))
	# 捕获mongo 连接超时 异常
	except pymongo.errors.ServerSelectionTimeoutError, e:
		log.error(u"统计英才简历条数错误，数据库连接超时， 异常信息： %s" % e.message)
	except:
		log.error(u"统计英才简历条数错误")

	while True:
		try:
			if src_conn is None:
				raise pymongo.errors.ServerSelectionTimeoutError
			# 英才简历通过爬取时间"crawled_time" 来导入
			db_cursor = src_conn.find({"crawled_time": {"$gte": min_time, "$lt": max_time}}).skip(
				page_size * page).limit(page_size)

		# 捕获mongo 连接超时 异常
		except pymongo.errors.ServerSelectionTimeoutError, e:
			log.error(u"数据库连接超时， 异常信息： %s" % e.message)
			# 暂停1小时再次检测连接是否正常
			time.sleep(3600)
			# 重新建立到数据库的连接
			src_conn = connect(database=constant.db_yingcai, collection=constant.db_yingcai_collection,
							   host=constant.db_src_ip, port=constant.db_src_port,
							   user=constant.db_src_user, password=constant.db_src_pass)
			dest_conn = connect(database=constant.db_dest_db, collection=constant.db_dest_collection,
								host=constant.db_dest_ip, port=constant.db_dest_port, user=constant.db_dest_user,
								password=constant.db_dest_pass)
			continue
		except Exception, e:
			log.error(u"读取数据出现异常， 异常信息： %s" % e.message)
			continue

		page += 1
		temp = 0
		for d in db_cursor:
			try:
				resume = {}
				resume = handling_yingcai(d)
				if resume != {}:
					cv_id = resume.get("cv_id")
					source = resume.get("source")
					if cv_id is None or source is None:
						continue
					# 调用pymongo 的update 方法，如果已有简历数据则更新覆盖，反之就插入
					# dest_conn.update({"cv_id": cv_id, "source": source}, resume, True, False)

					# 判断连接是否正常，连接失败抛出异常
					if dest_conn is None:
						raise pymongo.errors.ServerSelectionTimeoutError
					# 先判断数据库中是否有该简历， 如果有则判断该简历的name、phone、email 是否存在，以免被覆盖
					result = dest_conn.find_one({"cv_id": cv_id, "source": source})
					# 找到存在的简历
					if result is not None:
						# 若已有重复简历，需要提取出简历中的name、phone、email 字段，防止被新简历覆盖
						# 名字
						if resume.get("name") == "" and (result.get("name") != "" and result.get("name") != None):
							resume["name"] == result.get("name")
						# 电话
						if resume.get("phone") == "" and (result.get("phone") != "" and result.get("phone") != None):
							resume["phone"] == result.get("phone")
						# 邮件信息
						if resume.get("email") == "" and (result.get("email") != "" and result.get("email") != None):
							resume["email"] == result.get("email")

					# # 调用pymongo 的update 方法，如果已有简历数据则更新覆盖，反之就插入
					dest_conn.update({"cv_id": cv_id, "source": source}, resume, True, False)

			# 插入数据时 数据库连接超时
			except pymongo.errors.ServerSelectionTimeoutError, e:
				log.error(u" 插入数据时 数据库连接超时， 异常信息： %s" % e.message)
			except:
				if isinstance(resume, dict) and resume.has_key("cv_id"):
					log.error(u"英才数据解析异常， 异常数据Cv_id：%s" % resume["cv_id"])
				else:
					log.error(u"英才数据解析异常,解析过程中出现错误!")

			temp += 1
			all_temp += 1
		end = datetime.datetime.now()
		log.info(u"英才完成导入 %s 条数据，一共耗时 %d 秒 ！" % (all_temp, (end - start).seconds))
		# 判断是否是已经读取完数据，因为是分页查询的，每页1000条数据，若不满1000条则是最后的数据
		if temp % page_size != 0 or temp == 0:
			log.info(u"---------- 英才已经导入所有数据")
			break
