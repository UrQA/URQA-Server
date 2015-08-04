from django.conf.urls import patterns, url
from api.views import ProjectsList, ProjectsInfoList, DailyErrorList

urlpatterns = patterns('api.views',
    url(r'^api/projects', ProjectsList.as_view()),

    url(r'^api/(?P<api_key>.{8})/info$', ProjectsInfoList.as_view()),
    url(r'^api/(?P<api_key>.{8})/daily$', DailyErrorList.as_view()),
)
