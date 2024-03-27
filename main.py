from video_search_and_transcribe import ingest_prompt, search_youtube_by_keyword
from transcript_based_auto_clip import snippet_selector, video_transcriber

video_to_include = 10

prompt = """What is Donald Trump's opinion on the election? How can I make some funny videos about him?"""
video_base_path = "transcript_based_auto_clip/youtube_downloads"

keywords = ingest_prompt.generate_keywords(prompt, "gpt-3.5-turbo")
print(keywords)

video_urls = search_youtube_by_keyword.search_videos(
    keywords, max_results=video_to_include
)  # top 3 video selected
print(video_urls)

search_youtube_by_keyword.download_videos(video_urls)  # download video

video_transcriber.download_transcript(video_base_path)  # download transcript

snippet_selector.automate_snippet_generation(
    search_query=keywords, k=video_to_include
)  # top 3 snippet used to generate clips
