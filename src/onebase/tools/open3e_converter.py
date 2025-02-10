from open3e import *
from open3e.Open3Ecodecs import *
from open3e.Open3Edatapoints import dataIdentifiers as open3EDIDs
from open3e.Open3Eenums import E3Enums as open3EEnums

import onebase.core.codecs
from onebase.core.codecs import *

import json

def convertDIDs():

    open3eDict = open3EDIDs["dids"]
    oneBaseDictDIDs = dict()

    for didNumber in open3eDict.keys():
        did = int(didNumber)
        codec = open3eDict[did]
        numBytes = codec.string_len
        name = codec.id

        if type(codec) == open3e.Open3Ecodecs.RawCodec:
            newCodec = CodecRaw(numBytes,name)
            oneBaseDictDIDs[did] = newCodec
        elif (type(codec) == open3e.Open3Ecodecs.O3EInt or type(codec) == open3e.Open3Ecodecs.O3EInt8 or type(codec) == open3e.Open3Ecodecs.O3EInt16 or type(codec) == open3e.Open3Ecodecs.O3EInt32):
            byteWidth = codec.byte_width
            scale = codec.scale
            offset = codec.offset
            signed = codec.signed
            newCodec = CodecInt(numBytes,name,byteWidth,"little",scale, offset, signed)
            oneBaseDictDIDs[did] = newCodec
        elif type(codec) == open3e.Open3Ecodecs.O3EByteVal:
            offset = 0
            newCodec = CodecByte(numBytes,name,offset)
            oneBaseDictDIDs[did] = newCodec
        elif type(codec) == open3e.Open3Ecodecs.O3EBool:
            offset = codec.offset
            newCodec = CodecBool(numBytes,name,offset)
            oneBaseDictDIDs[did] = newCodec
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
        elif (type(codec) == open3e.Open3Ecodecs.O3EEnum):
            enumName = codec.listStr
            newCodec = CodecEnumeration(numBytes, name, enumName)
            oneBaseDictDIDs[did] = newCodec
        elif codec == onebase.core.codecs.CodecList:
            continue
        elif codec == onebase.core.codecs.CodecComplexType:
            continue
        else:
            print("DID " + str(did) + " could not be converted.")
            
    return oneBaseDictDIDs

def convertEnums():
    oneBaseDictEnums = dict()
    oneBaseDictEnums = open3EEnums

    return oneBaseDictEnums