from django.core.management.base import BaseCommand, CommandError
from lyrics.models import Song, Artist, Lyrics
import requests
import bs4
from datetime import datetime, timedelta
import time
from tqdm import tqdm

class Command(BaseCommand):
    def handle(self, *args, **options):

        #http://top40-charts.com/chart.php?cid=27&date=2017-07-22

        #get song artist, name from top 40 site
        def getArtistSong(PageUrl, date):
            res = requests.get(PageUrl)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            #gets all song names and saves to database
            for ana in soup.findAll('tr', {'class':'latc_song'}):
                for a in ana.findAll('a'):
                    if a.text != '' and a.text != None:
                        if 'song' in a['href']:
                            song = a.text
                        elif 'artist' in a['href']:
                            artist = a.text
                Artist.objects.update_or_create(name=artist)
                Song.objects.update_or_create(artist=Artist.objects.get(name=artist), name=song, defaults={'date':date})

        #gets all dates from dropdown
        date_list = []
        res = requests.get('http://top40-charts.com/chart.php?cid=27')
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        options = soup.find("select", {"name":"date"})
        for o in options.findAll('option'):
            date = datetime.strptime(o.text, '%d-%m-%Y').date()
            date_list.append(date)

        #scrapes all top 40 songs and artists using the dates in date_list
        for date in tqdm(date_list):
            time.sleep(2)
            try:
                getArtistSong('http://top40-charts.com/chart.php?cid=27' + '&date=' + str(date), date)
            except:
                time.sleep(60)
                getArtistSong('http://top40-charts.com/chart.php?cid=27' + '&date=' + str(date), date)
