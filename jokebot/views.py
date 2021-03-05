from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Message, Greeting, Joke

def index(request):
	message_list = Message.objects.order_by('message_date')
	context = {'message_list': message_list}
	return render(request, 'jokebot/index.html', context)

def submitMessage(request):
	if(request.POST['new_message']):
		new_message = request.POST['new_message']
		m = Message(message_text=new_message, message_nametag="you")
		m.save()
		return generateResponse(request, m)
	return HttpResponseRedirect(reverse('jokebot:index'))


def success(request):
	return HttpResponse("action was a success.")

def generateResponse(request, Message):
	joke_list = Joke.objects.all()
	try:
		joke = joke_list.get(0)
		return tellJoke(request, joke)
	except:
		return sendGreeting(request)

def tellJoke(request, Joke):
	return HttpResponse("Pretend I told a great joke.")

def sendGreeting(request):
	new_message = "Hi, I'm Jokebot 1.0! I don't know any jokes yet, would you like to tell me one?"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index')) 