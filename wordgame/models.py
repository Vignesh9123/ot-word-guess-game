from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Word(models.Model):
    text = models.CharField(
        max_length=5,
        unique=True,
        db_index=True,
        validators=[MinLengthValidator(5)]
    )

    def __str__(self):
        return self.text

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="games")
    started_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)
    won = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.word.text}"

class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="guesses")
    guess_text = models.CharField(
        max_length=5,
        validators=[MinLengthValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guess_text} ({self.game.user.username})"