import onebase as ob
import onebase.core as co
import onebase.uds as uds

from onebase.core.codecs import CodecInt8, CodecInt16, CodecInt32, CodecByte
from onebase.core.codecs import CodecBool, CodecUTF8, CodecHardwareSoftwareVersion
from onebase.core.codecs import CodecMACAddress, CodecIPAddress, CodecSDate
from onebase.core.codecs import CodecSTime, CodecUTC, CodecComplexType
from onebase.core.codecs import CodecEnumeration


InstanceCodecInt8 = CodecInt8(1, paramDIDName="CompressorSpeedPercent")  #DID 2346
InstanceCodecInt16 = CodecInt16(paramNumBytes=2, paramDIDName="DomesticHotWaterTemperatureSetpoint", paramSigned=True, paramScale=1.0) #DID 396
InstanceCodecInt32 = CodecInt32(paramNumBytes=4, paramDIDName="CurrentElectricalPowerConsumptionSystem", paramSigned=False, paramScale=1) #DID 2488
InstanceCodecByte = CodecByte(1, paramDIDName="CentralHeatingPumpType") #DID 2498
InstanceCodecBool = CodecBool(1, paramDIDName="PrimaryHeatExchangerBaseHeater") #DID 354
InstanceCodecUTF8 = CodecUTF8(paramNumBytes=40, paramDIDName="CentralHeatingOneCircuitName") #DID 627
InstanceCodecHardwareSoftwareVersion = CodecHardwareSoftwareVersion(paramNumBytes=8, paramDIDName="SoftwareVersion") #DID580
InstanceCodecMACAddress = CodecMACAddress(paramNumBytes=6, paramDIDName="GatewayMac") #DID593
InstanceCodecIPAddress = CodecIPAddress(paramNumBytes=4, paramDIDName="WLAN_IP-Address") #DID607.0
InstanceCodecSDate = CodecSDate(paramNumBytes=3, paramDIDName="Date") #DID505
InstanceCodecSTime = CodecSTime(paramNumBytes=3, paramDIDName="Time") #DID506
InstanceCodecUTC = CodecUTC(paramNumBytes=4, paramDIDName="UniversalTimeCoordinated") #DID507
InstanceCodecEnumeration = CodecEnumeration(paramNumBytes=1, paramDIDName="CentralHeatingRegulationMode", paramEnumName="RegulationTypes") #DID1004
InstanceCodecComplexType = CodecComplexType(paramNumBytes=2, paramDIDName="LegionellaProtectionActivation", paramListSubCodecs=[CodecByte(paramNumBytes=1, paramDIDName="Mode"),CodecByte(paramNumBytes=1, paramDIDName="State")]) #DID 873