from dotenv import load_dotenv
import os
import openai

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_keywords(prompt, model):
    response = openai.Completion.create(
        engine=model,
        prompt=f'Given the detailed description: "{prompt}". Generate a concise list of keywords for a YouTube search.',
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    keywords = response.choices[0].text.strip()
    return keywords
