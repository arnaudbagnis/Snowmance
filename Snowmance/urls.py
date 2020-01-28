"""Snowmance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from app.models.person import Person
from app.views import IndexView, RegisterView, PersonSearchView, PersonSearchTagView, LoginView, ProfileView

# from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', PersonSearchView.as_view(), name='app_index'),
    url(r'register/$', RegisterView.as_view(), name='app_register_view'),
    url(r'profil/$', ProfileView.as_view(), name='app_profile_view'),
    url(r'login/$', LoginView.as_view(), name='app_login_view'),
    path('person/tag/<int:pk>', PersonSearchTagView.as_view(), name='app_cocktail_search_tag')
]