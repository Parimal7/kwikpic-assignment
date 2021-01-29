from django.shortcuts import render
from catalog.middleware.filter_ip_middleware import property_not_important
# Create your views here.

#@property_not_important
def index2(request):
    return render(request, 'index2.html')
