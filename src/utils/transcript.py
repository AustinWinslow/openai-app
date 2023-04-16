import openai


def get_audio_segments(audio_file, number_of_segments, time_interval):
    audio_segments = []
    for n in range(0, number_of_segments):
        start_interval = time_interval * n
        end_interval = start_interval + time_interval
        audio_segments.append(audio_file[start_interval:end_interval])
    print("successfully extracted audio segments...")
    return audio_segments


def export_segments(audio_segments, save_path, video_title):
    for i, segment in enumerate(audio_segments):
        out_file = save_path + video_title + "-segment{0}.mp3".format(i)
        segment.export(out_file, format="mp3")
        print("successfully exported file:", out_file)


def transcribe_segments(audio_segments, file_path, video_title, ai_model,
                        response_type):
    print("attempting to transcribe segments...")
    transcript_segments = {"segments": {}}
    for i in range(0, len(audio_segments)):
        segment_name = video_title + "-segment" + str(i) + ".mp3"
        segment_file = open(file_path + segment_name, "rb")
        transcript_segments["segments"][i] = []
        transcript_segments["segments"][i].append(
            openai.Audio.transcribe(ai_model, segment_file,
                                    response_format=response_type))
    print("successfully transcribed audio segments...")
    return transcript_segments


def get_transcript(audio_segments, transcript_segments):
    transcript_list = []
    for i in range(0, len(audio_segments)):
        transcript_list.append(transcript_segments["segments"][i][0])
    transcript = " ".join(transcript_list)
    print("successfully generated transcript...")
    return transcript


def write_transcript(output_path, video_title, transcript):
    with open(output_path + "/" + video_title + ".txt", "w") as oufile:
        oufile.writelines(transcript)
    print("exported transcript to:", output_path+"transcript.txt")


def split_transcript(transcript):
    transcript_chunks = []
    buffer = ""
    words = 0
    chunks = 0
    while transcript != "":
        if transcript[0] == " ":
            words += 1
        if words < 2400:
            buffer += transcript[0]
            transcript = transcript[1:]
        elif words >= 2400 and words < 2500:
            if transcript[0] == "." and transcript[1] == " ":
                buffer += transcript[0]
                transcript = transcript[1:]
                transcript_chunks.append(buffer)
                buffer = ""
                words = 0
                chunks += 1
            else: 
                buffer += transcript[0]
                transcript = transcript[1:]
    transcript_chunks.append(buffer)
    if buffer != "":
        chunks += 1
    if len(transcript_chunks) > 0:
        print("successfully split transcript...")
    else:
        print("ERROR: Unable to split transcript...")
    return transcript_chunks, chunks