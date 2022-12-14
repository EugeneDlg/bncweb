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