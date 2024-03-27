from dotenv import load_dotenv
import os
import openai
import weaviate
import json

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")

client = weaviate.Client(
    url="http://localhost:8080", additional_headers={"X-OpenAI-Api-Key": openai.api_key}
)


def embed_transcripts(video_urls):
    pass
