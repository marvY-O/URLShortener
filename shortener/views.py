from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import URL
from .serializer import dbSerializer, shortURLResponseSerializer
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
import validators
import time

dId = 1
mId = 1

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


class shortURLResponse:
    def __init__(self, shortURL, longURL):
        self.shortURL = shortURL
        self.longURL = longURL


# Create your views here.
@api_view(['POST'])
def shorten(request):
    data = request.data
    print(data)
    if ("longURL" not in data):
        return Response("longURL not found!", status = status.HTTP_400_BAD_REQUEST)
    if (not validators.url(data["longURL"])):
        return Response("invalid URL!", status = status.HTTP_400_BAD_REQUEST)
    
    entry = URL.objects.filter(longURL = data["longURL"])
    print(entry.values())

    if (entry.exists()):
        surl = shortURLResponse(entry.values()[0]["shortURL"], data["longURL"])
        serializer = shortURLResponseSerializer(surl)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    newURL = URL()
    newURL.uid = generate(dId, mId)
    newURL.longURL = data["longURL"]
    newURL.shortURL = int_to_base62(newURL.uid)

    

    #print(newURL.shortURL)
    #print("url: {}; id: {}".format(newURL.shortURL, newURL.uid))

    newURL.save()

    surl = shortURLResponse(newURL.shortURL, data["longURL"])
    serializer = shortURLResponseSerializer(surl)
    return Response(serializer.data, status = status.HTTP_200_OK)


class RetrieveURL(APIView):
    def get(self, request, shortID):
        uid = base62_to_int(shortID)
        product = URL.objects.filter(uid=uid)

        if (not product.exists()):
            return Response("Invalid!", status = status.HTTP_400_BAD_REQUEST)
        
        return HttpResponseRedirect(redirect_to=product.values()[0]["longURL"])
