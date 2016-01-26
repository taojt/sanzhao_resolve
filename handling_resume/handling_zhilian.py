# !/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Tao Jiang'

from __init__ import *


def handling_zhilian(d={}):
	"""
	解析智联简历的方法，最后返回解析好的dict 类型resume
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

	"""
	简历resume 对象属性的默认值
	设置默认值的作用是保证与数据库中其他数据类型的数据格式进行统一化
	"""
	# 来源
	resume["source"] = u"智联"
	# 状态
	resume["status"] = "0"
	# 标志
	resume["flag"] = "0"

	# dimension_flag
	resume["dimension_flag"] = False

	# 设置 简历id
	resume["resume_id"] = str(uuid.uuid4()).replace("-", "")
	# 设置 cv_id
	if d.has_key("CvId"):
		resume["cv_id"] = d["CvId"]
	
	# create_time
	resume["create_time"] = long(time.time()*1000)
	
	# 最后爬取时间
	if d.has_key("Crawled_timestamp"):
		if d["Crawled_timestamp"] != 0:
			resume["crawled_time"] = long(d["Crawled_timestamp"])
		elif d.has_key("Crawled_time"):
			s = d["Crawled_time"]
			if re.match(r"\d{4}-\d{2}-\d{2}", s):
				timeStr = time.strptime(s, "%Y-%m-%d")
				timeStamp = time.mktime(timeStr) * 1000
				resume["crawled_time"] = long(timeStamp)

	# 更新时间
	if d.has_key("RefreshDate"):
		if re.match(r'\d{2}-\d{2}-\d{2}', d["RefreshDate"]):
			resume["update_time"] = "20" + d["RefreshDate"]
	if resume["update_time"] == "2000-00-00":
		if d.has_key("Crawled_time") and d["Crawled_time"] != "":
			resume["update_time"] = d["Crawled_time"]

	# 更新时间列表
	if d.has_key("RefreshDateList"):
		temp = []
		for i in range(len(d["RefreshDateList"])):
			if re.match(r'\d{2}-\d{2}-\d{2}', d["RefreshDateList"][i]):
				temp.append("20" + d["RefreshDateList"][i])

		if resume["update_time"] not in temp:
			temp.append(resume["update_time"])
		resume["resumeUpdateTimeList"] = temp

	# 关键字id
	if d.has_key("Keyword_id"):
		resume["keyword_id"] = d["Keyword_id"]

	# 解析简历主要内容，格式为杂乱html
	if d.has_key("RawHtml") and d["RawHtml"] != "":
		# 判断html 字符串是否存在，如果存在就调用下面方法进行html 相关解析
		# soup = BeautifulSoup(d["RawHtml"], "html5lib")
		try:
			soup = BeautifulSoup(d["RawHtml"], "lxml")
		except:
			soup = BeautifulSoup(d["RawHtml"], "html5lib")
		finally:
			if soup != None:
				# temps = 0
				# 若内容不为空，则按照源数据中的content内容，分为各个模块对数据进行解析
				handleHtml(resume, soup)
			else:
				resume = {}

	# 处理最后一份工作信息
	if len(resume["workExperienceList"]) > 0:
		resume["last_enterprise_industry"] = resume["workExperienceList"][0].get("enterprise_industry")
		resume["last_enterprise_name"] = resume["workExperienceList"][0].get("enterprise_name")
		# 最后一份工作
		salary = resume["workExperienceList"][0].get("salary")
		resume["last_enterprise_salary"] = handle_salary(salary)
		work_time = resume["workExperienceList"][0].get("work_time")
		resume["last_enterprise_time"] = handle_work_year(work_time)
		resume["last_position_name"] = resume["workExperienceList"][0].get("position_name")

	# 处理最后教育信息
	if len(resume["educationList"]) > 0:
		for i in range(len(resume["educationList"])):
			if resume["college_name"] == "":
				resume["college_name"] = resume["educationList"][i].get("college_name")
			if resume["profession_name"] == "":
				resume["profession_name"] = resume["educationList"][i].get("profession_name")
			if resume["degree"] == "":
				resume["degree"] = resume["educationList"][i].get("degree")

	# 返回解析好的简历 resume
	return resume


# 处理简历主要信息
def handleHtml(resume, soup):
	if soup.find("div", {"class": "summary"}) != None:
		summary = soup.find("div", {"class": "summary"})
		if summary.find("img") != None and summary.find("img").get("src") != None:
			# 设置图片网址
			resume["resume_img"] = summary.find("img").get("src")
		else:
			resume["resume_img"] = ""
		if summary.find("div", {"class": "summary-top"}) != None:
			# 处理个人基本信息
			personInfo = summary.find("div", {"class": "summary-top"})
			handlePersonalInfo(resume, personInfo)

	eDivs = soup.find_all("div", {"class": "resume-preview-all"})
	if isinstance(eDivs, list):
		for i in range(len(eDivs)):
			if eDivs[i].find("h3", {"class": "fc6699cc"}) != None:
				infoText = eDivs[i].find("h3", {"class": "fc6699cc"}).text
				divInfo = eDivs[i]
				if u"求职意向" in infoText:
					# 处理求职意向
					handleCareerInfo(resume, divInfo)
				elif u"自我评价" in infoText:
					# 处理自我评价
					handleSelfIntro(resume, divInfo)
				elif u"工作经历" in infoText:
					# 处理工作经历
					handleWorkExp(resume, divInfo)
				elif u"项目经历" in infoText:
					# 处理项目经历
					handleProject(resume, divInfo)
				elif u"教育经历" in infoText:
					# 处理教育经历
					handleEducation(resume, divInfo)
				elif u"培训经历" in infoText:
					# 处理培训经历
					handleTrain(resume, divInfo)
				elif u"语言能力" in infoText:
					# 处理语言能力
					handleLanguage(resume, divInfo)
				elif u"专业技能" in infoText:
					# 处理专业技能
					handleSkill(resume, divInfo)
				elif u"证书" in infoText:
					# 处理证书
					handleCertificate(resume, divInfo)
				elif u"在校学习情况" in infoText:
					# 处理在校获奖情况
					handleSchoolAward(resume, divInfo)
				elif u"在校实践经验" in infoText:
					# 处理在校实践经验
					handleSocial(resume, divInfo)
				elif u"特长职业目标" in infoText:
					# 处理特长职业目标
					handleCareerGoal(resume, divInfo)
				elif u"兴趣爱好" in infoText:
					# 处理兴趣爱好
					handleInterests(resume, divInfo)
				elif u"特殊技能" in infoText:
					# 处理特殊技能
					handleSpecialSkill(resume, divInfo)


# 处理个人基本信息
def handlePersonalInfo(resume, personInfo):
	if personInfo.find("span") != None and personInfo.span.get_text() != "":
		info = personInfo.span.get_text().split(u"    ")
		if isinstance(info, list):
			for i in range(len(info)):
				if u"男" in info[i] or u"女" in info[i]:
					resume["gender"] = info[i].strip()
				elif u"岁" in info[i]:
					temp = info[i].split(u"(")
					if len(temp) >= 1:
						# 设置年龄
						resume["age"] = temp[0].replace(u"岁", "")
					if len(temp) >= 2:
						# 设置生日
						birth = temp[1][:-1]
						birth_temp = re.match(u"(\d{4})年(\d*)月", birth)
						if birth_temp:
							year_info = birth_temp.group(1)
							month_info = birth_temp.group(2)
							if len(month_info) == 1:
								month_info = "0" + month_info
							s = year_info + "-" + month_info
							if re.match("\d{4}-\d{2}", s):
								resume["birthday"] = s
				elif u"工作经验" in info[i] or u"应届" in info[i]:
					# 设置工作时间
					work_year = info[i].strip()
					resume["work_year"] = handle_work_year(work_year)
				elif u"已婚" in info[i] or u"未婚" in info[i]:
					# 设置婚姻状态
					resume["marital_status"] = info[i].strip()
				else:
					resume["degree"] = info[i].strip()

		address = personInfo.text.split("\n")
		if isinstance(address, list) and len(address) >= 3:
			info = address[2].split("|")
			if isinstance(info, list):
				for i in range(len(info)):
					if u"现居住地" in info[i]:

						living = info[i].split(u"：")[1].strip()
						resume["living"] = living.replace(" ", "")
					elif u"户口" in info[i]:
						hometown = info[i].split(u"：")[1].strip()
						resume["hometown"] = hometown
					elif u"团员" in info[i] or u"群众" in info[i] or u"党员" in info[i] or u"无党派人士" in info[
						i] or u"民主党派" in info[i]:
						resume["politics"] = info[i].strip()
					else:
						resume["osExperience"] = info[i].strip()


# 处理求职意向
def handleCareerInfo(resume, divInfo):
	trInfos = divInfo.find_all("tr")
	if isinstance(trInfos, list):
		for i in range(len(trInfos)):
			tdInfo = trInfos[i].find_all("td")
			if isinstance(tdInfo, list) and (len(tdInfo)) == 2:
				if u"期望工作地区" in tdInfo[0].text:
					resume["expect_city"] = tdInfo[1].text.replace(u"、", ";")

				elif u"期望月薪" in tdInfo[0].text:
					expect_salary = tdInfo[1].text
					resume["expect_salary"] = handle_salary(expect_salary)

				elif u"目前状况" in tdInfo[0].text:
					resume["work_status"] = tdInfo[1].text

				elif u"期望工作性质" in tdInfo[0].text:
					resume["expect_job_type"] = tdInfo[1].text
					if resume["expect_job_type"] != "":
						resume["expect_job_type"] = resume["expect_job_type"].replace(u"、", ",")

				elif u"期望从事职业" in tdInfo[0].text:
					resume["expect_position"] = tdInfo[1].text.replace(u"、", ",")
					resume["expect_occupation"] = resume["expect_position"]

				elif u"期望从事行业" in tdInfo[0].text:
					resume["expect_industry"] = tdInfo[1].text.replace(u"、", ",")


# 处理自我评价
def handleSelfIntro(resume, divInfo):
	if divInfo.find("div") != None:
		resume["self_introduction"] = divInfo.find("div").text.replace("<br/>", "").strip()


# 处理工作经历
def handleWorkExp(resume, divInfo):
	temp1 = divInfo.find_all("h2")
	temp2 = divInfo.find_all("h5")
	temp3 = divInfo.find_all("div")

	if isinstance(temp1, list) and len(temp1) > 0:
		for i in range(len(temp1)):
			workList = {"start_date": "", "end_date": "", "experience_desc": "", "enterprise_name": "",
						"work_time": "", "position_name": "", "enterprise_size": "", "enterprise_industry": "",
						"enterprise_type": "", "salary": "", "department": "", "second_job_type": "",
						"first_job_type": ""}
			s = temp1[i].text.strip()
			info = s.split(u"  ")
			if len(info) > 0:
				if " - " in info[0]:
					time = info[0].split("-")
					if len(time) == 2:
						# 开始时间
						workList["start_date"] = time[0].replace(".", "-").strip()
						# 结束时间
						workList["end_date"] = time[1].replace(".", "-").strip()

			if len(info) > 1:
				if u"公司" in info[1]:
					# 设置企业名称
					workList["enterprise_name"] = info[1].strip()
			if len(info) > 2:
				if u"年" in info[2] or "月" in info[2]:
					# 设置工作时间
					work_time = info[2].strip()[1:-1]
					workList["work_time"] = handle_work_year(work_time)
			if i < len(temp2):
				if u"元/月" in temp2[i].text:
					info = temp2[i].text.split("|")
					if len(info) == 2:
						# 设置职位名称
						workList["position_name"] = info[0].strip()
						# 设置薪水
						salary = info[1].strip()
						workList["salary"] = handle_salary(salary)
			if i < len(temp3) / 2:
				if u"企业性质" in temp3[2 * i].text or u"规模" in temp3[2 * i].text:
					info = temp3[2 * i].text.strip().split("|")
					for j in range(len(info)):
						if u"企业性质" in info[j]:
							enter_temp = info[j].strip()
							if len(enter_temp) > 5:
								workList["enterprise_type"] = enter_temp[5:]
						elif u"规模" in info[j]:
							enter_temp = info[j].strip()
							if len(info[j].strip()) > 3:
								workList["enterprise_size"] = enter_temp[3:]
						else:
							workList["enterprise_industry"] = info[j].strip()
				if len(temp3) > (2 * i + 1) and temp3[2 * i + 1].find("tr") != None:
					info = temp3[2 * i + 1].find("tr").find_all("td")
					if len(info) == 2:
						workList["experience_desc"] = info[1].text.replace("<br/>", "").strip()
			resume["workExperienceList"].append(workList)


# 处理项目经历
def handleProject(resume, divInfo):
	temp1 = divInfo.find_all("h2")
	temp2 = divInfo.find_all("div", {"class": "resume-preview-dl"})
	if isinstance(temp1, list) and len(temp1) > 0:
		for i in range(len(temp1)):
			projectList = {"start_date": "", "end_date": "", "project_name": "", "project_desc": "",
						   "work_desc": "", "tools": "", "software": "", "hardware": ""}
			info = temp1[i].text.strip().split("  ")
			if len(info) == 2:
				time = info[0].split("-")
				if len(time) == 2:
					# 开始时间
					projectList["start_date"] = time[0].replace(".", "-").strip()
					# 结束时间
					projectList["end_date"] = time[1].replace(".", "-").strip()
				projectList["project_name"] = info[1].strip()
			if i < len(temp2):
				info = temp2[i].find_all("tr")
				for j in range(len(info)):
					s = info[j].text
					tdInfo = info[j].find_all("td")
					if len(tdInfo) == 2:
						if "软件环境" in s:
							projectList["software"] = tdInfo[1].text.replace("<br/>", ", ").strip()
						elif "硬件环境" in s:
							projectList["hardware"] = tdInfo[1].text.replace("<br/>", ", ").strip()
						elif "开发工具" in s:
							projectList["tools"] = tdInfo[1].text.replace("<br/>", ", ").strip()
						elif "责任描述" in s:
							projectList["work_desc"] = tdInfo[1].text.replace("<br/>", ", ").strip()
						elif "项目描述" in s:
							projectList["project_desc"] = tdInfo[1].text.replace("<br/>", ", ").strip()

			resume["projectList"].append(projectList)


# 处理教育经历
def handleEducation(resume, divInfo):
	info = divInfo.find("div", {"class": "resume-preview-dl educationContent"})
	if info != None:
		s = info.text.strip().split("\n")
		for i in range(len(s)):
			eduList = {"college_name": "", "profession_name": "", "degree": "", "start_date": "", "end_date": "",
					   "desc": ""}
			if s != None:
				temp = s[i].split("  ")
				degreeKeywords = ["初中", "高中", "本科", "硕士", "学士", "博士", "MBA", "大专", "职高" "中专", "专科"]
				if isinstance(temp, list):
					for j in range(len(temp)):
						if " - " in temp[j]:
							time = temp[j].split(" - ")
							if len(time) == 2:
								eduList["start_date"] = time[0].replace(".", "-").strip()
								eduList["end_date"] = time[1].replace(".", "-").strip()
						elif temp[j].strip() in degreeKeywords:
							eduList["degree"] = temp[j].strip()
						elif "学院" in temp[j] or "学校" in temp[j] or "大学" in temp[j] or "中学" in temp[
							j] or "college" in temp[j] or "school" in temp[j]:
							eduList["college_name"] = temp[j].strip()
						else:
							eduList["profession_name"] = temp[j].strip()

			resume["educationList"].append(eduList)


# 处理培训经历
def handleTrain(resume, divInfo):
	temp1 = divInfo.find_all("h2")
	temp2 = divInfo.find_all("tbody")
	if isinstance(temp1, list):
		for i in range(len(temp1)):
			trainList = {"start_date": "", "end_date": "", "train_name": "", "train_school": "", "train_city": "",
						 "train_desc": "", "train_certificate": ""}
			s = temp1[i].text.strip()
			info = s.split("  ")
			if len(info) == 2:
				time = info[0].split(" - ")
				if len(time) == 2:
					# 开始时间
					trainList["start_date"] = time[0].replace(".", "-").strip()
					# 结束时间
					trainList["end_date"] = time[1].replace(".", "-").strip()
				trainList["train_name"] = info[1].strip()
			if i < len(temp2):
				trInfo = temp2[i].find_all("tr")
				for j in range(len(trInfo)):
					s = trInfo[j].text
					tdInfo = trInfo[j].find_all("td")
					if len(tdInfo) == 2:
						if "培训机构" in s:
							trainList["train_school"] = tdInfo[1].text.strip()
						elif "培训地点" in s:
							trainList["train_city"] = tdInfo[1].text.strip()
						elif "所获证书" in s:
							trainList["train_certificate"] = tdInfo[1].text.strip()
						elif "培训描述" in s:
							trainList["train_desc"] = tdInfo[1].text.strip()
			resume["trainList"].append(trainList)


# 处理语言能力
def handleLanguage(resume, divInfo):
	info = divInfo.find("div", {"class": "resume-preview-dl resume-preview-line-height"})
	if info != None:
		s = info.text.strip().split("\n")
		for i in range(len(s)):
			lanList = {"language_name": "", "language_ability": "", "language_type": ""}
			s2 = s[i].split("：")
			if len(s2) == 2:
				# 排除为”无“的错误项
				if s2[0].strip() != "无":
					lanList["language_name"] = s2[0].strip()
					lanList["language_ability"] = s2[1].strip()
					resume["languageList"].append(lanList)


# 处理专业技能
def handleSkill(resume, divInfo):
	info = divInfo.find("div")
	if info != None:
		s = info.text.strip().split("\n")
		for i in range(len(s)):
			skillList = {"skill_time": "", "skill_name": "", "skill_degree": ""}
			s2 = s[i].split("|")
			if len(s2) == 2:
				skillList["skill_time"] = s2[1].strip()
				s3 = s2[0].split("：")
				if len(s3) == 2:
					skillList["skill_name"] = s3[0].strip()
					skillList["skill_degree"] = s3[1].strip()
			resume["skillList"].append(skillList)


# 处理证书
def handleCertificate(resume, divInfo):
	info = divInfo.find_all("h2")
	for i in range(len(info)):
		certiList = {"get_time": "", "certificate_name": "", "certificate_school": "", "certificate_score": ""}
		s = info[i].text.strip().split("  ")
		if len(s) == 2:
			certiList["get_time"] = s[0].replace(".", "-")
			certiList["certificate_name"] = s[1]
		resume["certificateList"].append(certiList)


# 处理在校获奖情况
def handleSchoolAward(resume, divInfo):
	temp1 = divInfo.find_all("h2")
	temp2 = divInfo.find_all("td", text=re.compile(u"奖项描述"))
	for i in range(len(temp1)):
		awardList = {"time": "", "award_name": "", "award_level": "", "award_desc": ""}
		scholarList = {"level": "", "name": ""}
		s = temp1[i].text.strip()
		if s.startswith("曾获"):
			s2 = s.split(" ")
			if len(s2) > 1:
				scholarList["level"] = s2[1]
			if len(s2) > 2:
				scholarList["name"] = s2[2]
			resume["scholarshipList"].append(scholarList)
		elif "曾获" in s:
			s2 = s.split(" ")
			if len(s2) == 4:
				awardList["time"] = s2[0].replace(".", "-")
				awardList["award_name"] = s2[3]
				awardList["award_level"] = s2[2]
			if i < len(temp2):
				tdInfo = temp2[i].parent.find_all("td")
				if len(tdInfo) == 2:
					awardList["award_desc"] = tdInfo[1].text
			resume["awardList"].append(awardList)


# 处理在校实践经验
def handleSocial(resume, divInfo):
	temp1 = divInfo.find_all("h2")
	temp2 = divInfo.find_all("tr")
	for i in range(len(temp1)):
		socialList = {"start_time": "", "end_time": "", "social_name": "", "social_desc": ""}
		info = temp1[i].text.split("  ")
		if len(info) == 2:
			time = info[0].split("-")
			if len(time) == 2:
				# 开始时间
				socialList["start_time"] = time[0].replace(".", "-").strip()
				# 结束时间
				socialList["end_time"] = time[1].replace(".", "-").strip()
			socialList["social_name"] = info[1].strip()
			if i < len(temp2):
				if "实践描述" in temp2[i].text:
					temp3 = temp2[i].text.strip().split("\n")
					if len(temp3) >= 2:
						socialList["social_desc"] = temp3[1]

			resume["socialList"].append(socialList)


# 处理特长职业目标
def handleCareerGoal(resume, divInfo):
	info = divInfo.find("div", {"class": "resume-preview-dl"})
	if info != None:
		resume["career_goal"] = info.text.replace("\n", " ").strip().strip("，")


# 处理兴趣爱好
def handleInterests(resume, divInfo):
	info = divInfo.find("div", {"class": "resume-preview-dl"})
	if info != None:
		resume["interests"] = info.text.replace("\n", " ").strip()


# 处理特殊技能
def handleSpecialSkill(resume, divInfo):
	info = divInfo.find("div", {"class": "resume-preview-dl"})
	if info != None:
		resume["speciall_skills"] = info.text.replace("\n", " ").strip()
