from django.core.exceptions import PermissionDenied    
from django.conf import settings
from django.urls import reverse

def property_not_important(function):
    """
    Decorator
    """
    orig_func = function
    setattr(orig_func, 'property_not_important', True)

    return function


class FilterIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        prop_not_important = getattr(view_func, 'property_not_important', False)
        if prop_not_important:
            print('property not important')
            raise PermissionDenied
        return view_func(request, *view_args, **view_kwargs)

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip not in settings.ALLOWED_IP_BLOCKS:
            raise PermissionDenied

        response = self.get_response(request)

        return response
        
