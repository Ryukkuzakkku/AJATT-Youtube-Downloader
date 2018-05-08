import os, sys ,time
import requests
from bs4 import BeautifulSoup
import pafy
from pydub import AudioSegment
import ffmpeg

AudioSegment.converter = r"C:\\FFmpeg\\bin\\ffmpeg.exe"

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

def split_audio_chunks(title, audio_file, split_time):
    in_file = ffmpeg.input(audio_file)
    in_file = ffmpeg.trim(in_file, start_frame=10, end_frame = 20)
    in_file = ffmpeg.output(in_file, 'out.mp4')
     



path = os.getcwd()
filenames = os.listdir(path)
for filename in filenames:
    os.rename(filename, filename.replace(".m4a", ".mp3"))
playlist_url = "https://www.youtube.com/watch?v=TXj6sPZiE5M&list=PLA02laFJ_V2WlY2y5aOvz_yJVOubbs51b"
split_audio_chunks("THE BOOTY MACHINE", "THE BOOTY MACHINE.mp3", split_time=1)


