from django.db import models

class Greeting(models.Model):
	greeting_text = models.CharField(max_length=200)
	def __str__(self):
		return self.greeting_text

class Joke(models.Model):
	setup_text = models.CharField(max_length=200)
	punchline_text = models.CharField(max_length=200)
	def __str__(self):
		return self.setup_text + " - " + self.punchline_texts