import openai


class OpenAi:
    def __init__(self, openai_api_key):
        self.openai = openai
        self.openai.api_key = openai_api_key

    async def question(self, text: str) -> str:
        response = await self.openai.Completion.acreate(
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
    a = OpenAi()
    print(a.question("Hello world!"))
