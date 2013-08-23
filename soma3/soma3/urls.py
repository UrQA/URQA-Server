# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from soma3 import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #test page
    url(r'^urqa$', 'urqa.views.index'),
    url(r'^urqa/posttest$', 'urqa.views.posttest'),
    url(r'^urqa/fileuploadtest$', 'urqa.views.fileuploadtest'),
    url(r'^urqa/cleanup$', 'urqa.views.cleanup'),

    #client module
    url(r'^urqa/client/connect$', 'client.views.connect'),
    url(r'^urqa/client/send/exception$', 'client.views.receive_exception'),
    url(r'^urqa/client/send/exception/native$', 'client.views.receive_native'),
    url(r'^urqa/client/send/exception/dump/(?P<idinstance>\d+)$', 'client.views.receive_native_dump'),
    url(r'^urqa/client/send/exception/log/(?P<idinstance>\d+)$', 'client.views.receive_exception_log'),
    #url(r'^urqa/client/send/eventpath/(?P<idsession>\d+)$', 'client.views.receive_eventpath'),
    #url(r'^urqa/client/send/eventpath/(?P<idsession>.+)$', 'client.views.receive_eventpath'),
    url(r'^urqa/client/send/eventpath$', 'client.views.receive_eventpath'),

    #user manage
    url(r'^urqa/user/registration$', 'usermanage.views.registration'),
    url(r'^urqa/user/delete', 'usermanage.views.delete_req'),
    url(r'^urqa/user/login$', 'usermanage.views.login_req'),
    url(r'^urqa/user/logout$', 'usermanage.views.logout_req'),

    #project manage
    url(r'^urqa/project/registration$', 'projectmanage.views.registration'),
    url(r'^urqa/project/delete$', 'projectmanage.views.delete_req'),
    url(r'^urqa/project/(?P<pid>\d+)/userdashboard$', 'projectmanage.views.userdashboard'),
    url(r'^urqa/project/(?P<pid>\d+)/userdashboard/dailyes$', 'projectmanage.views.dailyesgraph'),
    url(r'^urqa/project/(?P<pid>\d+)/userdashboard/typees$', 'projectmanage.views.typeesgraph'),
    #project manage static
    (r'(?:.*?/)?(?P<path>(css|font|js|images)/.+)$', 'projectmanage.views.mediapathrequest'),

    #errors
    url(r'^urqa/project/(?P<pid>\d+)/errors/(?P<iderror>\d+)/tag/new$', 'errors.views.newTag'),
    url(r'^urqa/project/(?P<pid>\d+)/errors/(?P<iderror>\d+)/tag/delete$', 'errors.views.deleteTag'),
    url(r'^urqa/project/(?P<pid>\d+)/errors/(?P<iderror>\d+)/comment/new$', 'errors.views.newComment'),
    url(r'^urqa/project/(?P<pid>\d+)/errors/(?P<iderror>\d+)/comment/delete$', 'errors.views.deleteComment'),

    #symbol
    url(r'^urqa/project/(?P<pid>\d+)/errors/(?P<iderror>\d+)/symbol/list$', 'errors.views.so_list'),
    url(r'^urqa/project/(?P<pid>\d+)/symbol/upload$', 'projectmanage.views.so_upload'),



    # Examples:
    # url(r'^$', 'soma4.views.home', name='home'),
    # url(r'^soma4/', include('soma4.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
