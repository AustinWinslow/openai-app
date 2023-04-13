import openai
import json
import audioread
import os
import shutil
import math
from pydub import AudioSegment
from utils.ytdlp import *

# import configuration options
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)
    user_org_id = config['UserAPI']['ORG_ID']
    user_api_key = config['UserAPI']['API_KEY']
    output_file_path = config['Options']['output_file_path']

# set api_key and org_id for openai
openai.organization = user_org_id
openai.api_key = user_api_key

# get video link
video_link = input("What video would you like to transcribe?\n")

# delete audio-extract.mp3 if it already exists
extract_exists = os.path.exists(os.path.join(os.getcwd(), 'assets', 'audio-extract.mp3'))
if extract_exists:
    try:
        os.remove('assets/audio-extract.mp3')
    except Exception as error:
        raise ValueError(error)

# download the audio from video link
download_audio(video_link)
# get the audio duration (seconds)
with audioread.audio_open('assets/audio-extract.mp3') as f:
    file_length = f.duration
audio_file = AudioSegment.from_file('assets/audio-extract.mp3')

# delete any existing segments
segments_exist = os.path.isdir("assets/segments")
if segments_exist:
    try:
        shutil.rmtree('assets/segments')
    except Exception as error:
        raise ValueError(error)

# create segments folder
os.mkdir('assets/segments')

# define 20 minutes in milliseconds
twenty_minutes = 1000 * 60 * 20

# calculate number of segments needed
number_of_segments = math.floor((file_length * 1000) / twenty_minutes) + 1

# cut the audio into 20 minute segments
audio_segments = []
for n in range(0, number_of_segments):
    start_interval = twenty_minutes * n
    end_interval = start_interval + twenty_minutes
    audio_segments.append(audio_file[start_interval:end_interval])

# export the audio segments to the filesystem
for i, segment in enumerate(audio_segments):
    out_file = 'assets/segments/segment{0}.mp3'.format(i)
    print('exporting', out_file)
    segment.export(out_file, format='mp3')

# transcribe segments, store in transcript segment list
transcript_segments = {"segments": {}}
for k in range(0, len(audio_segments)):
    segment_name = "segment" + str(k) + ".mp3"
    segment_file = open("assets/segments/" + segment_name, "rb")
    transcript_segments["segments"][k] = []
    transcript_segments["segments"][k].append(openai.Audio.transcribe('whisper-1',
                                              segment_file, response_format="text"))

# extract transcription from segment openai responses
transcript_list = []
for k in range(0, len(audio_segments)):
    transcript_list.append(transcript_segments['segments'][k][0])

# take list of transcripted audio from segments, join into one string
transcript = " ".join(transcript_list)

# write transcript to output file
with open(output_file_path+'transcript.txt', 'w') as outfile:
    outfile.writelines(transcript)

# delete mp3 files
extract_exists = os.path.exists(os.path.join(os.getcwd(), 'assets', 'audio-extract.mp3'))
if extract_exists:
    try:
        os.remove('assets/audio-extract.mp3')
    except Exception as error:
        raise ValueError(error)
segments_exist = os.path.isdir("assets/segments")
if segments_exist:
    try:
        shutil.rmtree('assets/segments')
    except Exception as error:
        raise ValueError(error)