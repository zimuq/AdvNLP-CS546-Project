"""
    Youtube transcript api file. Last modified:
"""
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extractId(url: str):
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        
        # Extract the video ID from the query parameters
        video_id = parse_qs(parsed_url.query)['v'][0] 
        return video_id
    except Exception as e:
        # Handle any exceptions, such as URL format errors
        print(f"Error: {e}")
        return None

def transcript_get(url: str):
    try:
        # Extract the video ID
        id = extractId(url)
        srt = YouTubeTranscriptApi.get_transcript(id)
    except Exception as err:
        # print(err)
        return None

    return srt