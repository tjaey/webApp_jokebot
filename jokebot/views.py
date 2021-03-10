from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models.query import QuerySet
import random

from .models import Message, Joke, JokeBotAI

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
		jokebotAI = JokeBotAI.objects.all()
		jokebot = jokebotAI[0]
		if(jokebot.said_setup()):
			return tellPunchline(request, jokebot)
		elif(jokebot.said_knock_knock()):
			return tellSetup(request, jokebot)
		elif(jokebot.heard_setup()):
			return learnPunchline(request, message, jokebot)
		elif(jokebot.heard_knock_knock()):
			return learnSetup(request, message, jokebot)
		elif(message.message_text == 'knock knock'):
			return learnNewJoke(request, jokebot)
		elif(message.message_text == "tell me a joke"):
			return tellJoke(request, jokebot)
		else:
			return sendGreetingGeneric(request)
	except:
		return sendGreetingError(request)

def tellJoke(request, jokebot):
	try:
		joke_list = Joke.objects.all()
		num = joke_list.count()
		joke_num = random.randint(1,num)
		joke = joke_list.get(id=joke_num)
		jokebot.current_joke = joke
		jokebot.gave_knock_knock = True
		jokebot.save()
		new_message = "Knock knock"
		m = Message(message_text=new_message, message_nametag="Jokebot")
		m.save()
		return HttpResponseRedirect(reverse('jokebot:index'))
	except:
		return sendGreetingNoJoke(request)

def tellSetup(request, jokebot):
	try:
		setup = jokebot.get_current_setup()
		jokebot.gave_setup = True
		jokebot.save()
		m = Message(message_text=setup, message_nametag="Jokebot")
		m.save()
		return HttpResponseRedirect(reverse('jokebot:index'))
	except:
		return sendGreetingNoJoke(request)

def tellPunchline(request, jokebot):
	try:
		punchline = jokebot.get_current_punchline()
		jokebot.gave_setup = False
		jokebot.gave_knock_knock = False
		jokebot.save()
		m = Message(message_text=punchline, message_nametag="Jokebot")
		m.save()
		return HttpResponseRedirect(reverse('jokebot:index'))
	except:
		return sendGreetingNoJoke(request)

def learnSetup(request, message, jokebot):
	jokebot.setup = True
	jokebot.new_setup = message.message_text
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
	j = Joke(setup_text=jokebot.get_new_setup(), punchline_text=message.message_text)
	j.save()
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


