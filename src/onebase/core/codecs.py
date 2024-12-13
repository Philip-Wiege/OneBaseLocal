import udsoncan
from typing import Optional, Any
import datetime
import json
import onebase.core.enumerations

class CodecRaw(udsoncan.DidCodec):
    def __init__(self, paramNumBytes: int, paramDIDName:str):
        self._numBytes = paramNumBytes
        self._DIDName = paramDIDName

    def encode(self, paramHexString: Any) -> bytes:
        _encodedBytes = bytes.fromhex(paramHexString)
        if len(_encodedBytes) != self._numBytes:
            raise ValueError('String must be %d long' % self._numBytes)
        return _encodedBytes

    def decode(self, paramEncodedBytes: bytes) -> Any:
        _decodedHexString = paramEncodedBytes.hex()
        return _decodedHexString

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self._numBytes, "name": self._DIDName, "args": {}})

    def getNumBytes(self) -> int:
        return self._numBytes

class CodecInt(udsoncan.DidCodec):
    def __init__(self, paramNumBytes: int, paramDIDName:str, paramByteWidth: int, paramByteOrder="little", paramScale: float = 1.0, paramOffset: int = 0, paramSigned=False):
        self._numBytes = paramNumBytes
        self._byteWidth = paramByteWidth
        self._byteOrder = paramByteOrder
        self._DIDName = paramDIDName
        self._scale = paramScale
        self._offset = paramOffset
        self._signed = paramSigned

    def encode(self, string_ascii: Any, paramRaw=False) -> bytes:        
        if(paramRaw):
            _hexString = string_ascii
            return CodecRaw.encode(self, _hexString)
        else:
            if (self._offset != 0):
                raise NotImplementedError("O3EInt.encode(): offset!=0 not implemented yet")
            else:
                val = round(eval(str(string_ascii))*self._scale)    # convert submitted data to numeric value and apply scaling factor
                string_bin = val.to_bytes(length=self._byteWidth, byteorder=self._byteOrder, signed=self._signed)
                return string_bin

    def decode(self, paramEncodedBytes: bytes, paramRaw=False) -> Any:
        if(paramRaw):
            return CodecRaw.decode(self, paramEncodedBytes)
        else:
            val = int.from_bytes(paramEncodedBytes[self._offset:self._offset + self._byteWidth], byteorder=self._byteOrder, signed=self._signed)
            return float(val) / self._scale

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self._numBytes, "name": self._DIDName, "args": {"scale":self._scale, "signed":self._signed, "offset":self._offset}})

    def getNumBytes(self) -> int:
        return self._numBytes

class CodecInt8(CodecInt):
    def __init__(self, paramNumBytes:int, paramDIDName:str, paramByteOrder="little", paramScale:float = 1.0, paramOffset:int = 0, paramSigned=False):
        CodecInt.__init__(self, paramNumBytes=paramNumBytes, paramDIDName=paramDIDName, paramByteWidth=1, paramByteOrder=paramByteOrder, paramScale=paramScale, paramOffset=paramOffset, paramSigned=paramSigned)

class CodecInt16(CodecInt):
    def __init__(self, paramNumBytes:int, paramDIDName:str, paramByteOrder="little", paramScale:float = 1.0, paramOffset:int = 0, paramSigned=False):
        CodecInt.__init__(self, paramNumBytes=paramNumBytes, paramDIDName=paramDIDName, paramByteWidth=2, paramByteOrder=paramByteOrder, paramScale=paramScale, paramOffset=paramOffset, paramSigned=paramSigned)

class CodecInt32(CodecInt):
    def __init__(self, paramNumBytes:int, paramDIDName:str, paramByteOrder="little", paramScale:float = 1.0, paramOffset:int = 0, paramSigned=False):
        CodecInt.__init__(self, paramNumBytes=paramNumBytes, paramDIDName=paramDIDName, paramByteWidth=4, paramByteOrder=paramByteOrder, paramScale=paramScale, paramOffset=paramOffset, paramSigned=paramSigned)

class CodecByte(udsoncan.DidCodec):
    def __init__(self, paramNumBytes:int, paramDIDName:str, paramOffset:int = 0):
        CodecInt.__init__(self, paramNumBytes=paramNumBytes, paramDIDName=paramDIDName, paramByteWidth=1, paramByteOrder="little", paramScale=1.0, paramOffset=paramOffset, paramSigned=False)

class CodecBool(udsoncan.DidCodec):
    def __init__(self, paramNumBytes:int, paramDIDName:str, paramOffset:int = 0):
        self._numBytes = paramNumBytes
        self._DIDName = paramDIDName
        self._offset = paramOffset

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw):
            _hexString = string_ascii
            return CodecRaw.encode(self, _hexString)
        else:
            if string_ascii == 'on':
                return bytes([1])
            else:
                return bytes([0])

    def decode(self, paramEncodedBytes: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw):
            return CodecRaw.decode(self, paramEncodedBytes)
        else:
            val = int(paramEncodedBytes[self.offset])
            if(val==0):
                return "off"
            else:
                return "on"

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self._numBytes, "name": self._DIDName, "args": {"offset":self._offset}})

    def getNumBytes(self) -> int:
        return self._numBytes

class CodecUTF8(udsoncan.DidCodec):
    def __init__(self, paramNumBytes: int, paramDIDName: str, paramOffset: int = 0):
        self._numBytes = paramNumBytes
        self._DIDName = paramDIDName
        self._offset = paramOffset

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw):
            _hexString = string_ascii
            _encodedBytes = CodecRaw.encode(self, _hexString)
        else:
            _byteArrayUTF8 = string_ascii.encode(encoding="utf-8")
            _encodedBytes = _byteArrayUTF8


        _paddingByte = b'\x00'
        if len(_encodedBytes) < self._numBytes:
            _resultPadddedCropped = _encodedBytes.ljust(self._numBytes, _paddingByte)
        elif len(_encodedBytes) > self._numBytes:
            _resultPadddedCropped = _encodedBytes[0:self._numBytes]
        else:
            _resultPadddedCropped = _encodedBytes


        return _resultPadddedCropped

    def decode(self, paramEncodedBytes: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): 
            return CodecRaw.decode(self, paramEncodedBytes)
        else:
            mystr = paramEncodedBytes[self._offset:self._offset+self._numBytes].decode('utf-8')
            return mystr.replace('\x00', '')
       
    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self._numBytes, "name": self._DIDName, "args": {"offset":self._offset}})

    def getNumBytes(self) -> int:
        return self._numBytes

class CodecHardwareSoftwareVersion(udsoncan.DidCodec):
    def __init__(self, paramNumBytes: int, paramDIDName: str):
        self._numBytes = paramNumBytes
        self._DIDName = paramDIDName

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)
        else:
            raise NotImplementedError("Encoding of HardwareSoftwareVersion not implemented.")

    def decode(self, paramEncodedBytes: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): 
            return CodecRaw.decode(self, paramEncodedBytes)
        lstv = []
        for i in range(0, self._numBytes, 2):
            lstv.append(str(int.from_bytes(paramEncodedBytes[i:i+2], byteorder="little")))
        return ".".join(lstv)

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self._numBytes, "id": self._DIDName, "args": {}})

    def getNumBytes(self) -> int:
        return self._numBytes

class CodecMACAddress(udsoncan.DidCodec):
    def __init__(self, paramNumBytes: int, paramDIDName: str):
        self._numBytes = paramNumBytes
        self._DIDName = paramDIDName

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)
        else:
            raise NotImplementedError("Encoding of MACAddress not implemented.")

    def decode(self, paramEncodedBytes: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): 
            return CodecRaw.decode(self, paramEncodedBytes)
        lstv = []
        for i in range(6):
            lstv.append(paramEncodedBytes[i:i+1].hex().upper())
        return "-".join(lstv)

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self._numBytes, "id": self._DIDName, "args": {}})

    def getNumBytes(self) -> int:
        return self._numBytes

class CodecIp4Addr(udsoncan.DidCodec): #TBD  # also working with IPV6
    def __init__(self, string_len: int, idStr: str):
        self.string_len = string_len
        self.id = idStr

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)
        raise Exception("not implemented yet")

    def decode(self, string_bin: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): 
            return CodecRaw.decode(self, string_bin)
        lstv = []
        for i in range(self.string_len):
            lstv.append(format(int(string_bin[i]), '03d'))
        return ".".join(lstv)

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self.string_len, "id": self.id, "args": {}})

    def __len__(self) -> int:
        return self.string_len

class CodecSDate(udsoncan.DidCodec): #TBD
    def __init__(self, string_len: int, idStr: str):
        self.string_len = string_len
        self.id = idStr

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)
        raise Exception("not implemented yet")

    def decode(self, string_bin: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): 
            return CodecRaw.decode(self, string_bin)
        return f"{int(string_bin[0]):02d}.{int(string_bin[1]):02d}.{2000+int(string_bin[2])}"

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self.string_len, "id": self.id, "args": {}})

    def __len__(self) -> int:
        return self.string_len

class CodecDateTime(udsoncan.DidCodec): #TBD
    def __init__(self, string_len: int, idStr: str, timeformat: str="VM"):
        self.string_len = string_len
        self.id = idStr
        self.timeformat = timeformat

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)
        raise Exception("not implemented yet")

    def decode(self, string_bin: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): 
            return CodecRaw.decode(self, string_bin)
        
        if self.timeformat == 'VM':
            dt = datetime.datetime(
                 string_bin[0]*100+string_bin[1], # year
                 string_bin[2],                   # month
                 string_bin[3],                   # day
                 string_bin[5],                   # hour
                 string_bin[6],                   # minute
                 string_bin[7]                    # second
                )
        if self.timeformat == 'ts':
            dt = datetime.datetime.fromtimestamp(int.from_bytes(string_bin[0:6], byteorder="little", signed=False))
        return { "DateTime": str(dt),
                 "Timestamp": int(dt.timestamp()*1000)
               }

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self.string_len, "id": self.id, "args": {"timeformat":self.timeformat}})

    def __len__(self) -> int:
        return self.string_len

class CodecSTime(udsoncan.DidCodec): #TBD
    def __init__(self, string_len: int, idStr: str):
        self.string_len = string_len
        self.id = idStr

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)
        else:
            string_bin = bytes()
            parts = string_ascii.split(":")
            return(bytes([int(p) for p in parts]))

    def decode(self, string_bin: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): 
            return CodecRaw.decode(self, string_bin)
        lstv = []
        for i in range(self.string_len):
            lstv.append(f"{(string_bin[i]):02d}")
        return ":".join(lstv)

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self.string_len, "id": self.id, "args": {}})

    def __len__(self) -> int:
        return self.string_len

class CodecUTC(udsoncan.DidCodec): #TBD
    def __init__(self, string_len: int, idStr: str, offset: int = 0):
        self.string_len = string_len
        self.id = idStr
        self.offset = offset

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes: 
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)
        raise Exception("not implemented yet")

    def decode(self, string_bin: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): 
            return CodecRaw.decode(self, string_bin)
        val = datetime.datetime.fromtimestamp(int.from_bytes(string_bin[0:4], byteorder="little", signed=False)).strftime('%Y-%m-%d %H:%M:%S')
        return str(val)

    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self.string_len, "id": self.id, "args": {"offset":self.offset}})

    def __len__(self) -> int:
        return self.string_len

class CodecEnum(udsoncan.DidCodec): #TBD
    def __init__(self, string_len: int, idStr: str, listStr:str):
        self.string_len = string_len
        self.id = idStr
        self.listStr = listStr

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)

        if type(string_ascii) == dict:
            input = string_ascii['Text']
        elif type(string_ascii) == str:
            input = string_ascii
        else:
            raise ValueError("Ivalid input for OEEnum")
        for key, value in enumerations.E3Enums[self.listStr].items():
            if value.lower() == input.lower():
                string_bin = key.to_bytes(length=self.string_len,byteorder="little",signed=False)
                return string_bin
        raise Exception("not found")

    def decode(self, string_bin: bytes, paramRaw:bool=False) -> str:
        if(paramRaw): 
            return CodecRaw.decode(self, string_bin)
        try:
            val = int.from_bytes(string_bin[0:self.string_len], byteorder="little", signed=False)
            txt = enumerations.E3Enums[self.listStr][val]
            return {"ID": val,
                    "Text": txt }
        except:
            return {"ID": val,
                    "Text": "not found in " + self.listStr}
        
    def getCodecInfo(self):
        return ({"codec": self.__class__.__name__, "len": self.string_len, "id": self.id, "args": {"listStr":self.listStr}})

    def __len__(self) -> int:
        return self.string_len
       
class CodecList(udsoncan.DidCodec): #TBD
    def __init__(self, string_len: int, idStr: str, subTypes: list, arraylength: int=0):
        self.string_len = string_len
        self.id = idStr
        self.subTypes = subTypes
        self.len = len

    def encode(self, string_ascii: Any, paramRaw:bool=False) -> bytes:        
        if(paramRaw): 
            return CodecRaw.encode(self, string_ascii)
        else:
            input_dict = {k.lower():v for k,v in string_ascii.items()}
            keys = list(input_dict.keys())
            # expect two keys: count and another one
            assert len(keys) == 2, "Too many keys in dict for OEList"
            assert "count" in keys, 'Key "count" missing for OEList'
            count = input_dict["count"]
            keys.remove("count")
            input_list = input_dict[keys[0]]
            list_type = self.subTypes[1]
            string_bin = bytes()
            string_bin+=self.subTypes[0].encode(count)
            assert count == len(input_list), '"count" and list lenght do not match for OEList'
            for i in range(count):
                try:
                    string_bin+=list_type.encode(input_list[i])
                except KeyError as e:
                    raise ValueError(f"Cannot encode value due to missing key: {e}")
            # zero padding
            string_bin+=bytes(self.string_len - len(string_bin))
        return string_bin

    def decode(self, string_bin: bytes, paramRaw:bool=False) -> Any:
        subTypes = self.subTypes
        idStr = self.id
        if(paramRaw): 
            return CodecRaw.decode(self, string_bin)
        result = {}
        index = 0
        if(self.len == 0): 
            count = 0

        for subType in self.subTypes:
            # we expect a byte element with the name "Count" or "count"
            if subType.id.lower() == 'count':
                count = int(subType.decode(string_bin[index:index+subType.string_len]))
                result[subType.id]=count 
                index =+ subType.string_len 

            elif type(subType) is CodecComplexType:
                result[subType.id] = []
                for i in range(count):
                    result[subType.id].append(subType.decode(string_bin[index:index+subType.string_len]))
                    index+=subType.string_len

            else:
                result[subType.id]=subType.decode(string_bin[index:index+subType.string_len]) 
                index = index + subType.string_len

        return dict(result)
    
    def getCodecInfo(self):
        argsSubTypes = []
        for subType in self.subTypes:
            argsSubTypes.append(subType.getCodecInfo())
        return ({"codec": self.__class__.__name__, "len": self.string_len, "id": self.id, "args": {"subTypes":argsSubTypes}})

    def __len__(self) -> int:
        return self.string_len

class CodecComplexType(udsoncan.DidCodec):
    def __init__(self, paramNumBytes:int, paramDIDName:str, paramListSubCodecs : list):
        self._numBytes = paramNumBytes
        self._DIDName = paramDIDName
        self._subTypes = paramListSubCodecs

    def encode(self, string_ascii:Any, paramRaw:bool=False) -> bytes:      
        if(paramRaw):
            _encodedBytes =  CodecRaw.encode(self, string_ascii) #just convert hex string to bytes
        else:
            try:
                _encodedBytes = bytes()
                for subType in self._subTypes:
                    _encodedBytes+=subType.encode(string_ascii[subType._DIDName])
            except KeyError as e:
                raise ValueError(f"Cannot encode value due to missing key: {e}")

        return _encodedBytes

    def decode(self, paramEncodedBytes: bytes, paramRaw:bool=False) -> Any:
        if(paramRaw): #just convert hex string to bytes
            return CodecRaw.decode(self, paramEncodedBytes)
        else:
            _result = dict()
            _index = 0
            for subType in self._subTypes:
                _result[subType._DIDName] = subType.decode(paramEncodedBytes[_index:_index+subType._numBytes])
                _index+=subType._numBytes
            return dict(_result)
    
    def getCodecInfo(self):
        argsSubTypes = []
        for subType in self._subTypes:
            argsSubTypes.append(subType.getCodecInfo())
        return ({"codec": self.__class__.__name__, "len": self._numBytes, "name": self._DIDName, "args": {"subTypes":argsSubTypes}})
    
    def getNumBytes(self) -> int:
        return self._numBytes