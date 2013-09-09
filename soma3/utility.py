# -*- coding: utf-8 -*-

import time
import datetime
import os
import string

from django.utils.timezone import utc

def getUTCDatetime():
    now = datetime.datetime.utcnow()
    return '%04d-%02d-%02d %02d:%02d:%02d' % (now.year, now.month, now.day,now.hour, now.minute, now.second)


def getDatetime():
    now = time.localtime()
    return '%04d-%02d-%02d %02d:%02d:%02d' % (now.tm_year, now.tm_mon, now.tm_mday,
                                              now.tm_hour, now.tm_min, now.tm_sec)

def naive2aware(time_str):
    naivetime = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return naivetime.replace(tzinfo=utc)


def getProjectPath():
    project_path = os.path.realpath(os.path.dirname(__file__))
    return project_path

def getTemplatePath():
    return getProjectPath() + '/templates/'

class RANK:
    toString = ['Unhandle','Critical','Major','Minor','Native']
    Suspense = -1
    Unhandle = 0
    Critical = 1
    Major    = 2
    Minor    = 3
    Native   = 4
    rankcolor = ['gray','red','blue', 'green' , 'purple']
    rankcolorbit = ["#cccdc7", "#de6363", "#5a9ccc", "#72c380", "#9d61dd" ]

class TimeRange:
    oneday = 1
    weekly = 7
    monthly = 30
    threemonthly = 90

class Status:
    toString = ['New','Open','Ignore','Renew']
    New = 0
    Open = 1
    Ignore = 2
    Renew = 3
#weekly, monthly, 3monthly
def getTimeRange(t):

    today = datetime.datetime.utcnow().replace(tzinfo=utc)
    #today = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    datedelta = datetime.timedelta(days =  -(t - 1))

    past = today + datedelta
    past = past.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    return past, today

def numbertostrcomma(num) :
    # num을 문자열로 만들어서 뒤집는다. num이 1234이면 a는 '4321'
    a = str(num)[::-1]
    # a를 가지고 (index, a[index]) 의 iter 를 만든다.
    # 그리고  index > 0 and index % 3 == 0 일때 a[index] 뒤에 ','를 붙인 list를 만든다.
    # b = ['4', '3', '2', '1,'] 형태가 된다.
    b = [c + ',' if (i and (i % 3 == 0)) else c for i, c in enumerate(a)]
    # 뒤집어진 문자열로 작업했기 때문에 다시 뒤집는다.
    b = b[::-1]
    # 문자열로 합쳐서 결과를 돌려준다.
    return string.join(b, '').replace('-,', '-')

def get_dict_value_matchin_key(dict,value):
    for _key,_value in dict.items():
        if _value == value:
            return _key

    return ''

def get_dict_value_matchin_number(dict,value):
    count = 0
    for _key,_value in dict.items():
        if _value == value:
            return count
        count += 1
    return count
