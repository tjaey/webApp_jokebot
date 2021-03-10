from django.test import TestCase

from .models import Joke

class JokeModelTests(TestCase):

	def test_has_joke_to_tell(self):
		"""
			has_joke_to_tell() returns false when Joke db is empty
		"""
