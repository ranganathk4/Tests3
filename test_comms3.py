import unittest
import comms3
import comms3

print unittest

class Comms3TestCase(unittest.TestCase):

    def test_upload(self):
        self.assertTrue(comms3.upload('ranganathk4', 's3uploadfile.txt'))

    def test_download(self):
        self.assertTrue(comms3.download('ranganathk4', 's3samplefile.txt'))

if __name__ == '__main__':
    unittest.main()
