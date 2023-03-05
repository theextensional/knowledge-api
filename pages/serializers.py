from rest_framework import serializers


class ProfileViewSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=1, max_length=50)
    last_name = serializers.CharField(min_length=1, max_length=50, allow_blank=True)
