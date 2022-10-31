from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth


# Create your models here.
class Game(models.Model):
    game_id = models.CharField(max_length=251, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    my_bulls = models.IntegerField(null=True)
    my_cows = models.IntegerField(null=True)
    my_guess = models.CharField(max_length=10, null=True)
    my_number = models.CharField(max_length=10, null=True)
    your_bulls = models.IntegerField(null=True)
    your_cows = models.IntegerField(null=True)
    your_guess = models.CharField(max_length=10, null=True)
    your_number = models.CharField(max_length=10, null=True)
    capacity = models.IntegerField(default=4, editable=False)
    attempts = models.IntegerField(default=0)
    available_digits_str = models.CharField(max_length=10, default="0123456789")
    dual_game = models.BooleanField(default=True)
    game_started = models.BooleanField(default=False)
    new_game_requested = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    upper_poster = models.CharField(max_length=250, null=True)
    result_code = models.IntegerField(null=True)
    elapsed = models.IntegerField(default=0)

    class Meta:
        ordering = ['game_id']
        db_table = 'game'

    def __str__(self):
        return self.game_id


class MyHistory(models.Model):
    game_id = models.ForeignKey(Game, to_field="game_id", on_delete=models.CASCADE)
    items = ArrayField(ArrayField(models.CharField(max_length=10), size=3), null=True)

    class Meta:
        ordering = ['game_id']
        db_table = 'my_history'

    def __str__(self):
        return self.game_id


class YourHistory(models.Model):
    game_id = models.ForeignKey(Game, to_field="game_id", on_delete=models.CASCADE)
    items = ArrayField(ArrayField(models.CharField(max_length=10), size=3), null=True)

    class Meta:
        ordering = ['game_id']
        db_table = 'your_history'

    def __str__(self):
        return self.game_id


class TotalSet(models.Model):
    game_id = models.ForeignKey(Game, to_field="game_id", on_delete=models.CASCADE)
    set = ArrayField(models.CharField(max_length=10, null=True), null=True)

    class Meta:
        ordering = ['game_id']
        db_table = 'total_set'

    def __str__(self):
        return self.game_id


class FixtureList(models.Model):
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    winner = models.IntegerField()
    attempts = models.IntegerField()
    time = models.DateTimeField()
    duration = models.IntegerField()

    class Meta:
        ordering = ['id']
        db_table = 'fixture_list'


class Privileges(models.Model):
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    create_other = models.BooleanField(default=False)
    modify_self = models.BooleanField(default=False)
    modify_other = models.BooleanField(default=False)
    delete_self = models.BooleanField(default=False)
    delete_other = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        db_table = 'privileges'

    def __str__(self):
        return self.username


# class UserExt(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField(upload_to="images/")
#
#     def __str__(self):
#         return str(self.user)
#
#
# def create_user_ext(self):
#     UserExt.objects.create(user=self)
#
#
# auth.models.User.add_to_class('create_user_ext', create_user_ext)
