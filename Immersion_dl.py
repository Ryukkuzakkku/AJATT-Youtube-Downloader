import os, sys ,time
import requests
from bs4 import BeautifulSoup
import pafy
from pydub import AudioSegment
import ffmpeg
import math
import datetime

AudioSegment.converter = r"C:\\FFmpeg\\bin\\ffmpeg.exe"

def time_to_minutes(time):
    if time is not 0:
        print("time: " + str(time / 1000))
        s = math.ceil(time / 1000)
        print(str(datetime.timedelta(seconds=s)))
        return str(datetime.timedelta(seconds=s)).replace(':', '.')
    return "0.00.00"
    

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
                os.rename(filename, filename.replace(".m4a", ".mp3"))
                
            split_audio_chunks(audio_file, split_time)

        except Exception as e:
            print(e)

def split_audio_chunks(audio_file, split_time):
    split_time = float(split_time * 1000)
    title = audio_file.replace('.mp3', '')
    sound = AudioSegment.from_mp3(audio_file)
    times_to_split = math.ceil((len(sound)) / (split_time))

    for i in range(times_to_split):
        print("i: " + str(i+1) + " times_to_split is: " + str(times_to_split))
        if i + 1 != times_to_split:
            export_audio = sound[split_time * i:split_time * (i + 1)]
            new_name = title + ' ' + time_to_minutes(int(split_time * i)) + ' - ' + time_to_minutes(int(split_time * (i + 1))) + '.mp3'
            export_audio.export(new_name, format="mp3")
        else: #if last time
            print("entered else loop")
            export_audio = sound[split_time * i:]
            new_name = title + ' ' + time_to_minutes(int(split_time * i)) + ' - ' + time_to_minutes(len(sound)) + '.mp3'
            export_audio.export(new_name, format="mp3")
        print("exported newsong")


    
     



path = os.getcwd()
filenames = os.listdir(path)
for filename in filenames:
    os.rename(filename, filename.replace(".m4a", ".mp3"))
playlist_url = "https://www.youtube.com/watch?v=TXj6sPZiE5M&list=PLA02laFJ_V2WlY2y5aOvz_yJVOubbs51b"
split_audio_chunks("test_file.mp3", split_time=72)


