# Description

This is an application inteded to interface with the openai api allowing for various uses. Ultimately I would like this to be a GUI application with lots of preset requests users can make along with their own input. For now I am focusing on chat applications and YouTube video summarization.

The YouTube video summaries are made by utilizing yt_dlp to download and convert youtube videos to audio format that then gets sent to openai's whisper model for transcription. The transcription then gets sent to a user-configurable chat model to be summarized.

# Configuration

The config file is in "config/config.json". You will need to set your api_key, org_id, and output_file_path in order for anything to work. You are also given the option to save the full transcript to your output directory. If you don't want to set to the string "False". You can also change the chat model if you wish. gpt-3-turbo is recommended because it is fairly competent and cheap. Since gpt-4 is still in beta, there is no access via api (as far as I know) currently.