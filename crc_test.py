from libraries.crc_utils import CRCUtils

# Client
data = "z"
encoded = CRCUtils.encode_data(data.encode())
with open("./encoded_data", "wb") as f:
    f.write(encoded)
print("DATA SENDED:", encoded)

# Server
data, crc = CRCUtils.get_data(encoded)
print("CRC ONLY:", crc)
print("DATA RECEIVED:", data)
print("The data is intact:", CRCUtils.check_integrity(data, crc))

# int_res = CRCUtils.int_to_bytes(55)
# int_struct_res = CRCUtils.int_struct_to_bytes(55)
# print(int_res,"==", int_struct_res, int_res == int_struct_res)
# float_bytes = CRCUtils.float_to_bytes(1.5)
# print(float_bytes, len(float_bytes))
# print(CRCUtils.float_from_bytes(float_bytes))

TOTAL_SIZE = 2


def _get_measurements(data_bytes: str):
    begin = 0
    end = 0
    while True:
        begin = end
        end = begin + TOTAL_SIZE
        measurement = data_bytes[begin:end]
        if not measurement:
            break
        yield measurement


print(list(enumerate(_get_measurements("12345"))))


print(CRCUtils.int_from_bytes(b"z\xdf\xdd"))
