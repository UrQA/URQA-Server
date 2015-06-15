# Create your views here.
# -*- coding: utf-8 -*-

import sys
import re
import json
import operator
from collections import OrderedDict
from django.db.models import Count

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.shortcuts import render

from urqa.models import AuthUser
from urqa.models import Errors
from urqa.models import Projects
from urqa.models import Instances
from urqa.models import Eventpaths
from urqa.models import Osstatistics
from urqa.models import Appstatistics
from urqa.models import Tags
from urqa.models import Comments
from urqa.models import Sofiles
from urqa.models import ErrorStatistics
from urqa.models import InstanceLog

from common import validUserPjt
from common import validUserPjtError
from common import getUserProfileDict
from common import getApikeyDict
from common import getSettingDict

import utility
from utility import naive2aware
from utility import getTimeRange
from utility import TimeRange
from utility import RANK
from utility import Status
from utility import toTimezone

from config import get_config


def newTag(request, apikey, iderror):
    #Error에 Tag를 생성함
    #커맨드를 생성한 사용자가 Project에 Tag를 쓸 수 있는지 검 증
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user,apikey,iderror)

    print msg
    if not result:
        return HttpResponse(msg)

    tag = request.POST['tag']
    tagElement, created = Tags.objects.get_or_create(iderror=errorElement, tag=tag, pid=projectElement)

    if not created:
        return HttpResponse('tag %s already exists' % tag)
    else:
        return HttpResponse('success')

def deleteTag(request, apikey, iderror):
    #Error의 Tag를 삭제함
    #커맨드를 생성한 사용자가 Project에 Tag를 삭제할 수 있는지 검증
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user, apikey, iderror)

    print msg
    if not result:
        return HttpResponse(msg)

    tag = request.POST['tag']
    try:
        tagElement = Tags.objects.get(iderror=errorElement, tag=tag)
        tagElement.delete()
    except ObjectDoesNotExist:
        HttpResponse('tag %s not exists' % tag)



    return HttpResponse('success')


def newComment(request, apikey, iderror):
    #Error에 Comment를 생성함.
    #커맨드를 생성한 사용자가 Project에 Comment를 쓸수있는지 검증
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user,apikey,iderror)

    print msg
    if not result:
        return HttpResponse(msg)

    time = utility.getUTCDatetime()
    datetime = naive2aware(time)

    #입력받은 POST데이터에서 comment받아옴
    comment = request.POST['comment']
    element = Comments.objects.create(uid=userElement, iderror=errorElement, datetime=datetime, comment=comment)

    #타임존을 적용한다.
    adtimezone = toTimezone(datetime,projectElement.timezone)
    print 'newcommand',adtimezone,datetime
    dict = {'imgsrc':userElement.image_path, 'name': userElement.last_name + userElement.first_name,
            'message': comment,
            'date': adtimezone.__format__('%Y.%m.%d<br>%H:%M:%S'),
            'id' : element.idcomment}

    print dict

    return HttpResponse(json.dumps(dict), 'application/json')

def deleteComment(request, apikey, iderror):
    #Comment 삭제
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user, apikey, iderror)

    print msg
    if not result:
        return HttpResponse(msg)

    #Commend ID를 입력받아 Comment를 삭제한다.
    idcomment = request.POST['idcomment']
    try:
        commentElement = Comments.objects.get(idcomment=idcomment)
        commentElement.delete()
    except ObjectDoesNotExist:
        HttpResponse('comment %s not exists' % idcomment)

    return HttpResponse('success')

def os(request,apikey,iderror):
    #Error Detail페이지에서 os버전별 통계데이터를 얻어오는 루틴
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user, apikey, iderror)

    print msg
    if not result:
        return HttpResponse(msg)

    #DB에서 OS통계데이터를 얻어오는 쿼리
    sql = "select idinstance as iderrorstatistics, osversion as keyname, count(*) as count "
    sql = sql + "from instances where iderror = %(id_error)s "
    sql = sql + "group by keyname order by count desc"

    params = {'id_error':iderror}
    places = ErrorStatistics.objects.raw(sql, params)

    #DB에서 받은데이터를 JSON데이터 생성
    data = []
    counter = 0
    others = 0
    for idx, pl in enumerate(places):
        counter += 1
        if counter <= 5:
            tuple = {'label' : pl.keyname, 'value' : pl.count}
            data.append(tuple)
        else:
            others += pl.count
    if others != 0:
        tuple = {'label' : 'Ohters' , 'value' : others}
        data.append(tuple)


    return HttpResponse(json.dumps(data),'application/json')



def app(request,apikey,iderror):
    #Error Detail페이지에서 엡 버전별 에러량을 보여주는 차트
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user, apikey, iderror)

    print msg
    if not result:
        return HttpResponse(msg)

    #DB에 요청할 Query 생성
    sql = "select idinstance as iderrorstatistics, appversion as keyname, count(*) as count "
    sql = sql + "from instances where iderror = %(id_error)s "
    sql = sql + "group by keyname order by count desc"

    params = {'id_error':iderror}
    places = ErrorStatistics.objects.raw(sql, params)

    #DB에서 온 값을 JSON으로 변환함
    data = []
    counter = 0
    others = 0
    for idx, pl in enumerate(places):
        counter += 1
        if counter <= 5:
            tuple = {'label' : pl.keyname, 'value' : pl.count}
            data.append(tuple)
        else:
            others += pl.count
    if others != 0:
        tuple = {'label' : 'Ohters' , 'value' : others}
        data.append(tuple)


    return HttpResponse(json.dumps(data),'application/json')

def device(request,apikey,iderror):
    #Error Detail페이지에서 Device별 에러량을 보여주는 루틴
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user, apikey, iderror)

    print msg
    if not result:
        return HttpResponse(msg)

    #DB쿼리를 생성
    sql = "select idinstance as iderrorstatistics, device as keyname, count(*) as count "
    sql = sql + "from instances where iderror = %(id_error)s "
    sql = sql + "group by keyname order by count desc"

    params = {'id_error':iderror}
    places = ErrorStatistics.objects.raw(sql, params)

    #DB로부터 받은 데이터를 JSON으로 변경
    data = []
    counter = 0
    others = 0
    for idx, pl in enumerate(places):
        counter += 1
        if counter <= 5:
            tuple = {'label' : pl.keyname, 'value' : pl.count}
            data.append(tuple)
        else:
            others += pl.count
    if others != 0:
        tuple = {'label' : 'Ohters' , 'value' : others}
        data.append(tuple)


    return HttpResponse(json.dumps(data),'application/json')

def country(request,apikey,iderror):
    #Error Detail페이지에서 Device별 에러량을 보여주는 루틴
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user, apikey, iderror)

    print msg
    if not result:
        return HttpResponse(msg)

    #DB쿼리를 생성
    sql = "select idinstance as iderrorstatistics, country as keyname, count(*) as count "
    sql = sql + "from instances where iderror = %(id_error)s "
    sql = sql + "group by keyname order by count desc"

    params = {'id_error':iderror}
    places = ErrorStatistics.objects.raw(sql, params)

    #DB로부터 받은 데이터를 JSON으로 변경
    data = []
    counter = 0
    others = 0
    for idx, pl in enumerate(places):
        counter += 1
        if counter <= 5:
            tuple = {'label' : pl.keyname, 'value' : pl.count}
            data.append(tuple)
        else:
            others += pl.count
    if others != 0:
        tuple = {'label' : 'Ohters' , 'value' : others}
        data.append(tuple)


    return HttpResponse(json.dumps(data),'application/json')


def errorDetail(request,apikey,iderror):
    #에러의 상세한 페이지를 보여주는 루틴
    valid , message , user ,ErrorsElement, projectelement = author_check_error_page(request.user, apikey, iderror)
    if not valid:
        print message
        return HttpResponseRedirect('/urqa')

    # Status New일 경우 Open으로 자동변경
    # SuperUser는 자동변경에서 예외
    if not user.is_superuser and ErrorsElement.status == Status.New:
        ErrorsElement.status = Status.Open
        ErrorsElement.save()

    #manual_Auto
    isManual = True
    if ErrorsElement.autodetermine == 1:
        isManual = False
    else:
        isManual = True

    #Error에 해당하는 Instance들을 최근 100개 가져온다.
    instanceElements = Instances.objects.filter(iderror = ErrorsElement).order_by('-datetime')[:100]

    #wifi
    wifi = Instances.objects.filter(iderror = ErrorsElement,wifion = 1).count()
    #gps
    gps = Instances.objects.filter(iderror = ErrorsElement,gpson = 1).count()
    #mobilenetwork
    mobilenetwork = Instances.objects.filter(iderror = ErrorsElement,mobileon = 1).count()

    numobins = float(ErrorsElement.numofinstances)

    ###taglist###
    tagsElements = Tags.objects.filter(iderror = ErrorsElement)
    taglist = []
    for tag in tagsElements:
        taglist.append(tag.tag)

    ###callstack###
    callstackstr = ErrorsElement.callstack
    if(RANK.Native == ErrorsElement.rank):
        callstackstrlist = callstackstr.split('\n')
    else:
        callstackstrlist = callstackstr.split('\n\t')
    counter = 0
    callstacklist = []
    compile = re.compile('\(.*?:[0-9]*?\)')
    nativecompile = re.compile('\[.*?:.*?\]')

    #print '-----------------------'
    for linstr in callstackstrlist:
        tmp = {'counter' : 0, 'source' : '', 'value' : ''}
        counter += 1
        tmp['counter'] = counter
        tmp['value'] = re.sub('\(.*?:[0-9]*?\)','',linstr)
        #native
        tmp['value'] = re.sub('\[.*?:.*?\]','',tmp['value'])
        #print tmp['value']

        list = compile.findall(linstr)
        nativelist =  nativecompile.findall(linstr)
        source = ''

        if len(list) > 0:
            source = list[0]
        if len(nativelist) > 0:
            source = nativelist[0]

        tmp['source'] = source
        #print tmp['source']
        callstacklist.append(tmp)

    #print '-----------------------'

    ####instance#######
    instancelist = []
    instanceCount = 0
    for instance in instanceElements:
        instancetuple = {'datetime' : "", 'osversion' : '','appversion' : '' , 'device' : '', 'country' : '', 'idinstance' : ''}
        adtimezone = toTimezone(instance.datetime,projectelement.timezone)
        instancetuple['date'] = adtimezone.__format__('%Y.%m.%d')
        instancetuple['time'] = adtimezone.__format__('%H:%M:%S')
        instancetuple['osversion'] = instance.osversion
        instancetuple['appversion'] = instance.appversion
        instancetuple['device'] = instance.device
        instancetuple['country'] = instance.country
        instancetuple['idinstance'] = instance.idinstance
        instancelist.append(instancetuple)
        instanceCount = instanceCount + 1
        if instanceCount >= 100:
            break

    #projectelement = Projects.objects.get(apikey = apikey)
    #platformdata = json.loads(get_config('app_platforms'))
    #platformtxt = get_dict_value_matchin_key(platformdata,projectelement.platform)


    CommentElements = Comments.objects.filter(iderror = iderror).order_by('datetime')
    commentlist = []
    for comment in CommentElements:
        commenttuple = {}
        try:
            commentuser = AuthUser.objects.get(id = comment.uid.id)
        except ObjectDoesNotExist:
            continue
        adtimezone = toTimezone(comment.datetime,projectelement.timezone)
        print 'here',adtimezone,comment.datetime
        commenttuple['imagesrc'] = commentuser.image_path
        commenttuple['name'] = commentuser.first_name + ' ' + commentuser.last_name
        commenttuple['comment'] = comment.comment
        commenttuple['date'] = adtimezone.__format__('%Y.%m.%d')
        commenttuple['time'] = adtimezone.__format__('%H:%M:%S')
        commenttuple['ownercomment'] = comment.uid == user and True or False
        commenttuple['id'] = comment.idcomment
        commentlist.append(commenttuple)

    #DB에서 얻어돈 데이터들을 Web에 표시할 수 있도록 Template Rendering적용
    userdict = getUserProfileDict(user)
    apikeydict = getApikeyDict(apikey)
    settingdict = getSettingDict(projectelement,user)

    adtimezone_first = toTimezone(ErrorsElement.createdate,projectelement.timezone)
    adtimezone_last = toTimezone(ErrorsElement.lastdate,projectelement.timezone)
    detaildict = {
        'iderror' : iderror,
        'ErrorScore' : ErrorsElement.errorweight,
        'isManual' :  isManual,
        'ErrorName' : ErrorsElement.errorname,
        'ErrorFile' : '(' +ErrorsElement.errorclassname + ':' + ErrorsElement.linenum + ')',
        'Errornumofinstances' : ErrorsElement.numofinstances,
        'Errorrecur' : ErrorsElement.recur,
        'Errorstatus' : ErrorsElement.status,
        'Errorswifi' : int(wifi/numobins * 100),
        'Errorsgps' : int(gps/numobins * 100),
        'ErrorStatus' : ErrorsElement.status + 1,
        'Errorsmobilenetwork' : int(mobilenetwork/numobins * 100),
        'Errorsmemoryusage' : ErrorsElement.totalmemusage / ErrorsElement.numofinstances,
        'createdate' : adtimezone_first.__format__('%Y.%m.%d'),
        'lastdate' : adtimezone_last.__format__('%Y.%m.%d'),
        'ErrorRankColor' : ErrorsElement.rank == RANK.Suspense and 'Nothing' or RANK.rankcolor[ErrorsElement.rank],
        'isNative' : ErrorsElement.rank == RANK.Native ,
        'tag_list' : taglist,
        'callstack' : callstacklist,
        'instance_list' : instancelist,
        'comment_list' : commentlist,
        'so_file_list' : Sofiles.objects.filter(pid = projectelement)
    }
    ctxdict  = dict(userdict.items() + apikeydict.items() + settingdict.items() + detaildict.items() )

    tpl = loader.get_template('details.html')
    #ctx = Context(ctxdict);
    return render(request,'details.html',ctxdict)

def instancedetatil(request, apikey, iderror, idinstance):
    #Instance Data의 자세한 내용을 표시
    #권한 있나 없나 체크
    valid , message , user ,ErrorsElement, projectelement = author_check_error_page(request.user, apikey, iderror)
    if not valid:
        print message
        return HttpResponseRedirect('/urqa')

    #instance정보
    instance = Instances.objects.filter(idinstance = int(idinstance)).values()
    #dict = instance.objects.values()
    #datetime은 json sealize 안되서 ....

    key_to_remove = 'datetime'
    #인스턴스테이블에 있는 애러 시간, 발생 클래스, 위치 기타 등등을 얻어와 웹에 보여줌
    dict = {key : value for key, value in instance[0].items() if key != key_to_remove}
    adtimezone = toTimezone(instance[0]['datetime'],projectelement.timezone)
    dict['datetime'] = adtimezone.__format__('%Y.%m.%d - %H:%M:%S')
    result = json.dumps(dict)

    #single 즉 get일땐 __dict__ filter 즉 복수 일땐 obejcts.values() 이것때문에 한시간 날림
    return HttpResponse(result,'application/json')

def log(request, apikey, iderror, idinstance):
    #Instance의 로그를 읽어와 보여줌
    #권한 있나 없나 체크
    valid , message , user ,ErrorsElement, projectelement = author_check_error_page(request.user, apikey, iderror)
    if not valid:
        print message
        return HttpResponseRedirect('/urqa')
    '''
    instanceElement = Instances.objects.get(idinstance = int(idinstance))

    logpath = instanceElement.log_path
    logstringlist = []
    #File Read operation
    try:
        logfile = open(logpath)
        for s in logfile:
            logstringlist.append(s)
    except IOError:
        print 'file read fail'
    '''
    try :
        instanceLog=InstanceLog.objects.get(idinstance= int(idinstance));
        logstring = instanceLog.log;
    except ObjectDoesNotExist:
        logstring = ''
        print '!!!!!!!log does not exist'
    print logstring
    logstringlist=logstring.split("\n")
    return HttpResponse(json.dumps(logstringlist),'appliacation/json')

#instanceEventpath
def instanceeventpath(request, apikey, iderror, idinstance):
    #Instance의 개별 EventPath를 얻어온다.
    #권한 있나 없나 체크
    valid , message , user ,ErrorsElement, projectelement = author_check_error_page(request.user, apikey, iderror)
    if not valid:
        print message
        return HttpResponseRedirect('/urqa')

    instanceElement = Instances.objects.get(idinstance = idinstance)

    EventPathElements = Eventpaths.objects.filter(idinstance = instanceElement).order_by('depth')

    #Event Path에는 시간, 클래스이름, 라인수, 사용자 Tag데이터가 들어간다.
    eventpathlist = []
    for eventpath in EventPathElements:
        adtimezone = toTimezone(eventpath.datetime,projectelement.timezone)
        eventpathttuple = {'date' : '' , 'time' : '', 'class' : '', 'methodline' : ''}
        eventpathttuple['date'] =adtimezone.__format__('%Y.%m.%d')
        eventpathttuple['time'] =adtimezone.__format__('%H:%M:%S')
        eventpathttuple['class'] = eventpath.classname
        eventpathttuple['methodline'] = str(eventpath.methodname) + ':' + str(eventpath.linenum)
        eventpathlist.append(eventpathttuple)
        #print 'evd',eventpath.depth

    return HttpResponse(json.dumps(eventpathlist),'application/json')


def calc_eventpath(errorElement):
    #최근 10개데이터에서 이벤트 패스를 분석한다.
    #이벤트패스에서 가장 많이 발생한 이벤트가 가중치가 높아지고 높은 데이터는 사용자에게 굵은 Box로 시각화 된다.
    #node들 추출하기
#    eventHashs = []
    instance_limit_count = 10 #최근 몇개의 Instance의 이벤트패스만 표시할지 결정
    depth_max = 10 # event path 최대 깊이
    depth_count = 6 # Depth몇개 표현할지 정함


    ins_count_limit = max(1, errorElement.numofinstances - instance_limit_count)

    id_count = 0
    k2i_table = {}
    i2k_table = {}
    link_table = {}

    depth = 10
    #print 'ins_count_limit',ins_count_limit
    while depth > (depth_max - depth_count):
        eventHash = {}
        #최근 인스턴스를 우선적으로 비교하기위해 -idinstance를 사용함
        eventElements = Eventpaths.objects.filter(iderror=errorElement,depth=depth,ins_count__gte=ins_count_limit).order_by('-idinstance')

        #print 'event:',depth,eventElements
        limit_count = 0
        for event in eventElements:
            key = str(depth) + ':' + event.classname + ':' + event.methodname + ':' + str(event.linenum)
            if event.label != None:
                key = key + ':' + event.label
            else:
                key = key + ': '
            #key = str(depth) + ':' + str(event.linenum)
            if not key in eventHash:
                eventHash[key] = 1
            else:
                eventHash[key] += 1
            limit_count += 1
            if limit_count == instance_limit_count:
                break;
        sorted_list = sorted(eventHash, key=eventHash.get, reverse=True)
        #print 'sorted_list',sorted_list
        #이벤트가 5개를 초과하면 5번째를 Others로 변경함
        other_count = 0
        if len(sorted_list) > 5:
            while len(sorted_list) > 4:
                key = sorted_list[4]
                other_count += eventHash[key]
                del(eventHash[key])
                sorted_list.pop(4)
            eventHash[str(depth) + ':' + 'Others: : : '] = other_count
            sorted_list.append(str(depth) + ':' + 'Others: : : ')
        #print sorted_list
        #print len(sorted_list)

        #id 발급하기
        for key in sorted_list:
            k2i_table[key] = id_count
            i2k_table[id_count] = key
            id_count += 1

        depth -= 1

    #print 'k2i_table',k2i_table
    #print 'i2k_table',i2k_table
    instanceElements = Instances.objects.filter(iderror=errorElement,ins_count__gte=ins_count_limit).order_by('-idinstance')

    #print 'instanceElements',instanceElements
    limit_count = 0
    for instanceElement in instanceElements:
        #print instanceElement.idinstance
        eventElements = Eventpaths.objects.filter(iderror=errorElement,idinstance=instanceElement).order_by('-depth')

        length = min(len(eventElements),depth_count)
        for i in range(0,length-1):
            #print i
            source_key = str(eventElements[i].depth) + ':' + eventElements[i].classname + ':' + eventElements[i].methodname + ':' + str(eventElements[i].linenum)
            if eventElements[i].label != None:
                source_key = source_key + ':' + eventElements[i].label
            else:
                source_key = source_key + ': '
            #source_key = str(eventElements[i].depth) + ':' + str(eventElements[i].linenum)
            #print 'source_key',source_key

            if not source_key in k2i_table:
                if (str(eventElements[i].depth) + ':' + 'Others: : : ') in k2i_table:
                    source_id = k2i_table[str(eventElements[i].depth) + ':' + 'Others: : : ']
                else:
                    print "Error : do not find source_key " , source_key
                    source_id = -1
            else:
                source_id = k2i_table[source_key]

            target_key = str(eventElements[i+1].depth) + ':' + eventElements[i+1].classname + ':' + eventElements[i+1].methodname + ':' + str(eventElements[i+1].linenum)
            if eventElements[i+1].label != None:
                target_key = target_key + ':' + eventElements[i+1].label
            else:
                target_key = target_key + ': '
            #target_key = str(eventElements[i+1].depth) + ':' + str(eventElements[i+1].linenum)
            #print 'target_key',target_key
            if not target_key in k2i_table:
                if (str(eventElements[i].depth) + ':' + 'Others: : : ') in k2i_table:
                    target_id = k2i_table[str(eventElements[i+1].depth) + ':' + 'Others: : : ']
                else:
                    print "Error : do not find target_key " , target_key
                    target_id = -1

                #target_id = k2i_table[str(eventElements[i+1].depth) + ':' + 'Others: : : ']
            else:
                target_id = k2i_table[target_key]

            link_key = '%d>%d' % (source_id, target_id)
            if link_key in link_table:
                link_table[link_key] += 1
            else:
                link_table[link_key] = 1
            #print source_key, target_key, source_id, target_id

        limit_count += 1
        if limit_count == instance_limit_count:
            break

    #print i2k_table
    #print link_table

    result = {}
    result['nodes'] = []
    for id in i2k_table:
        result['nodes'].append({'name':i2k_table[id]})
    result['links'] = []
    for link in link_table:
        key = link.split('>')
        sid = int(key[1])
        tid = int(key[0])
        result['links'].append({'source':sid,'target':tid,'value':link_table[link]})
    #print json.dumps(result)
    return result

#Deprecated eventpath
def eventpath(request,apikey,iderror):
    valid , message , user ,ErrorsElement, projectelement = author_check_error_page(request.user, apikey, iderror)
    if not valid:
        print message
        return HttpResponseRedirect('/urqa')
    result = calc_eventpath(ErrorsElement)
    return HttpResponse(json.dumps(result),'application/json')


def author_check_error_page(username,apikey,iderror):

    valid , message , userelement, projectelement = validUserPjt(username,apikey)

    if not valid:
        return valid , message , '',''

    try:
        ErrorsElement = Errors.objects.get(iderror = iderror)
    except ObjectDoesNotExist:
        return False, 'DoesNotExist ErrorsElement' , '',''

    return True, 'success' , userelement ,ErrorsElement, projectelement


"""
		SELECT DISTINCT `appstatistics`.`appversion` FROM `appstatistics` WHERE 
				`appstatistics`.`pid` = 186
						order by `appstatistics`.`appversion` DESC
	appElements = Appstatistics.objects.distinct().filter(pk=Projects.objects.get(apikey = apikey))
	
	valid_app = appElements.order_by('-appversion')
	valid_os = appElements.order_by('-osversion')
	

	valid_app , valid_os 의 for 문을 통한 자바스크립트 로직을 Front End 에서
	하는게 어떨지?
"""	
def filter_view(request,apikey):
    #Filter page를 Randering하는 루틴
    username = request.user

    valid , message , userelement, projectelement = validUserPjt(username,apikey)

    if not valid:
        return HttpResponseRedirect('/urqa')

    week, today = getTimeRange(TimeRange.weekly,projectelement.timezone)

    try:
        projectElement = Projects.objects.get(apikey = apikey)
    except ObjectDoesNotExist:
        print 'invalid pid'
        return HttpResponse('')

    # Post 로 원하는 Date의 range를 얻어와서
    errorElements = Errors.objects.filter(pid = projectElement , lastdate__range = (week, today) ).order_by('-errorweight','rank', '-lastdate')
    valid_tag = Tags.objects.filter(pid=projectElement).values('tag').distinct().order_by('tag')
    valid_class = errorElements.values('errorclassname').distinct().order_by('errorclassname')

    #valid_app = Appstatistics.objects.filter(iderror__in=errorElements).values('appversion').distinct().order_by('-appversion')
    #valid_os = Osstatistics.objects.filter(iderror__in=errorElements).values('osversion').distinct().order_by('-osversion')

    valid_app = Appstatistics.objects.filter(pid=projectElement).values('appversion').distinct().order_by('-appversion')
    valid_os = Osstatistics.objects.filter(pid=projectElement).values('osversion').distinct().order_by('-osversion')


    # Web Rendering용 데이터 만들기
    osv_list = []
    os_idx = -1
    prev_v = ['-1','-1','-1']
    for e in valid_os:
        v = e['osversion'].split('.')
        if len(v) < 2:
            v.append(' ')
        if len(v) < 3:
            v.append(' ')
        if v[0] != prev_v[0] or v[1] != prev_v[1]:
            prev_v = v
            os_idx += 1
            osv_list.append({})
            osv_list[os_idx]['key'] = '%s.%s' % (v[0],v[1])
            osv_list[os_idx]['value'] = []
        osv_list[os_idx]['value'].append(e['osversion'])


    appv_list = []
    app_idx = -1
    prev_v = ['-1','-1','-1']
    for e in valid_app:
        v = e['appversion'].split('.')
        if len(v) < 2:
            v.append(' ')
        if len(v) < 3:
            v.append(' ')
        if v[0] != prev_v[0] or v[1] != prev_v[1]:
            prev_v = v
            app_idx += 1
            appv_list.append({})
            appv_list[app_idx]['key'] = '%s.%s' % (v[0],v[1])
            appv_list[app_idx]['value'] = []
        appv_list[app_idx]['value'].append(e['appversion'])


    tag_list = []
    for e in valid_tag:
        tag_list.append(e['tag'])

    class_list = []
    for e in valid_class:
        class_list.append(e['errorclassname'])

    osv_margin = ''
    for i in range(0,5 - len(osv_list)):
        osv_margin += ' '

    appv_margin = ''
    for i in range(0,5 - len(appv_list)):
        appv_margin += ' '


    user = AuthUser.objects.get( username = request.user )

    tpl = loader.get_template('filter.html')
    filterdict = {
        #'ServerURL' : 'http://'+request.get_host() + '/urqa/project/',
        'tag_list' : tag_list,
        'class_list' : class_list,
        'osv_list' : osv_list,
        'margin' : {'osv':osv_margin,'appv':appv_margin},
        'appv_list' : appv_list,
        'max_error' : errorElements.count()
    }
    
    userdict = getUserProfileDict(user)
    apikeydict = getApikeyDict(apikey)
    settingdict = getSettingDict(projectelement,user)
    
    ctxdict  = dict(userdict.items() + apikeydict.items() + settingdict.items() + filterdict.items() )
    ctx = Context(ctxdict);


    return HttpResponse(tpl.render(ctx))

    #return render(request, 'filter.html', ctx)


def error_list(request,apikey):
    #Error Filtering페이지에서 보여줄 리스트를 랜더링함
    username = request.user

    valid , message , userelement, projectelement = validUserPjt(username,apikey)

    if not valid:
        return HttpResponseRedirect('/urqa')
    try:
        projectElement = Projects.objects.get(apikey = apikey)
    except ObjectDoesNotExist:
        print 'invalid pid'
        return HttpResponse(json.dumps({"response":"fail"}), 'application/json');

    jsonData = json.loads(request.POST['json'],encoding='utf-8')



    #Appstatistics.objects.values('ierror').annotate(iderror_count=Count('iderror')).filter(pid=projectElement).group_by('iderror')


    date = int(jsonData['date'])
    _status = [[0,1,2,3],[0],[1],[2],[3]]
    status = _status[int(jsonData['status'])]
    rank = jsonData['rank']
    tags = jsonData['tags']
    classes = jsonData['classes']
    appversion = jsonData['appv']
    if appversion and appversion[0] == 'All':
        appversion = []
    osversion = jsonData['osv']
    if osversion and osversion[0] == 'All':
        osversion = []

    page = jsonData['page']
    num = jsonData['num']
    #Filtering Query를 적용하여 해당하는  Error를 보여줌

    week, today = getTimeRange(date,projectElement.timezone)

    ##일단 로직을 추가 하고 page, num 처리하여씀 여기서 속도가 느릴 경우 errorElements 쪽을 수정
    errorElements = Errors.objects.filter(pid=projectElement,
                                          rank__in=rank,
                                          status__in=status,lastdate__range=(week,today)
    ).order_by('-errorweight','rank', '-lastdate')
    #print '1',errorElements
    #print classes
    if classes:
        errorElements = errorElements.filter(errorclassname__in=classes)
    #print tags
    if tags:
        #tagElements = Tags.objects.filter(iderror__in=errorElements,tag__in=tags).values('iderror').distinct().order_by('iderror')

        tagElements = Tags.objects.select_related('iderror').filter(iderror__in=errorElements,tag__in=tags).values('iderror').distinct().order_by('iderror')[page * num: (page+1) * num]
        print tagElements
        iderror_list = []
        for e in tagElements:
            iderror_list.append(int(e['iderror']))
        errorElements = errorElements.filter(iderror__in=iderror_list)
    #print appversion
    if appversion:
        print 'appversion',appversion
        appvElements = Appstatistics.objects.select_related().filter(iderror__in=errorElements,appversion__in=appversion).values('iderror').distinct().order_by('iderror')
        print 'appvElements',appvElements
        iderror_list = []
        for e in appvElements:
            iderror_list.append(int(e['iderror']))
        #if iderror_list:
        errorElements = errorElements.filter(iderror__in=iderror_list)
    #print osversion
    if osversion:
	iderror_list = []
	for v in osversion:
          if v == "M. ":
            v= "M"
          osvElements = Osstatistics.objects.select_related().filter(iderror__in=errorElements,osversion__startswith=v).values('iderror').distinct().order_by('iderror')
          for e in osvElements:
              iderror_list.append(int(e['iderror']))
        #if iderror_list:
        errorElements = errorElements.filter(iderror__in=iderror_list)

    #print errorElements


    errorElements = errorElements[page*num : (page+1) * num]

    result = []
    for e in errorElements.iterator():
        adtimezone = toTimezone(e.lastdate,projectelement.timezone)
        #print adtimezone
        new_e = {}
        new_e['iderror'] = e.iderror
        new_e['color'] = RANK.rankcolor[e.rank]
        new_e['rank'] = e.rank
        new_e['status'] = e.status#Status.toString[e.status]
        new_e['errorname'] = e.errorname
        new_e['errorclassname'] = e.errorclassname
        new_e['linenum'] = e.linenum
        new_e['count'] = e.numofinstances
        new_e['year'] = adtimezone.year
        new_e['month'] = '%02d' % adtimezone.month
        new_e['day'] = '%02d' % adtimezone.day
        new_e['es'] = e.errorweight
        new_e['auto'] = e.autodetermine
        new_e['tags'] = []
        tags = Tags.objects.filter(iderror=e)
        for t in tags:
            new_e['tags'].append(t.tag)
        result.append(new_e)
        #print new_e

    return HttpResponse(json.dumps(result), 'application/json')

def chstatus(request,apikey,iderror):
    #Error의 Status를 변경하는 루틴
    #Error의 Status는 0=New, 1=Open, 2=Ignore, 3=Fix를 의미한다.
    result, msg, userElement, projectElement, errorElement = validUserPjtError(request.user,apikey,iderror)

    print msg
    if not result:
        return HttpResponse(msg)
    status = request.POST['status']
    #print 'y',status
    errorElement.status = status
    errorElement.save()
    return HttpResponse('success')


"""
    errorElements = Errors.objects.filter(pid=projectElement)

    instances =
	Instances.objects.prefetch_related('iderror').filter(iderror__in=errorElements,,iderror__lastdate__range=(past,today),datetime__range=(past,today)).order_by('-appversion')[page * num : (page + 1) * num]

test query 

	Instances.objects.prefetch_related('iderror').annotate(sum_app=Count('appversion').group_by('appversion')
"""

def so_list(request,apikey,iderror):
	pass

def appv_ratio(request,apikey):
    #Filter페이지에 보여줄 App, OS Version의 비율을 계산하는 루틴
    #에러가 많이 발생한 App, OS Version일 수록 비율이 크게 계산된다.

    jsonData = json.loads(request.POST['json'],encoding='utf-8')

    num = request.POST.get('num', 10)
    page = request.POST.get('page', 0)

    retention = int(jsonData['retention'])
    depth = int(jsonData['depth'])

    username = request.user
    valid , message , userElement, projectElement = validUserPjt(username,apikey)
    if not valid:
        return HttpResponseRedirect('/urqa')

    past, today = getTimeRange(retention,projectElement.timezone)
    #errorElements = Errors.objects.filter(pid=projectElement,lastdate__range=(past,today))

    data = {'appv':{},'osv':{}}
    instances = Instances.objects.select_related('pid').filter(
        pid=projectElement, datetime__range=(past, today))

    #Instances.objects.select_related('pid').values('appversion').filter(pid=projectElement,datetime__range=(past,today)).annotate(count=Count('appversion')).order_by('-count')
    print 1
    appv_instances = instances.values('appversion').annotate(count=Count('appversion')).order_by('-count')
    for i in appv_instances.iterator():
        key = i['appversion']
        print key
        #if not key in data['appv']:
        data['appv'][key] = i['count']
        #else:
        #   data['appv'][key] += 1
    #print "data['appv']",data['appv']
    print 2
    osv_list = {}
    os_instances = instances.values('osversion').annotate(count=Count('osversion')).order_by('-count')
    for i in os_instances.iterator():
        k = i['osversion'].split('.')
        if len(k) < 2:
            k.append(' ')
        key = k[0]+'.'+k[1]
        if not key in data['osv']:
            data['osv'][key] = i['count']
            osv_list[key] = []
        else:
            data['osv'][key] += i['count']

    print 3
    max_count = 5
    appv_data = sorted(data['appv'].iteritems(), key=operator.itemgetter(1), reverse=True)

    appv_others = []
    if len(appv_data) > max_count:
        appv_others.append(appv_data[max_count-1][0])

    while len(appv_data) > max_count:
        appv_data[max_count-1] = ('Others',appv_data[max_count-1][1] + appv_data[max_count][1])
        appv_others.append(appv_data[max_count][0])
        appv_data.pop(max_count)
    print 4
    osv_data = sorted(data['osv'].iteritems(), key=operator.itemgetter(1), reverse=True)
    osv_others = []
    if len(appv_data) > max_count:
        osv_others.append(appv_data[max_count-1][0])

    print 5
    while len(osv_data) > max_count:
        osv_data[max_count-1] = ('Others', osv_data[max_count-1][1] + osv_data[max_count][1])
        osv_others.append(osv_data[max_count][0])
        osv_data.pop(max_count)

    print 6
    return HttpResponse(json.dumps({'total':instances.count(),'appv':appv_data,'osv':osv_data,'osv_list':osv_list,'appv_others':appv_others,'osv_others':osv_others}), 'application/json');

