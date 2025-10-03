from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .forms import LoginForm, RegisterForm

from .models import User

# Create your views here.

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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
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
        'user': user,
        'form': form
    }
    return render(request, 'login.html', context)