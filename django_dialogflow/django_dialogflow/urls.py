from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'chat/$', views.chat_view, name='chat'),
    url(r'^$', views.index_view, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^base_layout$', views.base_layout, name="base_layout"),
  	url(r'^serviceworker(.*.js)$', views.serviceworker, name="serviceworker"),
    url(r'^webhook/', views.webhook, name='webhook'),
]
