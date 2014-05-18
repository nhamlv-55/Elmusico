from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User


def main_page(request):
	# to load the main_page.html template
	template = get_template('main_page.html')
	# Set the variable in the template
	variables = Context({
		'head_title': 'Main page',
		'page_title': 'Welcome to Elmusico',
		'page_body': 'Blah blah blah blah blah'
		})
	#pass the variables and create a HTML output
	output = template.render(variables)
	#return it
	return HttpResponse(output)

def user_page(request, username):
	try:
		# print username
		user = User.objects.get(id=1)
		# print "1wsa"
	except User.DoesNotExist:
		raise Http404('Requested user not found.')


	#The automatically generated JOIN equivalent. To get all 
	# scoresheet that an user favor
	ScoreSheetList = user.favorite_set.all()

	template = get_template('user_page.html')
	variables = Context({
		'username': username,
		'favoriteList': ScoreSheetList
		})

	output = template.render(variables)
	return HttpResponse(output)