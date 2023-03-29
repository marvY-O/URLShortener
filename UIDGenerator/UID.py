### 64 bit unique number generator

## 1 bit signed/unsigned
## 41 bit timestamp
## 5 bits datacenterID
## 5 bits MachineID
## 12 bits sequence number

import time

class UID:

    @staticmethod
    def generate(dID, mID):
        """
        Generates a Unique ID (64bit Integer)
        """

        timens = time.time_ns()

        signedBit = 0
        datacenterID = dID
        timestamp = int(timens/pow(10,6))
        machineID = mID
        sequenceID = timens%pow(10,6)//4096

        signedBit = format(signedBit,'b').rjust(1, "0")
        timestamp = format(timestamp,'b').rjust(41, "0")
        datacenterID = format(datacenterID, 'b').rjust(5, "0")
        machineID = format(machineID,'b').rjust(5, "0")
        sequenceID = format(sequenceID, 'b').rjust(12, "0")

        uid = signedBit + timestamp + datacenterID + machineID + sequenceID

        uid = int(uid, 2)

        return uid

    @staticmethod
    def int_to_base62(uid):
        """
        Convert the UID to a base62 string.
        """

        if uid == 0:
            return '0'
        
        charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = []
        
        while uid:
            uid, remainder = divmod(uid, 62)
            result.append(charset[remainder])
        
        return ''.join(reversed(result))
    
    @staticmethod
    def base62_to_int(s):
        """
        Convert a base62 string to an integer.
        """
        charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base = len(charset)
        result = 0
        
        for i, c in enumerate(reversed(s)):
            result += charset.index(c) * (base ** i)
        
        return result