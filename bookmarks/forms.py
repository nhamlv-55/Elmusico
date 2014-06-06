import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from models import *
class RegistrationForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	# email = forms.EmailField(label='Email')
	password1 = forms.CharField(
		label='Password',
		widget=forms.PasswordInput()
	)
	password2 = forms.CharField(
		label='Password (Again)',
		widget=forms.PasswordInput()
	)

	# method to check password
	def cleaned_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
				raise forms.ValidationError('Passwords do not match.')

	def cleaned_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
			try:
				User.objects.get(username=username)
			except ObjectDoesNotExist:
				return username
				raise forms.ValidationError('Username is already taken.')


class ArtistSaveForm(forms.Form):
	name = forms.CharField(
		label='Artist Name',
		widget = forms.TextInput(attrs = {'size': 64})
		)
	image = forms.CharField(
		label = 'Image',
		widget = forms.TextInput(attrs = {'size': 64})
		)
	date= forms.DateField(
		label= 'Debut',
		widget = forms.DateInput(attrs = {'size': 64})
		)
	status = forms.CharField(
		label = 'Status',
		widget = forms.TextInput(attrs = {'size': 64})
		)
	
	bio = forms.CharField(
		label = 'Bio',
		widget = forms.Textarea(attrs={'cols':64,'rows':10})
		)

	
class MusicianSaveForm(forms.Form):
	name = forms.CharField(
		label='Musician Name',
		widget = forms.TextInput(attrs = {'size': 64})
		)
	dob= forms.DateField(
		label= 'Birthday',
		widget = forms.DateInput(attrs = {'size': 64})
		)
	
class AlbumSaveForm(forms.Form):
	name = forms.CharField(
		label='Album Name',
		widget = forms.TextInput(attrs = {'size': 64})
		)

	contributing_artist = forms.ModelChoiceField(
		queryset=Artist.objects.all()
		)

	
	release_date= forms.DateField(
		label= 'Release Date',
		widget = forms.DateInput(attrs = {'size': 64})
		)

	label = forms.CharField(
		label='Label',
		widget = forms.TextInput(attrs = {'size': 64})
		)

	genre = forms.CharField(
		label='Genre',
		widget = forms.TextInput(attrs = {'size': 64})
		)

class SongSaveForm_step1(forms.Form):
	album = forms.ModelChoiceField(
		label = 'Album',
		queryset=Album.objects.all()
		)

class SongSaveForm_step2(forms.Form):
    
    contributing_artist = forms.ModelChoiceField(
    	label = 'Contributing Artists', 
    	queryset=Artist.objects.all()
    )

    name = forms.CharField(
		label='Song Name',
		widget = forms.TextInput(attrs = {'size': 64})
		)
    trackid = forms.IntegerField(
		label='Track ID',
		widget = forms.TextInput(attrs = {'size': 64})
		)
    composer = forms.ModelChoiceField(
		label='Composer',
		queryset=Artist.objects.all()
		)
    genre = forms.CharField(
		label='Genre',
		widget = forms.TextInput(attrs = {'size': 64})
		)

class MemberSaveForm(forms.Form):
	time=forms.DateField(
		label = "Time",
		widget = forms.DateInput(attrs = {'size': 64})
		)
	role = forms.CharField(
		label = "Role",
		widget = forms.TextInput(attrs = {'size': 64}))

class VideoSaveForm(forms.Form):
	video_type= forms.CharField(
		label= 'Type',
		widget = forms.TextInput(attrs = {'size': 64})
		)
	url = forms.URLField(
		label= 'URL',
		widget = forms.TextInput(attrs = {'size': 64}))
	
class TabSaveForm(forms.Form):
	
	version = forms.CharField(
		label = 'Version',
		widget = forms.TextInput(attrs = {'size': 64})
		)

	instrument= forms.CharField(
		label= 'Instrument',
		widget = forms.TextInput(attrs = {'size': 64})
		)
	url = forms.URLField(
		label= 'URL',
		widget = forms.TextInput(attrs = {'size': 64}))
	tab = forms.CharField(
		label = 'ScoreSheet',
		widget = forms.Textarea(attrs = {'width': 64, 'height': 300})
		)

class SearchForm(forms.Form):
	query = forms.CharField(
	label='Enter anything to search',
	widget=forms.TextInput(attrs={'size': 32})
	)