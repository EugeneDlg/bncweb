from django.db import models
from django.urls import reverse


class Game(models.Model):
	game_id = models.CharField(max_length=250, unique=True)
	my_bulls = models.IntegerField()
	my_cows = models.IntegerField()
	your_bulls = models.IntegerField()
	your_cows = models.IntegerField()
	my_guess = models.IntegerField()
	your_guess = models.IntegerField()
	your_number = models.IntegerField()
	capacity = models.IntegerField()
	dual_game = models.BooleanField(default=True)
	game_started = models.BooleanField(default=True)
	start_time = models.DateTimeField(auto_now_add=True)
	finish_time = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['game_id']
		db_table = 'Game'

	def __str__(self):
		return self.game_id
