from abc import ABC

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TestAPI


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250)
    first_name = serializers.CharField(max_length=250)
    email = serializers.EmailField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


# class TestAPISerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=250)
#     item = serializers.CharField(max_length=10, default='item')
#     digit = serializers.IntegerField()
#     date = serializers.DateTimeField()
#
#     def create(self, validated_data):
#         return TestAPI.objects.create(**validated_data)


# class TestAPISerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TestAPI
#         fields = '__all__'


class TestAPISerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    item = serializers.CharField(max_length=10, required=False)
    digit = serializers.IntegerField()
    date = serializers.DateTimeField()
    username = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    def create(self, validated_data):
        return TestAPI.objects.create(**validated_data)