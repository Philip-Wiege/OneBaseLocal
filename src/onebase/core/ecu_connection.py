import udsoncan
from doipclient import DoIPClient
from doipclient.connectors import DoIPClientUDSConnector
from onebase.uds.uds_client import OneBaseUDSClient
from onebase.tools.open3e_converter import *
from udsoncan.exceptions import *
from udsoncan.services import *

from can.interface import Bus
from udsoncan.connections import PythonIsoTpConnection
from can.interfaces.socketcan import SocketcanBus
from can.interfaces.slcan import slcanBus
import isotp

import importlib
import binascii
import os
import sys
import time
import json

import onebase.core.codecs
from onebase.core.codecs import *

class ECUConnection():
    def __init__(self, paramTXAddress:int=0x680, paramRXAddress:int=None, paramConnectionType:str=None, paramConnectionInterface:str=None, paramFilepathDIDList:str=""):
        # calculate RX address
        self.tx = paramTXAddress
        if paramRXAddress == None:
            self.rx = paramTXAddress + 0x10
        else:
            self.rx = paramRXAddress

        # load DID definition file
        self.dataIdentifiers = convertDIDs()
        #self.dataIdentifiers = self._loadDIDFile(paramFilePath=paramFilepathDIDList)       

        # select backend
        if(paramConnectionType == "DoIP"): # DoIP
            conn = DoIPClientUDSConnector(DoIPClient(paramConnectionInterface, self.tx))

        elif (paramConnectionType == "SLCAN"): # SLCAN = CAN over Serial Interface
            # Refer to isotp documentation for full details about parameters
            isotp_params = {
                'stmin': 10,                            # Will request the sender to wait 10ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
                'blocksize': 0,                         # Request the sender to send 8 consecutives frames before sending a new flow control message
                'wftmax': 0,                            # Number of wait frame allowed before triggering an error
                'tx_data_length': 8,                    # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
                'tx_data_min_length': 8,                # Minimum length of CAN messages. When different from None, messages are padded to meet this length. Works with CAN 2.0 and CAN FD.
                'tx_padding': 0,                        # Will pad all transmitted CAN messages with byte 0x00.
                'rx_flowcontrol_timeout': 1000,         # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
                'rx_consecutive_frame_timeout': 1000,   # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
                'override_receiver_stmin': None,        # When sending, respect the stmin requirement of the receiver if set to None.
                'max_frame_size': 4095,                 # Limit the size of receive frame.
                'can_fd': False,                        # Does not set the can_fd flag on the output CAN messages
                'bitrate_switch': False,                # Does not set the bitrate_switch flag on the output CAN messages
                'rate_limit_enable': False,             # Disable the rate limiter
                'rate_limit_max_bitrate': 1000000,      # Ignored when rate_limit_enable=False. Sets the max bitrate when rate_limit_enable=True
                'rate_limit_window_size': 0.2,          # Ignored when rate_limit_enable=False. Sets the averaging window size for bitrate calculation when rate_limit_enable=True
                'listen_mode': False                    # Does not use the listen_mode which prevent transmission.
            }
            bus = slcanBus(channel=paramConnectionInterface, tty_baudrate=115200, bitrate=250000)
            tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=self.tx, rxid=self.rx) # Network layer addressing scheme
            stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)               # Network/Transport layer (IsoTP protocol)
            stack.set_sleep_timing(0.01, 0.01)                                                  # Balancing speed and load
            conn = PythonIsoTpConnection(stack)                                                 # interface between Application and Transport layer

        elif (paramConnectionType == "Telnet"): # Telnet = CAN over Remote Serial Interface (Telnet) RFC2217
            # Refer to isotp documentation for full details about parameters
            isotp_params = {
                'stmin': 10,                            # Will request the sender to wait 10ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
                'blocksize': 0,                         # Request the sender to send 8 consecutives frames before sending a new flow control message
                'wftmax': 0,                            # Number of wait frame allowed before triggering an error
                'tx_data_length': 8,                    # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
                'tx_data_min_length': 8,                # Minimum length of CAN messages. When different from None, messages are padded to meet this length. Works with CAN 2.0 and CAN FD.
                'tx_padding': 0,                        # Will pad all transmitted CAN messages with byte 0x00.
                'rx_flowcontrol_timeout': 1000,         # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
                'rx_consecutive_frame_timeout': 1000,   # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
                'override_receiver_stmin': None,        # When sending, respect the stmin requirement of the receiver if set to None.
                'max_frame_size': 4095,                 # Limit the size of receive frame.
                'can_fd': False,                        # Does not set the can_fd flag on the output CAN messages
                'bitrate_switch': False,                # Does not set the bitrate_switch flag on the output CAN messages
                'rate_limit_enable': False,             # Disable the rate limiter
                'rate_limit_max_bitrate': 1000000,      # Ignored when rate_limit_enable=False. Sets the max bitrate when rate_limit_enable=True
                'rate_limit_window_size': 0.2,          # Ignored when rate_limit_enable=False. Sets the averaging window size for bitrate calculation when rate_limit_enable=True
                'listen_mode': False                    # Does not use the listen_mode which prevent transmission.
            }
            bus = slcanBus(channel=paramConnectionInterface, tty_baudrate=115200, bitrate=250000)
            tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=self.tx, rxid=self.rx) # Network layer addressing scheme
            stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)               # Network/Transport layer (IsoTP protocol)
            stack.set_sleep_timing(0.01, 0.01)                                                  # Balancing speed and load
            conn = PythonIsoTpConnection(stack)                                                 # interface between Application and Transport layer

        elif (paramConnectionType == "SocketCAN"): # SocketCAN Interface on Linux Systems
            # Refer to isotp documentation for full details about parameters
            isotp_params = {
                'stmin': 10,                            # Will request the sender to wait 10ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
                'blocksize': 0,                         # Request the sender to send 8 consecutives frames before sending a new flow control message
                'wftmax': 0,                            # Number of wait frame allowed before triggering an error
                'tx_data_length': 8,                    # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
                'tx_data_min_length': 8,                # Minimum length of CAN messages. When different from None, messages are padded to meet this length. Works with CAN 2.0 and CAN FD.
                'tx_padding': 0,                        # Will pad all transmitted CAN messages with byte 0x00.
                'rx_flowcontrol_timeout': 1000,         # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
                'rx_consecutive_frame_timeout': 1000,   # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
                'override_receiver_stmin': None,        # When sending, respect the stmin requirement of the receiver if set to None.
                'max_frame_size': 4095,                 # Limit the size of receive frame.
                'can_fd': False,                        # Does not set the can_fd flag on the output CAN messages
                'bitrate_switch': False,                # Does not set the bitrate_switch flag on the output CAN messages
                'rate_limit_enable': False,             # Disable the rate limiter
                'rate_limit_max_bitrate': 1000000,      # Ignored when rate_limit_enable=False. Sets the max bitrate when rate_limit_enable=True
                'rate_limit_window_size': 0.2,          # Ignored when rate_limit_enable=False. Sets the averaging window size for bitrate calculation when rate_limit_enable=True
                'listen_mode': False                    # Does not use the listen_mode which prevent transmission.
            }
            bus = SocketcanBus(channel=paramConnectionInterface, bitrate=250000)                                     # Link Layer (CAN protocol)
            tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=self.tx, rxid=self.rx) # Network layer addressing scheme
            stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)               # Network/Transport layer (IsoTP protocol)
            stack.set_sleep_timing(0.01, 0.01)                                                  # Balancing speed and load
            conn = PythonIsoTpConnection(stack)
        
        else: # SocketCAN Interface on Linux Systems as default
            # Refer to isotp documentation for full details about parameters
            isotp_params = {
                'stmin': 10,                            # Will request the sender to wait 10ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
                'blocksize': 0,                         # Request the sender to send 8 consecutives frames before sending a new flow control message
                'wftmax': 0,                            # Number of wait frame allowed before triggering an error
                'tx_data_length': 8,                    # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
                'tx_data_min_length': 8,                # Minimum length of CAN messages. When different from None, messages are padded to meet this length. Works with CAN 2.0 and CAN FD.
                'tx_padding': 0,                        # Will pad all transmitted CAN messages with byte 0x00.
                'rx_flowcontrol_timeout': 1000,         # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
                'rx_consecutive_frame_timeout': 1000,   # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
                'override_receiver_stmin': None,        # When sending, respect the stmin requirement of the receiver if set to None.
                'max_frame_size': 4095,                 # Limit the size of receive frame.
                'can_fd': False,                        # Does not set the can_fd flag on the output CAN messages
                'bitrate_switch': False,                # Does not set the bitrate_switch flag on the output CAN messages
                'rate_limit_enable': False,             # Disable the rate limiter
                'rate_limit_max_bitrate': 1000000,      # Ignored when rate_limit_enable=False. Sets the max bitrate when rate_limit_enable=True
                'rate_limit_window_size': 0.2,          # Ignored when rate_limit_enable=False. Sets the averaging window size for bitrate calculation when rate_limit_enable=True
                'listen_mode': False                    # Does not use the listen_mode which prevent transmission.
            }
            bus = SocketcanBus(channel="can0", bitrate=250000)                                     # Link Layer (CAN protocol)
            tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=self.tx, rxid=self.rx) # Network layer addressing scheme
            stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)               # Network/Transport layer (IsoTP protocol)
            stack.set_sleep_timing(0.01, 0.01)                                                  # Balancing speed and load
            conn = PythonIsoTpConnection(stack)

        # configuration for udsoncan client
        config = dict(udsoncan.configs.default_client_config)
        config['data_identifiers'] = self.dataIdentifiers
        # increase default timeout
        config['request_timeout'] = 1 #seconds
        config['p2_timeout'] = 1 #seconds
        config['p2_star_timeout'] = 1 #seconds
        
        # run uds client
        self.uds_client = OneBaseUDSClient(conn, config=config)
        self.uds_client.open()

    def _loadDIDFile(self, paramFilePath:str):
        didDictionary = dict()

        if (paramFilePath  == "" or paramFilePath == None):
            return didDictionary
        else:
            with open(paramFilePath) as json_file:
                data = json.load(json_file)
  
            for did in data:
                print(data[did]["name"])
                
                codec = data[did]["codec"]
                name = data[did]["name"]
                numBytes = data[did]["numBytes"]
                
                if data[did]["codec"] == "CodecInt16":
                    print("CodecInt16 found")
                    scale = data[did]["args"]["scale"]
                    signed = data[did]["args"]["signed"]
                    offset = data[did]["args"]["offset"]

                    codecInstance = CodecInt16(paramNumBytes= numBytes, paramDIDName=name, paramSigned=signed, paramScale=scale, paramOffset=offset)
                    
                    didDictionary[int(did)] = codecInstance

            return didDictionary

    def _readByDid(self, did:int, raw:bool=False, paramVerbose:bool=False):
        if(did in self.dataIdentifiers):
            if paramVerbose:
                print("DID not in DID Dictionary")
            response = self.uds_client.read_data_by_identifier([did])
            return response.service_data.values[did]
        else:
            request = udsoncan.Request(service=udsoncan.services.ReadDataByIdentifier,data=(did).to_bytes(2, byteorder='big'))
            response = self.uds_client.send_request(request)

            if(response.positive):
                return binascii.hexlify(response.data[2:]).decode('utf-8')
            else:
                return f"negative response, {response.code}:{response.invalid_reason}"
    
    def _writeByDid(self, did:int, val, raw:bool, useService77=False, paramVerbose:bool=False):
        response = self.uds_client.write_data_by_identifier(did, val, useService77)
        succ = (response.valid & response.positive)
        return succ, response.code
    
    def readDataByIdentifier(self, paramDid:int, paramSubDid:int=-1, paramRaw:bool=False, paramVerbose:bool=False):

        if(paramDid in self.dataIdentifiers): #DID is in DID list so decoding is known
            selectedDid = self.dataIdentifiers[paramDid]

            if type(selectedDid) == onebase.core.codecs.CodecComplexType:# DID is complex

                numSubDids = len(selectedDid.subTypes)

                if paramSubDid == -1: #no sub-DID defined means read whole DID
                    return self._readByDid(paramDid,paramRaw, paramVerbose)
                
                elif paramSubDid >= 0 and paramSubDid < numSubDids: #sub-DID index is valid which means read only sub-DID
                    selectedSubDid = selectedDid.subTypes[paramSubDid]
                    nameSelectedSubDid = selectedSubDid.id

                    out1 = self._readByDid(paramDid,paramRaw, paramVerbose)

                    if paramRaw: #if raw reading is activated the result is a hex string
                        lenSubDid = selectedSubDid.string_len
                        hexSubStringStartIndex = 0
                        hexSubStringEndIndex = hexSubStringStartIndex + lenSubDid*2

                        for indexSubDid in range(numSubDids):
                            if (indexSubDid == paramSubDid):
                                break
                            else:
                                lenCurrentSubDid = selectedDid.subTypes[indexSubDid].string_len
                                hexSubStringStartIndex += lenCurrentSubDid*2
                                hexSubStringEndIndex += lenCurrentSubDid*2

                        hexSubString = out1[hexSubStringStartIndex:hexSubStringEndIndex]

                        return hexSubString, nameSelectedSubDid
                    else:
                        return out1[nameSelectedSubDid], nameSelectedSubDid
                    
                else: #sub-DID index undefined
                    raise NotImplementedError("Sub-DID Index " + str(paramSubDid) + "is not defined.")
            else: # DID is not complex
                return self._readByDid(paramDid,paramRaw, paramVerbose)
        else: #DID is not in DID list
            return self._readByDid(paramDid,paramRaw, paramVerbose)

    def writeDataByIdentifier(self, paramDid:int, paramValue:any, paramSubDid:int=-1, paramRaw:bool=False, paramCheckAfterWrite:bool=False, paramService77:bool=False, paramSimulateOnly=False, paramVerbose:bool=False):
        if(paramDid in self.dataIdentifiers): #DID is in DID list so decoding is known
            selectedDid = self.dataIdentifiers[paramDid]
            if (type(selectedDid) == onebase.core.codecs.CodecComplexType): #DID is complex
                # Step 1: Read raw data of complete complex DID as string
                numSubDids = len(selectedDid.subTypes)
                rawDidDataString = self.readDataByIdentifier(paramDid=paramDid, paramVerbose=paramVerbose, paramRaw=True)

                # Step 2: Find sub-DID bytes that need to be modified in DID
                bytesProcessed = 0
                bytesSubDid = ""
                
                for indexSubDid in range(0, numSubDids):
                    selectedSubDid = selectedDid.subTypes[indexSubDid]
                    lenSubDid = selectedSubDid.string_len
                    startIndexSubDid = bytesProcessed
                    endIndexSubDid = startIndexSubDid + lenSubDid-1
   
                    if indexSubDid == paramSubDid:
                        matchingSubDid = selectedSubDid
                        if paramVerbose:
                            print("DID: " + str(paramDid))
                            print("DID Name: " + str(selectedDid.id))
                            print("Raw DID Data: " + str(rawDidDataString))
                            print("DID " + str(paramDid) + " consists of " + str(numSubDids) + " Sub-DIDs.")
                            print("Sub DID: " + str(indexSubDid))
                            print("Sub DID Name: " + selectedSubDid.id)
                            print("Start Byte: " + str(startIndexSubDid))
                            print("End Byte: " + str(endIndexSubDid))

                        startStringIndexSubDid = (2*startIndexSubDid)
                        endStringIndexSubDid = ((endIndexSubDid+1)*2)
                        
                        bytesSubDid = rawDidDataString[startStringIndexSubDid:endStringIndexSubDid]
                              
                    bytesProcessed += lenSubDid

                # Step 3: Modify bytes in raw complete DID data
                encodedData = matchingSubDid.encode(paramValue)
                encodedDataHexString = encodedData.hex()
                
                if len(bytesSubDid) == len(encodedDataHexString):
                    if (paramSubDid == numSubDids-1): #if is last sub DID
                        rawDidDataNew = rawDidDataString[:startStringIndexSubDid] + encodedDataHexString
                    elif(paramSubDid == 0): # if is first sub DID
                        rawDidDataNew = encodedDataHexString + rawDidDataString[endStringIndexSubDid:]
                    else:
                        rawDidDataNew = rawDidDataString[0:startStringIndexSubDid] + encodedDataHexString + rawDidDataString[endStringIndexSubDid:]
                    
                    if paramVerbose:
                        print("New Raw Sub DID Data: " + encodedDataHexString)
                        print("New Raw DID Data: " + rawDidDataNew)

                    if not paramSimulateOnly:
                        self._writeByDid(paramDid,rawDidDataNew,True,paramService77)

                else:
                    raise NotImplementedError("Encoded Sub-DID length does not match the length in complex DID")   

            else: #DID is not complex
                self._writeByDid(paramDid, paramValue, paramRaw, paramService77)
        else: #DID is not in DID list so decoding is unknown. Force raw writing
            raise NotImplementedError("Writing to unknown DIDs is currently not supported.")
            
    def close(self):
        self.uds_client.close()