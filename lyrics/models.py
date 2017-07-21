from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)

class Song(models.Model):
    artist = models.ForeignKey(Artist)
    name = models.CharField(max_length=255, blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Lyrics(models.Model):
    artist = models.ForeignKey(Artist)
    song = models.ForeignKey(Song)

    lyrics = models.TextField('Lyrics')
    updated = models.DateTimeField(blank=True, null=True)

    def __str__ (self):
        return str(self.artist) + ': ' + str(self.song)
