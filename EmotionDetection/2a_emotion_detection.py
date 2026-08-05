import requests

def emotion_detector(text_to_analyze):
    """
    Min funktion för att skicka text till Watson NLP och få tillbaka känslor.
    """
    # API-urlen som gavs i uppgiften
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Headers som krävs för modellen
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # JSON-formatet som Watson vill ha, där min textvariabel petas in
    my_obj = { "raw_document": { "text": text_to_analyze } }
    
    # Gör ett POST-anrop (lägger till en timeout så koden inte hänger sig)
    response = requests.post(url, json=my_obj, headers=headers, timeout=10)
    
    # Enligt instruktionen ska jag än så länge bara returnera text-attributet av response-objektet
    return response.text
