from rest_framework import serializers


class TokenUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
