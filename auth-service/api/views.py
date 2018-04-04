from django.shortcuts import render

from rest_framework_simplejwt.views \
    import TokenObtainPairView as BaseTokenObtainPairView

from api.serializers import TokenObtainPairSerializer


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
