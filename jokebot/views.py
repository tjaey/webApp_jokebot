from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Message, Greeting, Joke, JokeBotAI

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

def error(request):
	return HttpResponse("action was an error.")

def generateResponse(request, message):
	try:
		jokebot = JokeBotAI.objects.get(pk=1)
		if(jokebot.heard_setup()):
			return learnPunchline(request, message, jokebot)
		elif(jokebot.heard_knock_knock()):
			return learnSetup(request, message, jokebot)
		elif(message.message_text == 'knock knock'):
			return learnNewJoke(request, jokebot)
		elif(message.message_text == "tell me a joke"):
			return tellJoke(request)
		else:
			return sendGreetingGeneric(request)
	except:
		return sendGreetingError(request)

def tellJoke(request):
	try:
		joke_list = Joke.objects.all()
		joke = joke_list.get(id=0)
		new_message = "Pretend I told a great joke ;P"
		m = Message(message_text=new_message, message_nametag="Jokebot")
		m.save()
		return HttpResponseRedirect(reverse('jokebot:index'))
	except:
		return sendGreetingNoJoke(request)

def learnSetup(request, message, jokebot):
	jokebot.setup = True
	jokebot.save()
	new_message = message.message_text
	new_message += " who?"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index'))

def learnPunchline(request, message, jokebot):
	jokebot.knock_knock = False
	jokebot.setup = False
	jokebot.save()
	new_message = "Hahaha! Thank you! That was a great joke!"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index')) 

def learnNewJoke(request, jokebot):
	jokebot.knock_knock = True
	jokebot.save()
	new_message = "Who's there?"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index'))

def sendGreetingNoJoke(request):
	new_message = "Hi, I'm Jokebot 1.0! I don't know any jokes yet, would you like to tell me one?"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index'))

def sendGreetingGeneric(request):
	new_message = "Hi, I'm Jokebot 1.0!\nIf you would like me to tell you a joke say 'tell me a joke'.\nIf you would like to teach me a joke say 'knock knock'."
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index')) 

def sendGreetingError(request):
	new_message = "error"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index'))


