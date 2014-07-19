# Create your views here.
# -*- coding: utf-8 -*-

import json
import operator
import datetime
import sys
from django.template import Context, loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from common import validUserPjt
from common import getUserProfileDict
from common import getApikeyDict
from common import getSettingDict

from utility import getTimeRange
from utility import Status
from utility import getTimezoneMidNight
from utility import toTimezone

from urqa.models import AuthUser
from urqa.models import Errors
from urqa.models import Instances
from urqa.models import Appruncount
from urqa.models import ErrorsbyApp
from urqa.models import SessionbyApp
from urqa.models import CountrysbyApp
def statistics(request,apikey):
    username = request.user

    valid , message , userelement, projectelement = validUserPjt(username,apikey)

    if not valid:
        return HttpResponseRedirect('/urqa')

    #ser = AuthUser.objects.get(username = request.user)

    #tpl = loader.get_template('statistics.html')

    userdict = getUserProfileDict(userelement)
    apikeydict = getApikeyDict(apikey)
    settingdict = getSettingDict(projectelement,userelement)

    statisticsdict = {
        'ServerURL' : 'http://'+request.get_host() + '/urqa/project/',
    }

    ctxdict = dict(userdict.items() + apikeydict.items() + settingdict.items() + statisticsdict.items() )
    ctx = Context(ctxdict)
    return render(request, 'statistics.html', ctx)
    #return HttpResponse(tpl.render(ctx))


def chartdata_sbav(request,apikey):
    jsonData = json.loads(request.POST['json'],encoding='utf-8')
    retention = int(jsonData['retention'])

    username = request.user
    valid , message , userElement, projectElement = validUserPjt(username,apikey)
    if not valid:
        return HttpResponseRedirect('/urqa')

    print 'retention', retention
    # Common Data
    #midnight = getTimezoneMidNight(projectElement.timezone)
    #print >> sys.stderr,projectElement.timezone,midnight
    #print >> sys.stderr,'utc',toTimezone(midnight,'UTC')
    past, today = getTimeRange(retention,projectElement.timezone)
    #print >> sys.stderr,'time',past,today


    sql = 'select idappruncount2 as idsessionbyapp, sum(appruncount) as runcount, appversion, DATE_FORMAT(CONVERT_TZ(datetime,"UTC",%(timezone)s),"%%y-%%m-%%d") as sessionday'
    sql = sql + ' from urqa.appruncount2'
    sql = sql + ' where pid = %(pidinput)s and datetime >= %(pasttime)s'
    sql = sql + ' Group by appversion, sessionday'

    #print >> sys.stderr,'%d-%d-%d %d:%d:%d' % (past.year,past.month,past.day,past.hour,past.minute,past.second);
    #params = {'timezone':projectElement.timezone,'pidinput':projectElement.pid,'pasttime':past}
    params = {'timezone':projectElement.timezone,'pidinput':projectElement.pid,'pasttime':'%d-%d-%d %d:%d:%d' % (past.year,past.month,past.day,past.hour,past.minute,past.second)}
    places = SessionbyApp.objects.raw(sql, params)
    #print >> sys.stderr,'places',places

    appversions = []
    dates = []
    for idx, pl in enumerate(places):
        if not pl.appversion in appversions:
            appversions.append(pl.appversion)
        if not pl.sessionday in dates:
            dates.append(pl.sessionday)
    #print >> sys.stderr,'appversion',appversions
    #print >> sys.stderr,'dates',dates

    #AppruncountElemtns = Appruncount.objects.filter(pid=projectElement,date__range=(past,today))
    result = {}

    # Chart 0 session by appversion
    #appversions = AppruncountElemtns.values('appversion').distinct().order_by('appversion')
    categories = []
    appcount_data = {}
    for appversion in appversions:
        appcount_data[appversion] = []
    #print >> sys.stderr,'appcount_data',appcount_data

    for i in range(retention-1,-1,-1):
        day1 = getTimezoneMidNight(projectElement.timezone) + datetime.timedelta(days =  -i)
        #print >> sys.stderr,'day',day1,day1.month,day1.day,day1.hour,day1.minute
        #print >> sys.stderr,'utc',toTimezone(day1,'UTC')
        categories.append(day1.strftime('%b-%d'))

        for appversion in appversions:
            #appcount_data[appversion['appversion']].append(Appruncount.objects.filter(pid=projectElement,appversion=appversion['appversion'],date__range=(day1,day2)))
            #runcounts = Appruncount.objects.filter(pid=projectElement,appversion=appversion['appversion'],date=day1.strftime('20%y-%m-%d'))
            result_runcount = 0
            for idx, pl in enumerate(places):
                if pl.appversion == appversion and pl.sessionday == day1.strftime('%y-%m-%d'):
                    result_runcount = pl.runcount
                    #print >> sys.stderr,appversion,pl.sessionday,pl.runcount
                    break

            #for runcount in runcounts:
            #    result_runcount = result_runcount + runcount.runcount
            appcount_data[appversion].append(int(result_runcount));

    appver_data = []

    for appversion in appversions:
        appver_data.append(
            {
                'name': appversion,
                'data': appcount_data[appversion]
            }
        )

    chart_sbav = {'categories':categories,'data':appver_data}
    result['chart_sbav'] = chart_sbav

    #print >> sys.stderr, 'result',result
    return HttpResponse(json.dumps(result), 'application/json');

def chartdata_ebav(request,apikey):
    jsonData = json.loads(request.POST['json'],encoding='utf-8')
    retention = int(jsonData['retention'])

    username = request.user
    valid , message , userElement, projectElement = validUserPjt(username,apikey)
    if not valid:
        return HttpResponseRedirect('/urqa')

    # Common Data
    result = {}

    #appcount_data = {}
    categories = []
    #appver_data = []

    sql = "select count(*) as errorcount ,appversion, DATE_FORMAT(CONVERT_TZ(datetime,'UTC',%(timezone)s),'%%y-%%m-%%d') as errorday "
    sql = sql + "from instances A, errors B "
    sql = sql + "where A.iderror = B.iderror "
    sql = sql + "and pid = %(pidinput)s "
    sql = sql + "and B.status in (0,1) "
    sql = sql + "and A.datetime > %(pasttime)s"
    sql = sql + "group by errorday,appversion"

    past, today = getTimeRange(retention,projectElement.timezone)

    params = {'timezone':projectElement.timezone,'pidinput':projectElement.pid,'pasttime':'%d-%d-%d %d:%d:%d' % (past.year,past.month,past.day,past.hour,past.minute,past.second)}
    places = ErrorsbyApp.objects.raw(sql, params)

    #listing app version
    appversions = []
    for idx, pl in enumerate(places):
        appversions.append(pl.appversion)

    appversionList = list(set(appversions))
    appversionList.sort()
    #loop for retention
    dates = []
    for idx, pl in enumerate(places):
        dates.append(pl.errorday)
    print >> sys.stderr,'dates',dates
    #dateList = list(set(dates))
    #dateList.sort()
    dateList = []
    for i in range(retention-1,-1,-1):
        day1 = getTimezoneMidNight(projectElement.timezone) + datetime.timedelta(days =  -i)
        dateList.append(day1.strftime('%y-%m-%d'))
        categories.append(day1.strftime('%b-%d'))
    returnValue = []
    #print >> sys.stderr,'dateList',dateList
    for version in appversionList:
        dataList = [0] * len(dateList)
        for index, date in enumerate(dateList):
            for idx, pl in enumerate(places):
                if pl.appversion == version and pl.errorday == date:
                    dataList[index] = pl.errorcount

        returnValue.append(
            {
                'name': version,
                'data': dataList
            }
        )


    #Fixed, Ignore 찾기
    """
    sql = "select count(*) as errorcount ,appversion, DATE_FORMAT(A.datetime, '%%m-%%d') as errorday "
    sql = sql + "from instances A, errors B "
    sql = sql + "where A.iderror = B.iderror "
    sql = sql + "and pid = %(pidinput)s "
    sql = sql + "and B.status in (2) "
    sql = sql + "and A.datetime > (curdate() - interval %(intervalinput)s day) "
    sql = sql + "group by DATE_FORMAT(A.datetime, '%%m%%d'),appversion"

    params = {'pidinput':projectElement.pid,'intervalinput':retention - 1}
    places = ErrorsbyApp.objects.raw(sql, params)

    dataList = [0] * len(dateList)
    for index, date in enumerate(dateList):
        for idx, pl in enumerate(places):
            if pl.errorday == date:
                dataList[index] = pl.errorcount
    if max(dataList) > 0:
        returnValue.append(
            {
                'name': 'Fixed',
                'data': dataList
            }
        )
    sql = "select count(*) as errorcount ,appversion, DATE_FORMAT(A.datetime, '%%m-%%d') as errorday "
    sql = sql + "from instances A, errors B "
    sql = sql + "where A.iderror = B.iderror "
    sql = sql + "and pid = %(pidinput)s "
    sql = sql + "and B.status in (3) "
    sql = sql + "and A.datetime > (curdate() - interval %(intervalinput)s day) "
    sql = sql + "group by DATE_FORMAT(A.datetime, '%%m%%d'),appversion"

    params = {'pidinput':projectElement.pid,'intervalinput':retention - 1}
    places = ErrorsbyApp.objects.raw(sql, params)

    dataList = [0] * len(dateList)
    for index, date in enumerate(dateList):
        for idx, pl in enumerate(places):
            if pl.errorday == date:
                dataList[index] = pl.errorcount
    if max(dataList) > 0:
        returnValue.append(
            {
                'name': 'Ignore',
                'data': dataList
            }
        )
    """
    chart1 = {'categories':categories,'data':returnValue}
    result['chart1'] = chart1
    #print >>sys.stderr, chart1
    return HttpResponse(json.dumps(result), 'application/json');


def chartdata_erbc(request,apikey):
    jsonData = json.loads(request.POST['json'],encoding='utf-8')
    retention = int(jsonData['retention'])

    username = request.user
    valid , message , userElement, projectElement = validUserPjt(username,apikey)
    if not valid:
        return HttpResponseRedirect('/urqa')

    print 'retention', retention
    # Common Data
    past, today = getTimeRange(retention,projectElement.timezone)
    #print 'past',past, 'today',today
    errorElements = Errors.objects.filter(pid=projectElement,status__in=[Status.New,Status.Open],lastdate__range=(past,today)).order_by('errorclassname','errorweight')
    #instanceElements = Instances.objects.select_related().filter(iderror__in=errorElements,datetime__range=(past,today))
    #AppruncountElemtns = Appruncount.objects.filter(pid=projectElement,date__range=(past,today))
    result = {}

    #chart2
    chart2 = []
    pre_class = ''
    #print 'past',past
    for e in errorElements:
        instanceCount = Instances.objects.filter(iderror=e,datetime__gte=past).count()
        if pre_class != e.errorclassname:
            pre_class = e.errorclassname
            chart2.append([e.errorclassname, instanceCount])
        else:
            last = len(chart2)
            chart2[last-1] = [e.errorclassname,chart2[last-1][1] + (instanceCount)]



    result['chart2'] = chart2
    return HttpResponse(json.dumps(result), 'application/json');

def chartdata_erbd(request,apikey):
    jsonData = json.loads(request.POST['json'],encoding='utf-8')
    retention = int(jsonData['retention'])

    username = request.user
    valid , message , userElement, projectElement = validUserPjt(username,apikey)
    if not valid:
        return HttpResponseRedirect('/urqa')

    print 'retention', retention
    # Common Data
    past, today = getTimeRange(retention,projectElement.timezone)
    #print 'past',past, 'today',today
    errorElements = Errors.objects.filter(pid=projectElement,status__in=[Status.New,Status.Open],lastdate__range=(past,today)).order_by('errorclassname','errorweight')
    instanceElements = Instances.objects.select_related().filter(iderror__in=errorElements,datetime__range=(past,today))
    #AppruncountElemtns = Appruncount.objects.filter(pid=projectElement,date__range=(past,today))
    result = {}

    #chart3 - Device error
    temp_data = {}
    activities = []
    instances = instanceElements.order_by('device')
    for i in instances:
        if i.device:
            device = i.device
        else:
            device = "Unknown"
        if not device in activities:
            activities.append(device)
            temp_data[device] = 1
        else:
            temp_data[device] += 1

    sorted_dic = sorted(temp_data.iteritems(), key=operator.itemgetter(1), reverse=True)
    categories = []
    temp_data = []
    i = 0
    others_count = 0
    for l,v in sorted_dic:
        i += 1
        if i>25:
            others_count += v
        else:
            categories.append(l)
            temp_data.append(v)
    if others_count != 0:
        categories.append('Others')
        temp_data.append(others_count)

    dev_data = [{'name':'Device','data':temp_data}]
    chart3 = {'categories':categories,'data':dev_data}
    result['chart3'] = chart3

    return HttpResponse(json.dumps(result), 'application/json');

def chartdata_erba(request,apikey):
    jsonData = json.loads(request.POST['json'],encoding='utf-8')
    retention = int(jsonData['retention'])

    username = request.user
    valid , message , userElement, projectElement = validUserPjt(username,apikey)
    if not valid:
        return HttpResponseRedirect('/urqa')

    print 'retention', retention
    # Common Data
    past, today = getTimeRange(retention,projectElement.timezone)
    #print 'past',past, 'today',today
    errorElements = Errors.objects.filter(pid=projectElement,status__in=[Status.New,Status.Open],lastdate__range=(past,today)).order_by('errorclassname','errorweight')
    instanceElements = Instances.objects.select_related().filter(iderror__in=errorElements,datetime__range=(past,today))
    #AppruncountElemtns = Appruncount.objects.filter(pid=projectElement,date__range=(past,today))
    result = {}

    #chart4
    temp_data = {}
    activities = []
    instances = instanceElements.order_by('lastactivity')
    for i in instances:
        if i.lastactivity:
            lastactivity = i.lastactivity
        else:
            lastactivity = "Unknown"
        if not lastactivity in activities:
            activities.append(lastactivity)
            temp_data[lastactivity] = 1
        else:
            temp_data[lastactivity] += 1
    sorted_dic = sorted(temp_data.iteritems(), key=operator.itemgetter(1), reverse=True)
    categories = []
    temp_data = []
    i = 0
    others_count = 0
    for l,v in sorted_dic:
        i += 1
        if i>25:
            others_count += v
        else:
            categories.append(l)
            temp_data.append(v)
    if others_count != 0:
        categories.append('Others')
        temp_data.append(others_count)

    act_data = [{'name':'Activity','data':temp_data}]
    chart4 = {'categories':categories,'data':act_data}
    result['chart4'] = chart4
    return HttpResponse(json.dumps(result), 'application/json');


def chartdata_erbv(request,apikey):
    jsonData = json.loads(request.POST['json'],encoding='utf-8')
    retention = int(jsonData['retention'])

    username = request.user
    valid , message , userElement, projectElement = validUserPjt(username,apikey)
    if not valid:
        return HttpResponseRedirect('/urqa')

    print 'retention', retention
    # Common Data
    past, today = getTimeRange(retention,projectElement.timezone)
    #print 'past',past, 'today',today
    errorElements = Errors.objects.filter(pid=projectElement,status__in=[Status.New,Status.Open],lastdate__range=(past,today)).order_by('errorclassname','errorweight')
    instanceElements = Instances.objects.select_related().filter(iderror__in=errorElements,datetime__range=(past,today))
    #AppruncountElemtns = Appruncount.objects.filter(pid=projectElement,date__range=(past,today))
    result = {}


    #Chart5
    categories = []
    ver_data = []
    temp_data = {}
    instances = instanceElements.order_by('-appversion','-osversion')

    appv_idx = -1
    for i in instances:
        if not i.appversion in categories:
            appv_idx += 1
            categories.append(i.appversion)
        if not i.osversion in temp_data:
            temp_data[i.osversion] = []
        while len(temp_data[i.osversion]) <= appv_idx:
            temp_data[i.osversion].append(0)
        #score = float(i.iderror.errorweight) / i.iderror.numofinstances
        temp_data[i.osversion][appv_idx] += 1#score

    for t in temp_data:
        idx = 0
        for e in temp_data[t]:
            temp_data[t][idx] = e#round(e,2)
            idx += 1
        ver_data.append({'name':t,'data':temp_data[t]})

    chart5 = {'categories':categories,'data':ver_data}
    result['chart5'] = chart5

    return HttpResponse(json.dumps(result), 'application/json');

def chartdata_ebcs(request,apikey):
     jsonData = json.loads(request.POST['json'],encoding='utf-8')
     retention = int(jsonData['retention'])

     username = request.user
     valid , message , userElement, projectElement = validUserPjt(username,apikey)
     if not valid:
         return HttpResponseRedirect('/urqa')

     print 'retention', retention
     # Common Data
     result = {}

     #chart6
     temp_data = {}
     activities = []

     sql = "select count(*) count, country from errors e, instances i, projects p"
     sql = sql + "where e.iderror = i.iderror"
     sql = sql + "and e.pid = p.pid"
     sql = sql + "and p.pid = %(pname)s"
     sql = sql + "group by country"
     sql = sql + "order by count desc"
     sql = sql + "limit 10"

     params = {'pname':projectElement.pid}
     counts = CountrysbyApp.objects.raw(sql, params)

     categories = []
     temp_data = []

     for idx, pl in enumerate(counts):
         categories.append(pl.country)
         temp_data.append(pl.count)


     act_data = [{'name':'Country','data':temp_data}]
     chart6 = {'categories':categories,'data':act_data}
     result['chart6'] = chart6
     return HttpResponse(json.dumps(result), 'application/json');
