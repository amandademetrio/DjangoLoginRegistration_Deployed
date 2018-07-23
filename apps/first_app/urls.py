from django.conf.urls import url
from . import views

urlpatterns = [
    #Rendering routes
    url(r'^$', views.index),
    url(r'user/(?P<number>[0-9]+)$', views.loaduser),
    url(r'myaccount/(?P<number>[0-9]+)$', views.loadedituser),

    #Processing routes
    url(r'processregistration$', views.registration), 
    url(r'logout$', views.logout),
    url(r'login$', views.login),
    url(r'addquote$', views.addquote),
    url(r'edituser$', views.edituser),
    url(r'createlike$', views.createlike),
    url(r'deletequote/(?P<number>[0-9]+)$', views.deletequote)
] 