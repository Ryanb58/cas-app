"""
"""
from django.conf.urls import url, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from api.views import Me


urlpatterns = [
    url('^me/$', Me.as_view()),
    url('^token/$', TokenObtainPairView.as_view()),
    url('^token/refresh/$', TokenRefreshView.as_view()),
]
