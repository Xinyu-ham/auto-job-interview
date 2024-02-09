from interview import Interviewer
from speech_service import SpeechService

ROUNDS = 4
VOICE = 'shimmer'

interviewer = Interviewer(jd, ROUNDS)
speech = SpeechService(voice=VOICE)

starting_question = interviewer.start_interview()
speech.text_to_speech(starting_question.message)

for _ in range(ROUNDS):
    reply = input("Your response: ")
    speech.speech_to_text(interviewer.respond(reply).message)

speech.text_to_speech(interviewer.evaluate_interview().message)