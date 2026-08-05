from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector")
def sent_analyzer():
    # Hämtar argumentet från webbgränssnittet
    text_to_analyze = request.args.get('textToAnalyze')

    # Kör funktionen från paketet
    response = emotion_detector(text_to_analyze)

    # Felhantering: Kollar om värdet är None (Task 7)
    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    # Formaterar outputen exakt enligt instruktionerna
    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

@app.route("/")
def render_index_page():
    # Laddar startsidan
    return render_template('index.html')

if __name__ == "__main__":
    # Kör servern
    app.run(host="0.0.0.0", port=5000)
