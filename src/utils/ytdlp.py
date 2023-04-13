import yt_dlp

def download_audio(link):
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio',
                         'outtmpl': 'audio-extract.mp3', 'paths': {'home': 'assets/'}}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    print(video_title)
    video.download(link)