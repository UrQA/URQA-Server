from rest_framework import serializers
from urqa.models import Projects, Errors


class ProjectsSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Projects
        exclude = ('owner_uid',)


class ErrorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Errors