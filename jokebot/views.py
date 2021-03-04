from django.shortcuts import render
from django.http import HttpResponse

from .models import Message

def index(request):
	return render(request, 'jokebot/index.html')
