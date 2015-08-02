from django.conf.urls import patterns, url
from api.views import ProjectsList, ErrorsList, ProjectsList2

urlpatterns = patterns('api.views',
    url(r'^api/projects$', ProjectsList.as_view()),
    url(r'^api/projects2$', ProjectsList2.as_view()),
    url(r'^api/(?P<api_key>.{8})/errors$', ErrorsList.as_view()),
)
