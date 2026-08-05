import unittest
from EmotionDetection.emotion_detection import emotion_detector

class TestEmotionDetector(unittest.TestCase):
    def test_emotion_detector(self):
        # Joy
        result_1 = emotion_detector("I am glad my cats liked the origami")
        self.assertEqual(result_1['dominant_emotion'], 'joy')

        # Anger
        result_2 = emotion_detector("I am really mad about this bug")
        self.assertEqual(result_2['dominant_emotion'], 'anger')

        # Disgust
        result_3 = emotion_detector("I feel disgusted just hearing about it")
        self.assertEqual(result_3['dominant_emotion'], 'disgust')

        # Sadness
        result_4 = emotion_detector("I am so sad my bicycle taxi app crashed")
        self.assertEqual(result_4['dominant_emotion'], 'sadness')

        # Fear
        result_5 = emotion_detector("I am really afraid that this will fail")
        self.assertEqual(result_5['dominant_emotion'], 'fear')

if __name__ == '__main__':
    unittest.main()
