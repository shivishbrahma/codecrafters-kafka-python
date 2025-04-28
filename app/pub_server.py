import struct
from .pub_kafka import ErrorCode

def handle_request(request_buffer: bytes):
    res = bytes()
    request_message_size = struct.unpack_from(">I",buffer=request_buffer[:4])[0]
    request_api_key = struct.unpack_from(">H",buffer=request_buffer[4:6])[0]
    request_api_version = struct.unpack_from(">H",buffer=request_buffer[6:8])[0]
    correlation_id = struct.unpack_from(">I",buffer=request_buffer[8:12])[0]
    
    message_size = len(correlation_id.to_bytes(4, byteorder="big"))
    error_code = ErrorCode.NONE
    if request_api_version >= 3:
        error_code = ErrorCode.UNSUPPORTED_VERSION

    print("\nRequest: \n======")
    print(f"request_message_size: {request_message_size}")
    print(f"request_api_key: {request_api_key}")
    print(f"request_api_version: {request_api_version}")

    print("\nResponse: \n======")
    print(f"message_size: {message_size}")
    print(f"correlation_id: {correlation_id}")
    print(f"error_code: {error_code}")

    res += message_size.to_bytes(4, byteorder="big")
    res += correlation_id.to_bytes(4, byteorder="big")
    if error_code.value > ErrorCode.NONE.value:
        res += error_code.to_bytes()
    return res