from pyflink.common import WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaSource

env = StreamExecutionEnvironment.get_execution_environment()

# Configure Kafka source
kafka_source = (
    KafkaSource.builder()
    .set_bootstrap_servers("localhost:9092")
    .set_topics("clickstream-events")
    .set_group_id("flink-consumer-group")
    .set_starting_offsets(KafkaOffsetsInitializer.latest())
    .set_value_only_deserializer(SimpleStringSchema())
    .build()
)

# Create data stream from Kafka
stream = env.from_source(
    kafka_source, WatermarkStrategy.no_watermarks(), "Kafka Source"
)

# Process the stream
processed = stream.map(lambda x: x.upper())
processed.print()

env.execute("Kafka Integration Example")

# to be tested
