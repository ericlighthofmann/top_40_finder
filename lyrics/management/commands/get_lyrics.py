from django.core.management.base import BaseCommand, CommandError
from lyrics.models import Song, Artist, Lyrics
import requests
import bs4
from datetime import datetime, timedelta
import time
from tqdm import tqdm
from lyrics.models import Song, Artist

class Command(BaseCommand):
    def handle(self, *args, **options):

        all_songs = Song.objects.all()
        error_counter = 0
        def format_song(song):
            punctuation = ['?', ':', ';', '.', '!', '/', '\"', '\'', '&', '*']
            song = song.lower().replace(' ', '-').replace('\n', '')
            song = ''.join(c for c in song if c not in punctuation)
            return song
        def format_artist(artist):
            punctuation = ['?', ':', ';', '.', '!', '/', '\"', '\'', '&', '*']
            artist = artist.lower().replace(' ', '-').replace('\n', '')
            artist = ''.join(c for c in artist if c not in punctuation)
            return artist
        def getArtistSong(url, artist_name, song_name, artist_fk, song_fk, error_counter):
            try:
                res = requests.get(url)
                res.raise_for_status()
            except Exception as e:
                error_counter += 1
                pass
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            #gets all song lyrics and saves to db
            lyrics = ''
            for ana in soup.findAll('p', class_='verse'):
                if ana.text != 'about' and ana.text != 'site map':
                    lyrics += (' ' + ana.text.replace('\ br', '').replace('\n', ' '))
                    #print (lyrics)
            Lyrics.objects.update_or_create\
            (
            artist=artist_fk, song=song_fk, \
            defaults={'lyrics': lyrics}
            )

        for song in tqdm(all_songs):
            time.sleep(1)
            song_fk = song
            artist_fk = song.artist
            song_name = format_song(song.name)
            artist_name = format_artist(song.artist.name)
            #print (song_name, artist_name)
            getArtistSong('http://www.metrolyrics.com/' + song_name\
             + '-lyrics-' + artist_name + '.html', song_name, artist_name, artist_fk, song_fk, error_counter)

        print ('You had a ' + str(error_count/all_songs.count()*100) + ' success rate.')
