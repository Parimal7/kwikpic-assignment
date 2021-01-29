# Project Structure

The main project is called locallibrary, and it has two applications
- catalog(fully functional)
- notifications(only one view for testing purpose).

The MiddleWare can be defined once in any application of our choice. In this case, it is defined in the catalog application.

```python
#filepath = catalog/middleware/filter_ip_middleware.py
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
```

The decorator **property_not_important** can be imported to all applications under the project. For example, in the notifications application view,

```python
from django.shortcuts import render
from catalog.middleware.filter_ip_middleware import property_not_important
# Create your views here.

@property_not_important
def index2(request):
    return render(request, 'index2.html')

```

This will perform the required function.