import struct
from .pub_kafka import (
    KafkaErrorCode,
    KafkaAPIKey,
    KafkaException,
    KafkaAPIRequest,
    KafkaAPIString,
    KafkaAPIRequestBody,
)
from typing import Tuple


def parse_request(request_buffer: bytes) -> Tuple[KafkaAPIRequest, KafkaErrorCode]:
    # > : big-endian
    # B : 1 byte unsigned byte
    # H : 2 bytes unsigned short
    # I : 4 bytes unsigned int
    error_code = KafkaErrorCode.NONE
    try:
        message_size = struct.unpack_from(">I", buffer=request_buffer[:4])[0]
        api_key = struct.unpack_from(">H", buffer=request_buffer[4:6])[0]
        api_version = struct.unpack_from(">H", buffer=request_buffer[6:8])[0]
        correlation_id = struct.unpack_from(">I", buffer=request_buffer[8:12])[0]

        index = 12
        length = struct.unpack_from(">H", buffer=request_buffer[index : index + 2])[0]
        index += 2
        contents = request_buffer[index : index + length].decode()
        index += length + 1
        print("index:", index)

        request_api = KafkaAPIKey.from_code(api_key)
        client = KafkaAPIString(length=length, contents=contents)

        # Request Object
        request = KafkaAPIRequest(
            message_size=message_size,
            api_key=request_api,
            # api_version=api_version,
            correlation_id=correlation_id,
            client_id=client,
            body=KafkaAPIRequestBody(),
        )

        if request_api is None:
            raise KafkaException(
                error_code=KafkaErrorCode.UNSUPPORTED_VERSION,
                message="API Key is not supported",
            )

        # API Version Validation
        if not (
            request_api.get_min_version()
            <= api_version
            <= request_api.get_max_version()
        ):
            raise KafkaException(
                error_code=KafkaErrorCode.UNSUPPORTED_VERSION,
                message="API Version is not supported",
            )

        if request_api == KafkaAPIKey.ApiVersions:
            length = struct.unpack_from(">B", buffer=request_buffer[index : index + 1])[
                0
            ]
            index += 1
            contents = request_buffer[index : index + length].decode()
            request.body.client_id = KafkaAPIString(
                length=length,
                contents=contents,
            )
            index += length

            length = struct.unpack_from(">B", buffer=request_buffer[index : index + 1])[
                0
            ]
            index += 1
            contents = request_buffer[index : index + length].decode()
            request.body.client_software_version = KafkaAPIString(
                length=length,
                contents=contents,
            )

        if request_api == KafkaAPIKey.DescribeTopicPartitions:
            num_of_topics = (
                struct.unpack_from(">B", buffer=request_buffer[index : index + 1])[0]
                - 1
            )
            index += 1

            for _ in range(num_of_topics):
                topic_name_length = (
                    struct.unpack_from(">B", buffer=request_buffer[index : index + 1])[
                        0
                    ]
                    - 1
                )
                index += 1

                topic_name = request_buffer[index : index + topic_name_length].decode()
                index += topic_name_length + 1
                request.body.topics.append(
                    KafkaAPIString(length=topic_name_length, contents=topic_name)
                )

            request.body.response_partition_limit = struct.unpack_from(
                ">I", buffer=request_buffer[index : index + 4]
            )[0]
            index += 4
            request.body.cursor = request_buffer[index : index + 1]

    except KafkaException as e:
        print(e)
        error_code = e.error_code

    return (request, error_code)


def handle_request(request_buffer: bytes):
    tag_buffer = b"\x00"
    throttle_time_ms = 0

    request, error_code = parse_request(request_buffer)

    res = struct.pack(">I", request.correlation_id)  # 4

    if request.api_key == KafkaAPIKey.ApiVersions:
        res += struct.pack(">H", error_code.value)
        api_keys = [api_key.value for api_key in KafkaAPIKey]
        res += struct.pack(">B", len(api_keys) + 1)

        for api_key in api_keys:
            res += struct.pack(
                ">HHH", api_key.api_key, api_key.min_version, api_key.max_version
            )
            res += tag_buffer
        res += struct.pack(">I", throttle_time_ms)
        res += tag_buffer

    if request.api_key == KafkaAPIKey.DescribeTopicPartitions:
        res += tag_buffer
        res += struct.pack(">I", throttle_time_ms)

        error_code = KafkaErrorCode.UNKNOWN_TOPIC_OR_PARTITION
        res += struct.pack(">B", len(request.body.topics) + 1)  # array_length + 1
        for topic in request.body.topics:
            topic_name = topic.contents.encode()
            topic_name_length = len(topic_name) + 1
            topic_id = 0
            is_internal = 0
            partition_array = b"\x01"
            topic_authorized_operations = b"\x00\x00\x0d\xf8"
            next_cursor = request.body.cursor

            res += error_code.to_bytes(2)
            res += struct.pack(">B", topic_name_length)
            res += topic_name
            res += topic_id.to_bytes(16)
            res += struct.pack(">B", is_internal)
            res += partition_array
            res += topic_authorized_operations
            res += tag_buffer

        res += next_cursor
        res += tag_buffer

    message_size = len(res)
    res = message_size.to_bytes(4) + res

    print("\nRequest: ", request)

    return res
