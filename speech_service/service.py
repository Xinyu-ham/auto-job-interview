import time 
from openai import OpenAI
from playsound import playsound
import pyaudio


class SpeechService:
    client: OpenAI
    voice: str

    def __init__(self, openai_api_key: str='', voice: str='shimmer') -> None:
        if openai_api_key:
            self.client = OpenAI(openai_api_key)
        else:
            self.client = OpenAI()
        self.voice = voice

    def play_audio(self, wav_file: str) -> None:
        playsound(wav_file)

    def speech_to_text(self, wav_file: str) -> str:
        with open(wav_file, 'rb') as f:
            return self.client.audio.transcriptions.create(model='whisper-1', file=f, response_format='text')
        
    def text_to_speech(self, text: str, play=True, output_path: str='tmp/response.mp3') -> str:
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=text
        )
        response.stream_to_file(output_path)
        if play:
            self.play_audio(output_path)

    def record_audio(self, output_file='tmp/test.wav', duration=5) -> None:
        pass


if __name__ == "__main__":
    transribe = SpeechService()
    transribe.play_audio("test/test.wav", 5)
    print(transribe.speech_to_text("test/test.wav"))
