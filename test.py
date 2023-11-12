"""
    Test.py
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

def main():
    url = 'jD9n01Mck0Q'
    res = ytb.transcript_get(url)
    if not res:
        print('[See Print Error for Details]')
    # print(type(res))
    print(len(res))
    print(api_transcript_to_str(res[200:330]))

if __name__ == '__main__':
    main()