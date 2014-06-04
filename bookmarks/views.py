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

def song_save_page(request):
	if request.method == 'POST':
		form = SongSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.
			song, created = Song.objects.get_or_create(
				SongName=form.cleaned_data['name'],
				ASIN = form.cleaned_data['asin'],
				TrackId = form.cleaned_data['trackid'],
				ContributingArtists = form.cleaned_data['contributing_artist'],
				Genre = form.cleaned_data['genre'],
				Composer = form.cleaned_data['composer']
				)
			song.save()
			return HttpResponseRedirect(
				'/user/%s/' % request.user.username
			)
	else:
		form = SongSaveForm()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('song_save.html', variables)

def song_save_page_step1(request):
	if request.method == 'POST':
		form = SongSaveForm_step1(request.POST)
		if form.is_valid():
			ContributingArtists = form.cleaned_data['contributing_artist'].ArtistId
			print ContributingArtists
			t=HttpResponseRedirect(
				'/create_song_step2/%s/' %ContributingArtists
			)
			print t
			return t
	else:
		form = SongSaveForm_step1()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('song_save_step1.html', variables)

def song_save_page_step2(request, contributing_artist):
	print "DSADASDSADSA"
	if request.method == 'POST':
		form = SongSaveForm_step2(request.POST, ContributingArtists = contributing_artist)
		if form.is_valid():
			print "vl"
			# Create or get link.
			song, created = Song.objects.get_or_create(
				SongName=form.cleaned_data['name'],
				ASIN = form.cleaned_data['asin'],
				TrackId = form.cleaned_data['trackid'],
				ContributingArtists = Artist.objects.get(ArtistId=contributing_artist),
				Genre = form.cleaned_data['genre'],
				Composer = form.cleaned_data['composer']
				)
			song.save()
			return HttpResponseRedirect(
				'/song/%s/' % song.SongId
			)
	else:
		print "X"
		form = SongSaveForm_step2(ContributingArtists = contributing_artist)
		print form
		print "X2"
		variables = RequestContext(request, {
			'form': form
			})
		print form
		print "X3"
		return render_to_response('song_save_step2.html', variables)

def video_save_page(request):
	if request.method == 'POST':
		form = VideoSaveForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect(
				'/user/%s/' % request.user.username
			)
	else:
		form = VideoSaveForm()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('video_save.html', variables)

def search_page(request):
	form = SearchForm()
	artists = []
	albums = []
	songs = []

	show_results = False
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = SearchForm({'query' : query})
			artists = Artist.objects.filter (ArtistName__icontains=query)[:10]
			albums = Album.objects.filter (AlbumName__icontains=query)[:10]
			songs = Song.objects.filter(SongName__icontains=query)[:10]
		print songs, artists, albums
	variables = RequestContext(request, { 'form': form,
		'artists': artists,
		'albums': albums,
		'songs': songs,
		'show_results': show_results,
		# 'show_tags': True,
		# 'show_user': True
		})
	return render_to_response('search.html', variables)

def artist_page(request, artist_name):
	albums=[]
	try:
		# print username
		artist = Artist.objects.get(ArtistName=artist_name)
		# print "1wsa"
	except Artist.DoesNotExist:
		raise Http404('Requested artist not found.')


	#The automatically generated JOIN equivalent. To get all 
	# scoresheet that an user favor
	# ScoreSheetList = user.favorite_set.all()
	albums = Album.objects.filter(ContributingArtists__ArtistName = artist_name)
	# debut = artist.

	template = get_template('artist_page.html')
	variables = RequestContext(request, {
		'artist_name': artist_name,
		'albums': albums,
		'artist': artist
		})

	output = template.render(variables)
	return render_to_response('artist_page.html', variables)

def album_page(request, album_name):
	songs=[]
	try:
		# print username
		album = Album.objects.get(AlbumName=album_name)
		# print "1wsa"
	except Album.DoesNotExist:
		raise Http404('Requested album not found.')


	#The automatically generated JOIN equivalent. To get all 
	# scoresheet that an user favor
	# ScoreSheetList = user.favorite_set.all()
	songs = Song.objects.filter(ASIN_id__AlbumName = album_name)
	# debut = artist.

	template = get_template('album_page.html')
	variables = RequestContext(request, {
		'album_name': album_name,
		'songs': songs,
		'album': album
		})

	output = template.render(variables)
	return render_to_response('album_page.html', variables)

def song_page(request, song_id):
	tabs=[]
	try:
		# print username
		song = Song.objects.get(SongId=song_id)
		# print "1wsa"
	except Song.DoesNotExist:
		raise Http404('Requested song not found.')


	#The automatically generated JOIN equivalent. To get all 
	# scoresheet that an user favor
	# ScoreSheetList = user.favorite_set.all()
	# tabs = ScoreSheet.objects.filter(ContributingArtists__ArtistName = artist_name)
	# debut = artist.

	template = get_template('song_page.html')
	variables = RequestContext(request, {
		'song_name': song.SongName
		})

	output = template.render(variables)
	return render_to_response('song_page.html', variables)