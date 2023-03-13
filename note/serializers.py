from rest_framework import serializers


class NoteAddViewSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=20000)


class NoteEditViewSerializer(serializers.Serializer):
    new_title = serializers.CharField(max_length=255)
    new_content = serializers.CharField(max_length=20000)

    def validate(self, data):
        if data['new_title'] is None and data['new_content'] is None:
            raise serializers.ValidationError("required new_title or new_content, or both")

        return data
