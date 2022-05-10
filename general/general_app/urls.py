from django.urls import path

from . import views

app_name = 'general_app'
urlpatterns = [
    path('', views.index_view, name='index-view'),
    path('clients/', views.clients_view, name='clients-view'),
    path('deletesim/', views.delete_sim_view, name='delete-sim-view'),
    path('maks-func/', views.maks_view, name='maks-func-view'),
    path('info-view/', views.info_view, name='info-view'),
    path('server/<int:server_id>/', views.server_view, name='server-view'),
]
