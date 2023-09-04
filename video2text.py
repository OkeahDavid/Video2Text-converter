import os
import moviepy.editor as mp
import speech_recognition as sr

def extract_audio_from_video(video_path):
    """
    Extracts audio from a given video file and saves it as a WAV file.
    
    Args:
        video_path (str): Path to the video file.
        
    Returns:
        str: Path to the extracted audio file.
    """
    video = mp.VideoFileClip(video_path)
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    video.audio.write_audiofile(audio_path)
    return audio_path

def convert_audio_to_text(audio_path, api_key=None):
    """
    Converts audio to text using speech recognition.
    
    Args:
        audio_path (str): Path to the audio file.
        api_key (str, optional): API key for Google Cloud Speech-to-Text. Defaults to None.
        
    Returns:
        str: Transcription of the audio.
    """
    r = sr.Recognizer()
    text = ""
    
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
        
        try:
            if api_key:
                text = r.recognize_google_cloud(audio, credentials_json=api_key)
            else:
                text = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    return text

def main():
    video_file_path = "path/to/file"  # Replace with your video file path
    api_key = None
    
    # Extract audio and convert to text
    audio_path = extract_audio_from_video(video_file_path)
    transcription = convert_audio_to_text(audio_path, api_key)
    
    # Clean up the extracted audio file
    os.remove(audio_path)
    
    # Store transcription in a TXT file
    output_file_path = os.path.splitext(video_file_path)[0] + ".txt"
    with open(output_file_path, "w") as f:
        f.write(transcription)

    print("Transcription saved to:", output_file_path)

if __name__ == "__main__":
    main()
