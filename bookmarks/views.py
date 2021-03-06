from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render, get_object_or_404
from bookmarks.forms import *

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
	create_or_edit ="Create"
	if request.method == 'POST':
		form = ArtistSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.

			try:
				artist= Artist.objects.get(
					ArtistName=form.cleaned_data['name'],
					# Date = form.cleaned_data['date']
				)
				artist.Date=form.cleaned_data['date']
				artist.Status=form.cleaned_data['status']
				artist.Bio = form.cleaned_data['bio']
				artist.Image = form.cleaned_data['image']
			except ObjectDoesNotExist:
				artist, create = Artist.objects.get_or_create(
					ArtistName=form.cleaned_data['name'],
					Date=form.cleaned_data['date'],
					Status=form.cleaned_data['status'],
					Bio = form.cleaned_data['bio'],
					Image = form.cleaned_data['image']
					)			
			
			artist.save()
			return HttpResponseRedirect(
				'/artist/%s/' % artist.ArtistId
			)
	elif request.GET.has_key('artist_id'):
		create_or_edit = "Edit"
		artist_id = request.GET['artist_id']
		print "elif"
		try:
			artist = Artist.objects.get(ArtistId=artist_id)
			name= artist.ArtistName
			date= artist.Date
			status = artist.Status
			bio = artist.Bio
			image=artist.Image
		except ObjectDoesNotExist:
			pass
		form = ArtistSaveForm({
			'name': name,
			'date': date,
			'status':status,
			'bio':bio,
			'image':image
		})
	else:
		form = ArtistSaveForm()
	variables = RequestContext(request, {
		'form': form,
		'create_or_edit': create_or_edit
		})
	return render_to_response('artist_save.html', variables, context_instance = RequestContext(request))

def musician_save_page(request):
	create_or_edit ="Create"
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
	elif request.GET.has_key('musician_id'):
		musician_id = request.GET['musician_id']
		create_or_edit = "Edit"
		print "elif"
		try:
			musician = Musician.objects.get(MusicianId=musician_id)
			name= musician.MusicianName
			date= artist.DOB
		except ObjectDoesNotExist:
			pass
		form = MusicianSaveForm({
			'name': name,
			'date': date,
		})
	else:
		form = MusicianSaveForm()

	variables = RequestContext(request, {
		'form': form,
		'create_or_edit': create_or_edit
		})
	return render_to_response('musician_save.html', variables)

def album_save_page(request):
	create_or_edit ="Create"
	if request.method == 'POST':
		form = AlbumSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.
			try:
				album = Album.objects.get(
					AlbumName=form.cleaned_data['name'],
					ContributingArtists = form.cleaned_data['contributing_artist']
					)
				album.ReleaseDate=form.cleaned_data['release_date']
				album.Label = form.cleaned_data['label']
				album.Genre = form.cleaned_data['genre']
			except ObjectDoesNotExist:
				album, create = Album.objects.get_or_create(
					AlbumName = form.cleaned_data['name'],
					ContributingArtists = form.cleaned_data['contributing_artist'],
					ReleaseDate = form.cleaned_data['release_date'],
					Label = form.cleaned_data['label'],
					Genre = form.cleaned_data['genre']

					)
			album.save()
			return HttpResponseRedirect(
				'/album/%s/' % album.AlbumId
			)
	elif request.GET.has_key('album_id'):
		album_id = request.GET['album_id']
		create_or_edit = "Edit"
		print "elif"
		try:
			album = Album.objects.get(AlbumId=album_id)
			name= album.AlbumName
			contributing_artist = album.ContributingArtists
			date= album.ReleaseDate
			label = album.Label
			genre= album.Genre
		except ObjectDoesNotExist:
			print "doesnt exist"
			pass
		form = AlbumSaveForm({
			'name': name,
			'release_date': date,
			'label':label,
			'genre':genre,
			# 'contributing_artist':contributing_artist
		})
	else:
		form = AlbumSaveForm()
	variables = RequestContext(request, {
		'form': form,
		'create_or_edit': create_or_edit
		})
	return render_to_response('album_save.html', variables)

def song_save_page_step1(request):
	if request.method == 'POST':
		form = SongSaveForm_step1(request.POST)
		if form.is_valid():
			Album = form.cleaned_data['album'].AlbumId

			t=HttpResponseRedirect(
				'/create_song_step2/%s/' %Album
			)
			print t
			return t
	else:
		form = SongSaveForm_step1()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('song_save_step1.html', variables)

def song_save_page_step2(request, album_id):
	if request.method == 'POST':
		form = SongSaveForm_step2(request.POST )
		if form.is_valid():
			print "vl"
			# Create or get link.
			song, created = Song.objects.get_or_create(
				SongName=form.cleaned_data['name'],
				AlbumId = Album.objects.get(AlbumId=album_id),
				TrackId = form.cleaned_data['trackid'],
				ContributingArtists = form.cleaned_data['contributing_artist'],
				Genre = form.cleaned_data['genre'],
				Composer = form.cleaned_data['composer']
				)
			song.save()
			return HttpResponseRedirect(
				'/song/%s/' % song.SongId
			)
	else:
		form = SongSaveForm_step2()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('song_save_step2.html', variables)

def video_save_page_step1(request):
	form = SearchForm()
	songs = []

	show_results = False
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = SearchForm({'query' : query})
			songs = Song.objects.filter(SongName__icontains=query)[:10]
	variables = RequestContext(request, { 
		'form': form,
		'songs': songs,
		'show_results': show_results,
		})
	return render_to_response('video_save_step1.html', variables)

def video_save_page_step2(request, song_id):
	if request.method == 'POST':
		form = VideoSaveForm(request.POST)
		print song_id
		if form.is_valid():
			print "vl"
			# Create or get link.
			video, created = Video.objects.get_or_create(
				SongId_id = song_id,
				Type = form.cleaned_data['video_type'],
				Url = form.cleaned_data['url']
				)
			

			video.save()
			return HttpResponseRedirect(
				'/song/%s/' % song_id
			)
		else:
			print "nvl"
	elif request.GET.has_key('video_id'):
		video_id = request.GET['video_id']
		print "elif"
		try:
			video = Video.objects.get(VideoId=video_id)
			video_type = video.Type
			url=video.Url
		except ObjectDoesNotExist:
			pass
		form = VideoSaveForm({
			'video_type':video_type,
			'url': url
		})
	else:
		form = VideoSaveForm()
	variables = RequestContext(request, {
		'form': form
		})
	return render_to_response('video_save_step2.html', variables)

def tab_save_page_step1(request):
	form = SearchForm()
	songs = []

	show_results = False
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = SearchForm({'query' : query})
			songs = Song.objects.filter(SongName__icontains=query)[:10]
	variables = RequestContext(request, { 
		'form': form,
		'songs': songs,
		'show_results': show_results,
		})
	return render_to_response('tab_save_step1.html', variables)

def tab_save_page_step2(request, song_id):
	if request.method == 'POST':
		form = TabSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.

			scoresheet, created = ScoreSheet.objects.get_or_create(
				SongId_id = song_id,
				Version = form.cleaned_data['version'],
				Instrument = form.cleaned_data['instrument'],
				Url = form.cleaned_data['url'],
				Tab = form.cleaned_data['tab']
				)
			
			

			scoresheet.save()
			return HttpResponseRedirect(
				'/tab/%s/' % scoresheet.ScoreId
			)
	else:
		form = TabSaveForm()
		variables = RequestContext(request, {
			'form': form
			})
		return render_to_response('tab_save_step2.html', variables)


def relation_page(request, relation_string):
	print relation_string
	artist_id, musician_id = relation_string.split("_")

	# ------------------------------------
	if request.method == 'POST':
		form = MemberSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.
			member, created = Member.objects.get_or_create(
				ArtistId = Artist.objects.get(ArtistId=artist_id),
				MusicianId = Musician.objects.get(MusicianId = musician_id),
				Role=form.cleaned_data['role'],
				Time = form.cleaned_data['time']
				)
			member.save()
			return HttpResponseRedirect(
				'/artist/%s/' % artist_id
			)
	# ------------------------------------
	else:
		form = MemberSaveForm()

	variables = RequestContext(request, {
		'form': form
		})
	return render_to_response('member_save.html', variables)



def search_page(request):
	form = SearchForm()
	artists = []
	albums = []
	songs = []
	musicians = []
	show_results = False
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = SearchForm({'query' : query})
			artists = Artist.objects.filter (ArtistName__icontains=query)[:10]
			albums = Album.objects.filter (AlbumName__icontains=query)[:10]
			songs = Song.objects.filter(SongName__icontains=query)[:10]
			musicians = Musician.objects.filter(MusicianName__icontains =query)[:10]
		print songs, artists, albums
	variables = RequestContext(request, { 'form': form,
		'artists': artists,
		'albums': albums,
		'songs': songs,
		'musicians': musicians,
		'show_results': show_results,
		# 'show_tags': True,
		# 'show_user': True
		})
	return render_to_response('search.html', variables)

def search_member_page(request, artist_id):
	form = SearchForm()
	musicians =[]

	show_results = False
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = SearchForm({'query' : query})
			musicians = Musician.objects.filter (MusicianName__icontains=query)[:10]
	variables = RequestContext(request, { 'form': form,
		'musicians': musicians,
		'show_results': show_results,
		'artist_id':artist_id
		})
	return render_to_response('search_member.html', variables)

def artist_page(request, artist_id):
	albums=[]
	members=[]
	try:
		# print username
		artist = Artist.objects.get(ArtistId=artist_id)
		# print "1wsa"
	except Artist.DoesNotExist:
		raise Http404('Requested artist not found.')


	artist_name = artist.ArtistName

	albums = Album.objects.filter(ContributingArtists__ArtistName = artist_name)

	members = Member.objects.filter(ArtistId_id__ArtistId = artist.ArtistId)
	template = get_template('artist_page.html')
	variables = RequestContext(request, {
		'artist_name': artist_name,
		'albums': albums,
		'artist': artist,
		'members': members
		})

	output = template.render(variables)
	return render_to_response('artist_page.html', variables)

def album_page(request, album_id):
	songs=[]
	try:
		# print username
		album = Album.objects.get(AlbumId=album_id)
		# print "1wsa"
	except Album.DoesNotExist:
		raise Http404('Requested album not found.')

	album_name = album.AlbumName
	#The automatically generated JOIN equivalent. To get all 
	# scoresheet that an user favor
	# ScoreSheetList = user.favorite_set.all()
	songs = Song.objects.filter(AlbumId_id__AlbumName = album_name)

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
	videos=[]
	try:
		# print username
		song = Song.objects.get(SongId=song_id)
		# print "1wsa"
	except Song.DoesNotExist:
		raise Http404('Requested song not found.')

	tabs = ScoreSheet.objects.filter(SongId_id__SongId = song_id)
	videos = Video.objects.filter(SongId_id__SongId = song_id)
	album = Album.objects.get(AlbumId = song.AlbumId_id)
	contributing_artist = Artist.objects.get(ArtistId = song.ContributingArtists_id)
	if len(videos)>0:
		demo_vid = videos[0].Url
		demo_vid = demo_vid.split('=')[1]
	else:
		demo_vid=False
	template = get_template('song_page.html')
	variables = RequestContext(request, {
		'album': album,
		'song_name': song.SongName,
		'videos': videos,
		'tabs':tabs,
		'demo_vid':demo_vid,
		'contributing_artist': contributing_artist
		})

	output = template.render(variables)
	return render_to_response('song_page.html', variables)

def tab_page(request, score_id):
	try:
		tab = ScoreSheet.objects.get(ScoreId=score_id)
	except Artist.DoesNotExist:
		raise Http404('Requested scoresheet not found.')

	scoresheet = tab.Tab
	song = Song.objects.get(SongId = tab.SongId_id)
	template = get_template('tab_page.html')
	variables = RequestContext(request, {
		'tab':tab,
		'scoresheet': scoresheet,
		'song':song
		})
	output = template.render(variables)
	return render_to_response('tab_page.html', variables)

def musician_page(request, musician_id):
	groups = []
	try:
		musician = Musician.objects.get(MusicianId = musician_id)
	except:
		raise Http404('Requested artist not found.')

	groups = Member.objects.filter(MusicianId_id__MusicianId = musician.MusicianId)
	print groups[0].ArtistId
	template = get_template('musician_page.html')
	variables = RequestContext(request, {
		'musician': musician,
		'groups': groups
		})

	output = template.render(variables)
	return render_to_response('musician_page.html', variables)