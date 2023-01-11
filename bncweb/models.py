from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Visitors(models.Model):
    ip_address = models.GenericIPAddressField()
    os = models.CharField(max_length=250, default='')
    browser = models.CharField(max_length=250, default='')
    time = models.DateTimeField()

    class Meta:
        db_table = 'visitors'

    def __str__(self):
        return str(self.ip_address)


class TestAPI(models.Model):
    username = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    item = models.CharField(max_length=10, default='item')
    digit = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'testapi'

    def __str__(self):
        return str(self.username)

