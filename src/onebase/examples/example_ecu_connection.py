from onebase.core.ecu_connection import ECUConnection

# DoIP: Linux, Windows, MacOS
InstanceECUConnection680 = ECUConnection(paramTXAddress=0x680, paramRXAddress=0x690, paramConnectionType="DoIP", paramConnectionInterface="192.168.0.1", paramFilepathDIDList="../did_definitions/BV_OneBase_DIDs.json")

# SLCAN: Windows
InstanceECUConnection680 = ECUConnection(paramTXAddress=0x680, paramRXAddress=0x690, paramConnectionType="SLCAN", paramConnectionInterface="COM3", paramFilepathDIDList="../did_definitions/BV_OneBase_DIDs.json")

# SLCAN: MacOS
InstanceECUConnection680 = ECUConnection(paramTXAddress=0x680, paramRXAddress=0x690, paramConnectionType="SLCAN", paramConnectionInterface="/dev/tty.usbmodem2085309C53301", paramFilepathDIDList="../did_definitions/BV_OneBase_DIDs.json")

# SLCAN Remote Telnet: Linux, Windows, MacOS
InstanceECUConnection680 = ECUConnection(paramTXAddress=0x680, paramRXAddress=0x690, paramConnectionType="Telnet", paramConnectionInterface="rfc2217://10.0.1.137:5000", paramFilepathDIDList="../did_definitions/BV_OneBase_DIDs.json")

# SocketCAN: Linux
InstanceECUConnection680 = ECUConnection(paramTXAddress=0x680, paramRXAddress=0x690, paramConnectionType="SocketCAN", paramConnectionInterface="can0", paramFilepathDIDList="../did_definitions/BV_OneBase_DIDs.json")