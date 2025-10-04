import datetime
from django import template
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .forms import AdminDayForm, AdminUserForm, GuessForm, LoginForm, RegisterForm

from .models import Game, User, Word

css_classes = {
    'gray': 'bg-gray-500',
    'yellow': 'bg-yellow-500',
    'green': 'bg-green-500'
}
def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    return None

def index(request):
    user = get_current_user(request)
    games_played_today = Game.objects.filter(user=user, started_at__date=datetime.date.today()).count()
    context = {
        'user': user,
        'games_played_today': games_played_today
    }
    return render(request, 'index.html', context)

def register(request):
    user = get_current_user(request)
    if user:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            if user:
                form.add_error('username', 'Username already exists. Please choose a different username.')
            else:
                password = form.cleaned_data['password']
                User.objects.create_user(username=username, password=password)
                return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def login(request):
    user = get_current_user(request)
    if user:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                request.session['user_id'] = user.id
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password. Please ensure you have registered.')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

def logout(request):
    request.session.flush()
    return redirect('index')

def start_game(request):
    user = get_current_user(request)
    if not user:
        return redirect('index')
    games_played_today = Game.objects.filter(user=user, started_at__date=datetime.date.today()).count()
    if games_played_today >= 3:
        print('games_played_today', games_played_today)
        messages.error(request, 'You have already played 3 games today. Please come back tomorrow.')
        return redirect('index')
    print('games_played_today', games_played_today)
    game = Game.objects.create(user=user, word=Word.objects.order_by('?').first())
    return redirect('play', game_id=game.id)

def play(request, game_id):
    print('game_id', game_id)
    user = get_current_user(request)
    if not user:
        return redirect('index')
    game = Game.objects.filter(user=user, id=game_id).first()
    if not game:
        return redirect('index')
    if game.finished:
        return redirect('index')
    if game.guesses.count() >= 5:
        game.finished = True
        game.won = False
        game.save()
        return redirect('index')
    if request.method == 'POST':
        target = game.word.text
        form = GuessForm(request.POST)
        if form.is_valid():
            guess_text = form.cleaned_data['guess_text']
            guess = game.guesses.create(game=game, guess_text=guess_text)
            if guess.guess_text == target:
                game.finished = True
                game.won = True
                game.save()
            
    else:
        form = GuessForm()
    display = []
    for g in game.guesses.all():
        row = []
        guess = g.guess_text
        target_chars = list(target)
        colors = ['gray' for _ in range(5)]

        for i, c in enumerate(guess):
            if c == target_chars[i]:
                colors[i] = 'green'
                target_chars[i] = None
        for i, c in enumerate(guess):
            if c in target_chars and colors[i] == 'gray':
                colors[i] = 'yellow'
                target_chars[target_chars.index(c)] = None
        for i, c in enumerate(guess):    
            row.append({
                    'char': c, 
                    'color': colors[i], 
                    'css_class': css_classes[colors[i]]
            })
        display.append(row)
    context = {
        'game': game,
        'form': form,
        'display': display or [],
        'guesses': game.guesses.count(),
        'remaining_rows': [""] * (5 - game.guesses.count()),
        'list_of_5': list(range(5))
    }
    return render(request, 'play.html', context)

def get_admin_day_report(date):
    games_on_date = Game.objects.filter(started_at__date=date)
    users_played = games_on_date.values('user').distinct().count()
    correct_guesses = games_on_date.filter(won=True).count()
    class Report():
        headers = ['Number of Users Played', 'Number of Correct Guesses']
        values = []
    report = Report()
    report.values.append([users_played, correct_guesses])
    return report

def get_admin_user_report(username):
    user = User.objects.filter(username=username).first()
    class Report():
        headers = ['Date', 'Number of Games Played', 'Number of Correct Guesses']
        values = []
    report = Report()
    if user:
        dates = user.games.values_list('started_at__date', flat=True).distinct()
        for date in dates:
            games_on_date = user.games.filter(started_at__date=date)
            games_played_on_date = games_on_date.count()
            correct_guesses_on_date = games_on_date.filter(won=True).count()
            report.values.append([date, games_played_on_date, correct_guesses_on_date])
    return report
    

def admin_day(request):
    user = get_current_user(request)
    if not user or not user.is_admin:
        return redirect('index')
    if request.method == 'POST':
        form = AdminDayForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            report = get_admin_day_report(date)
            context = {
                'report': report,
                'form': form
            }
            return render(request, 'admin_day.html', context)
    else:
        form = AdminDayForm()
    context = {
        'form': form
    }
    return render(request, 'admin_day.html', context)

def admin_user(request):
    user = get_current_user(request)
    if not user or not user.is_admin:
        return redirect('index')
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            report = get_admin_user_report(username)
            context = {
                'report': report,
                'form': form,
                'username': username
            }
            return render(request, 'admin_user.html', context)
    else:
        form = AdminUserForm()
    context = {
        'form': form
    }
    return render(request, 'admin_user.html', context)