from django.conf.urls import patterns, include, url

urlpatterns = patterns('ui.views',
    url(r'^signin', 'signin'),
    url(r'^signout', 'signout'),
    url(r'^.*', 'index'),
)
