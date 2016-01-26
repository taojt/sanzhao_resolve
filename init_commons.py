# !/usr/bin/python
# -*- coding:utf-8 -*-
import constant
import ConfigParser
import logging

log = logging.getLogger("DataUpdate")


def init_property():
	"""
	初始化变量
	:return:
	"""
	cf = ConfigParser.RawConfigParser()
	try:
		cf.read("resume_config.conf")
		constant.min_time = cf.get("resume_info", "min_time")
		constant.max_time = cf.get("resume_info", "max_time")
		constant.start_time = cf.get("resume_info", "start_time")

		constant.db_src_ip = cf.get("db_info", "db_src_ip")
		constant.db_src_port = cf.get("db_info", "db_src_port")
		constant.db_src_user = cf.get("db_info", "db_src_user")
		constant.db_src_pass = cf.get("db_info", "db_src_pass")
		constant.db_dest_ip = cf.get("db_info", "db_dest_ip")
		constant.db_dest_port = cf.get("db_info", "db_src_port")
		constant.db_dest_user = cf.get("db_info", "db_dest_user")
		constant.db_dest_pass = cf.get("db_info", "db_dest_pass")
		constant.db_qcwy = cf.get("db_info", "db_qcwy")
		constant.db_qcwy_collection = cf.get("db_info", "db_qcwy_collection")
		constant.db_zhilian = cf.get("db_info", "db_zhilian")
		constant.db_zhilian_collection = cf.get("db_info", "db_zhilian_collection")
		constant.db_yingcai = cf.get("db_info", "db_yingcai")
		constant.db_yingcai_collection = cf.get("db_info", "db_yingcai_collection")

		constant.db_dest_db = cf.get("db_info", "db_dest_db")
		constant.db_dest_collection = cf.get("db_info", "db_dest_collection")

	except:
		log.error("init propetry error !")


def set_config(config, value):
	"""
	修改变量并写回配置文件
	:param config:
	:param value:
	:return:
	"""
	cf = ConfigParser.RawConfigParser()
	try:
		cf.read("resume_config.conf")
		cf.set("resume_info", config, value)
		cf.write(open("resume_config.conf", "w"))
	except IOError:
		log.error("config file write back error !")
