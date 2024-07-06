import unittest
import json
from index import sms_encoding_info

# Load test data from JSON file
with open('test_data.json') as f:
    test_data = json.load(f)

def generate_test_function(text, expected_encoding, expected_length):
    def test_function(self):
        encoding, bit_length = sms_encoding_info(text)
        self.assertEqual(encoding, expected_encoding)
        self.assertEqual(bit_length, expected_length)
    return test_function

class TestSMSEncodingInfo(unittest.TestCase):
    pass

# Dynamically create test methods
for i, message in enumerate(test_data["messages"]):
    test_func = generate_test_function(message["text"], message["encoding"], message["length"])
    setattr(TestSMSEncodingInfo, f'test_sms_encoding_info_{i}', test_func)

# Run the tests
if __name__ == '__main__':
    unittest.main()
