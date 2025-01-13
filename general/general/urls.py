"""general URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from general_app.views import *
from rest_framework.authtoken import views


urlpatterns = [
    path('', include('general_app.urls', namespace='index')),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/v1/humans/', HumansAPIView.as_view()),
    path('api/v1/human-contacts/', HumanContactsAPIView.as_view()),
    path('api/v1/human-names/', HumanNamesAPIView.as_view()),
    path('api/v1/human-terminals/', HumanTerminalPresenceAPIView.as_view()),
    path('api/v1/human-sim-cards/', HumanSimPresenceAPIView.as_view()),
    path('api/v1/installations/', InstallationsAPIView.as_view()),
    path('api/v1/objects/', ObjectAPIView.as_view()),
    path('api/v1/object/<int:pk>/', ObjectsAPIUpdate.as_view()),
    path('api/v1/schedule/', ScheduleAPIView.as_view()),
    path('api/v1/simlist/', SimAPIView.as_view()),
    path('api/v1/termlist/', TerminalAPIView.as_view()),
    path('api/v1/tracker-models/', ModelTerminalsAPIView.as_view()),
    path('api/v1/userlist/', UsersAPIView.as_view()),
    path('auth/', include('django.contrib.auth.urls')),
]
