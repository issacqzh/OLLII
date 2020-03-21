from django.urls import path
from . import views

urlpatterns = [
	path('help4mom/',views.help4mom,name='help4mom'),
	path('home/',views.home,name='home'),
	path('about/',views.about,name='about'),
	path('implementor/',views.implementor,name='implementor'),
	path('vocabulary/',views.vocabulary,name='vocabulary'),
	path('definition/',views.definition,name='definition')
]