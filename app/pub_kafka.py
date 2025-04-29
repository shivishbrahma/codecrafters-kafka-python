from enum import Enum
from dataclasses import dataclass


@dataclass
class KafkaAPIKeyDetails:
    api_key: int
    min_version: int
    max_version: int


class KafkaAPIKey(Enum):
    # Produce = 0
    # Fetch = 1
    # ListOffsets = 2
    # Metadata = 3
    # OffsetCommit = 8
    # OffsetFetch = 9
    # FindCoordinator = 10
    # JoinGroup = 11
    # Heartbeat = 12
    # LeaveGroup = 13
    # SyncGroup = 14
    # DescribeGroups = 15
    # ListGroups = 16
    # SaslHandshake = 17
    ApiVersions = KafkaAPIKeyDetails(api_key=18, min_version=0, max_version=4)
    # CreateTopics = 19
    # DeleteTopics = 20
    # DeleteRecords = 21
    # InitProducerId = 22
    # OffsetForLeaderEpoch = 23
    # AddPartitionsToTxn = 24
    # AddOffsetsToTxn = 25
    # EndTxn = 26
    # WriteTxnMarkers = 27
    # TxnOffsetCommit = 28
    # DescribeAcls = 29
    # CreateAcls = 30
    # DeleteAcls = 31
    # DescribeConfigs = 32
    # AlterConfigs = 33
    # AlterReplicaLogDirs = 34
    # DescribeLogDirs = 35
    # SaslAuthenticate = 36
    # CreatePartitions = 37
    # CreateDelegationToken = 38
    # RenewDelegationToken = 39
    # ExpireDelegationToken = 40
    # DescribeDelegationToken = 41
    # DeleteGroups = 42
    # ElectLeader = 43
    # IncrementalAlterConfigs = 44
    # AlterPartitionReassignments = 45
    # ListPartitionReassignments = 46
    # OffsetDelete = 47
    # DescribeClientQuotas = 48
    # AlterClientQuotas = 49
    # DescribeUserScramCredentials = 50
    # AlterUserScramCredentials = 51
    # DescribeQuorum = 55
    # UpdateFeatures = 57
    # DescribeCluster = 60
    # DescribeProducers = 61
    # UnregisterBroker = 64
    # DescribeTransactions = 65
    # ListTransactions = 66
    # ConsumerGroupHeartbeat = 68
    # ConsumerGroupDescribe = 69
    # GetTelemetrySubscriptions = 71
    # PushTelemetry = 72
    # ListClientMetricsResources = 74
    # DescribeTopicPartitions = 75
    DescribeTopicPartitions = KafkaAPIKeyDetails(
        api_key=75, min_version=0, max_version=0
    )
    # AddRaftVoter = 80
    # RemoveRaftVoter = 81

    def get_min_version(self):
        return self.value.min_version

    def get_max_version(self):
        return self.value.max_version

    @staticmethod
    def from_code(code: int):
        for key in KafkaAPIKey:
            if key.value.api_key == code:
                return key
        raise KafkaException(
            error_code=KafkaErrorCode.UNSUPPORTED_VERSION,
            message="API Key is not supported",
        )

    def __str__(self):
        return f"{self.name}({self.value.api_key})"


class KafkaErrorCode(Enum):
    UNKNOWN_SERVER_ERROR = -1
    NONE = 0
    OFFSET_OUT_OF_RANGE = 1
    CORRUPT_MESSAGE = 2
    UNKNOWN_TOPIC_OR_PARTITION = 3
    INVALID_FETCH_SIZE = 4
    LEADER_NOT_AVAILABLE = 5
    NOT_LEADER_OR_FOLLOWER = 6
    REQUEST_TIMED_OUT = 7
    BROKER_NOT_AVAILABLE = 8
    REPLICA_NOT_AVAILABLE = 9
    MESSAGE_TOO_LARGE = 10
    STALE_CONTROLLER_EPOCH = 11
    OFFSET_METADATA_TOO_LARGE = 12
    NETWORK_EXCEPTION = 13
    COORDINATOR_LOAD_IN_PROGRESS = 14
    COORDINATOR_NOT_AVAILABLE = 15
    NOT_COORDINATOR = 16
    INVALID_TOPIC_EXCEPTION = 17
    RECORD_LIST_TOO_LARGE = 18
    NOT_ENOUGH_REPLICAS = 19
    NOT_ENOUGH_REPLICAS_AFTER_APPEND = 20
    INVALID_REQUIRED_ACKS = 21
    ILLEGAL_GENERATION = 22
    INCONSISTENT_GROUP_PROTOCOL = 23
    INVALID_GROUP_ID = 24
    UNKNOWN_MEMBER_ID = 25
    INVALID_SESSION_TIMEOUT = 26
    REBALANCE_IN_PROGRESS = 27
    INVALID_COMMIT_OFFSET_SIZE = 28
    TOPIC_AUTHORIZATION_FAILED = 29
    GROUP_AUTHORIZATION_FAILED = 30
    CLUSTER_AUTHORIZATION_FAILED = 31
    INVALID_TIMESTAMP = 32
    UNSUPPORTED_SASL_MECHANISM = 33
    ILLEGAL_SASL_STATE = 34
    UNSUPPORTED_VERSION = 35
    TOPIC_ALREADY_EXISTS = 36
    INVALID_PARTITIONS = 37
    INVALID_REPLICATION_FACTOR = 38
    INVALID_REPLICA_ASSIGNMENTS = 39
    INVALID_CONFIG = 40
    NOT_CONTROLLER = 41
    INVALID_REQUEST = 42
    UNSUPPORTED_FOR_MESSAGE_FORMAT = 43
    POLICY_VIOLATION = 44
    OUT_OF_ORDER_SEQUENCE_NUMBER = 45
    DUPLICATE_SEQUENCE_NUMBER = 46
    INVALID_PRODUCER_EPOCH = 47
    INVALID_TXN_STATE = 48
    INVALID_PRODUCER_ID_MAPPING = 49
    INVALID_TRANSACTION_TIMEOUT = 50
    CONCURRENT_TRANSACTIONS = 51
    TRANSACTION_COORDINATOR_FENCED = 52
    TRANSACTIONAL_ID_AUTHORIZATION_FAILED = 53
    SECURITY_DISABLED = 54
    OPERATION_NOT_ATTEMPTED = 55
    KAFKA_STORAGE_ERROR = 56
    LOG_DIR_NOT_FOUND = 57
    SASL_AUTHENTICATION_FAILED = 58
    UNKNOWN_PRODUCER_ID = 59
    REASSIGNMENT_IN_PROGRESS = 60

    def to_bytes(self, length):
        return self.value.to_bytes(length)

    def __str__(self):
        return f"[{self.name}-{self.value}]"


class KafkaException(Exception):
    def __init__(self, error_code: KafkaErrorCode, message: str, *args):
        self.error_code = error_code
        self.message = message
        super().__init__(f"{str(error_code)}: {message}", *args)
