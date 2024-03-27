from dotenv import load_dotenv
import os
import openai

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_keywords(prompt, model):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "assistant",
                "content": "You are a picky Youtuber Assistnant that is trying to look for video assets based on topic and demand from your Youtuber user",
            },
            {
                "role": "user",
                "content": f'Given the detailed description: "{prompt}". Generate a concise list of keywords for a YouTube search.',
            },
        ],
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    keywords = response.choices[0].message.content.strip()
    return keywords
