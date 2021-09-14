from django.urls import path

from . import views


app_name = 'general_app'
urlpatterns = [
    path('', views.index_view, name='index-view'),
]
