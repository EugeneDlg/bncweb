from django.db import models
from django.contrib.auth.models import User


class Extension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="images/")

    def __str__(self):
        return str(self.user)


def create_extension(self):
    Extension.objects.create(user=self)


User.add_to_class('create_extension', create_extension)
