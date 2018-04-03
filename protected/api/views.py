from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers import TokenUserSerializer


class Me(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_classes = ()

    def get(self, request):
        return Response(TokenUserSerializer(request.user).data)
