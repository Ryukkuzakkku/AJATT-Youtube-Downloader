import requests
from bs4 import BeautifulSoup
import pytube

def get_video_list(playlist_url):
    r = requests.get(playlist_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    link_list = []
    
    for link in soup.findAll('a'):
        if "index" in link.get('href') and "/watch" in link.get('href'): #filters ot content not in playlist
            print("pre-test: " + link.get('href'))
            link_list.append("https://www.youtube.com" + str(link.get('href')).split("&index=", 1)[0]) #strips all the playlist crap, leaves youtube url

    for i in link_list:
        print(i)

    return link_list

playlist_url = "https://www.youtube.com/watch?v=R5FgWjm-ejw&list=PLA02laFJ_V2UhiIwqIwRUK-mIct0opc5M"
get_video_list(playlist_url)
