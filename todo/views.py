import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View

from todo.models import Todo


class TodoListView(ListView):
    queryset = Todo.objects.all()
    template_name = 'index.html'


class CustomView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.content_type == "application/json":
            return JsonResponse({'status': 'failed', 'error': 'Unsupported content-type'})
        return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class TodoCreate(CustomView):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args, **kwargs):
        title = json.loads(request.body).get('title')
        if not title:
            return JsonResponse({'status': 'failed', 'error': 'Missed key named "title"'}, status=400)
        todo = Todo.objects.create(title=title)
        return JsonResponse({'status': 'success', 'id': todo.id})


@method_decorator(csrf_exempt, name='dispatch')
class TodoConfirm(CustomView):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args, **kwargs):
        obj_id = json.loads(request.body).get('id')
        if not obj_id:
            return JsonResponse({'status': 'failed', 'error': 'Missed key named "id"'}, status=400)
        try:
            todo = Todo.objects.get(id=obj_id)
        except Todo.DoesNotExist:
            return JsonResponse({'status': 'failed', 'error': 'Object not found'}, status=404)
        todo.completed = not todo.completed
        todo.save()
        return JsonResponse({'status': 'success', 'id': todo.id})


@method_decorator(csrf_exempt, name='dispatch')
class TodoDelete(CustomView):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args, **kwargs):
        obj_id = json.loads(request.body).get('id')
        if not obj_id:
            return JsonResponse({'status': 'failed', 'error': 'Missed key named "id"'}, status=400)
        try:
            todo = Todo.objects.get(id=obj_id)
        except Todo.DoesNotExist:
            return JsonResponse({'status': 'failed', 'error': 'Object not found'}, status=404)
        todo.delete()
        return JsonResponse({'status': 'success', 'id': todo.id})


from django.shortcuts import render, redirect
import cmd
import random
import smtplib
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from todo.forms import RegistrationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import AddBook
from django.contrib.auth.hashers import make_password
from email.mime.text import MIMEText
from core.settings import *
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = True
            user.save()




            return redirect('login')

    else:
        form = RegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})
# todo/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    form = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('base')
            else:
                messages.error(request, 'Username or password is incorrect')
    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('base')

