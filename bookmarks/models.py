from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Artist(models.Model):
	ArtistId = models.IntegerField(primary_key = True)
	ArtistName = models.TextField()
	Date = models.DateTimeField()
	Status = models.TextField()



class Album(models.Model):
	ASIN = models.CharField(max_length = 10, primary_key = True)
	AlbumName = models.TextField()
	ContributingArtists = models.ForeignKey(Artist, to_field = 'ArtistId')
	ReleaseDate = models.DateTimeField()
	Label = models.TextField()
	Genre = models.TextField()

class Song(models.Model):
	SongId = models.IntegerField(primary_key = True)
	ASIN = models.ForeignKey(Album)
	TrackId = models.IntegerField(unique = True)
	ContributingArtists = models.ForeignKey(Artist, to_field = 'ArtistId')
	Genre = models.TextField()
	Composer = models.TextField()


class Video(models.Model):
	VideoId = models.IntegerField(primary_key = True)
	SongId = models.ForeignKey(Song, to_field = "SongId")
	Type = models.TextField()
	Url = models.URLField()

class ScoreSheet(models.Model):
	ScoreId = models.IntegerField(primary_key = True)
	SongId = models.ForeignKey(Song, to_field = "SongId")
	Version = models.IntegerField()
	Instrument = models.TextField()
	Url = models.URLField()



class Musician(models.Model):
	MusicianId = models.IntegerField(primary_key = True)
	MusicianName = models.TextField()
	DOB = models.DateTimeField()

class Member(models.Model):
	RelationshipId = models.IntegerField(primary_key = True)
	ArtistId = models.ForeignKey(Artist, to_field = "ArtistId")
	MusicianId = models.ForeignKey(Musician, to_field = "MusicianId")
	Role = models.TextField()
	Time = models.DateTimeField()

class Favorite(models.Model):
	FavoriteId = models.IntegerField(primary_key = True)
	# title = models.CharField(max_length = 200)
	user = models.ForeignKey(User)
	ScoreSheet = models.ForeignKey(ScoreSheet)