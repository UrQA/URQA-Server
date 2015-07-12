# Create your views here.
# -*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.response import Response

from api.serializers import ProjectsSerializer, ErrorsSerializer
from api.utils import ProjectsPermission

from urqa.models import Projects, Viewer, Errors


class ProjectsList(generics.ListCreateAPIView):
    model = Projects
    serializer_class = ProjectsSerializer

    def get_count(self, queryset):
        return len(list(queryset))

    def get(self, request):
        viewer_list = [v['pid'] for v in Viewer.objects.filter(uid=self.request.user.id).values('pid')]

        page = int(self.request.query_params.get('page', 1))
        page_size = int(self.request.query_params.get('page_size', 10))

        queryset = self.model.objects.raw('''
          SELECT `projects`.`pid`, `projects`.`name` , projects.apikey, projects.platform, projects.stage, count('errors.iderror') count
          FROM `instances`
          INNER JOIN `errors` ON ( `instances`.`iderror` = `errors`.`iderror` ) INNER JOIN `projects` ON ( `errors`.`pid` = `projects`.`pid` )
          WHERE instances.datetime > '2015-6-14 15:0:0'
          AND errors.status in (0,1)
          {owner_id}
          {viewer_id}
          GROUP BY projects.pid
        '''.format(
            owner_id=' AND projects.owner_id = {0} '.format(
                self.request.user.id
            ) if not self.request.user.is_superuser else '',
            viewer_id='OR projects.pid in ({0}) '.format(
                ','.join(viewer_list)
            ) if not self.request.user.is_superuser else ''
        ))

        count = self.get_count(queryset)
        queryset = queryset[(page -1) * page_size:page * page_size]

        return Response({
            'count': count,
            'results': [self.serializer_class(data).data for data in queryset]
        })

class ErrorsList(generics.ListAPIView):
    model = Errors
    serializer_class = ErrorsSerializer
    paginate_by_param = 'page_size'
    paginate_by = 10
    permission_classes = (ProjectsPermission,)
    def get_queryset(self):
        queryset = self.model.objects
        pid = Projects.objects.get(apikey= self.kwargs.get('api_key')).pid
        queryset = queryset.filter(pid=pid)
        return queryset