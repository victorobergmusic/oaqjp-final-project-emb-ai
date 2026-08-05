"""Unit tests for the emotion service client."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection import EmotionDetectionError, emotion_detector


class TestEmotionDetector(unittest.TestCase):
    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_returns_scores_and_dominant_emotion(self, mock_post):
        response = Mock(status_code=200)
        response.json.return_value = {
            "emotionPredictions": [
                {
                    "emotion": {
                        "anger": 0.01,
                        "disgust": 0.02,
                        "fear": 0.03,
                        "joy": 0.90,
                        "sadness": 0.04,
                    }
                }
            ]
        }
        mock_post.return_value = response

        result = emotion_detector("I am glad this works")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.90)
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.kwargs["timeout"], 10)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_empty_input_returns_none_values_without_api_call(self, mock_post):
        result = emotion_detector("   ")

        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(all(value is None for value in result.values()))
        mock_post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_bad_request_returns_none_values(self, mock_post):
        mock_post.return_value = Mock(status_code=400)

        result = emotion_detector("invalid")

        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_network_failure_raises_controlled_error(self, mock_post):
        mock_post.side_effect = requests.Timeout("timed out")

        with self.assertRaises(EmotionDetectionError):
            emotion_detector("hello")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_malformed_response_raises_controlled_error(self, mock_post):
        response = Mock(status_code=200)
        response.json.return_value = {"unexpected": "response"}
        mock_post.return_value = response

        with self.assertRaises(EmotionDetectionError):
            emotion_detector("hello")


if __name__ == "__main__":
    unittest.main()
