from openai import OpenAI
import os
import requests

# check it whether it contains the keyword "iphone" or "galaxy" or "samsung" or "google" or "pixel" 
def get_phone_brand_by_keyword_matching(model):
   # use orignal model name to match because Mate maybe confused with ultimate in lower case
    
    if "Apple" in model :
        return "Apple"
    elif "Samsung" in model:
        return "Samsung"
    elif "Google" in model: 
        return "Google"
    elif "Xiaomi" in model: 
        return "Xiaomi"
    elif "Huawei" in model :
        return "Huawei"
    elif "OnePlus" in model:
        return "OnePlus"
    elif "Oppo" in model:
        return "Oppo"
    elif "Vivo" in model:
        return "Vivo"
    elif "Realme" in model:
        return "Realme"
    elif "Nokia" in model:
        return "Nokia"
    elif "Motorola" in model:
        return "Motorola"
    elif "LG" in model:
        return "LG"
    elif "Sony" in model:
        return "Sony"
    elif "Asus" in model:
        return "Asus"
    elif "Lenovo" in model:
        return "Lenovo"
    elif "ZTE" in model:
        return "ZTE"
    elif "HTC" in model:
        return "HTC"
    elif "BlackBerry" in model:
        return "BlackBerry"
    elif "Honor" in model:
        return "Honor"
    elif "Meizu" in model:
        return "Meizu"
    elif "Alcatel" in model:
        return "Alcatel"
    elif "Microsoft" in model:
        return "Microsoft"
    elif "Nubia" in model:
        return "Nubia"
    elif "Sharp" in model:
        return "Sharp"
    else:
        return "Unknown"
def get_phone_brand_by_keyword_matching2(model):
    # Add more first use brand keywords as needed like xiaomi, huawei, etc.
    model = model.lower()
    if "apple" in model: 
        return "Apple"
    elif "samsung" in model :
        return "Samsung"
    elif "google" in model :
        return "Google"
    elif "xiaomi" in model :
        return "Xiaomi"
    elif "huawei" in model :
        return "Huawei"
    elif "oneplus" in model:
        return "OnePlus"
    elif "oppo" in model:
        return "Oppo"
    elif "vivo" in model:
        return "Vivo"
    elif "realme" in model:
        return "Realme"
    elif "nokia" in model:
        return "Nokia"
    elif "motorola" in model:
        return "Motorola"
    elif "lg" in model:
        return "LG"
    elif "sony" in model:
        return "Sony"
    elif "asus" in model:
        return "Asus"
    elif "lenovo" in model:
        return "Lenovo"
    elif "zte" in model:
        return "ZTE"
    elif "htc" in model:
        return "HTC"
    elif "blackberry" in model:
        return "BlackBerry"
    elif "honor" in model:
        return "Honor"
    elif "meizu" in model:
        return "Meizu"
    elif "alcatel" in model:
        return "Alcatel"
    elif "microsoft" in model:
        return "Microsoft"
    elif "nubia" in model:
        return "Nubia"
    elif "sharp" in model:
        return "Sharp"
    else:
        return "Unknown"
    

def get_phone_brand_by_secondary_keyword_matching(model):
    # just use iPhone and Galaxy and Pixel etc as secondary keywords 

    if "iPhone" in model:
        return "Apple"
    elif "Galaxy" in model:
        return "Samsung"
    elif "Pixel" in model:
        return "Google"
    elif "Mi" in model or "Redmi" in model:
        return "Xiaomi"
    elif "Nova" in model or "Mate" in model:
        return "Huawei"
    elif "Ace" in model:
        return "OnePlus"
    elif "Find" in model:
        return "Oppo"
    elif "iQOO" in model:
        return "Vivo"
    elif "Xperia" in model:
        return "Sony"
    elif "ZenFone" in model or "ROG" in model:
        return "Asus"
    elif "Lumia" in model or "Surface" in model:
        return "Microsoft"
    else:
        return "Unknown"
    
def get_phone_brand_by_secondary_keyword_matching2(model):
    # Add more secondary keywords as needed like iPhone, Galaxy, Pixel etc.
    model = model.lower()
    if "iphone" in model:
        return "Apple"
    elif "galaxy" in model:
        return "Samsung"
    elif "pixel" in model:
        return "Google"
    elif "mi" in model or "redmi" in model:
        return "Xiaomi"
    elif "nova" in model or "mate" in model:
        return "Huawei"
    elif "ace" in model:
        return "OnePlus"
    elif "find" in model:
        return "Oppo"
    elif "iqoo" in model:
        return "Vivo"
    elif "xperia" in model:
        return "Sony"
    elif "zenfone" in model or "rog" in model:
        return "Asus"
    elif "lumia" in model or "surface" in model:
        return "Microsoft"
    else:
        return "Unknown"
   
    


def get_phone_brand_by_local_map(model):
    # a map between phone model to phone brand
    # vivo X series 
    phone_brands = {
        "x100pro": "Vivo",
        "x100": "Vivo",
        "x90pro": "Vivo",
        "x90": "Vivo",
        "x80pro": "Vivo",
        "x80": "Vivo",
        # flip phones
        "zflip5": "Samsung",
        "zflip4": "Samsung",
        "zflip3": "Samsung",
        "zflip2": "Samsung",
        "zflip": "Samsung",
        "zfold5": "Samsung",
        "zfold4": "Samsung",
        "zfold3": "Samsung",
        "zfold2": "Samsung",
        "zfold": "Samsung",



        # Add more entries as needed
    }
    key = model.lower()
    key = key.replace(" ", "")
    # check if the model is in the map
    if key in phone_brands:
        return phone_brands[key]
    else:
        return "Unknown"

def google_search(query, api_key,cse_id, num_results=10):
    """
    Perform a Google search using the provided query, API key, and custom search engine ID.

    :param query: The search query string.
    :param api_key: Your Google API key.
    :param cse_id: Your custom search engine ID.
    :param num_results: Number of search results to return.
    :return: A list of search results.
    """
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx':cse_id,
        'num': num_results
    }
    response = requests.get(search_url, params=params)
    results = response.json()
    return results.get("items", [])

def extract_brand_name(response):
    # Split the response by spaces
    words = response.split()

    # Check if the response is just one word (likely the brand name)
    if len(words) == 1:
        return response
    else:
        # If the response is a sentence, find the word after "is"
        if "is" in words:
            is_index = words.index("is")
            # Return the word after "is" if it exists
            if is_index + 1 < len(words):
                return words[is_index + 1].rstrip('.')
        return "Unknown"   

def get_phone_brand_by_LLM(model):
    key = "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"
    google_key  = "AIzaSyAB5ty3hgqLpnyEL2CCjTdOOohsqgeaBD8"
    cse_id = "67ab01209dbc245fb"
    query = f"smartphone {model}"
    search_results = google_search(query, google_key,cse_id)
    search_results_titles = ". ".join([result['title'] for result in search_results])
    print(search_results_titles)
    user_message_content = f"What is the brand name of the phone {model} based on these search results: {search_results_titles}"
    client = OpenAI(api_key=key)
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "Your task is to extract and provide only the brand name from the given information. For example, if the search results are '1. Galaxy S21 Ultra - Samsung's latest flagship, 2. Samsung Galaxy S21 review', the response should be 'Samsung'."},
        {"role": "user", "content": user_message_content}
      ]
    )
    result = completion.choices[0].message.content.strip()
    print(result)
    return extract_brand_name(result)
    



def get_phone_brand(model):
   #first try to get the brand by keyword matching
    brand = get_phone_brand_by_keyword_matching(model)
    if(brand != "Unknown"):
        return brand
    
    brand = get_phone_brand_by_keyword_matching2(model)
    if(brand != "Unknown"):
        return brand
    
    brand = get_phone_brand_by_secondary_keyword_matching(model)
    if(brand != "Unknown"):
        return brand
    
    brand = get_phone_brand_by_secondary_keyword_matching2(model)
    if(brand != "Unknown"):
        return brand
    
    brand = get_phone_brand_by_local_map(model)
    if(brand != "Unknown"):
        return brand
    
    brand = get_phone_brand_by_LLM(model)
    if(brand != "Unknown"):
        return brand
    return "Unknown"
    

    
