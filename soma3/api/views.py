# Create your views here.
# -*- coding: utf-8 -*-
from django.db.models import Count

from rest_framework import generics
from rest_framework.views import APIView

from api.serializers import ProjectsSerializer, ErrorsbyAppSerializer

from urqa.models import Projects, Viewer, Instances, ErrorsbyApp


class ProjectsList(generics.ListCreateAPIView):
    model = Projects
    serializer_class = ProjectsSerializer
    # paginate_by_param = 'page_size'
    # paginate_by = 10


    def get_queryset(self):
        viewer_list = [v['pid'] for v in Viewer.objects.filter(uid=self.request.user.id).values('pid')]

        queryset = self.model.objects.raw('''
          SELECT `projects`.`pid`, `projects`.`name` , projects.apikey, projects.platform, projects.stage, count('errors.iderror') count
          FROM `instances`
          INNER JOIN `errors` ON ( `instances`.`iderror` = `errors`.`iderror` ) INNER JOIN `projects` ON ( `errors`.`pid` = `projects`.`pid` )
          WHERE instances.datetime > '2015-6-14 15:0:0'
          AND errors.status in (0,1)
          {owner_id}
          {viewer_id}
          GROUP BY projects.pid;
        '''.format(
            owner_id=' AND projects.owner_id = {0} '.format(
                self.request.user.id) if not self.request.user.is_superuser else '',
            viewer_id='OR projects.pid in ({0}) '.format(
                ','.join(viewer_list)) if not self.request.user.is_superuser else ''
        ))
        return queryset

class ProjectsInfoList(APIView):
	'''
		대시보드 기초 구성 API
		:return
			weeklyBug
			weeklyActiveUser
			avgBugRate
			bugFixRate
	'''
	pass

class DailyErrorList(generics.ListCreateAPIView):
    serializer_class = ErrorsbyAppSerializer
    '''
    original query
    sql = "select count(*) as errorcount ,appversion, DATE_FORMAT(datetime,'%%y-%%m-%%d') as errorday "
    sql = sql + "from instances A, errors B "
    sql = sql + "where A.iderror = B.iderror "
    sql = sql + "and B.pid = %(pidinput)s "
    sql = sql + "and B.status in (0,1) "
    sql = sql + "and A.datetime > %(pasttime)s"
    sql = sql + "group by errorday"
    '''
    def get_queryset(self):
        api_key = self.kwargs.get('api_key')

        pid = Projects.objects.get(apikey= api_key).pid
        queryset = ErrorsbyApp.objects.raw('''
			select count(*) as errorcount, appversion, DATE_FORMAT(datetime,'%%y-%%m-%%d') as errorday 
			from instances A
			inner join errors B on B.iderror = A.iderror
			where B.status in (0, 1)
			and B.pid = '%s'
			group by errorday
			order by errorday desc
			limit %d
		''' % (pid, 7)
        )
        return queryset


class RankErrorList(generics.ListCreateAPIView):
	'''
		Rank 별 Error 갯수를 리턴하는 API
	'''
	pass


class ClassErrorList(generics.ListCreateAPIView):
	'''
		Class 별 Error 갯수를 리턴하는 API
	'''
	pass


class OSErrorList(generics.ListCreateAPIView):
	'''
		OS Version 별 Error 갯수를 리턴하는 API
	'''
	pass


