from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Game


class SettingsForm(forms.Form):
    def __init__(self, user, post_dict=None, *args, **kwargs):
        self.user = user
        self.post_dict = post_dict
        game = Game.objects.get(user=user)
        dictionary = {
            'capacity': game.capacity,
            'dual_game': int(game.dual_game)
        }
        super().__init__(dictionary, *args, **kwargs)

    def save(self):
        game = Game.objects.get(user=self.user)
        game.capacity = int(self.post_dict['capacity'])
        game.dual_game = bool(int(self.post_dict['dual_game']))
        game.save()

    caps = ((3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"))
    game_type = ((0, "Single"), (1, "Dual"))
    capacity = forms.ChoiceField(choices=caps, label="Capacity",
                                 help_text="How many digits will be used for playing?")
    dual_game = forms.ChoiceField(choices=game_type, label="Game type", widget=forms.RadioSelect,
                                  help_text='Will I play with you or without you?')

    class Meta:
        model = Game
        fields = ('capacity', 'dual_game')


