from django.db import models


# Create your models here.
class Game(models.Model):
    game_id = models.CharField(max_length=251, unique=True)
    my_bulls = models.IntegerField(null=True, default=5, editable=False)
    my_cows = models.IntegerField(null=True)
    your_bulls = models.IntegerField(null=True)
    your_cows = models.IntegerField(null=True)
    my_guess = models.IntegerField(null=True)
    your_guess = models.IntegerField(null=True)
    your_number = models.IntegerField(null=True)
    capacity = models.IntegerField(default=4, editable=False)
    dual_game = models.BooleanField(null=True)
    game_started = models.BooleanField(null=True)
    start_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)

    class Meta:
        ordering = ['game_id']
        db_table = 'game'

    def __str__(self):
        return self.game_id