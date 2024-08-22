from django.db import models

class Tracks(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

class Artists(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

class SpotifyUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    image_uri = models.CharField(max_length=255)
    profile_uri = models.CharField(max_length=255)
    tracks = models.ManyToManyField(Tracks)
    artists = models.ManyToManyField(Artists)


# TODO handle the genres also
#class Genres(models.Model):
#    name = models.CharField(max_length=255)