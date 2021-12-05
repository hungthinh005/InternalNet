from django.http import HttpResponse
from django.shortcuts import redirect

def roles(allowed_roles=[]):
    def layer(access_func):
        def layer1(request, *args, **kwargs):
            # group = None
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return access_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to do this')
        return layer1
    return layer