from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.hotel_index, name='hotel_index'),  # http://127.0.0.1:8000/hotel/ 首页路由
    url(r'^login/', views.hotel_login, name='hotel_login'),  # http://127.0.0.1:8000/hotel/login 登陆路由
]