from interview import Interviewer
from speech_service import SpeechService
import argparse

from config import Config as cfg

parser = argparse.ArgumentParser()
parser.add_argument('--input-ui', type=str, default=cfg.DEFAULT_INPUT_UI, help='Input UI for the interview')
parser.add_argument('--voice', type=str, default=cfg.DEFAULT_VOICE, help='Voice for the text-to-speech service')
parser.add_argument('--rounds', type=int, default=cfg.DEFAULT_INTERVIEW_ROUNDS, help='Number of rounds in the interview including the Q&A round')
args = parser.parse_args()

# if args.input_ui != 'text':
#     raise NotImplementedError('Only text input is supported at the moment')
if args.rounds < 2:
    raise ValueError('Number of rounds should be at least 2')


ROUNDS = args.rounds
VOICE = args.voice

def main(jd_source: str='tmp/job_description.txt') -> None:
    with open(jd_source, 'r') as f:
        jd = f.read()
    interviewer = Interviewer(cfg, jd, ROUNDS)
    speech = SpeechService(cfg, voice=VOICE)

    starting_question = interviewer.start_interview()
    speech.text_to_speech(starting_question.message)

    for _ in range(ROUNDS):
        if args.input_ui == 'text':
            reply = input("Your response: ")
        elif args.input_ui == 'voice':
            reply = speech.get_user_response('voice')
        response = interviewer.respond(reply)
        speech.text_to_speech(response.message)

    speech.text_to_speech(interviewer.evaluate_interview().message)

if __name__ == '__main__':
    main()