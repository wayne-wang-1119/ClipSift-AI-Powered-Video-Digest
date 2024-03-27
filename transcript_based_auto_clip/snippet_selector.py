from dotenv import load_dotenv
import os
import openai
import weaviate
import json
import subprocess

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def create_schema_if_not_exists(client, schema):
    existing_classes = client.schema.get()["classes"]
    existing_class_names = {cls["class"] for cls in existing_classes}

    for cls in schema["classes"]:
        class_name = cls["class"]
        if class_name in existing_class_names:
            print(f"Class '{class_name}' already exists, skipping creation.")
        else:
            client.schema.create_class(cls)
            print(f"Class '{class_name}' created.")


with open("transcript_based_auto_clip/data_schema/schema.json", "r") as schema_file:
    schema = json.load(schema_file)


def index_video_transcripts(
    client, base_path="transcript_based_auto_clip/youtube_downloads"
):
    """
    Indexes video transcripts by creating data objects for each segment and adding them to Weaviate.

    Args:
        base_path (str): The base path where the video transcripts are located. Defaults to "transcript_based_auto_clip/youtube_downloads".

    Returns:
        None
    """
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


def find_best_k_contents(client, search_query, k):
    """
    Find the best k contents based on a search query using the OpenAI client.

    Parameters:
        search_query (str): The search query to find the best k contents.
        k (int): The number of best contents to retrieve.
        client (OpenAI): The OpenAI client used to query the data.

    Returns:
        list: A list of dictionaries containing the best k contents. Each dictionary has the following keys:
            - videoId (str): The ID of the video.
            - start (float): The start time of the content.
            - duration (float): The duration of the content.
            - end (float): The end time of the content.
            - text (str): The text of the content.
    """
    results = (
        client.query.get("TranscriptSegment", ["videoId", "text", "start", "duration"])
        .with_near_text({"concepts": [search_query]})
        .with_limit(k)
        .do()
    )
    print(results)

    best_transcripts = []
    for result in results["data"]["Get"]["TranscriptSegment"]:
        best_transcripts.append(
            {
                "videoId": result["videoId"],
                "start": result["start"],
                "duration": result["duration"],
                "end": result["start"] + result["duration"],
                "text": result["text"],
            }
        )

    return best_transcripts


def automate_snippet_generation(
    search_query, k, base_path="transcript_based_auto_clip/youtube_downloads"
):
    """
    Generates snippets of videos based on a search query and saves them to the output folder.

    Args:
        search_query (str): The search query to find the best k contents.
        k (int): The number of contents to retrieve.
        base_path (str, optional): The base path of the YouTube downloads. Defaults to "transcript_based_auto_clip/youtube_downloads".

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If there is an error executing the FFmpeg command.

    Note:
        - This function requires the Weaviate client to be running on http://localhost:8080.
        - The function indexes the video transcripts before finding the best k contents.
        - The output folder "./output_clips" will be created if it doesn't exist.
        - The function uses FFmpeg to extract the snippets from the videos.

    Example:
        automate_snippet_generation("AI", 5)
    """

    client = weaviate.Client(
        url="http://localhost:8080",
        additional_headers={"X-OpenAI-Api-Key": openai.api_key},
    )
    create_schema_if_not_exists(client, schema)
    index_video_transcripts(client, base_path)
    best_transcripts = find_best_k_contents(client, search_query, k)
    print(f"Best transcripts: {best_transcripts}")

    output_folder = "./output_clips"
    os.makedirs(
        output_folder, exist_ok=True
    )  # Create the output directory if it doesn't exist

    for transcript in best_transcripts:
        # Extract the snippet from the video
        print(f"Generating snippet for {transcript['videoId']}")
        video_id = transcript["videoId"]
        start_time = transcript["start"]
        end_time = transcript["end"]
        video_path = os.path.join(base_path, video_id, f"{video_id}.mp4")
        output_path = os.path.join(
            output_folder, f"{video_id}_{start_time}_{end_time}.mp4"
        )

        # Construct the FFmpeg command
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            video_path,
            "-ss",
            str(start_time),
            "-to",
            str(end_time),
            "-c",
            "copy",
            output_path,
        ]

        # Execute the FFmpeg command
        try:
            subprocess.run(ffmpeg_command, check=True)
            print(f"Generated snippet: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate snippet for {video_id}: {e}")
