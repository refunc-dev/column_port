from functools import wraps
from django.http import Http404
from django.shortcuts import render

import uuid


def owner_check(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'project_id' in kwargs:
            project_list = list(map(str, list(request.user.members_projects.all().values_list('id', flat=True))))
            if kwargs['project_id'] not in project_list:
                raise Http404
        return func(request, *args, **kwargs)
    return wrapper