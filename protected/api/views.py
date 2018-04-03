from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views \
    import TokenObtainPairView as BaseTokenObtainPairView


from api.serializers import TokenUserSerializer
from api.serializers import TokenObtainPairSerializer


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(TokenUserSerializer(request.user).data)


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
