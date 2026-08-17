import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inference.predict import predict_email

class TestInference(unittest.TestCase):
    
    def test_predict_empty_string(self):
        result = predict_email("")
        self.assertIn("prediction", result)
        self.assertIn("probability", result)
        self.assertEqual(result["prediction"], "legitimate")
        self.assertEqual(result["probability"], 0.0)
        
    def test_predict_normal_string(self):
        result = predict_email("Please review the document attached.")
        self.assertIn("prediction", result)
        self.assertIn("probability", result)
        self.assertIsInstance(result["probability"], float)

if __name__ == '__main__':
    unittest.main()
