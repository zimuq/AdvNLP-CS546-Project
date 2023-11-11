"""
    Youtube transcript api file. Last modified:
"""
from youtube_transcript_api import YouTubeTranscriptApi

def transcript_get(url: str):

    try:
        srt = YouTubeTranscriptApi.get_transcript(url)
    except Exception as err:
        print(err)
        return None

    return srt