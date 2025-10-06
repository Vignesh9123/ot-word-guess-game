from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from wordgame.models import Word, User

class Command(BaseCommand):
    help = "Populate the database with initial data"

    def handle(self, *args, **options):
        if not Word.objects.exists():
            words = ["AUDIO","HOMER","JOKER","TONER","TOWER","APPLE","GRAPE","PLANT","SHIFT","BRAVE",
                    "CRANE","DRIVE","EPOCH","FAITH","GHOST","HONEY","INNER","JUDGE","KNOCK","LIGHT"]
            for i in range(20):
                word = Word(text=words[i])
                word.save() 
        
        if not User.objects.filter(username="AdminUser").exists():
            user = User(username="AdminUser", password=make_password("AdminPassword@123"), is_admin=True)
            user.save()
        
        self.stdout.write(self.style.SUCCESS("Database initialized successfully with admin user. Please login with username: AdminUser and password: AdminPassword@123"))
