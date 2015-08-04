from rest_framework import serializers
from urqa.models import Projects


class ProjectsSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = Projects


class ErrorsbyAppSerializer(serializers.Serializer):
    errorcount = serializers.IntegerField()
    appversion = serializers.CharField(max_length=45)
    errorday = serializers.CharField(max_length=45)

