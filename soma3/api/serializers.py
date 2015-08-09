from rest_framework import serializers
from urqa.models import Projects, ErrorsbyApp


class ProjectsSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = Projects


class ErrorsbyAppSerializer(serializers.Serializer):
	class meta:
		model = ErrorsbyApp

