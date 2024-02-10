import os
from datetime import datetime

from config import Config

from openai import OpenAI
from playsound import playsound
import pyaudio 
import webrtcvad
import wave

class SpeechService:
    cfg: Config
    voice: str
    client: OpenAI

    def __init__(self, cfg, voice, openai_api_key: str='') -> None:
        self.cfg = cfg
        if openai_api_key:
            self.client = OpenAI(openai_api_key)
        else:
            self.client = OpenAI()
        self.voice = voice
        if not os.path.exists(self.cfg.TEMPORARY_FOLDER):
            os.makedirs(self.cfg.TEMPORARY_FOLDER)

    def play_audio(self, wav_file: str) -> None:
        playsound(wav_file)

    def speech_to_text(self, wav_file: str) -> str:
        with open(wav_file, 'rb') as f:
            return self.client.audio.transcriptions.create(model=self.cfg.AUDIO_MODEL_WHISPER, file=f, response_format='text')
        
    def text_to_speech(self, text: str, play=True, output_path: str='') -> str:
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=text
        )

        

        if not output_path:
            output_path = 'output.wav'
        output_path = os.path.join(self.cfg.TEMPORARY_FOLDER, 'output.wav')
        if os.path.exists(output_path):
            os.remove(output_path)
        response.write_to_file(output_path)
        if play:
            self.play_audio(output_path)
        
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        demo_file = f'test/ai_demo_{now}.wav'
        response.write_to_file(demo_file)

    def record_audio(self, output_path='') -> str:
        if not output_path:
            output_path = 'user_response.wav'
        output_path = os.path.join(self.cfg.TEMPORARY_FOLDER, output_path)

        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK_DURATION_MS = self.cfg.VOICE_RECORDING_CHUNK_DURATION_MS
        CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
        MAX_RECORD_SECONDS = self.cfg.VOICE_RECORDING_MAX_DURATION
        SILENCE_DURATION = self.cfg.VOICE_RECORDING_SILENCE_DURATION

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK_SIZE)
        
        print("Begin your response...")
        
        frames = []
        vad = webrtcvad.Vad()
        vad.set_mode(self.cfg.VOICE_RECORDING_VAD_AGGRESSION)

        consequtive_silence = SILENCE_DURATION // (CHUNK_DURATION_MS / 1000)
        silence_counter = 0
        while True and silence_counter < consequtive_silence:
            data = stream.read(CHUNK_SIZE)
            frames.append(data)
            is_speech = vad.is_speech(data, RATE)
            if not is_speech:
                silence_counter += 1
            else:
                silence_counter = 0
        
        stream.stop_stream()
        stream.close()
        audio.terminate()

        print("Recording finished.")

        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        now = datetime.now().strftime('%Y%m%d%H%M%S')
        demo_file = f'test/me_demo_{now}.wav'
        with wave.open(demo_file, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        
        return output_path

    def get_user_response(self, input_ui: str, user_response_file='') -> str:
        if input_ui == 'text':
            return input("Your response: ")
        elif input_ui == 'voice':
            output_file = self.record_audio(user_response_file)
            return self.speech_to_text(output_file)
        



if __name__ == "__main__":
    transribe = SpeechService()
    transribe.play_audio("test/test.wav", 5)
    print(transribe.speech_to_text("test/test.wav"))
