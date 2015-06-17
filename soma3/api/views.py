# Create your views here.
# -*- coding: utf-8 -*-
from rest_framework import generics, serializers
from urqa.models import Projects

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects

class ProjectsList(generics.ListCreateAPIView):
    model = Projects
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        queryset = self.model.objects.all()

        return queryset