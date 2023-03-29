import UID
import unittest

dId = 1
mId = 1
uid_b = format(UID.UID.generate(dId, mId), 'b').rjust(64, '0')

class TestGenerate(unittest.TestCase):
    def test_signedBit(self):
        self.assertEqual(uid_b[0], '0')
    def test_datacenterId(self):
        self.assertEqual(uid_b[42:47], format(dId, 'b').rjust(5, "0"))
    def test_machineId(self):
        self.assertEqual(uid_b[47:52], format(mId, 'b').rjust(5, "0"))


if __name__ == '__main__':
    unittest.main()

