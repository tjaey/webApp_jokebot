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

def error(request):
	return HttpResponse("action was an error.")

def generateResponse(request, Message):
	try:
		if(request.session['knock_knock']):
			return learnSetup(request, Message)
		elif(Message.message_text == 'knock knock'):
			return learnNewJoke(request)
		elif(Message.message_text == "tell me a joke"):
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

def learnSetup(request, Message):
	request.session['setup'] = True
	request.session['setup_text'] = Message.message_text
	new_message = Message.message_text+" who?"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index'))

def learnPunchline(request, Message):
	request.session['knock_knock'] = False
	request.session['setup'] = False
	new_message = "Hahaha! Thank you! That was a great joke!"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index')) 

def learnNewJoke(request):
	new_message = "Who's there?"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	request.session['knock_knock'] = True
	return HttpResponseRedirect(reverse('jokebot:index'))

def sendGreetingNoJoke(request):
	new_message = "Hi, I'm Jokebot 1.0! I don't know any jokes yet, would you like to tell me one?"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index'))

def sendGreetingGeneric(request):
	request.session['setup'] = False
	request.session['knock_knock'] = False
	new_message = "Hi, I'm Jokebot 1.0!\nIf you would like me to tell you a joke say 'tell me a joke'.\nIf you would like to teach me a joke say 'knock knock'."
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index')) 

def sendGreetingError(request):
	new_message = "error"
	m = Message(message_text=new_message, message_nametag="Jokebot")
	m.save()
	return HttpResponseRedirect(reverse('jokebot:index'))


