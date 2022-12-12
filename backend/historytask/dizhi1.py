import re
import os
import cpca
import numpy as np
import pandas as pd
import numpy as np
from LAC import LAC
import time
import numpy


car_search = r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁台琼使领军北南成广沈济空海]{1}[A-Z]{1}[A-Za-z0-9零一幺二三四五六七八九]{4}[A-Za-z0-9零一幺二三四五六七八九挂领学警港澳]{1}(?!\d)'
#车牌
def car_ID_extract(text):

    all_car_id = re.findall(car_search, text)
    car_id = []
    car_id1 = ""
    if all_car_id:
        for i in all_car_id:
            if not i in car_id:
                car_id.append(i)
        for i in car_id:
            car_id1 = car_id1 + ' ' + "".join(tuple(i))   #将列表转字符串
    if len(car_id) == 0:
        car_id1 = "无车牌信息"
        # print(car_id1)
        return car_id1
    else:
        # print(car_id1)
        return car_id1#返回字符串


def person_id_extract(text):
    person_id = re.findall(
        r"([1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx])", text)
    per_id = ""
    if person_id:
        matrix = numpy.array(person_id)
        for i in matrix[:, 0]:
            per_id = per_id + ' ' + "".join(tuple(i))
    if len(per_id) == 0:
        per_id = "无身份证信息"
        # print(per_id)
        return per_id
    else:
        # print(per_id)
        return per_id

lac = LAC(mode="lac")

# 句子提取名字
def lac_username(sentences: str) -> list:
    # 装载LAC模型
    user_name_list = []
    lac = LAC(mode="lac")
    lac_result = lac.run(sentences)
    for index, lac_label in enumerate(lac_result[1]):
        if lac_label == "PER":
            user_name_list.append(lac_result[0][index])
    return user_name_list


def extract_nameLAC(text):
    lac_name = lac_username(text)
    if len(lac_name) == 0:
        lac_name = "无姓名信息"
        # print(lac_name)
        return lac_name
    else:
        lac_name = set(lac_name)
        # print(lac_name)
        return str(list(lac_name))

def lac_useraddress(sentences: str) -> list:
    # 装载LAC模型
    user_name_list = []
    lac = LAC(mode="lac")
    lac_result = lac.run(sentences)
    for index, lac_label in enumerate(lac_result[1]):
        if lac_label == "LOC":
            user_name_list.append(lac_result[0][index])
    return user_name_list


def extract_addressLAC(text):
    lac_address = lac_useraddress(text)
    if len(lac_address) == 0:
        lac_address = "无地址信息"
        # print(lac_address)
        return lac_address
    else:
        lac_address = set(lac_address)
        # print(lac_address)
        return str(list(lac_address))

def extract_color(text):
   p = re.compile(r"[蓝黄白黑绿][牌|色]")
   color = p.findall(text)
   if len(color) == 0:
       color = "无车牌颜色信息"
       # print(color)
       return color
   else:
       color = set(color)
       # print(type(color))
       return str(list(color))


def lac_usertime(sentences: str) -> list:
    # 装载LAC模型
    user_name_list = []
    lac = LAC(mode="lac")
    lac_result = lac.run(sentences)
    for index, lac_label in enumerate(lac_result[1]):
        if lac_label == "TIME":
            user_name_list.append(lac_result[0][index])
    return user_name_list


def extract_timeLAC(text):
    lac_time = lac_usertime(text)
    lac_time = list(filter(lambda x: x != '最近' and x != '现在', lac_time))
    if len(lac_time) == 0:
        lac_time = "无时间信息"
        return lac_time
    else:
        lac_time = set(lac_time)
        return str(list(lac_time))

def extract(text1):
    dict = {'name': extract_nameLAC(text=text1),
            'car_ID': car_ID_extract(text=text1),
            'person_id': person_id_extract(text=text1),
            'color': extract_color(text=text1),
            'addressLAC':extract_addressLAC(text=text1),
            'time':extract_timeLAC(text=text1)}
    # print(dict)