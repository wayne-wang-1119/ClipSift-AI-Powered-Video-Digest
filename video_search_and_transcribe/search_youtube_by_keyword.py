from apiclient.discovery import build
import os
import pytube  # or use youtube-dl
from dotenv import load_dotenv

load_dotenv()
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=youtube_api_key)


def search_videos(keywords, max_results=5):
    search_response = (
        youtube.search()
        .list(q=keywords, part="id,snippet", maxResults=max_results, type="video")
        .execute()
    )

    videos = []
    for search_result in search_response.get("items", []):
        videos.append(
            f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
        )

    return videos


def download_videos(video_urls):
    for url in video_urls:
        yt = pytube.YouTube(url)
        stream = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        stream.download()
        print(f"Downloaded {url}")


if __name__ == "__main__":
    keywords = (
        "Python lists"  # This would be the output from your GPT-3 generated keywords
    )
    video_urls = search_videos(keywords)
    download_videos(video_urls)
