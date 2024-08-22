from django.db import models

class Artist(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

class Track(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    artists = models.ManyToManyField(Artist)

class SpotifyUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    #TODO image_uri = models.CharField(max_length=255)
    profile_uri = models.CharField(max_length=255)
    tracks = models.ManyToManyField(Track)
    artists = models.ManyToManyField(Artist)


# TODO handle the genres also
#class Genres(models.Model):
#    name = models.CharField(max_length=255)