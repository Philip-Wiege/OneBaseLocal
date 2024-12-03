import onebase as ob
import onebase.core as co
import onebase.core.codecs as cd
import onebase.uds as uds

InstanceCodecInt16 = cd.CodecInt16(paramNumBytes=2, paramDIDName="DomesticHotWaterTemperatureSetpoint", paramSigned=True, paramScale=1.0)
InstanceCodecInt32 = cd.CodecInt32(paramNumBytes=4, paramDIDName="TotalElectricalEnergy", paramSigned=False, paramScale=10)
InstanceCodecUTF8 = cd.CodecUTF8(paramNumBytes=40, paramDIDName="CentralHeatingOneCircuitName")