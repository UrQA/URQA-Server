# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from soma3 import settings
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


"""
UrQA: UrQA URL Settting
UrQA의 URL 설정
"""

urlpatterns = patterns('',
    #test page
    url(r'^$', RedirectView.as_view(url='/urqa/')),                 #UrQA메인페이지로 리다이렉트
    url(r'^urqa/$', 'urqa.views.index'),                            #UrQA메인페이지
    url(r'^urqa/login$', 'urqa.views.login'),                       #UrQA Login URL
    url(r'^urqa/posttest$', 'urqa.views.posttest'),                 #Test, Reserved
    url(r'^urqa/fileuploadtest$', 'urqa.views.fileuploadtest'),     #Test, Reserved
    url(r'^urqa/cleanup$', 'urqa.views.cleanup'),                   #Test, Reserved

    #unity cross domain
    url(r'^crossdomain.xml$', 'urqa.views.unity_crossdomain'),      #Unity Support cross-domain redirect

    #client module
    url(r'^urqa/client/connect$', 'client.views.connect'),          #Client Connection URL
    url(r'^urqa/client/send/exception$', 'client.views.receive_exception'),         #Client Exception Handler
    url(r'^urqa/client/send/exception/native$', 'client.views.receive_native'),     #Client Android Native Exception
    #url(r'^urqa/client/send/exception/dump/(?P<idinstance>\d+)$', 'client.views.receive_native_dump'),     #deprecated
    #url(r'^urqa/client/send/exception/log/(?P<idinstance>\d+)$', 'client.views.receive_exception_log'),    #deprecated
    #url(r'^urqa/client/send/eventpath/(?P<idsession>\d+)$', 'client.views.receive_eventpath'),             #deprecated
    #url(r'^urqa/client/send/eventpath/(?P<idsession>.+)$', 'client.views.receive_eventpath'),              #deprecated
    #url(r'^urqa/client/send/eventpath$', 'client.views.receive_eventpath'),                                #deprecated

    #user manage
    url(r'^urqa/user/registration$', 'usermanage.views.registration'),      #User 회원가입
    url(r'^urqa/user/resetpassword$', 'usermanage.views.resetpassword'),    #User password reset
    url(r'^urqa/user/delete$', 'usermanage.views.delete_req'),              #User 회원탈퇴
    url(r'^urqa/user/login$', 'usermanage.views.login_req'),                #User Login
    url(r'^urqa/user/logout$', 'usermanage.views.logout_req'),              #User Logout

    #oauth module
    url(r'^urqa/user/login_by_google$', 'oauth.views.login_by_google'),     #UrQA Google auth Login
    url(r'^urqa/user/auth_return/$', 'oauth.views.auth_return'),            #Urqa Google auth return point

    #project-list
    url(r'^urqa/projects$', 'projectmanage.views.projects'),                #UrQA Project list page

    #project manage
    url(r'^urqa/project/registration$', 'projectmanage.views.registration'),                #Project Create
    url(r'^urqa/project/(?P<apikey>.{8})/delete$', 'projectmanage.views.delete_req'),       #Project Remove
    url(r'^urqa/project/(?P<apikey>.{8})/modify$', 'projectmanage.views.modify_req'),       #Project Modify setting
    url(r'^urqa/project/(?P<apikey>.{8})/$', 'projectmanage.views.projectdashboard'),       #Project Dashboard
    url(r'^urqa/project/(?P<apikey>.{8})/dailyes/$', 'projectmanage.views.dailyesgraph'),   #Project Error by date graph
    url(r'^urqa/project/(?P<apikey>.{8})/typees/$', 'projectmanage.views.typeesgraph'),     #Project Error by type graph
    url(r'^urqa/project/(?P<apikey>.{8})/typees/color$', 'projectmanage.views.typeescolor'),#Proejct Color Logic
    url(r'^urqa/project/(?P<apikey>.{8})/viewer/registration$', 'projectmanage.views.viewer_registration'),#Project Viewer registration
    url(r'^urqa/project/(?P<apikey>.{8})/viewer/delete$', 'projectmanage.views.viewer_delete'), #Project Viewer remove


    #project manage static
    (r'(?:.*?/)?(?P<path>(css|font|js|images)/.+)$', 'urqa.views.mediapathrequest'),    #static file mapping
    #tutorial page
    (r'(?:.*?/)?(?P<path>(tutorial)/.+)$', 'urqa.views.tutorialrequest'),               #UrQA Tutorial Page


    #errors
    url(r'^urqa/project/(?P<apikey>.{8})/errors/$', 'errors.views.filter_view'),        #Error Filtering page
    url(r'^urqa/project/(?P<apikey>.{8})/errors/list$', 'errors.views.error_list'),     #Error List Page
    url(r'^urqa/project/(?P<apikey>.{8})/errors/appv_ratio$', 'errors.views.appv_ratio'),   #Error app version ratio
    #url(r'^urqa/project/(?P<apikey>.{8})/errors/osv_ratio$', 'errors.views.osv_ratio'),     #Error Os Version ratio
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/$', 'errors.views.errorDetail'), #Error Detail page
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/(?P<idinstance>\d+)$', 'errors.views.instancedetatil'),    #Error Instance Detail Page
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/(?P<idinstance>\d+)/log$', 'errors.views.log'),    #Error Log View Page
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/(?P<idinstance>\d+)/instanceeventpath$', 'errors.views.instanceeventpath'),    #Error Instance event path
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/eventpath$', 'errors.views.eventpath'),    #Error Event path calculation
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/tag/new$', 'errors.views.newTag'),         #Error Tagging
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/tag/delete$', 'errors.views.deleteTag'),   #Error Delete Tagging
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/comment/new$', 'errors.views.newComment'), #Error Create comment
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/comment/delete$', 'errors.views.deleteComment'),   #Error Delete Comment

    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/os$', 'errors.views.os'),          #Error OS Statistics
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/app$', 'errors.views.app'),        #Error App Statistics
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/device$', 'errors.views.device'),  #Error Device Statistics
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/country$', 'errors.views.country'),#Error Country Statistics

    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/status$', 'errors.views.chstatus'),#Error Change Status

    #Statistics
    url(r'^urqa/project/(?P<apikey>.{8})/statistics/$', 'statistics.views.statistics'),                 #Statistics Page
    #url(r'^urqa/project/(?P<apikey>.{8})/statistics/chartdata', 'statistics.views.chartdata'),
    url(r'^urqa/project/(?P<apikey>.{8})/statistics/chartdata/sbav', 'statistics.views.chartdata_sbav'), #Statistic Sessions Count by Appversion Chart
    url(r'^urqa/project/(?P<apikey>.{8})/statistics/chartdata/ebav', 'statistics.views.chartdata_ebav'), #Statistic Errors Count by Appversion Chart
    url(r'^urqa/project/(?P<apikey>.{8})/statistics/chartdata/erbc', 'statistics.views.chartdata_erbc'), #Statistic Error by Country Chart
    url(r'^urqa/project/(?P<apikey>.{8})/statistics/chartdata/erbd', 'statistics.views.chartdata_erbd'), #Statistic Error by Device Chart
    url(r'^urqa/project/(?P<apikey>.{8})/statistics/chartdata/erba', 'statistics.views.chartdata_erba'), #Statistic Error by Activity Chart
    url(r'^urqa/project/(?P<apikey>.{8})/statistics/chartdata/erbv', 'statistics.views.chartdata_erbv'), #Statistic Error by App/OS version Chart
    url(r'^urqa/project/(?P<apikey>.{8})/statistics/chartdata/ebcs', 'statistics.views.chartdata_ebcs'), #Statistic Error by Country Chart

    #symbol
    url(r'^urqa/project/(?P<apikey>.{8})/errors/(?P<iderror>\d+)/symbol/list$', 'errors.views.so_list'), #Uploaded Symbol(*.so)
    url(r'^urqa/project/(?P<apikey>.{8})/symbol/upload$', 'projectmanage.views.so_upload'),              #NDK Symbol(*.so) file upload

    #proguard map
    url(r'^urqa/project/(?P<apikey>.{8})/proguardmap/upload$', 'projectmanage.views.proguardmap_upload'),#Proguard Map file upload
    url(r'^urqa/project/(?P<apikey>.{8})/proguardmap/delete$', 'projectmanage.views.proguardmap_delete'),#Proguard Map file delete

    url(r'^urqa/v2/', include('api.urls'))
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
