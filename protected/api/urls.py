"""
"""
from django.conf.urls import url, include

from api.views import Me


urlpatterns = [
    url('^me/$', Me.as_view()),
]
