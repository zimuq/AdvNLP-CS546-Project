"""
    Test.py
"""
import youtube_transcript_api_get as ytb
import os
import openai
openai.api_key = "YOUR_API_KEY" # set up open ai key

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

def testOpenaiAPICall(prompt):
    if len(prompt) > 100000:
        print("Probably exceed the maximum tokens limit, please check your prompt!")
        return "See Above Warning"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0
        )
    except Exception as err:
        print(f"Error: function testOpenaiAPICall() encounter API call error {err}")
        return "See Above Exception"
    return response

def generateCOT(givenCaption):
    givenCaption = """
    """
    prompt1 = """
        1) the original caption mentions that Oneplus Open has almost the similar weight as iPhone 14 Pro Max, which is a regular 
        phone weight; 
    """
    prompt2 = """
        2) the original caption also mentions that Oneplus Open is lighter than you would expect; 
    """
    prompt3 = """
        3) Both 1) and 2) told us Oneplus Open (a fold phone) is as light as a regular phone, so we can only know the reviewer is 
        positive towards Oneplus Open without showing any opinion towards iPhone 14 Pro Max. 
    """
    final_cot = "Let me give you a chain-of-thoughts: " + prompt1 + prompt2 + prompt3
    return final_cot

if __name__ == '__main__':
    prompt = """
    Can you do the sentiment analysis if I provide you with the caption from a smartphone review video?
    """
    url = 'jD9n01Mck0Q'
    prompt = api_transcript_to_str(url)
    res = testOpenaiAPICall(prompt)
    print(res)