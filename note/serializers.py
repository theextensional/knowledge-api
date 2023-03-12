from rest_framework import serializers


class NoteAddViewSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField(max_length=20000)