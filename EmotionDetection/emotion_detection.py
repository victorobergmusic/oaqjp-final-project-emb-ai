import json
import requests

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    my_obj = { "raw_document": { "text": text_to_analyze } }

    response = requests.post(url, json=my_obj, headers=headers, timeout=10)

    # Felhantering för ogiltig/tom inmatning (Task 7)
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    formatted_response = json.loads(response.text)
    emotions = formatted_response['emotionPredictions'][0]['emotion']

    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    emotion_list = [anger_score, disgust_score, fear_score, joy_score, sadness_score]
    emotion_keys = ['anger', 'disgust', 'fear', 'joy', 'sadness']

    dominant_emotion_index = 0
    highest_score = 0.0

    for index, score in enumerate(emotion_list):
        if score > highest_score:
            highest_score = score
            dominant_emotion_index = index

    dominant_emotion = emotion_keys[dominant_emotion_index]

    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
