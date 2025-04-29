import struct
from .pub_kafka import KafkaErrorCode, KafkaAPIKey, KafkaException


# > : big-endian
# B : 1 byte unsigned byte
# H : 2 bytes unsigned short
# I : 4 bytes unsigned int
def handle_request(request_buffer: bytes):
    tag_buffer = b"\x00"
    throttle_time_ms = 0
    error_code = KafkaErrorCode.NONE
    try:
        request_message_size = struct.unpack_from(">I", buffer=request_buffer[:4])[0]
        request_api_key = struct.unpack_from(">H", buffer=request_buffer[4:6])[0]
        request_api_version = struct.unpack_from(">H", buffer=request_buffer[6:8])[0]
        correlation_id = struct.unpack_from(">I", buffer=request_buffer[8:12])[0]

        request_api = KafkaAPIKey.from_code(request_api_key)

        # API Version Validation
        if not (
            request_api.get_min_version()
            <= request_api_version
            <= request_api.get_max_version()
        ):
            raise KafkaException(
                error_code=KafkaErrorCode.UNSUPPORTED_VERSION,
                message="API Version is not supported",
            )

    except KafkaException as e:
        print(e)
        error_code = e.error_code

    res = struct.pack(">I", correlation_id)
    res += struct.pack(">H", error_code.value)

    if request_api == KafkaAPIKey.ApiVersions:
        api_keys = [api_key.value for api_key in KafkaAPIKey]

        res += struct.pack(">B", len(api_keys) + 1)

        for api_key in api_keys:
            res += struct.pack(
                ">HHH", api_key.api_key, api_key.min_version, api_key.max_version
            )
            res += tag_buffer
        res += struct.pack(">I", throttle_time_ms)
        res += tag_buffer

    if request_api == KafkaAPIKey.DescribeTopicPartitions:
        pass

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
