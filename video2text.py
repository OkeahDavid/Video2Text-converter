import os
import moviepy.editor as mp
import speech_recognition as sr

def convert_video_to_text(video_path, api_key=None):
    # Extract audio from the video
    video = mp.VideoFileClip(video_path)
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    video.audio.write_audiofile(audio_path)

    # Load the audio file
    r = sr.Recognizer()

    # Set API key if provided
    if api_key:
        r.recognize_google_cloud(audio_path, credentials_json=api_key)
    else:
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)

    # Convert audio to text
    text = ""
    try:
        if api_key:
            text = r.recognize_google_cloud(audio)
        else:
            text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return text

# Provide the path to the video file in your download folder
video_file_path = path/to/file  # Replace with your video file path

# Optionally provide API key if available
api_key = None

transcription = convert_video_to_text(video_file_path, api_key)
# Store transcription in a TXT file
output_file_path = os.path.splitext(video_file_path)[0] + ".txt"
with open(output_file_path, "w") as f:
    f.write(transcription)

print("Transcription saved to:", output_file_path)
