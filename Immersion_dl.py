import os, sys ,time
import requests
from bs4 import BeautifulSoup
import pafy
from pydub import AudioSegment

def get_video_list(playlist_url):
    r = requests.get(playlist_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    link_list = []
    
    for link in soup.findAll('a'):
        if "index" in link.get('href') and "/watch" in link.get('href'): #filters ot content not in playlist
            link_list.append("https://www.youtube.com" + str(link.get('href')).split("&", 1)[0]) #strips all the playlist crap, leaves youtube url


    return set(link_list) #returns list with no duplicates

def process_videos(playlist_url, split_time):
    path =  os.getcwd()
    link_list = get_video_list(playlist_url)
    for link in link_list:
        try:
            print("Downloading: " + link)
            video = pafy.new(link)
            bestaudio = video.getbestaudio(preftype="m4a")
            bestaudio.download()

            audio_file = video.title.replace('/', '_') + "." + bestaudio.extension
            print("\n\n\n\n" + audio_file)

            filenames = os.listdir(path)

            for filename in filenames:
                os.rename(audio_file, audio_file.replace(".m4a", ".mp4"))

            audio_file = video.title.replace('/', '_') + ".mp4"

            split_audio_chunks(audio_file)

        except Exception as e:
            print(e)

def split_audio_chunks(audio_file):
    sound = AudioSegment.from_file(audio_file, "mp4")
    slice_times = len(sound) / split_time

    for i in range (slice_times):
        if i is not slice_times - 2:
            split_segment = sound[split_time * i:split_time * (i + 1)]
            new_title = video.title.replace('/', '_') + str(split_time * i) + ".00 - " + str(split_time * (i + 1) + ".00." + 'mp4')
            split_segment.export(new_title, format='mp4' )
        print(new_title + " Processed")



print(os.getcwd())        
playlist_url = "https://www.youtube.com/watch?v=TXj6sPZiE5M&list=PLA02laFJ_V2WlY2y5aOvz_yJVOubbs51b"
##process_videos(playlist_url, split_time=1)

filenames = os.listdir(path)

for filename in filenames:
    print(filename)

split_audio_chunks("_a_non gets the power.mp4")


