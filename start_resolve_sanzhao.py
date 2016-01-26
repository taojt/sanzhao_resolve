# !/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Tao Jiang'

import datetime
import logging
import logging.config
import time

import constant
from init_commons import init_property, set_config
from test.test_qcwy import test_qcwy
from test.test_yingcai import test_yingcai
from test.test_zhilian import test_zhilian
from test.test_count import test_count
from convert_time import str_to_num, time_add

logging.config.fileConfig("logger.conf")
log = logging.getLogger("FatherThread")


def test():
	"""
	启动简历导入程序， 通过一个while循环每天固定时间持续导入数据
	:return:
	"""
	while True:
		try:
			log.info(u"初始化配置变量信息")
			init_property()
			log.info(u"初始化配置完成")
		except:
			log.error(u"初始化配置信息错误")
			return

		# 判断是否是启动的时间，启动时间设定是由配置文件完成
		if datetime.datetime.today().hour % 12 == int(constant.start_time):

			min_time = constant.min_time
			max_time = constant.max_time
			log.info(u"开始启动程序 时间区间为 %s -- %s  " % (min_time, max_time))
			min_time_num = str_to_num(min_time)
			max_time_num = str_to_num(max_time)
			log.info(u"当前导入简历的爬取时间区间为 %d -- %d" % (min_time_num, max_time_num))

			# 统计前一天的简历使用情况
			count_max_time_num = min_time_num
			# 判断是否是第一次， 如果是第一次导入数据，不统计
			if min_time != "1970-01-01 08:00:00":
				count_min_time = time_add(min_time, -24)
				count_min_time_num = str_to_num(count_min_time)
				log.info(u"当前统计简历数据的时间区间为 %s -- %s  " % (count_min_time, min_time))
				test_count(count_min_time_num, count_max_time_num)

			# 处理英才简历信息
			test_yingcai(min_time_num, max_time_num)

			# 处理智联简历信息
			test_zhilian(min_time_num, max_time_num)

			# 处理前程简历信息
			test_qcwy(min_time_num, max_time_num)

			try:
				log.info(u"------------- 启动修改前时间： %s -- %s ." % (constant.min_time, constant.max_time))
				constant.min_time = max_time
				constant.max_time = time_add(max_time, 12)
				set_config("min_time", constant.min_time)
				set_config("max_time", constant.max_time)
				log.info(u"------------- 修改后的时间： %s -- %s ." % (constant.min_time, constant.max_time))
			except Exception, e:
				log.error(u"--------- 修改时间错误, 错误信息 %s" % e.message)

		try:
			log.info(u"---------------------------- 程序开始休眠 .")
			time.sleep(3590)
		except Exception, e:
			log.error(u"--------- 程序休眠错误， 错误信息： %s" % e.message)


if __name__ == '__main__':
	test()
