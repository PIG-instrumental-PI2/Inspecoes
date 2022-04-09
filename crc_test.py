from libraries.crc_utils import CRCUtils

CRC_SIZE = 32

# Client
data = "z12334"
encoded = CRCUtils.encode_data(data.encode())
with open("./encoded_data", "wb") as f:
    f.write(encoded)
print("DATA SENDED:", encoded)

# Server
data, crc = CRCUtils.get_data(encoded)
print("CRC ONLY:", crc)
print("DATA RECEIVED:", data)
print("The data is intact:", CRCUtils.check_integrity(data, crc))
