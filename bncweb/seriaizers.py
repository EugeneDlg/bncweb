from rest_framework import serializers
from django.contrib.auth.models import User

# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=250)
#     first_name = serializers.CharField(max_length=250)
#     email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'