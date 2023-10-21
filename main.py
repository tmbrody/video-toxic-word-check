import whisper
import torch
from datetime import timedelta
import os

subtitles_file = "subtitles.srt"

with open(subtitles_file, "w", encoding="utf-8") as file:
    file.write("")

def process_audio_directory(directory):
    for file in os.listdir(directory):
        audio_file_path = os.path.join(directory, file)
        transcribe_audio(audio_file_path)

def transcribe_audio(path):
    print("Loading whisper model...\n")

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = whisper.load_model('large-v2').to(device)

    print("Whisper model loaded.")
    print("Checking for toxic words...\n")

    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    toxic_segments = []

    with open("toxic.txt", "r", encoding="utf-8") as file:
        toxic_words = file.read().split("|")

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        with open(subtitles_file, "a", encoding="utf-8") as file:
            file.write(segment)

        for word in toxic_words:
            if word in text:
                toxic_segments.append((startTime, endTime))

    toxic_segments = list(set(toxic_segments))
    toxic_segments.sort(key=lambda x: x[0])

    if len(toxic_segments) == 0:
        print("No toxic words found.")
    else:
        print(f"Found {len(toxic_segments)} toxic words in the video:\n")

        for startTime, endTime in toxic_segments:
            print(f"Found one at: {startTime} --> {endTime}")

if __name__ == "__main__":
    audio_directory = "audio"
    process_audio_directory(audio_directory)