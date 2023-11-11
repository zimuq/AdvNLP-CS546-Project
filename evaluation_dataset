"""
Class Evaluation Dataset
"""
import youtube_transcript_api_get as ytb

def api_transcript_to_str(transcript):
    """
        transfer transcript returned by api call to a long str
    """
    output_str = ''
    for t in transcript:
        text = t['text'].replace('\n', ' ')
        output_str += text
        output_str += ' '

    return output_str

class CaptionExtractionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class YoutubeVideo:
    def __init__(self, title, id, url, caption=None) -> None:
        self.title = title
        self.id = id
        self.url = url
        self.caption = caption # caption is a datastruct returned by youtube api call

    def getTitle(self):
        return self.title
    
    def getId(self):
        return self.id
    
    def getUrl(self):
        return self.url
    
    def getCaption(self):
        return self.caption
    
    def extractVideoCaption(self):
        if self.caption:
            return True
        try:
            self.caption = ytb.transcript_get(self.id)
        except Exception as err:
            print(err.message)
            raise CaptionExtractionError(err.args)

        return True
    
    def getCaptionAsString(self):
        if self.caption:
            return api_transcript_to_str(self.caption)

class Channel:
    def __init__(self, channel_name, channel_url, videos_list=[]) -> None:
        self.channel_name = channel_name
        self.channel_url = channel_url
        self.videos_list = videos_list

        self.video_dict = {}

    def getChannelName(self):
        return self.channel_name
    
    def getUrl(self):
        return self.channel_url
    
    def getVideosList(self):
        return self.videos_list
    
    def addNewVideo(self, new_video):
        if isinstance(new_video, YoutubeVideo):
            self.videos_list.append(new_video)
            return True
        return False
    

class EvaluationDataset:
    def __init__(self, channel_list, videos_list=[]) -> None:
        self.channel_list = channel_list
        self.videos_list = videos_list

        self.video_dict = {}

    def getChannelList(self):
        return self.channel_list
    
    def getVideosList(self):
        return self.videos_list

    