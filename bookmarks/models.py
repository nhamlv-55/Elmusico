from django.db import models
from django import forms

# Create your models here.
from django.contrib.auth.models import User

class Artist(models.Model):
	ArtistId = models.AutoField(primary_key = True)
	ArtistName = models.TextField()
	Date = models.DateField()
	Status = models.TextField()
	Bio = models.TextField()
	Image = models.URLField()
	def __unicode__(self):
		return self.ArtistName

class Album(models.Model):
	AlbumId = models.AutoField(primary_key = True)
	AlbumName = models.TextField()
	ContributingArtists = models.ForeignKey(Artist, to_field = 'ArtistId')
	ReleaseDate = models.DateField()
	Label = models.TextField()
	Genre = models.TextField()
	def __unicode__(self):
		return self.AlbumName



class Song(models.Model):
	SongId = models.AutoField(primary_key = True)
	SongName = models.TextField()
	AlbumId = models.ForeignKey(Album)
	TrackId = models.IntegerField()
	ContributingArtists = models.ForeignKey(Artist, related_name='contributing_artist')
	Genre = models.TextField()
	Composer = models.ForeignKey(Artist, related_name = 'composer')

	def __unicode__(self):
		return '%s by %s' % (self.SongName, self.ContributingArtists)


class Video(models.Model):
	VideoId = models.AutoField(primary_key = True)
	SongId = models.ForeignKey(Song, to_field = "SongId")
	Type = models.TextField()
	Url = models.URLField()

class ScoreSheet(models.Model):
	ScoreId = models.AutoField(primary_key = True)
	SongId = models.ForeignKey(Song, to_field = "SongId")
	Version = models.IntegerField()
	Instrument = models.TextField()
	Url = models.URLField()
	Tab = models.TextField()



class Musician(models.Model):
	MusicianId = models.AutoField(primary_key = True)
	MusicianName = models.TextField()
	DOB = models.DateTimeField()

class Member(models.Model):
	RelationshipId = models.AutoField(primary_key = True)
	ArtistId = models.ForeignKey(Artist, to_field = "ArtistId")
	MusicianId = models.ForeignKey(Musician, to_field = "MusicianId")
	Role = models.TextField()
	Time = models.DateField()
	
class Favorite(models.Model):
	FavoriteId = models.AutoField(primary_key = True)
	# title = models.CharField(max_length = 200)
	user = models.ForeignKey(User)
	ScoreSheet = models.ForeignKey(ScoreSheet)