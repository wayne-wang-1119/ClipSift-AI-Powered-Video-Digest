from apiclient.discovery import build
import os
import pytube  # or use youtube-dl
from dotenv import load_dotenv

load_dotenv()
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=youtube_api_key)


def search_videos(keywords, max_results):
    search_response = (
        youtube.search()
        .list(q=keywords, part="id,snippet", maxResults=max_results, type="video")
        .execute()
    )

    videos = {}
    for search_result in search_response.get("items", []):
        videoId = search_result["id"]["videoId"]
        videos[videoId] = (
            f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
        )

    return videos


def download_videos(video_urls):
    for id, url in video_urls.items():
        yt = pytube.YouTube(url)
        stream = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        stream.download(
            filename=f"{id}.mp4",
            output_path=f"transcript_based_auto_clip/youtube_downloads/{id}",
        )
        print(f"Downloaded {id}")


if __name__ == "__main__":
    keywords = "Python lists"
    video_urls = search_videos(keywords, 2)
    download_videos(video_urls)
