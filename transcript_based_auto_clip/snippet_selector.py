from dotenv import load_dotenv
import os
import openai

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def lookup_snippets(trancript, model):
    """
    Given a transcript and a model, this function generates a concise list of keywords for a YouTube search based on the detailed description in the transcript.

    Parameters:
    - trancript (str): The detailed description in the transcript.
    - model (str): The name of the model to use for generating the keywords.

    Returns:
    - snippets (str): A string containing the generated keywords for a YouTube search.
    """
    response = openai.Completion.create(
        engine=model,
        prompt=f'Given the detailed description: "{trancript}". Pick the transcipt that is most relevant for demostration purpose.',
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    snippets = response.choices[0].text.strip()
    return snippets

def auto_clip(video_urls, snippets, model):
    """
    Given a list of video URLs, a list of snippets, and a model, this function automatically clips videos based on the snippets.

    Parameters:
    - video_urls (list): A list of video URLs.
    - snippets (list): A list of snippets.
    - model (str): The name of the model to use for generating the keywords.

    Returns:
    - None
    """
    for video_id, url in video_urls.items():
        
