
import pandas as pd
import requests as rq
import time
from tqdm import tqdm

de_sample = pd.read_csv('de_sample.csv')
uk_sample = pd.read_csv('uk_sample.csv')



api_key = 'AIzaSyDy-t_XHu90XKf6bSTWxg3mAs_4gMHJ4OI'


def make_request(tweet_text: str, api_key: str, lang: str):    
    endpoint_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": tweet_text},
        "languages": [lang],
        "requestedAttributes": {"TOXICITY": {}},
    }

    params = {"key": api_key}
    try:
        response = rq.post(endpoint_url, params=params, json=data)
        response_data = response.json()
        response = response_data['attributeScores']['TOXICITY']['spanScores'][0]['score']['value']


    except rq.exceptions.RequestException as e:
        print("Error making the request:", e)

    return response


de_sample['score'] = pd.NA
for index, row in tqdm(de_sample.iterrows(), total=de_sample.shape[0]):
    score = make_request(row['text'], api_key, 'de') 
    de_sample.at[index, 'score'] = score

de_sample.to_csv("results/de_sample.csv")



uk_sample['score'] = pd.NA
for index, row in tqdm(uk_sample.iterrows(), total=uk_sample.shape[0]):
    score = make_request(row['text'], api_key, 'de') 
    uk_sample.at[index, 'score'] = score
    
uk_sample.to_csv("results/uk_sample.csv")

