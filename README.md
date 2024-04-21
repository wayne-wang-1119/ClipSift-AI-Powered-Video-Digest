# ClipSift-AI-Powered-Video-Digest

ClipSift is a tool for you to automatically speed up content / asset searching. By providing a natural lanaguage description, you can easily query the top relevant YouTube videos and get the most relevant clips to review. Copyrights reserved to the original creators of the videos.

# Starting Guide:

To start using, you should have docker running and use Weaviate through docker, so you have a local, free vector database for later when we want to find the best matching video assets.

To setup, you can follow: [Weaviate Starter's Guide](https://weaviate.io/developers/weaviate/quickstart#can-i-use-another-deployment-method)

Or, simply run the following in your terminal:

```bash
export OPENAI_API_KEY="sk..."
docker compose up -d
```

Additionally, you need YOUTUBE_API_KEY. You can obtain one from Google's Cloud platform for free and create a project for free.
You can follow the linked here to do so: [How to get Youtube API Key](https://stackoverflow.com/a/44399524)

Put everything in your .env on the top level.

```bash
#create a .env, and in .env
OPENAI_API_KEY="sk..."
YOUTUBE_API_KEY="..."
```

# TLDR: How to run and use?

inside top level `scripts`, change the prompt to the keyword you are trying to serach in respective script starting with
header `collect_`
then run:

```bash
python scripts/collect_youtube.py # for collecting youtube video assets
python scripts/collect_twitter.py # for collecting twitter video assets
```

to remove duplicate in the database:

```bash
python scripts/clean_duplicate_in_db.py
```

to remove downloaded assets under youtube_downloads

```bash
sh scripts/clean_downloaded_video.sh
```

# Project Arch

The entire project has two major parts:

1. video search and download
2. transcript and clip

This is to ensure scalable design for downloading more platform's assets

### Video search and download

This dir contains all you need to download any video based on a text entry description, example: Python Linked List definition -> GPT will generate key words to use to search -> Query YouTube's database -> Download and done!

### Transcript and clip

This dir contains all you need to process the transcripts and find the best matching contents and corp it automatically for you to use. By default, the same instruction for video search step will be shared here as instruction to find the best match, but you can manually change it as well. In here we index all the documents, send it to the weaviate docker instance, and query it to do hybrid search to find the best matching snippets of videos. Lastly, we crop them and store on the top level, so you can directly use it in your video.

# Outputs:

Located on the top level, under output_clips
