from open3e import *
from open3e.Open3Ecodecs import *
from open3e.Open3Edatapoints import dataIdentifiers as open3EDIDs
from open3e.Open3Eenums import E3Enums as open3EEnums

import onebase.core.codecs
from onebase.core.codecs import *

import json

def convertDIDs():

    open3eDict = open3EDIDs["dids"]
    oneBaseDict = dict()

    for didNumber in open3eDict.keys():
        did = int(didNumber)
        codec = open3eDict[str(didNumber)]
        numBytes = codec.string_len
        name = codec.id

        if type(codec) == open3e.Open3Ecodecs.RawCodec:
            newCodec = CodecRaw(numBytes,name)
            oneBaseDict[did] = newCodec
        elif codec == onebase.core.codecs.CodecInt:
            continue
        elif codec == onebase.core.codecs.CodecInt8:
            continue
        elif codec == onebase.core.codecs.CodecInt16:
            continue
        elif codec == onebase.core.codecs.CodecInt32:
            continue
        elif codec == onebase.core.codecs.CodecByte:
            continue
        elif codec == onebase.core.codecs.CodecBool:
            continue
        elif codec == onebase.core.codecs.CodecUTF8:
            continue
        elif codec == onebase.core.codecs.CodecHardwareSoftwareVersion:
            continue
        elif codec == onebase.core.codecs.CodecMACAddress:
            continue
        elif codec == onebase.core.codecs.CodecIPAddress:
            continue
        elif codec == onebase.core.codecs.CodecDateTime:
            continue
        elif codec == onebase.core.codecs.CodecSTime:
            continue
        elif codec == onebase.core.codecs.CodecUTC:
            continue
        elif codec == onebase.core.codecs.CodecEnumeration:
            continue
        elif codec == onebase.core.codecs.CodecList:
            continue
        elif codec == onebase.core.codecs.CodecComplexType:
            continue
        else:
            print("DID " + str(did) + " could not be converted.")
            
    return oneBaseDict


def convertEnums():
    pass