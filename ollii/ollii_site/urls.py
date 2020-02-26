from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('about/',views.about,name='about'),
	path('help4mom/',views.help4mom,name='help4mom'),
	path('vocabulary/',views.vocabulary,name='vocabulary'),
	path('later/',views.later,name='later')
]