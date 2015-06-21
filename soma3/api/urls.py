from django.conf.urls import patterns, url
from api.views import ProjectsList

urlpatterns = patterns('api.views',
    url(r'^api/projects', ProjectsList.as_view()),
)
