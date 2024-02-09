from openai import OpenAI
from dataclasses import dataclass

@dataclass
class Response:
    role: str 
    message: str
    
    def __init__(self, role: str, message: str) -> None:
        self.role = role
        self.message = message

    def __repr__(self) -> str:
        return f"{self.role}: {self.message}"
    
    def __str__(self) -> str:
        return f"{self.role}: {self.message}"


@dataclass
class Transcipt:
    context: str
    responses: Response
    @classmethod
    def create_context_from_job_description(cls, job_description: str) -> Response:
        context = f"You are an interviewer hiring for a job. The following is the job description: {job_description}. Pretend the interview is happening right now, and ask the candidate a question."
        responses = [Response('system', context)]
        return cls(context, responses)

    def user_response(self, response: str) -> Response:
        response = Response('user', response)
        self.responses.append(response)

    def interviewer_response(self, response: str) -> Response:
        response = Response('assistant', response)
        self.responses.append(response)
        return response
    
    def system_instruction(self, instruction: str) -> Response:
        self.responses.append(Response('system', instruction))

    @property
    def data(self) -> list[dict[str, str]]:
        return [{'role': response.role, 'content': response.message} for response in self.responses]

class Interviewer:
    job_description: str
    client: OpenAI
    model: str
    rounds: int

    def __init__(self, job_description: str, rounds: int=3, openai_api_key: str='', model: str='gpt-3.5-turbo') -> None:
        self.job_description = job_description
        self.transcipt = Transcipt.create_context_from_job_description(job_description) 
        if openai_api_key:
            self.client = OpenAI(openai_api_key)
        else:
            self.client = OpenAI()
        self.model = model
        self.rounds = rounds

    def _generate_response(self) -> Response:
         reponse = self.client.chat.completions.create(model=self.model, messages=self.transcipt.data)
         return self.transcipt.interviewer_response(reponse.choices[0].message.content)
    
    def start_interview(self) -> Response:
        self.transcipt = Transcipt.create_context_from_job_description(self.job_description)
        self.transcipt.user_response("Please ask the first question.")
        return self._generate_response()
    
    def respond(self, reply: str) -> Response:
        self.transcipt.user_response(reply)
        self.rounds -= 1
        if self.rounds > 1:
            return self._generate_response()
        elif self.rounds == 1:
            return self.qna()
        else:
            return self.end_interview()
    
    def qna(self) -> Response:
        self.transcipt.system_instruction("You have asked the last question. End this interview after checking if the candidate has any questions.")
        return self._generate_response()

    def end_interview(self) -> Response:
        self.transcipt.system_instruction("Answer candidate's questions, then end the interview.")
        return self._generate_response()
        
    def evaluate_interview(self) -> Response:
        self.transcipt.system_instruction("Now suppose you are a career coach having a mock interview with the candidate. Provide strict and critical feedback on the interview, as well as a score out of 69.")
        return self._generate_response()

if __name__ == "__main__":
    jd = '''
Food truck located in Resorts World Sentosa looking to hire cashier.

Job requirements

- Cook fried items 

- take orders and hand orders to customers

- able to work weekends

- preferably if candidate has experience with cooking

Young dynamic team

Standard MOM leave benefits

44 Hour work week, beyond that, attractive OT payable.'''
    questions = 3
    interviewer = Interviewer(jd, rounds=questions)
    print(interviewer.start_interview())
    for _ in range(questions):
        reply = input("Your response: ")
        print(interviewer.respond(reply))
    print(interviewer.evaluate_interview())


