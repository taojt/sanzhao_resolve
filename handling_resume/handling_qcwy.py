# !/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Tao Jiang'

from __init__ import *


def handling_qcwy(d={}):
	"""
	解析前程无忧简历的方法，最后返回解析好的dict 类型resume
	:param d:
	:return:
	"""
	resume = {"resume_id": "", "cv_id": "", "phone": "", "name": "", "email": "", "create_time": long(0),
			  "crawled_time": long(0), "update_time": "", "resume_keyword": "", "resume_img": "",
			  "self_introduction": "", "expect_city": "", "expect_industry": "", "expect_salary": "",
			  "expect_position": "", "expect_job_type": "",
			  "expect_occupation": "", "starting_date": "", "gender": "", "age": "", "degree": "",
			  "enterprise_type": "", "work_status": "", "source": "", "college_name": "",
			  "profession_name": "", "last_enterprise_name": "", "last_position_name": "",
			  "last_enterprise_industry": "",
			  "last_enterprise_time": "", "last_enterprise_salary": "", "last_year_salary": "", "hometown": "",
			  "living": "", "birthday": "", "marital_status": "", "politics": "", "work_year": "",
			  "height": "", "interests": "", "career_goal": "", "specialty": "",
			  "special_skills": "", "drive_name": "", "country": "", "osExperience": "", "status": "0",
			  "flag": "0", "dimension_flag": False, "version": [], "keyword_id": [],
			  "resumeUpdateTimeList": [], "educationList": [], "workExperienceList": [], "projectList": [],
			  "trainList": [], "certificateList": [], "languageList": [], "skillList": [], "awardList": [],
			  "socialList": [], "schoolPositionList": [], "productList": [], "scholarshipList": []}


	# 来源
	resume["source"] = "前程无忧"
	# 状态
	resume["status"] = "0"
	# 标志
	resume["flag"] = "0"
	# 标志dimension_flag
	resume["dimension_flag"] = False
	# create_time
	resume["create_time"] = long(time.time()*1000)
	
	# 简历ID
	resume["resume_id"] = str(uuid.uuid4()).replace("-", "")

	if d.has_key("resumeId"):
		resume["cv_id"] = d["resumeId"]
	else:
		resume["cv_id"] = ""

	# 最后爬取时间
	if d.has_key("last_crawled_time"):
		resume["crawled_time"] = long(d["last_crawled_time"])
	else:
		resume["crawled_time"] = ""
	# 更新时间
	if d.has_key("resumeUpdateTime"):
		resume["update_time"] = d["resumeUpdateTime"]

	# 关键字id
	if d.has_key("keyword_id"):
		resume["keyword_id"] = d["keyword_id"]

	# 更新时间列表
	if d.has_key("resumeUpdateTimeList"):
		resume["resumeUpdateTimeList"] = d["resumeUpdateTimeList"]
		if resume["update_time"] not in resume["resumeUpdateTimeList"]:
			resume["resumeUpdateTimeList"].append(resume["update_time"])

	# 居住地信息
	if d.has_key("livingArea"):
		resume["living"] = d["livingArea"].replace("-", "")

	if d.has_key("resumeContent"):
		# 通过 BeautifulSoup 读取 resumeContent 的 html内容并进行解析
		if d["resumeContent"] != "":
			re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
			# re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
			re_comment = re.compile('<!--[^>]*-->')  # HTML注释
			re_script = re.compile(r'<script[^>]*?>[\s\S]*?<\/script>', re.I)
			s = d["resumeContent"]
			s = re_style.sub("", s)
			s = re_script.sub("", s)
			s = re_comment.sub("", s)

			s = s.replace(r'\"', '')

			mainInfo = Selector(text=s).xpath("//div[@id='divResume']")
			# print mainInfo[0].extract()
			if len(mainInfo) > 0 and mainInfo[0] is not None:
				handleHtml(resume, mainInfo[0])
			else:
				resume = {}

	# 返回解析好的简历信息
	return resume


# 解析个人信息
def handlePersonInfo(resume, personInfo):
	# td = personInfo.find("td",attrs={"valign":"top"})
	td = personInfo.xpath(".//td[@valign='top']/table/tbody")

	# 查找更深入的标签，获得最基本的个人信息，年龄，生日等
	if td is not None and len(td) > 0:
		personBasicInfoElements = td[0].xpath(".//td[@height='26'][@colspan='4']/span[@class='blue']//text()")
		if personBasicInfoElements is not None and len(personBasicInfoElements) > 0:

			personBasicInfoString = personBasicInfoElements[0].extract()
			personBasicInfoStrings = personBasicInfoString.replace(u"\\u00a0", "").replace(" ", "").split(r"|")
			for info in personBasicInfoStrings:
				if info is not None and info.strip() != "":
					if u"岁" in info:
						ageInfos = info.split("（")
						if len(ageInfos) >= 2:
							if u"岁" in ageInfos[0]:
								resume["age"] = ageInfos[0].replace(u"岁", "").strip()
							if u"年" in ageInfos[1] and u"月" in ageInfos[1]:
								birth = ageInfos[1].replace("）", "")
								birth_info = re.match(u"(\d{4})年(\d{1,2})月(\d{1,2})日", birth)
								if birth_info:
									year_info = birth_info.group(1)
									mon_info = birth_info.group(2)
									day_info = birth_info.group(3)
									if len(mon_info) == 1:
										mon_info = "0" + mon_info
									if len(day_info) == 1:
										day_info = "0" + day_info
								resume["birthday"] = year_info + "-" + mon_info + "-" + day_info
					elif u"男" in info or u"女" in info:
						resume["gender"] = info.strip()
					elif u"未婚" in info or u"已婚" in info or u"保密" in info:
						resume["marital_status"] = info.strip()
					elif u"cm" in info:
						height = info.strip()
						resume["height"] = str(height).replace("cm", "")

					elif u"工作经验" in info or u"应届毕业生" in info:
						work_year = info.strip()
						resume["work_year"] = handle_work_year(work_year)

					elif u"团员" in info or u"群众" in info or u"党员" in info or u"无党" in info or u"民主党派" in info or u"其他" in info:
						resume["politics"] = info.strip()

		# 解析居住地信息
		lifeElements = td[0].xpath(".//td[@width='42%'][@height='20']//text()")
		if len(lifeElements) == 1:
			living = lifeElements[0].extract()
			if resume["living"] == "":
				resume["living"] = living.replace("-", "").strip()

		# 解析家乡信息
		hometownInfo = td[0].xpath(".//td[@width='20%'][@height='20']//text()")
		if len(hometownInfo) == 1:
			residence = hometownInfo[0].extract()
			resume["hometown"] = residence.strip()


# 解析最后一份工作信息
def handleLastWorkInfo(resume, lastWorkInfo):
	timeinfo = lastWorkInfo.xpath(".//span[contains(@style,'color:#676767;')]//text()")
	if len(timeinfo) > 0:
		work_time = timeinfo[0].extract().replace("[", "").replace("]", "").strip()
		resume["last_enterprise_time"] = handle_work_year(work_time)

	lastCompanyInfos = lastWorkInfo.xpath(".//tr")
	for com in lastCompanyInfos:
		# print com.extract()
		if len(com.xpath("string(.)")) > 0:
			info = com.xpath("string(.)").extract()[0]
			if u"公　司" in info:
				enterprise_name = com.xpath(".//td[@width='230']//text()")
				if len(enterprise_name) > 0:
					resume["last_enterprise_name"] = enterprise_name[0].extract().replace("#→start→#", "").replace(
						"#←end←#", "").strip()
			elif u"职　位" in info:
				position_name = com.xpath(".//td//text()").extract()
				if len(position_name) > 1:
					resume["last_position_name"] = position_name[1].replace("#→start→#", "").replace("#←end←#",
																									 "").strip()
			elif u"行　业" in info:
				industry_name = com.xpath(".//td//text()").extract()
				if len(industry_name) > 1:
					resume["last_enterprise_industry"] = industry_name[1].replace("#→start→#", "").replace("#←end←#",
																										   "").strip()


# 解析最高教育学历信息
def handlelastEducationInfo(resume, lastEducationInfo):
	educations = lastEducationInfo.xpath(".//tr")
	for edu in educations:
		if len(edu.xpath("string(.)").extract()) > 0:
			info = edu.xpath("string(.)").extract()[0]
			if u"学　历" in info:
				educationStr = edu.xpath("td[@width='230']//text()").extract()
				if len(educationStr) > 0:
					resume["degree"] = educationStr[0].strip()

			elif u"学　校" in info:
				educationStr = edu.xpath("td//text()").extract()
				if len(educationStr) > 1:
					resume["college_name"] = educationStr[1].strip()
			elif u"专　业" in info:
				educationStr = edu.xpath("td//text()").extract()
				if len(educationStr) > 1:
					resume["profession_name"] = educationStr[1].replace("#→start→#", "").replace(
						"#←end←#", "").strip()


# 解析自我评价
def handleSelfBrief(resume, info):
	introInfos = info.xpath(".//span//text()")
	if len(introInfos) > 0:
		resume["self_introduction"] = introInfos[0].extract().strip()
		keywords = info.xpath(".//div[@class='keydiv']//text()")
		s = ""
		for key in keywords:
			s = s + key.extract().strip() + ";"
		resume["resume_keyword"] = s.replace("#→start→#", "").replace(
			"#←end←#", "").strip().strip(";")


# 解析求职意向
def handleIntentInfo(resume, info):
	intentInfos = info.xpath(".//td[@class='text_left']")
	if len(intentInfos) > 0:
		for intent in intentInfos:
			intentText = intent.xpath("string(.)")
			if len(intentText) > 0:
				temp = intentText[0].extract()
			if u"到岗时间" in temp:
				s = temp.split(u"：")
				if len(s) == 2:
					resume["starting_date"] = s[1].strip()
			elif u"工作性质" in temp:
				s = temp.split(u"：")
				if len(s) == 2:
					resume["expect_job_type"] = s[1].strip()
			elif u"希望行业" in temp:
				s = temp.split(u"：")
				if len(s) == 2:
					resume["expect_industry"] = s[1].strip().replace(u"，", ",").replace("#→start→#", "").replace(
						"#←end←#", "").strip()
			elif u"目标地点" in temp:
				s = temp.split(u"：")
				if len(s) == 2:
					resume["expect_city"] = s[1].strip().replace(u"，", ";")
			elif u"期望月薪" in temp:
				s = temp.split(u"：")
				if len(s) == 2:
					if u"不显示" in s[1]:
						resume["expect_salary"] = u"面议"
					else:
						salary = s[1].strip()
						resume["expect_salary"] = handle_salary(salary)
			elif u"目标职能" in temp:
				s = temp.split(u"：")
				if len(s) == 2:
					resume["expect_position"] = s[1].strip().replace(u"，", ",").replace("#→start→#", "").replace(
						"#←end←#", "").strip()
			elif u"求职状态" in temp:
				s = temp.split(u"：")
				if len(s) == 2:
					resume["work_status"] = s[1].strip()


# 解析工作经验
def handleWorkExpe(resume, tableInfo):
	positionList = []
	industryList = []
	workTimeList = []
	basicInfoList = []
	departList = []
	descList = []
	basicInfo = tableInfo.xpath(".//td[@colspan='2'][@class='text_left']")
	for basic in basicInfo:
		x = basic.xpath(".//b")
		if len(x) > 0:
			workTimeList.append(x.xpath("string(.)")[0].extract())
			basicInfoList.append(basic.xpath("text()")[0].extract())
		else:
			descList.append(basic.xpath("string(.)")[0].extract())

	indusInfo = tableInfo.xpath(".//td[@width='78%']//text()")
	for indus in indusInfo:
		industryList.append(indus.extract())

	departInfo = tableInfo.xpath(".//td[@class='text_left']/b//text()")
	for depart in departInfo:
		departList.append(depart.extract())
	positionInfo = tableInfo.xpath(".//td[@class='text']/b//text()")
	for posi in positionInfo:
		positionList.append(posi.extract())

	for i in range(len(basicInfoList)):
		workList = {"enterprise_name": "", "position_name": "", "experience_desc": "", "start_date": "", "end_date": "",
					"enterprise_size": "", "work_time": "", "enterprise_industry": "", "department": "", "salary": "",
					"first_job_type": "", "second_job_type": ""}
		s1 = basicInfoList[i].split("：")
		if len(s1) == 2:
			s2 = s1[0].split("--")
			if len(s2) == 2:
				start = s2[0].strip()
				start_temp = re.match("(\d{4}) /(\d{1,2})", start)
				if start_temp:
					year_info = start_temp.group(1)
					month_info = start_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					start = year_info + "-" + month_info
				workList["start_date"] = start
				end = s2[1].strip()
				end_temp = re.match("(\d{4}) /(\d{1,2})", end)
				if end_temp:
					year_info = end_temp.group(1)
					month_info = end_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					end = year_info + "-" + month_info
				workList["end_date"] = end
			s3 = s1[1].split("(")
			if len(s3) > 0:
				workList["enterprise_name"] = s3[0].strip()
			if len(s3) > 1:
				workList["enterprise_size"] = s3[1].replace(")", "").strip()
		if len(workTimeList) > i:
			s = workTimeList[i].replace("[", "").replace("]", "").strip()
			work_time = s
			workList["work_time"] = handle_work_year(work_time)
		if len(descList) > i:
			workList["experience_desc"] = descList[i].strip()
		if len(industryList) > i:
			workList["enterprise_industry"] = industryList[i].strip()
		if len(departList) > i:
			workList["department"] = departList[i].strip()
		if len(positionList) > i:
			workList["position_name"] = positionList[i].strip()

		resume["workExperienceList"].append(workList)


# 处理教育经历信息
def handleEducation(resume, tableInfo):
	# print tableInfo.extract()
	eduElements = tableInfo.xpath(".//tr")
	eduList = {"start_date": "", "end_date": "", "degree": "", "college_name": "", "profession_name": "", "desc": ""}

	for eduEle in eduElements:
		if len(eduEle.xpath(".//hr")) > 0:
			resume["educationList"].append(eduList)
			eduList = {"start_date": "", "end_date": "", "degree": "", "college_name": "", "profession_name": "",
					   "desc": ""}
			continue
		times = eduEle.xpath(".//td[@width='26%']//text()")
		if len(times) > 0:
			s = times[0].extract()
			s1 = s.split("--")
			if len(s1) == 2:
				start = s1[0].strip()
				start_temp = re.match("(\d{4}) /(\d{1,2})", start)
				if start_temp:
					year_info = start_temp.group(1)
					month_info = start_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					start = year_info + "-" + month_info
				eduList["start_date"] = start
				end = s1[1].strip()
				end_temp = re.match("(\d{4}) /(\d{1,2})", end)
				if end_temp:
					year_info = end_temp.group(1)
					month_info = end_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					end = year_info + "-" + month_info

				eduList["end_date"] = end
		college = eduEle.xpath(".//td[@width='30%']//text()")
		if len(college) > 0:
			eduList["college_name"] = college[0].extract().strip()
		if len(college) > 1:
			eduList["profession_name"] = college[1].extract().strip()
			eduList["profession_name"] = eduList["profession_name"].replace("#→start→#", "").replace(
						"#←end←#", "").strip()
		degree = eduEle.xpath(".//td[@width='14%']//text()")
		if len(degree) > 0:
			eduList["degree"] = degree[0].extract().strip()
		desc = eduEle.xpath(".//td[@class='text_left']//text()")
		if len(desc) > 0:
			s = desc[0].extract().strip()
			if re.match("\d{4}", s):
				eduList["desc"] = ""
			else:
				eduList["desc"] = s

	resume["educationList"].append(eduList)


# 处理获奖信息
def handleAward(resume, tableInfo):
	# print tableInfo.extract()
	awardList = {"time": "", "award_name": "", "award_level": ""}
	awardElements = tableInfo.xpath(".//tr")
	for awardEle in awardElements:
		# print awardEle
		if len(awardEle.xpath(".//hr")) > 0:
			resume["awardList"].append(awardList)
			awardList = {"time": "", "award_name": "", "award_level": ""}
			continue
		times = awardEle.xpath(".//td[@class='text_left']//text()")

		if len(times) > 0:
			start = times[0].extract().strip()
			start_temp = re.match("(\d{4}) /(\d{1,2})", start)
			if start_temp:
				year_info = start_temp.group(1)
				month_info = start_temp.group(2)
				if len(month_info) == 1:
					month_info = "0" + month_info
				start = year_info + "-" + month_info
			awardList["time"] = start
		name = awardEle.xpath(".//td[@class='text']//text()")
		if len(name) > 0:
			awardList["award_name"] = name[0].extract().strip()
		if len(name) > 1:
			awardList["award_level"] = name[1].extract().strip()
	resume["awardList"].append(awardList)


# 处理社会经验信息
def handleSocial(resume, tableInfo):
	timeList = []
	nameList = []
	descList = []

	timeEle = tableInfo.xpath(".//td[@width='25%']/text()")
	if len(timeEle) > 0:
		for i in range(len(timeEle)):
			timeList.append(timeEle[i].extract())

	nameEle = tableInfo.xpath(".//td[@class='text']/text()")
	if len(nameEle) > 0:
		for i in range(len(nameEle)):
			nameList.append(nameEle[i].extract())

	descEle = tableInfo.xpath(".//td[@colspan='2'][@class='text_left']/text()")
	if len(descEle) > 0:
		for i in range(len(descEle)):
			descList.append(descEle[i].extract())

	for i in range(len(nameList)):
		s = {"start_time": "", "end_time": "", "social_name": "", "social_desc": ""}
		s["social_name"] = nameList[i].strip()
		if len(timeList) > i:
			time_temp = timeList[i]
			temp = time_temp.split("--")
			if len(temp) == 2:
				start = temp[0].strip()
				start_temp = re.match("(\d{4}) /(\d{1,2})", start)
				if start_temp:
					year_info = start_temp.group(1)
					month_info = start_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					start = year_info + "-" + month_info
				s["start_time"] = start
				end = temp[1].strip()
				end_temp = re.match("(\d{4}) /(\d{1,2})", end)
				if end_temp:
					year_info = end_temp.group(1)
					month_info = end_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					end = year_info + "-" + month_info

				s["end_time"] = end

		if len(descList) > i:
			s["social_desc"] = descList[i].strip()
		resume["socialList"].append(s)


# 校内职务信息
def handleSchoolPosition(resume, tableInfo):
	schoolList = {"start_time": "", "end_time": "", "position_name": "", "position_desc": ""}
	schoolElements = tableInfo.xpath(".//tr")
	for schEle in schoolElements:
		# print awardEle
		if len(schEle.xpath(".//hr")) > 0:
			resume["schoolPositionList"].append(schoolList)
			schoolList = {}
			continue
		times = schEle.xpath(".//td[@width='25%']//text()")

		if len(times) > 0:
			s = times[0].extract().strip()
			s1 = s.split("--")
			if len(s1) == 2:
				start = s1[0].strip()
				start_temp = re.match("(\d{4}) /(\d{1,2})", start)
				if start_temp:
					year_info = start_temp.group(1)
					month_info = start_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					start = year_info + "-" + month_info
				schoolList["start_time"] = start
				end = s1[1].strip()
				end_temp = re.match("(\d{4}) /(\d{1,2})", end)
				if end_temp:
					year_info = end_temp.group(1)
					month_info = end_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					end = year_info + "-" + month_info

				schoolList["end_time"] = end
		name = schEle.xpath(".//td[@class='text']//text()")
		if len(name) > 0:
			schoolList["position_name"] = name[0].extract().strip()
		desc = schEle.xpath(".//td[@colspan='2']")
		if len(desc) > 0:
			desc_temp = desc[0].xpath("string(.)")
			if len(desc_temp) > 0:
				schoolList["position_desc"] = desc_temp[0].extract().strip()
	resume["schoolPositionList"].append(schoolList)


# 处理项目经历信息
def handleProject(resume, tableInfo):
	trElements = tableInfo.xpath(".//tr")
	proList = {"start_date": "", "end_date": "", "project_name": "", "project_desc": "", "work_desc": "", "tools": "",
			   "software": "", "hardware": ""}
	for trEle in trElements:

		if len(trEle.xpath(".//hr")) > 0:
			resume["projectList"].append(proList)
			proList = {"start_date": "", "end_date": "", "project_name": "", "project_desc": "", "work_desc": "",
					   "tools": "", "software": "", "hardware": ""}
			continue
		time = trEle.xpath(".//td[@colspan='2'][@class='text_left']//text()")
		if len(time) > 0:
			s = time[0].extract()
			s1 = s.split(u"：")
			if len(s1) > 0:
				s2 = s1[0].split("--")
				if len(s2) == 2:
					start = s2[0].strip()
					start_temp = re.match("(\d{4}) /(\d{1,2})", start)
					if start_temp:
						year_info = start_temp.group(1)
						month_info = start_temp.group(2)
						if len(month_info) == 1:
							month_info = "0" + month_info
						start = year_info + "-" + month_info
						proList["start_date"] = start
					end = s2[1].strip()
					end_temp = re.match("(\d{4}) /(\d{1,2})", end)
					if end_temp:
						year_info = end_temp.group(1)
						month_info = end_temp.group(2)
						if len(month_info) == 1:
							month_info = "0" + month_info
						end = year_info + "-" + month_info

					proList["end_date"] = end
			if len(s1) > 1:
				proList["project_name"] = s1[1].strip()
		titles = trEle.xpath(".//td[@class='text_left'][@valign='top']//text()")
		if len(titles) > 0:
			title = titles[0].extract()
			if u"项目描述" in title:
				desc = trEle.xpath(".//td[@class='text']")
				if len(desc) > 0:
					proList["project_desc"] = desc[0].xpath("string(.)")[0].extract().replace("<[^b][^<>]*>",
																							  "").strip()
			elif u"责任描述" in title:
				desc = trEle.xpath(".//td[@class='text']")
				if len(desc) > 0:
					proList["work_desc"] = desc[0].xpath("string(.)")[0].extract().replace("<[^b][^<>]*>", "").strip()
			elif u"软件环境" in title:
				desc = trEle.xpath(".//td[@class='text']")
				if len(desc) > 0:
					proList["software"] = desc[0].xpath("string(.)")[0].extract().replace("<[^b][^<>]*>", "").strip()
			elif u"硬件环境" in title:
				desc = trEle.xpath(".//td[@class='text']")
				if len(desc) > 0:
					proList["hardware"] = desc[0].xpath("string(.)")[0].extract().replace("<[^b][^<>]*>", "").strip()
			elif u"开发工具" in title:
				desc = trEle.xpath(".//td[@class='text']")
				if len(desc) > 0:
					proList["tools"] = desc[0].xpath("string(.)")[0].extract().replace("<[^b][^<>]*>", "").strip()
	resume["projectList"].append(proList)


# 培训经历
def handleTrain(resume, tableInfo):
	trainList = {"start_date": "", "end_date": "", "train_name": "", "train_school": "", "train_desc": "",
				 "train_certificate": ""}
	trainElements = tableInfo.xpath(".//tr")
	for trainEle in trainElements:
		# print awardEle
		if len(trainEle.xpath(".//hr")) > 0:
			resume["trainList"].append(trainList)
			trainList = {"start_date": "", "end_date": "", "train_name": "", "train_school": "", "train_desc": "",
						 "train_city": "", "train_certificate": ""}
			continue

		times = trainEle.xpath(".//td[@width='20%'][@class='text_left']//text()")
		if len(times) > 0:
			s = times[0].extract().strip().strip(u"：")
			s1 = s.split("--")
			if len(s1) == 2:
				start = s1[0].strip()
				start_temp = re.match("(\d{4}) /(\d{1,2})", start)
				if start_temp:
					year_info = start_temp.group(1)
					month_info = start_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					start = year_info + "-" + month_info
				trainList["start_date"] = start
				end = s1[1].strip()
				end_temp = re.match("(\d{4}) /(\d{1,2})", end)
				if end_temp:
					year_info = end_temp.group(1)
					month_info = end_temp.group(2)
					if len(month_info) == 1:
						month_info = "0" + month_info
					end = year_info + "-" + month_info

				trainList["end_date"] = end
		name = trainEle.xpath(".//td[@width='29%']//text()")
		if len(name) > 0:
			trainList["train_school"] = name[0].extract().strip()
			trainList["train_city"] = ""

		if len(name) > 1:
			trainList["train_name"] = name[1].extract().strip()
		cert = trainEle.xpath(".//td[@width='22%']//text()")
		if len(cert) > 0:
			trainList["train_certificate"] = cert[0].extract().strip()
		desc = trainEle.xpath(".//td[@colspan='4']//text()")
		if len(desc) > 0:
			trainList["train_desc"] = desc[0].extract().strip()
	resume["trainList"].append(trainList)


# 证书信息
def handleCertificate(resume, tableInfo):
	certList = {"get_time": "", "certificate_name": "", "certificate_score": ""}
	certElements = tableInfo.xpath(".//tr")
	for certEle in certElements:
		# print awardEle
		if len(certEle.xpath(".//hr")) > 0:
			resume["certificateList"].append(certList)
			certList = {"get_time": "", "certificate_name": "", "certificate_score": ""}
			continue

		times = certEle.xpath(".//td[@width='18%']//text()")
		if len(times) > 0:
			start = times[0].extract().strip()
			start_temp = re.match("(\d{4}) /(\d{1,2})", start)
			if start_temp:
				year_info = start_temp.group(1)
				month_info = start_temp.group(2)
				if len(month_info) == 1:
					month_info = "0" + month_info
				start = year_info + "-" + month_info
			certList["get_time"] = start

		name = certEle.xpath(".//td[@width='52%']//text()")
		if len(name) > 0:
			certList["certificate_name"] = name[0].extract().strip()
			certList["certificate_school"] = ""
		cert = certEle.xpath(".//td[@width='30%']//text()")
		if len(cert) > 0:
			certList["certificate_score"] = cert[0].extract().strip()
	resume["certificateList"].append(certList)


# 语言能力
def handleLanguageSkill(resume, tableInfo):
	langElements = tableInfo.xpath(".//tr")
	for langEle in langElements:
		langList = {"language_name": "", "language_ability": "", }
		name = langEle.xpath(".//td[@width='130']//text()")

		if len(name) > 0:
			langList["language_name"] = name[0].extract().strip()
			if u"等级：" in langList["language_name"]:
				langList["language_name"] = langList["language_name"].replace(u"等级：", "")

		ability = langEle.xpath(".//td[@class = 'text']//text()")
		if len(ability) > 0:
			langList["language_ability"] = ability[0].extract().strip()
			langList["language_type"] = ""

		resume["languageList"].append(langList)


# IT 技能
def handleSkill(resume, tableInfo):
	skillElements = tableInfo.xpath(".//tr")
	for i in range(1, len(skillElements)):
		skillList = {"skill_name": "", "skill_ability": "", "skill_time": ""}
		name = skillElements[i].xpath(".//td[@class ='text_left']//text()")
		if len(name) > 0:
			skillList["skill_name"] = name[0].extract().strip()

		ability = skillElements[i].xpath(".//td[@class = 'text']//text()")
		if len(ability) > 0:
			skillList["skill_ability"] = ability[0].extract().strip()
		if len(ability) > 1:
			skillList["skill_time"] = ability[1].extract().strip()

		if skillList != {"skill_name": "", "skill_ability": "", "skill_time": ""}:
			resume["skillList"].append(skillList)


# 其他信息
def handleOther(resume, tableInfo):
	otherElements = tableInfo.xpath(".//tr")
	for i in range(len(otherElements)):
		otherList = {}
		name = otherElements[i].xpath(".//td[@width ='16%']//text()")
		temp = otherElements[i].xpath(".//td[@width ='86%']//text()")
		if len(name) > 0 and len(temp) > 0:
			info = name[0].extract()
			if u"特长" in info:
				resume["specialty"] = temp[0].extract().strip()
			elif u"兴趣爱好" in info:
				resume["interests"] = temp[0].extract().strip()
			elif u"职业目标" in info:
				resume["career_goal"] = temp[0].extract().strip()
			elif u"特殊技能" in info:
				resume["special_skills"] = temp[0].extract().strip()


# 解析简历内容信息模块
def handleHtml(resume, soup):
	# 解析个人信息模块
	# 年龄
	resume["age"] = ""
	# 出生日期
	resume["birthday"] = ""
	# 性别
	resume["gender"] = ""
	# 婚姻状态
	resume["marital_status"] = ""
	# 身份，如团员，党员等
	resume["politics"] = ""
	# 身高
	resume["height"] = ""
	# 工作时间
	resume["work_year"] = ""

	# 获取个人信息
	personInfo = soup.xpath(
		".//table[contains(@style,'margin-top:3px;padding:8px 0 0 8px;background:#f5f9fd;border:1px solid #88b4e0;line-height:22px;')]")
	# print personInfo[0].extract()
	if len(personInfo) > 0:
		handlePersonInfo(resume, personInfo[0])

	# 解析最后一份工作信息
	lastWorkInfos = soup.xpath(".//table[contains(@style, 'margin:8px auto;line-height:22px;padding:0 0 0 8px;')]")
	# print len(lastWorkInfos)
	if len(lastWorkInfos) > 0:
		handleLastWorkInfo(resume, lastWorkInfos[0])


	# 解析最高教育学历信息
	lastEducationInfos = soup.xpath(".//table[contains(@style,'margin:8px auto;line-height:22px;padding:0 0 0 10px;')]")
	if len(lastEducationInfos) > 0:
		handlelastEducationInfo(resume, lastEducationInfos[0])

	# 解析主要简历信息
	informationResume = soup.xpath(".//td[@id= 'divInfo']")
	if informationResume is not None and len(informationResume) > 0:

		# print informationResume[0].extract()
		# 最近工作年薪
		lastYearSalary = informationResume[0].xpath(
			".//table[contains(@style, 'margin:8px auto;line-height:20px;padding:0 0 0 8px;')]")
		if len(lastYearSalary) > 0:
			lastYearSalaryElements = lastYearSalary[0].xpath(".//td[@width='221']//text()")
			if len(lastYearSalaryElements) > 0:
				salary = lastYearSalaryElements[0].extract()
				resume["last_year_salary"] = salary.strip().replace(u"年薪", "").replace(u"人民币", "")


		# 获取简历各个模块的信息
		information = informationResume[0].xpath(".//table")
		for info in information:
			cvTitle = info.xpath(".//td[@class= 'cvtitle']")
			if len(cvTitle) <= 0:
				continue
			else:
				cv = cvTitle[0]
				if len(cv.xpath("string(.)")) > 0:
					introInfo = cv.xpath("string(.)").extract()[0]
					if u"自我评价" in introInfo:
						handleSelfBrief(resume, info)
					elif u"求职意向" in introInfo:
						handleIntentInfo(resume, info)
					else:
						handleWorkExpAndEdu(resume, info)


def handleWorkExpAndEdu(resume, information):
	# print information.extract()
	# 获取标题的标签
	title = information.xpath(".//td[@class='cvtitle']")
	# 获取标题对应的信息标签
	infos = information.xpath(".//table[@class='table_set']")

	# 标记位，使标题与信息主体对应
	if len(title) != len(infos):
		return

	for i in range(len(title)):
		titleStr = title[i].xpath("string(.)")
		if len(titleStr) > 0:
			temp = titleStr[0].extract()
			if u"工作经验" in temp:
				handleWorkExpe(resume, infos[i])
			elif u"项目经验" in temp:
				handleProject(resume, infos[i])
			elif u"教育经历" in temp:
				handleEducation(resume, infos[i])
			elif u"所获奖项" in temp:
				handleAward(resume, infos[i])
			elif u"校内职务" in temp:
				handleSchoolPosition(resume, infos[i])
			elif u"培训经历" in temp:
				handleTrain(resume, infos[i])
			elif u"证书" in temp:
				handleCertificate(resume, infos[i])
			elif u"语言能力" in temp:
				handleLanguageSkill(resume, infos[i])
			elif u"IT 技能" in temp:
				handleSkill(resume, infos[i])
			elif u"社会经验" in temp:
				handleSocial(resume, infos[i])
			elif u"其他信息" in temp:
				handleOther(resume, infos[i])
