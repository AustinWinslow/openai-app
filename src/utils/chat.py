import openai


def summarize_transcript(transcript_chunks, chunks, chat_model):
    print("attempting to summarize transcript...")
    response_chunks = {"chunks": {}}
    for i in range(0, chunks):
        prompt = [{"role": "user",
                   "content": "Please summarize this video transcript: "
                   + transcript_chunks[i]}]
        response_chunks["chunks"][i] = []
        model = openai.ChatCompletion.create(
            model=chat_model,
            messages=prompt
        )
        response_chunks["chunks"][i].append(model.choices[0].message)
    responses = []
    for i in range(0, chunks):
        responses.append(
            response_chunks["chunks"][i][0].content
        )
    response = " ".join(responses)
    print("successfully summarized transcript...")
    return response