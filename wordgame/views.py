import datetime
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .forms import LoginForm, RegisterForm

from .models import Game, User, Word


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
    template = loader.get_template('index.html')
    context = {
        'user': user
    }
    return HttpResponse(template.render(context))

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
                form.add_error('username', 'Invalid username or password. Please ensure you have registered.')
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
        return redirect('index')
    print('games_played_today', games_played_today)
    game = Game.objects.create(user=user, word=Word.objects.order_by('?').first())
    return redirect('play', game_id=game.id)

def play(request, game_id):
    print('game_id', game_id)
    return HttpResponse(f'Game {game_id}')