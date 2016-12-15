from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update_ratings$', views.update_ratings, name='update_ratings'),
    url(r'^register', views.register, name='register'),
    url(r'^rankings', views.get_ratings, name='rankings')
]
