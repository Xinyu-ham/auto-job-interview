from interview import Interviewer
from speech_service import SpeechService
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input-ui', type=str, default='text', help='Input UI for the interview')
parser.add_argument('--voice', type=str, default='shimmer')
parser.add_argument('--rounds', type=int, default=3, help='Number of rounds in the interview including the Q&A round')
args = parser.parse_args()

ROUNDS = args.rounds
VOICE = args.voice

if args.input_ui != 'text':
    raise NotImplementedError('Only text input is supported at the moment')

with open('tmp/job_description.txt', 'r') as f:
    jd = f.read()

interviewer = Interviewer(jd, ROUNDS)
speech = SpeechService(voice=VOICE)

starting_question = interviewer.start_interview()
speech.text_to_speech(starting_question.message)

for _ in range(ROUNDS):
    if args.input_ui == 'text':
        reply = input("Your response: ")
    response = interviewer.respond(reply)
    speech.text_to_speech(response.message)

speech.text_to_speech(interviewer.evaluate_interview().message)