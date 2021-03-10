from django.db import models

class Joke(models.Model):
	setup_text = models.CharField(max_length=200)
	punchline_text = models.CharField(max_length=200)
	def __str__(self):
		return self.setup_text + " - " + self.punchline_text
	def get_setup(self):
		return self.setup_text
	def get_punchline(self):
		return self.punchline_text

class Message(models.Model):
	message_text = models.CharField(max_length=200)
	message_nametag = models.CharField(max_length=50)
	message_date = models.DateTimeField('date sent', auto_now_add=True)
	def __str__(self):
		return "\'" + self.message_text + "\'" +  " - " + self.message_nametag
	def get_message(self):
		return self.message_text

class JokeBotAI(models.Model):
	knock_knock = models.BooleanField(default=False)
	setup = models.BooleanField(default=False)
	new_setup = models.CharField(max_length=200)
	current_joke = models.ForeignKey(Joke, on_delete=models.CASCADE)
	gave_knock_knock = models.BooleanField(default=False)
	gave_setup = models.BooleanField(default=False)
	def heard_knock_knock(self):
		return self.knock_knock
	def heard_setup(self):
		return self.setup
	def get_new_setup(self):
		return self.new_setup
	def get_current_setup(self):
		return self.current_joke.get_setup()
	def get_current_punchline(self):
		return self.current_joke.get_punchline()
	def said_knock_knock(self):
		return self.gave_knock_knock
	def said_setup(self):
		return self.gave_setup



