"""Analyze English text with the IBM Skills Network emotion service."""

import requests

EMOTION_API_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
EMOTION_API_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")
REQUEST_TIMEOUT_SECONDS = 10


class EmotionDetectionError(RuntimeError):
    """Raised when the remote emotion service cannot return a valid result."""


def _empty_result():
    """Return the stable response shape used for invalid input."""
    return {**{emotion: None for emotion in EMOTION_KEYS}, "dominant_emotion": None}


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for a piece of text.

    Empty input produces a result whose values are all ``None``. Failures in
    the remote service raise ``EmotionDetectionError`` so callers can present
    a controlled error response instead of leaking an internal exception.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    payload = {"raw_document": {"text": text_to_analyze.strip()}}

    try:
        response = requests.post(
            EMOTION_API_URL,
            json=payload,
            headers=EMOTION_API_HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise EmotionDetectionError("Could not reach the emotion service.") from exc

    if response.status_code == 400:
        return _empty_result()

    try:
        response.raise_for_status()
        response_payload = response.json()
        raw_emotions = response_payload["emotionPredictions"][0]["emotion"]
        emotions = {key: float(raw_emotions[key]) for key in EMOTION_KEYS}
    except requests.RequestException as exc:
        raise EmotionDetectionError("The emotion service returned an error.") from exc
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise EmotionDetectionError(
            "The emotion service returned an unexpected response."
        ) from exc

    dominant_emotion = max(emotions, key=emotions.get)
    return {**emotions, "dominant_emotion": dominant_emotion}
