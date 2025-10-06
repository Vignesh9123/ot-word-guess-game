from django.core.management.base import BaseCommand
from wordgame.models import Word

class Command(BaseCommand):
    help = "Populate the database with initial data"

    def handle(self, *args, **options):
        words = ["AUDIO","HOMER","JOKER","TONER","TOWER","APPLE","GRAPE","PLANT","SHIFT","BRAVE",
                "CRANE","DRIVE","EPOCH","FAITH","GHOST","HONEY","INNER","JUDGE","KNOCK","LIGHT"]
        for i in range(20):
            word = Word(text=words[i])
            word.save() 
        
        self.stdout.write(self.style.SUCCESS("Database initialized successfully."))
