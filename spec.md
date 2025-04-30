# Kafka API Specification

## APIVersions - Key: 18

### Request v4

```json
{
    "message_size": [4, "0:4"],
    "request_header": {
        "api_key": [2, "4:6"],
        "api_version": [2, "6:8"],
        "correlation_id": [4, "8:12"],
        "client_id": {
            "length": [2, "12:14"],
            "contents": [9, "14:23"]
        },
        "tag_buffer": [1, "23:24"]
    },
    "request_body": {
        "client_id": {
            "length": [1, "24:25"],
            "contents": [9, "25:34"]
        },
        "client_software_version": {
            "length": [1, "34:35"],
            "contents": [3, "35:38"]
        },
        "tag_buffer": [1, "38:39"]
    }
}
```

### Response v4

```json
{
    "message": [4, "0:4"],
    "response_header": {
        "correlation_id": [4, "4:8"]
    },
    "response_body": {
        "error_code": [2, "8:10"],
        "api_versions_array": {
            "array_length": [1, "10:11"],
            "api#1": {
                "api_key": [2],
                "min_api_version": [2],
                "max_api_version": [2],
                "tag_buffer": [1]
            },
            "api#2": {
                "api_key": [2],
                "min_api_version": [2],
                "max_api_version": [2],
                "tag_buffer": [1]
            },
            "api#3": {
                "api_key": [2],
                "min_api_version": [2],
                "max_api_version": [2],
                "tag_buffer": [1]
            }
        },
        "throttle_time": [4],
        "tag_buffer": [1]
    }
}
```

## DescribeTopicPartitions - Key: 75

### Request v0

```json
{
    "message_size": [4, "0:4"],
    "request_header": {
        "api_key": [2, "4:6"],
        "api_version": [2, "6:8"],
        "correlation_id": [4, "8:12"],
        "client_id": {
            "length": [2, "12:14"],
            "contents": [9, "14:23"]
        },
        "tag_buffer": [1, "23:24"]
    },
    "request_body": {
        "topics_array": {
            "array_length": [1, "24:25"],
            "topic": {
                "topic_name_length": [1, "25:26"],
                "topic_name": [3, "26:29"],
                "topic_tag_buffer": [1, "29:30"]
            }
        },
        "response_partition_limit": [4, "30:34"],
        "cursor": [1, "34:35"],
        "tag_buffer": [1, "35:36"]
    }
}
```

### Response v0

```json
{
    "message_size": [4],
    "response_header": {
        "correlation_id": [4],
        "tag_buffer": [1]
    },
    "response_body": {
        "throttle_time": [4],
        "topics_array": {
            "array_length": [1],
            "topic#1": {
                "error_code": [2],
                "topic_name": {
                    "length": [1],
                    "content": [3]
                },
                "topic_id": [16],
                "is_internal": [1],
                "partitions_array": {
                    "array_length": [1],
                    "partition#0": {
                        "error_code": [2],
                        "partition_index": [4],
                        "leader_id": [4],
                        "leader_epoch": [4],
                        "replica_nodes": {
                            "array_length": [1],
                            "replica_node": [4]
                        },
                        "isr_nodes": {
                            "array_length": [1],
                            "isr_node": [4]
                        },
                        "eligible_leader_replicas": {
                            "array_length": [1]
                        },
                        "last_known_elr": {
                            "array_length": [1]
                        },
                        "offline_replicas": {
                            "array_length": [1]
                        },
                        "tag_buffer": [1]
                    },
                    "partition#1": {
                        "error_code": [2],
                        "partition_index": [4],
                        "leader_id": [4],
                        "leader_epoch": [4],
                        "replica_nodes": {
                            "array_length": [1],
                            "replica_node": [4]
                        },
                        "isr_nodes": {
                            "array_length": [1],
                            "isr_node": [4]
                        },
                        "eligible_leader_replicas": {
                            "array_length": [1]
                        },
                        "last_known_elr": {
                            "array_length": [1]
                        },
                        "offline_replicas": {
                            "array_length": [1]
                        },
                        "tag_buffer": [1]
                    }
                },
                "topic_authorized_operations": [4],
                "tag_buffer": [1]
            }
        },
        "next_cursor": [1],
        "tag_buffer": [1]
    }
}
```

### Response v0 - Unknown Topic

```json
{
    "message_size": [4],
    "response_header": {
        "correlation_id": [4],
        "tag_buffer": [1]
    },
    "response_body": {
        "throttle_time": [4],
        "topics_array": {
            "array_length": [1],
            "topic#1": {
                "error_code": [2],
                "topic_name": {
                    "length": [1],
                    "content": [3]
                },
                "topic_id": [16],
                "is_internal": [1],
                "partitions_array": {
                    "array_length": [1]
                },
                "topic_authorized_operations": [4],
                "tag_buffer": [1]
            },
        },
        "next_cursor": [1],
        "tag_buffer": [1]
    }
}
```