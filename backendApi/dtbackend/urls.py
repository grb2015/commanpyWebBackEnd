from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^getuserinfo', views.getuserinfo, name='getuserinfo'),  
]