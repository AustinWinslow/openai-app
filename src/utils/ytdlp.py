import yt_dlp
import re

def download_audio(link):
  print("attempting to download video...")
  global video_title 
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio',
                         'outtmpl': 'audio-extract.mp3',
                         'paths': {'home': 'assets/'},
                         'quiet': True}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = re.sub(r'[^a-zA-Z0-9 ]', '', info_dict['title'])
    video.download(link)
    print("successfully downloaded video:", video_title)
  return video_title