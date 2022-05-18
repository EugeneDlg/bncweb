from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class Game(models.Model):
    game_id = models.CharField(max_length=251, unique=True)
    my_bulls = models.IntegerField(null=True, default=5, editable=False)
    my_cows = models.IntegerField(null=True)
    my_guess = models.IntegerField(null=True)
    my_number = models.IntegerField(null=True)
    your_bulls = models.IntegerField(null=True)
    your_cows = models.IntegerField(null=True)
    your_guess = models.IntegerField(null=True)
    your_number = models.IntegerField(null=True)
    capacity = models.IntegerField(default=4, editable=False)
    attempts = models.IntegerField(default=0)
    available_digits_str = models.CharField(max_length=10, default="0123456789")
    dual_game = models.BooleanField(default=True)
    game_started = models.BooleanField(default=True)
    new_game_requested = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    upper_poster = models.CharField(max_length=250, null=True)

    class Meta:
        ordering = ['game_id']
        db_table = 'game'

    def __str__(self):
        return self.game_id


class MyHistory(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    items = ArrayField(ArrayField(models.IntegerField(), size=3), size=100)

    class Meta:
        ordering = ['game_id']
        db_table = 'my_history'

    def __str__(self):
        return self.game_id


class YourHistory(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    items = ArrayField(ArrayField(models.IntegerField(), size=3))

    class Meta:
        ordering = ['game_id']
        db_table = 'your_history'

    def __str__(self):
        return self.game_id


class TotalSet(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    set = ArrayField(models.IntegerField())

    class Meta:
        ordering = ['game_id']
        db_table = 'total_set'

    def __str__(self):
        return self.game_id


class CurrentSet(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    set = ArrayField(models.IntegerField())

    class Meta:
        ordering = ['game_id']
        db_table = 'current_set'

    def __str__(self):
        return self.game_id
