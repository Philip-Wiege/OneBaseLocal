import onebase as ob
import onebase.core as co
import onebase.uds as uds

from onebase.core.codecs import *


InstanceCodecInt8 = CodecInt8(1, paramDIDName="CompressorSpeedPercent")  #DID 2346
InstanceCodecInt16 = CodecInt16(paramNumBytes=2, paramDIDName="DomesticHotWaterTemperatureSetpoint", paramSigned=True, paramScale=1.0) #DID 396
InstanceCodecInt32 = CodecInt32(paramNumBytes=4, paramDIDName="CurrentElectricalPowerConsumptionSystem", paramSigned=False, paramScale=1) #DID 2488
InstanceCodecByte = CodecByte(1, paramDIDName="CentralHeatingPumpType") #DID 2498
InstanceCodecUTF8 = CodecUTF8(paramNumBytes=40, paramDIDName="CentralHeatingOneCircuitName") #DID 627
InstanceCodecComplexType = CodecComplexType(paramNumBytes=2, paramDIDName="LegionellaProtectionActivation", paramListSubCodecs=[CodecByte(paramNumBytes=1, paramDIDName="Mode"),CodecByte(paramNumBytes=1, paramDIDName="State")]) #DID 873