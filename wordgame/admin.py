from django.contrib import admin

# Register your models here.

from .models import Game, Guess, User, Word

admin.site.register(User)
admin.site.register(Game)
admin.site.register(Guess)
admin.site.register(Word)

