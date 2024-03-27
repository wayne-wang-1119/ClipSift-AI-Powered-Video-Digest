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

with open("data_schema/schema.json", "r") as schema_file:
    schema = json.load(schema_file)
    client.schema.create(schema)


def index_video_transcripts(base_path="./youtube_downloads"):
    for video_id in os.listdir(base_path):
        video_path = os.path.join(base_path, video_id)
        if os.path.isdir(video_path):
            transcript_path = os.path.join(video_path, f"{video_id}_transcript.json")

            if os.path.exists(transcript_path):
                with open(transcript_path, "r") as file:
                    transcript_data = json.load(file)

                    for segment in transcript_data:
                        # Weaviate schema expects 'text', 'videoId', 'start', and 'duration'
                        data_object = {
                            "text": segment["text"],
                            "videoId": video_id,
                            "start": segment["start"],
                            "duration": segment["duration"],
                        }

                        # Add to Weaviate
                        client.data_object.create(data_object, "TranscriptSegment")


def find_best_k_contents(search_query, k=2):
    results = (
        client.query.get("TranscriptSegment", ["videoId", "text", "start", "duration"])
        .with_near_text({"concepts": [search_query]})
        .with_where(
            {
                "operator": "LessThan",
                "operands": [
                    {"path": ["duration"]},
                    {
                        "valueFloat": 300
                    },  # Looking for segments less than 300 seconds (5 minutes)
                ],
            }
        )
        .do()
    )

    return results["data"]["Get"]["TranscriptSegment"]
