# !/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Tao Jiang'

from __init__ import *


def handling_yingcai(d={}):
	"""
	解析英才简历的方法，最后返回解析好的dict 类型resume
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

	# 简历ID
	resume["resume_id"] = str(uuid.uuid4()).replace("-", "")

	# cv_id
	if "resumeID" in d:
		resume["cv_id"] = d.get("resumeID")

	# 爬取时间
	if "crawled_time" in d:
		resume["crawled_time"] = long(d.get("crawled_time"))

	# create_time
	resume["create_time"] = long(time.time()*1000)

	# 关键字
	if "keyword_id" in d:
		resume["keyword_id"] = d.get("keyword_id")

	# 更新时间
	if "refreshDate" in d and d["refreshDate"] != "":
		s = str(d.get("refreshDate"))
		if re.match(r"\d{8}", s):
			resume["update_time"] = s[0:4] + "-" + s[4:6] + "-" + s[6:8]

	# 更新时间列表
	if "refreshDateList" in d and isinstance(d["refreshDateList"], list):
		for i in range(len(d["refreshDateList"])):
			temp = str(d["refreshDateList"][i])
			if re.match(r"\d{8}", temp):
				temp2 = s[0:4] + "-" + s[4:6] + "-" + s[6:8]
				resume["resumeUpdateTimeList"].append(temp2)
	if resume["update_time"] != "" and resume["update_time"] not in resume["resumeUpdateTimeList"]:
		resume["resumeUpdateTimeList"].append(resume["update_time"])

	# 来源
	resume["source"] = u"英才"
	# 　状态
	resume["status"] = "0"
	# 标记
	resume["flag"] = "0"
	# 标记dimension_flag
	resume["dimension_flag"] = False

	# print d["crawled_time"],type(d["crawled_time"])
	# 解析简历主要模块
	if "simple_resume" in d and isinstance(d["simple_resume"], dict):
		# 解析最后一次工作公司名
		if "recentCompanyName" in d["simple_resume"]:
			resume["last_enterprise_name"] = d["simple_resume"].get("recentCompanyName").strip()

		# 解析学校名
		if "college" in d["simple_resume"]:
			resume["college_name"] = d["simple_resume"].get("college").replace("<b>", "").replace("</b>", "")

		# 解析主修课程
		if "major" in d["simple_resume"]:
			resume["profession_name"] = d["simple_resume"].get("major").replace("<br>", "").replace("</br>",
																									"").replace("<b>",
																												"").replace(
				"<br/>", "").replace("</b>", "")

		# 解析学历
		if "oriDegreeName" in d["simple_resume"]:
			resume["degree"] = d["simple_resume"].get("oriDegreeName")

		# 年龄
		if "age" in d["simple_resume"]:
			resume["age"] = d["simple_resume"].get("age").replace(u"岁", "")

		# 期望薪水
		if "expSalary" in d["simple_resume"]:
			salary = d["simple_resume"].get("expSalary")
			resume["expect_salary"] = handle_salary(salary)

	if "resume_detil" in d and isinstance(d["resume_detil"], dict):
		# 公司企业类型
		if "expComTypeName" in d["resume_detil"]:
			resume["enterprise_type"] = d["resume_detil"].get("expComTypeName")

		# 性别
		if "gender" in d["resume_detil"]:
			resume["gender"] = d["resume_detil"].get("gender")

		# 生日
		if "birthday" in d["resume_detil"]:
			resume["birthday"] = d["resume_detil"].get("birthday")

		# 解析工作状态
		if "workStatus" in d["resume_detil"]:
			resume["work_status"] = d["resume_detil"].get("workStatus")
			# workStatus为数字时转换为string
			if re.match("\d+", resume["work_status"]):
				resume["work_status"] = u"离职"

		# 解析驾照
		if "drivName" in d["resume_detil"]:
			resume["drive_name"] = d["resume_detil"].get("drivName")

		# 期待职业类型
		if "expJobTypeName" in d["resume_detil"]:
			resume["expect_job_type"] = d["resume_detil"].get("expJobTypeName")

		# 身高
		if "height" in d["resume_detil"]:
			resume["height"] = str(d["resume_detil"].get("height"))
			if resume["height"] == "0":
				resume["height"] = ""

		# 婚姻状态
		if "marry" in d["resume_detil"]:
			resume["marital_status"] = d["resume_detil"].get("marry")

		# 国籍
		if "nationality" in d["resume_detil"]:
			country = d["resume_detil"].get("nationality")
			if country.startswith("{"):
				resume["country"] = u"中国"
			else:
				resume["country"] = country.strip()

		# 其他经历
		if "osExperience" in d["resume_detil"]:
			resume["osExperience"] = d["resume_detil"].get("osExperience")

		# 工作时间
		if "workTime" in d["resume_detil"]:
			work_year = d["resume_detil"].get("workTime")
			resume["work_year"] = handle_work_year(work_year)

		# 期待职业
		if "expJobsName" in d["resume_detil"]:
			resume["expect_position"] = d["resume_detil"].get("expJobsName")

		# expect_occupation
		if "expJobs" in d["resume_detil"] and isinstance(d["resume_detil"]["expJobs"], list):
			s = ""
			for i in range(len(d["resume_detil"]["expJobs"])):
				if isinstance(d["resume_detil"]["expJobs"][i], dict) and "categoryName" in d["resume_detil"]["expJobs"][
					i]:
					s += d["resume_detil"]["expJobs"][i].get("categoryName") + "/"
			resume["expect_occupation"] = s.strip("/").strip()

		# 自我介绍
		if "selfEval" in d["resume_detil"]:
			resume["self_introduction"] = d["resume_detil"].get("selfEval")

		# 解析证书信息
		if "certs" in d["resume_detil"] and isinstance(d["resume_detil"]["certs"], list):
			for i in range(len(d["resume_detil"]["certs"])):
				cert = d["resume_detil"]["certs"][i]
				if "time" in cert:
					value_time = cert.get("time")
					if value_time is None:
						value_time = ""
				else:
					value_time = ""

				if "school" in cert:
					value_school = cert.get("school")
					if value_school is None:
						value_school = ""
				else:
					value_school = ""

				if "certName" in cert:
					value_name = cert.get("certName")
					if value_name is None:
						value_name = ""
				else:
					value_name = ""

				if "score" in cert:
					if cert["score"] is None:
						value_score = ""
					else:
						value_score = cert.get("score")
				else:
					value_score = ""

			resume["certificateList"].append(
				{"get_time": value_time, "certificate_name": value_name, "certificate_school": value_school,
				 "certificate_score": value_score})

		# 解析 hometown
		if "domicile" in d["resume_detil"] and isinstance(d["resume_detil"]["domicile"], dict):
			s = ''
			if "provName" in d["resume_detil"]["domicile"]:
				s += d["resume_detil"]["domicile"].get("provName").strip()
			if "cityName" in d["resume_detil"]["domicile"]:
				s = s + d["resume_detil"]["domicile"].get("cityName").strip()
			if "distName" in d["resume_detil"]["domicile"]:
				s = s + d["resume_detil"]["domicile"].get("distName").strip()
			resume["hometown"] = s.strip()

		# 解析居住地
		if "living" in d["resume_detil"] and isinstance(d["resume_detil"]["living"], dict):
			s = ""
			if "provName" in d["resume_detil"]["living"]:
				s += d["resume_detil"]["living"].get("provName")
			if "cityName" in d["resume_detil"]["living"]:
				s = s + d["resume_detil"]["living"].get("cityName")
			if "distName" in d["resume_detil"]["living"]:
				s = s + d["resume_detil"]["living"].get("distName")
			resume["living"] = s

		# 解析期待行业
		if "expIndustry" in d["resume_detil"] and isinstance(d["resume_detil"]["expIndustry"], list):
			s = ""
			for i in range(len(d["resume_detil"]["expIndustry"])):
				expIndu = d["resume_detil"]["expIndustry"][i]
				if isinstance(expIndu, dict) and "bigName" in expIndu:
					s = s + expIndu["bigName"] + ","
			resume["expect_industry"] = s.strip(",")

		# 解析期待工作城市
		if "expLocation" in d["resume_detil"] and isinstance(d["resume_detil"]["expLocation"], list):
			s = ""
			for i in range(len(d["resume_detil"]["expLocation"])):
				expIndu = d["resume_detil"]["expLocation"][i]
				if isinstance(expIndu, dict) and "cityName" in expIndu:
					if expIndu["cityName"] not in s:
						s = s + expIndu["cityName"] + ";"

			resume["expect_city"] = s.strip(";")

		# 解析语言信息列表
		if "langSkills" in d["resume_detil"] and isinstance(d["resume_detil"]["langSkills"], list):
			for i in range(len(d["resume_detil"]["langSkills"])):
				langskill = d["resume_detil"]["langSkills"][i]
				if "langValue" in langskill:
					name = langskill.get("langValue")
					if name is None:
						name = ""
				else:
					name = ""
				if "level" in langskill:
					level = langskill.get("level")
					if level is None:
						level = ""
				else:
					level = ""
				if "typeName" in langskill:
					types = langskill.get("typeName")
					if types is None:
						types = ""
				else:
					types = ""
				resume["languageList"].append(
					{"language_name": name, "language_ability": level, "language_type": types})

		# 解析项目经历
		if d["resume_detil"].has_key("projects") and isinstance(d["resume_detil"]["projects"], list):
			for i in range(len(d["resume_detil"]["projects"])):
				project = d["resume_detil"]["projects"][i]
				if project.has_key("name"):
					name = project["name"]
					if name is None:
						name = ""
				else:
					name = ""
				if project.has_key("start"):
					start = project["start"]
					if start is None:
						start = ""
				else:
					start = ""
				if project.has_key("end"):
					end = project["end"]
					if end is None:
						end = ""
				else:
					end = ""
				if project.has_key("projDesc"):
					desc = project["projDesc"]
					if desc is None:
						desc = ""
				else:
					desc = ""
				if project.has_key("resp"):
					resp = project["resp"]
					if resp is None:
						resp = ""
				else:
					resp = ""

			resume["projectList"].append(
				{"start_date": start, "end_date": end, "project_name": name, "project_desc": desc,
				 "work_desc": resp, "tools": "", "software": "", "hardware": ""})

		# 解析培训经历
		if d["resume_detil"].has_key("training") and isinstance(d["resume_detil"]["training"], list):
			for i in range(len(d["resume_detil"]["training"])):
				train = d["resume_detil"]["training"][i]
				if train.has_key("school"):
					school = train["school"]
					if school is None:
						school = ""
				else:
					school = ""
				if train.has_key("start"):
					start = train["start"]
					if start is None:
						start = ""
				else:
					start = ""
				if train.has_key("end"):
					end = train["end"]
					if u"今" in end:
						end = u"至今"
					if end is None:
						end = ""
				else:
					end = ""
				if train.has_key("desc"):
					desc = train["desc"]
					if desc is None:
						desc = ""
				else:
					desc = ""

				if train.has_key("course"):
					course = train["course"]
					if course is None:
						course = ""
				else:
					course = ""
				resume["trainList"].append(
					{"start_date": start, "end_date": end, "train_name": course, "train_school": school,
					 "train_desc": desc, "train_city": "", "train_certificate": ""})

		# 解析技能信息列表
		if d["resume_detil"].has_key("skills") and isinstance(d["resume_detil"]["skills"], list):
			for i in range(len(d["resume_detil"]["skills"])):
				skill = d["resume_detil"]["skills"][i]
				if skill.has_key("name"):
					name = skill["name"]
					if name is None:
						name = ""
				else:
					name = ""
				if skill.has_key("level"):
					level = skill["level"]
					if level is None:
						level = ""
				else:
					level = ""
				if skill.has_key("exp"):
					exp = skill["exp"]
					if exp is None:
						exp = ""
				else:
					exp = ""
				resume["skillList"].append({"skill_name": name, "skill_degree": level, "skill_time": exp})

		# 产品信息列表
		if d["resume_detil"].has_key("production") and isinstance(d["resume_detil"]["production"], list):
			for i in range(len(d["resume_detil"]["production"])):
				produc = d["resume_detil"]["production"][i]
				if produc.has_key("name"):
					name = produc["name"]
					if name is None:
						name = ""
				else:
					name = ""
				if produc.has_key("desc"):
					desc = produc["desc"]
					if desc is None:
						desc = ""
				else:
					desc = ""
				if produc.has_key("begin"):
					start = num_to_str(produc["begin"])
					if start is None:
						start = ""
				else:
					start = ""
				if produc.has_key("end"):
					end = num_to_str(produc["end"])
					if end is None:
						end = ""
				else:
					end = ""
				resume["productList"].append(
					{"product_name": name, "start_time": start, "end_time": end, "product_desc": desc})

		# 解析教育信息列表
		if d["resume_detil"].has_key("education") and isinstance(d["resume_detil"]["education"], list):
			for i in range(len(d["resume_detil"]["education"])):
				edu = d["resume_detil"]["education"][i]
				if edu.has_key("start"):
					start_date = edu["start"]
				else:
					start_date = ""
				if edu.has_key("end"):
					end_date = edu["end"]
					if u"今" in end_date:
						end_date = u"至今"
				else:
					end_date = ""
				if edu.has_key("college"):
					college_name = edu["college"].replace("<b>", "").replace("</b>", "")
					if college_name is None:
						college_name = ""
				else:
					college_name = ""
				if edu.has_key("major"):
					profession_name = edu["major"].replace("<br>", "").replace("</br>", "").replace("<b>",
																									"").replace(
						"</b>", "").replace("<br/>", "")
				else:
					profession_name = ""
				if edu.has_key("description"):
					desc = edu["description"]
					if desc is None:
						desc = ""
					else:
						desc = desc.replace("<br />", "  ")
				else:
					desc = ""
				if edu.has_key("degreeName"):
					degree = edu["degreeName"]
					if degree is None:
						degree = ""
				else:
					degree = ""
				resume["educationList"].append(
					{"start_date": start_date, "end_date": end_date, "degree": degree,
					 "profession_name": profession_name, "college_name": college_name, "desc": desc})

		# 工作信息列表
		if d["resume_detil"].has_key("experience") and isinstance(d["resume_detil"]["experience"], list):
			for i in range(len(d["resume_detil"]["experience"])):
				exper = d["resume_detil"]["experience"][i]
				if exper.has_key("comName"):
					comName = exper["comName"]
				else:
					comName = ""
				if exper.has_key("department"):
					depart = exper["department"]
				else:
					depart = ""
				if exper.has_key("bigName"):
					indus = exper["bigName"]
				else:
					indus = ""
				if exper.has_key("salary"):
					salary = exper["salary"]
					if salary is not None:
						salary = handle_salary(salary)
				else:
					salary = ""
				if exper.has_key("start"):
					start = exper["start"]
				else:
					start = ""
				if exper.has_key("end"):
					if u"今" in exper["end"]:
						end = u"至今"
					else:
						end = exper["end"]
				else:
					end = ""
				if exper.has_key("inputJobName"):
					posi_name = exper["inputJobName"]
				else:
					posi_name = ""
				if exper.has_key("comType"):
					enter_type = exper["comType"]
				else:
					enter_type = ""
				if exper.has_key("comSize"):
					enter_size = exper["comSize"]
				else:
					enter_size = ""
				if exper.has_key("jobType"):
					job_type = exper["jobType"]
				else:
					job_type = ""
				if exper.has_key("jobName"):
					second_job_type = exper["jobName"]
				else:
					second_job_type = ""
				if exper.has_key("workDesc"):
					exper_desc = exper["workDesc"]
					if exper_desc is None:
						exper_desc = ""
					else:
						exper_desc = exper_desc.replace("<br />", "  ").strip()
				else:
					exper_desc = ""

				resume["workExperienceList"].append(
					{"enterprise_name": comName, "enterprise_industry": indus, "experience_desc": exper_desc,
					 "salary": salary, "start_date": start, "end_date": end, "position_name": posi_name,
					 "first_job_type": job_type, "second_job_type": second_job_type, "department": depart,
					 "enterprise_type": enter_type, "enterprise_size": enter_size, "work_time": ""})

		if len(resume["workExperienceList"]) >= 1:
			resume["last_enterprise_industry"] = resume["workExperienceList"][0].get(
				"enterprise_industry")
			resume["last_enterprise_name"] = resume["workExperienceList"][0].get("enterprise_name")
			resume["last_enterprise_salary"] = resume["workExperienceList"][0].get("salary")
			resume["last_position_name"] = resume["workExperienceList"][0].get("position_name")

		# 解析教育信息
		if resume["profession_name"] == "":
			if len(resume["educationList"]) > 0:
				resume["profession_name"] = resume["educationList"][0].get("profession_name")

		if resume["degree"] == "":
			if len(resume["educationList"]) > 0:
				resume["degree"] = resume["educationList"][0].get("degree")

		if resume["college_name"] == "":
			if len(resume["educationList"]) > 0:
				resume["college_name"] = resume["educationList"][0].get("college_name")

	# 返回解析好的简历 resume
	return resume
