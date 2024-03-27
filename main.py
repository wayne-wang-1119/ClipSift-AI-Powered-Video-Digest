from video_search_and_transcribe import ingest_prompt, search_youtube_by_keyword
from transcript_based_auto_clip import snippet_selector, video_transcriber

prompt = """
    Linked List is a data structure that uses a pointer to connect nodes together. What is the purpose of the pointer? The purpose is to 
    move through the list in a certain direction. The pointer is used to access the next node in the list.
"""
video_base_path = "transcript_based_auto_clip/youtube_downloads"

keywords = ingest_prompt.generate_keywords(prompt, "gpt-3.5-turbo")
print(keywords)

video_urls = search_youtube_by_keyword.search_videos(
    keywords, 3
)  # top 3 video selected
print(video_urls)

video_transcriber.download_transcript(video_base_path)  # download transcript

snippet_selector.automate_snippet_generation(
    search_query=keywords, k=3
)  # top 3 snippet used to generate clips
