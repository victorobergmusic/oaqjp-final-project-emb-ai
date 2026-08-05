"""Flask entry point for the emotion detection web application."""

from flask import Flask, render_template, request

from EmotionDetection import EmotionDetectionError, emotion_detector

app = Flask(__name__)


@app.get("/emotionDetector")
def sent_analyzer():
    """Analyze the supplied text and return a readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    try:
        response = emotion_detector(text_to_analyze)
    except EmotionDetectionError as exc:
        app.logger.warning("Emotion analysis failed: %s", exc)
        return "The emotion service is temporarily unavailable. Please try again.", 502

    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!", 400

    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


@app.get("/")
def render_index_page():
    """Render the application page."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
