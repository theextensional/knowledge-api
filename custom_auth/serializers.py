from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=1, max_length=50)
    password2 = serializers.CharField(min_length=1, max_length=50)
    username = serializers.SlugField(min_length=1, max_length=50)
    email = serializers.EmailField(min_length=1, max_length=50)


class AddTokenSerializer(serializers.Serializer):
    app_name = serializers.CharField(min_length=1, max_length=20)


class EditTokenSerializer(serializers.Serializer):
    app_name = serializers.CharField(min_length=1, max_length=20)
    token_id = serializers.IntegerField(min_value=1)
