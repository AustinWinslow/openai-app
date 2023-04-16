import openai
import json
import audioread
import math
import os
from pydub import AudioSegment
from utils.ytdlp import *
from utils.file_manipulation import *
from utils.transcript import *
from utils.chat import *

# import configuration options
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)
    user_org_id = config['UserAPI']['ORG_ID']
    user_api_key = config['UserAPI']['API_KEY']
    output_file_path = config['Options']['output_file_path']
    chat_model = config['Options']['chat_model']
    save_transcript = config['Options']['save_transcript']
# set api_key and org_id for openai
openai.organization = user_org_id
openai.api_key = user_api_key

# get video link
video_link = input("What video would you like to transcribe?\n")
print("\n\n\n")

# download the audio from video link
video_title = download_audio(video_link)
# rename file to video title
os.rename("assets/audio-extract.mp3", "assets/" + video_title + ".mp3")
# get the audio duration (seconds) 
with audioread.audio_open('assets/' + video_title + '.mp3') as f:
    file_length = f.duration
audio_file = AudioSegment.from_file('assets/' + video_title + '.mp3')

# create segments folder
os.mkdir('assets/segments')

# define 20 minutes in milliseconds
twenty_minutes = 1000 * 60 * 20
# calculate number of segments needed
number_of_segments = math.floor((file_length * 1000) / twenty_minutes) + 1
# cut the audio into 20 minute segments
audio_segments = get_audio_segments(audio_file, number_of_segments,
                                    twenty_minutes)

# export the audio segments to the filesystem
export_segments(audio_segments, "assets/segments/", video_title)

# transcribe segments, store in transcript segment list
transcript_segments = transcribe_segments(audio_segments, "assets/segments/",
                                        video_title, "whisper-1", "text")

# extract transcription from segment openai responses
transcript = get_transcript(audio_segments, transcript_segments)

# write transcript to output file
write_transcript(output_file_path, video_title, transcript)

# delete mp3 files
remove_file("assets", video_title + ".mp3")
remove_directory("assets", "segments")
if save_transcript != "True":
    remove_file(output_file_path, video_title + ".txt")

# summarize transcript
transcript_chunks, chunks = split_transcript(transcript)
summary = summarize_transcript(transcript_chunks, chunks, chat_model)
write_transcript(output_file_path, video_title + "Summary ", summary)
print("your summary has been saved to " + output_file_path + "/" + video_title + ".txt")