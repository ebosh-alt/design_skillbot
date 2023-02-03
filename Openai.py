import openai
from config import openai_api_key


class OpenAI:
    def __init__(self):
        self.openai = openai
        self.openai.api_key = openai_api_key

    def question(self, text: str):
        response = self.openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6
        )
        return response['choices'][0]['text']


if __name__ == "__main__":
    a = OpenAI()
    print(a.question("Hello world!"))
