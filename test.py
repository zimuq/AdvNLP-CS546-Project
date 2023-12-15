"""
    Test.py
"""
import youtube_transcript_api_get as ytb
import os
import csv
import openai
from openai import OpenAI
openai_api_key = "Your_API_KEY"

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

    prompt_set = {
        "fact_1": 
                """ 
                    1) the original caption mentions that Oneplus Open has almost the similar weight as iPhone 14 Pro Max, 
                    which is a regular phone weight; 
                """,
        "fact_2":
                """
                    2) the original caption also mentions that Oneplus Open is lighter than you would expect; 
                """,
        "fact_3":
                """
                    3) Both 1) and 2) told us Oneplus Open (a fold phone) is as light as a regular phone, so we can only know 
                    the reviewer is positive towards Oneplus Open without showing any opinion towards iPhone 14 Pro Max.
                """
    }
    prompt_set
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

def readManuallyLabels(csv_file_path):
    data_dict = {}
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            channel_name = row['channel_name']
            if channel_name == '': # empty channel name
                continue
            video_link = row['video_link']
            phone_brand = row['phone_brand']
            phone_model = row['phone_model']
            score = int(row['score'])  # Convert score to integer
            # try:
            #     score = int(row['score'])  # Convert score to integer
            # except Exception as e:
            #     print(video_link)
            
            # Create the nested dictionary structure
            if channel_name not in data_dict:
                data_dict[channel_name] = {}
            if video_link not in data_dict[channel_name]:
                data_dict[channel_name][video_link] = {}
            if phone_brand not in data_dict[channel_name][video_link]:
                data_dict[channel_name][video_link][phone_brand] = {}
            
            # Add phone_model and score to the dictionary
            data_dict[channel_name][video_link][phone_brand][phone_model] = score
    return data_dict

def openaiAPICall(prompt: str = None, caption: str = None):
    if prompt is None:
        prompt = """Given the following video caption, please anaylze the stance of the smartphone reviewer towards any mentioned 
                    smartphone brands/models in this video. For example, your output should be in the format: iPhone 13 Pro: 1 (positive), 
                    Samsung: 0 (neutral), Google Pixel 3: -1 (negative), OnePlus 8: 0.5/-0.5 (half positive/half negative, in these cases,
                    you can optionally provide the justifications)
                """
    model_name = "gpt-3.5-turbo"
    if len(caption + prompt) > 6000:
        print("Probably exceed the maximum tokens limit, please check your input!")
        model_name = "gpt-3.5-turbo-16k"
        # return "See Above Warning"
    try:
        client = OpenAI(api_key = openai_api_key)
        completion = client.chat.completions.create(
            model=model_name, #"gpt-3.5-turbo", "gpt-3.5-turbo-16k"
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": caption}
            ]
        )
        response = completion.choices[0].message.content.strip()
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=100,
        #     temperature=0
        # )
    except Exception as err:
        print(f"Error: function openaiAPICall() encounter API call error {err}")
        return "See Above Exception"
    return response

def evaluateByLLM(caption):
    prompt = """Given the following scores of some smartphone brands/models, please compare the results from dataset_predict with 
                dataset_correct and calculate the precision, recall, F1, and MSE (scores' mean square error). For any unmatched
                smartphone brands/models, set them as 0 score, and penalize with an error = 1.5. For example, your output should be 
                in the format of a python dictionary string: {'precision': 0.5, 'recall': 0.5, 'F1 score': 0.5, 'MSE': 0.5}
             """
    try:
        client = OpenAI(api_key = openai_api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": caption}
            ]
        )
        response = completion.choices[0].message.content.strip()
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=100,
        #     temperature=0
        # )
    except Exception as err:
        print(f"Error: function openaiAPICall() encounter API call error {err}")
        return "See Above Exception"
    return response

def evaluateDataset(csv_file_name, channel_name):
    rs = readManuallyLabels(csv_file_name) # rs is a dictionary
    videos_dict = rs[channel_name]
    videos_count = 0
    result_dict = None

    for url, scores in videos_dict.items():
        print(f"Processing video {url}, please wait...")

        # Get caption from Youtube API
        res = ytb.transcript_get(url)
        if res is None:
            continue
        caption = api_transcript_to_str(res)

        # Call OpenAI API to do stance analysis
        response = openaiAPICall(caption=caption)

        dataset_predict = "dataset_predict:\n" + response
        dataset_correct = "dataset_correct:\n" + str(scores)

        # print(dataset_predict + dataset_correct)

        # Call LLM to evaluate
        results = evaluateByLLM(dataset_predict + dataset_correct)

        try:
            res_dict = eval(results)
            if result_dict is None:
                result_dict = res_dict
            else:
                for k, v in res_dict.items():
                    result_dict[k] += v
            videos_count +=1
        except Exception as err:
            print(err)
            # return url, results
        print(f"Finish processing video... result = {result_dict}.")
        
    return videos_count, result_dict

def main():
    # url = 'jD9n01Mck0Q'
    # url = 'https://www.youtube.com/watch?v=jD9n01Mck0Q'
    # res = ytb.transcript_get(url)
    # if not res:
    #     print('[See Print Error for Details]')
    # # print(type(res))
    # print(len(res))
    # str_caption = api_transcript_to_str(res)
    # print(str_caption[:30])

    # re = openaiAPICall(str_caption)
    # print(re)

    csv_file = 'std_manual_label.csv'
    count, results = evaluateDataset(csv_file, channel_name='mkbhd')
    print(count, results)
    for k, v in results.items():
        results[k] = v / count
    print(count, results)

if __name__ == '__main__':
    # prompt = """
    # Can you do the sentiment analysis if I provide you with the caption from a smartphone review video?
    # """
    
    # csv_file = 'manual_label.csv'
    # rs = readManuallyLabels(csv_file)
    # print(rs)

    main()
    # count = 7
    # results = {'precision': 3.571428571428571, 'recall': 3.821428571428571, 'F1 score': 3.388095238095238, 'MSE': 5.041666666666667}
    # for k, v in results.items():
    #     results[k] = v / count
    # print(count, results)