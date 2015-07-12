from rest_framework import permissions
from urqa.models import Projects


class ProjectsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        api_key = view.kwargs.get('api_key')
        if not api_key:
            return False
        return True if get_or_none(Projects, apikey=api_key) else False

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None