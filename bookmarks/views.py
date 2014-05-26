from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render, get_object_or_404
from bookmarks.forms import *

# def main_page(request):
# 	# to load the main_page.html template
# 	template = get_template('main_page.html')
# 	# Set the variable in the template
# 	variables = Context({
# 		'head_title': 'Main page',
# 		'page_title': 'Welcome to Elmusico',
# 		'page_body': 'Blah blah blah blah blah'
# 		})
# 	#pass the variables and create a HTML output
# 	output = template.render(variables)
# 	#return it
# 	return HttpResponse(output)

def main_page(request):
	return render_to_response(
		'main_page.html',
		# {'user': request.user},
		context_instance = RequestContext(request)
	)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

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
	variables = RequestContext(request, {
		'username': username,
		'favoriteList': ScoreSheetList
		})

	output = template.render(variables)
	return render_to_response('user_page.html', variables)

def register_page(request):
	print request
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			# Some magic SQL happen here!
			
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				# print username;
				password=form.cleaned_data['password1'],
				# print password;
				# email=form.cleaned_data['email']
				)
			return HttpResponseRedirect('/register/success/')
	else:
		form = RegistrationForm()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response(
			'registration/register.html',
			variables,
			context_instance = RequestContext(request)
			)

def artist_save_page(request):
	if request.method == 'POST':
		form = ArtistSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.
			artist, created = Artist.objects.get_or_create(
				ArtistName=form.cleaned_data['name'],
				Date=form.cleaned_data['date'],
				Status=form.cleaned_data['status']
				)
			artist.save()
			return HttpResponseRedirect(
				'/user/%s/' % request.user.username
			)
		print "invalid form"
		return HttpResponseRedirect(
				'/user/%s/' % request.user.username
		)
	else:
		form = ArtistSaveForm()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('artist_save.html', variables, context_instance = RequestContext(request))

def musician_save_page(request):
	if request.method == 'POST':
		form = MusicianSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.
			musician, created = Musician.objects.get_or_create(
				MusicianName=form.cleaned_data['name'],
				DOB=form.cleaned_data['dob']				
				)
			musician.save()
			return HttpResponseRedirect(
				'/user/%s/' % request.user.username
			)
	else:
		form = MusicianSaveForm()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('musician_save.html', variables)

def album_save_page(request):
	if request.method == 'POST':
		form = AlbumSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.
			album, created = Album.objects.get_or_create(
				AlbumName=form.cleaned_data['name'],
				ContributingArtists = form.cleaned_data['contributing_artist'],
				ReleaseDate=form.cleaned_data['release_date'],
				Label = form.cleaned_data['label'],
				Genre = form.cleaned_data['genre']
				)
			album.save()
			return HttpResponseRedirect(
				'/user/%s/' % request.user.username
			)
	else:
		form = AlbumSaveForm()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('album_save.html', variables)

def search_page(request):
	form = SearchForm()
	artists = []
	albums = []

	show_results = False
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = SearchForm({'query' : query})
			artists = Artist.objects.filter (ArtistName__icontains=query)[:10]
			albums = Album.objects.filter (AlbumName__icontains=query)[:10]
	variables = RequestContext(request, { 'form': form,
		'artists': artists,
		'albums': albums,
		'show_results': show_results,
		# 'show_tags': True,
		# 'show_user': True
		})
	return render_to_response('search.html', variables)