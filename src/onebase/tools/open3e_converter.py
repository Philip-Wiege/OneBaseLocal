from open3e import *
from open3e.Open3Ecodecs import *
from open3e.Open3Edatapoints import dataIdentifiers as open3EDIDs
from open3e.Open3Eenums import E3Enums as open3EEnums

import onebase.core.codecs
from onebase.core.codecs import *

import json

def convertDIDs(self):

    oneBaseDict = dict()

    for didNumber in open3EDIDs.keys():
        did = int(didNumber)
        codec = open3EDIDs[didNumber]

        if codec == onebase.core.codecs.CodecRaw:
            pass
        if codec == onebase.core.codecs.CodecInt:
            pass
        if codec == onebase.core.codecs.CodecInt16:
            pass
        elif codec == onebase.core.codecs.CodecInt32:
            pass
        else:
            print("DID " + str(did) + " could not be converted.")


def convertEnums(self):
    pass