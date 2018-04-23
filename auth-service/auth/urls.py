"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views import generic
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework import views, serializers, status, routers
from rest_framework.response import Response

import django_cas_ng.views

from api.views import (
    TokenObtainPairView, UserViewSet, GroupViewSet, RealmViewSet,
    ExternalAuthenticationViewSet, OrganizationViewSet, login
)


api_router = routers.DefaultRouter()

api_router.register(r'users', UserViewSet, base_name='user')
api_router.register(
    r'organizations', OrganizationViewSet, base_name='organization')
api_router.register(r'groups', GroupViewSet, base_name='group')
api_router.register(r'realms', RealmViewSet, base_name='realm')
api_router.register(
    r'external_authentication', ExternalAuthenticationViewSet,
    base_name='external_authentication')

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', generic.RedirectView.as_view(
         url='/api/', permanent=False), name='home'),
    url(r'^api/auth/$', get_schema_view()),
    # url(r'^api/auth/', include(
    #     'rest_framework.urls', namespace='rest_framework')),

    url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
    url(r'^api/auth/token/verify/$', TokenVerifyView.as_view(),
        name='token_verify'),

    url(r'^api/auth/', include((api_router.urls, 'api'))),

    url(r'^accounts/login$', login, name='cas_ng_login'),
    # url(r'^accounts/login$', django_cas_ng.views.login, name='cas_ng_login'),
    url(r'^accounts/logout$', django_cas_ng.views.logout, name='cas_ng_logout'),
]
