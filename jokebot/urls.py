from django.urls import path

from . import views

app_name = 'jokebot'

urlpatterns = [
	path('', views.index, name='index'),
	path('submitMessage/', views.submitMessage, name='submitMessage'),
	path('success/', views.success, name='success'),
]