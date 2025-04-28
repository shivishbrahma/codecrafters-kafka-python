import struct
from .pub_kafka import ErrorCode, MIN_VERSION, MAX_VERSION, APIKey

def handle_request(request_buffer: bytes):
    res = bytes()
    request_message_size = struct.unpack_from(">I",buffer=request_buffer[:4])[0]
    request_api_key = struct.unpack_from(">H",buffer=request_buffer[4:6])[0]
    request_api_version = struct.unpack_from(">H",buffer=request_buffer[6:8])[0]
    request_api = APIKey(request_api_key)
    correlation_id = struct.unpack_from(">I",buffer=request_buffer[8:12])[0]

    request_min_v = request_api.get_min_version()
    request_max_v = request_api.get_max_version()
    tag_buffer = 0
    throttle_time_ms = 0
    num_api_keys = 2
    error_code = ErrorCode.NONE

    # API Version Validation
    if request_api_version >= request_min_v and request_api_version <= request_max_v:
        print("API Version is supported")
    else:
        print("API Version is not supported")
        error_code = ErrorCode.UNSUPPORTED_VERSION

    res += correlation_id.to_bytes(4)
    res += error_code.to_bytes()

    if request_api == APIKey.ApiVersions:
        res += num_api_keys.to_bytes(1)
        res += request_api_key.to_bytes(2)
        res += request_min_v.to_bytes(2)
        res += request_max_v.to_bytes(2)
    
    res += tag_buffer.to_bytes(1)
    res += throttle_time_ms.to_bytes(4)
    res += tag_buffer.to_bytes(1)
    
    message_size = len(res)
    res = message_size.to_bytes(4) + res

    print("\nRequest: \n======")
    print(f"request_message_size: {request_message_size}")
    print(f"request_api_key: {request_api_key}")
    print(f"request_api_version: {request_api_version}")
    print(f"request_api: {request_api}")

    print("\nResponse: \n======")
    print(f"message_size: {message_size}")
    print(f"correlation_id: {correlation_id}")
    print(f"error_code: {error_code}")
    return res