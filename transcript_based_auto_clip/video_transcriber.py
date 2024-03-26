import os
import json
from youtube_transcript_api import YouTubeTranscriptApi

video_base_path = "../youtube_videos"

for video_id in os.listdir(video_base_path):
    video_path = os.path.join(video_base_path, video_id)
    if os.path.isdir(video_path):
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_path = os.path.join(video_path, f"{video_id}_transcript.json")
            with open(transcript_path, "w") as f:
                json.dump(transcript_list, f)
            print(f"Saved transcript for {video_id}")
        except Exception as e:
            print(f"Error obtaining transcript for {video_id}: {e}")
