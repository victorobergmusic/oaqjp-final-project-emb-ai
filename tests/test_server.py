"""Tests for the Flask routes."""

import unittest
from unittest.mock import patch

from EmotionDetection import EmotionDetectionError
from server import app


class TestServer(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_index_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NLP Emotion Detection", response.data)

    @patch("server.emotion_detector")
    def test_analysis_response_is_formatted(self, mock_detector):
        mock_detector.return_value = {
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.90,
            "sadness": 0.04,
            "dominant_emotion": "joy",
        }

        response = self.client.get(
            "/emotionDetector", query_string={"textToAnalyze": "cats & origami"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The dominant emotion is joy.", response.data)
        mock_detector.assert_called_once_with("cats & origami")

    @patch("server.emotion_detector")
    def test_invalid_input_returns_bad_request(self, mock_detector):
        mock_detector.return_value = {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

        response = self.client.get("/emotionDetector")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")

    @patch("server.emotion_detector")
    def test_service_failure_returns_bad_gateway(self, mock_detector):
        mock_detector.side_effect = EmotionDetectionError("service unavailable")

        response = self.client.get(
            "/emotionDetector", query_string={"textToAnalyze": "hello"}
        )

        self.assertEqual(response.status_code, 502)
        self.assertIn(b"temporarily unavailable", response.data)


if __name__ == "__main__":
    unittest.main()
