"""
"""
from django.conf.urls import url, include

from rest_framework_simplejwt.views import TokenRefreshView

from api.views import Me, TokenObtainPairView


urlpatterns = [
    url('^me/$', Me.as_view()),
    url('^token/$', TokenObtainPairView.as_view()),
    url('^token/refresh/$', TokenRefreshView.as_view()),
]
