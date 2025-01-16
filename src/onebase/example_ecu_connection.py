from onebase.core.ecu_connection import ECUConnection

InstanceECUConnection680 = ECUConnection(paramTXAddress=0x680, paramRXAddress=0x690, paramConnectionType="DoIP", paramConnectionInterface="192.168.0.1", paramFilepathDIDList="BV_OneBase_DIDs.json")

InstanceECUConnection680 = ECUConnection(paramTXAddress=0x680, paramRXAddress=0x690, paramConnectionType="SLCAN", paramConnectionInterface="COM3", paramFilepathDIDList="BV_OneBase_DIDs.json")

InstanceECUConnection680 = ECUConnection(paramTXAddress=0x680, paramRXAddress=0x690, paramConnectionType="SocketCAN", paramConnectionInterface="can0", paramFilepathDIDList="BV_OneBase_DIDs.json")