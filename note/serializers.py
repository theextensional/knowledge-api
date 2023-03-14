from rest_framework import serializers


class NoteAddViewSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=20000)


class NoteEditViewSerializer(serializers.Serializer):
    new_title = serializers.CharField(max_length=255, required=False)
    new_content = serializers.CharField(max_length=20000, required=False)

    def validate(self, data):
        if not data.get('new_title') and not data.get('new_content'):
            raise serializers.ValidationError("required new_title or new_content, or both")

        return data
