from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Message

def index(request):
	message_list = Message.objects.order_by('message_date')
	context = {'message_list': message_list}
	return render(request, 'jokebot/index.html', context)

def submitMessage(request):
	if(request.POST['new_message']):
		new_message = request.POST['new_message']
		m = Message(message_text=new_message, message_nametag="you")
		m.save()
	return HttpResponseRedirect(reverse('jokebot:index'))

def success(request):
	return HttpResponse("action was a success.")