import csv

from pyflink.common import Types, WatermarkStrategy
from pyflink.common.time import Time
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.window import TumblingEventTimeWindows

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

# Read (page, timestamp) records from the generated CSV file
data = []
with open("page_clicks.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            data.append((row[0], int(row[1])))

clicks = env.from_collection(
    collection=data,
    type_info=Types.TUPLE([Types.STRING(), Types.LONG()]),
)


# Extract event-time timestamps from the embedded second field (seconds → milliseconds)
class ClickTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp):
        return value[1] * 1000  # Flink expects milliseconds


watermark_strategy = (
    WatermarkStrategy.for_monotonous_timestamps().with_timestamp_assigner(
        ClickTimestampAssigner()
    )
)

clicks_with_watermarks = clicks.assign_timestamps_and_watermarks(watermark_strategy)

# Map each event to (page, 1) so the reduce sums counts correctly,
# then key by page and aggregate within 5-second event-time windows.
page_counts = (
    clicks_with_watermarks.map(
        lambda x: (x[0], 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()])
    )
    .key_by(lambda x: x[0])
    .window(TumblingEventTimeWindows.of(Time.seconds(5)))
    .reduce(lambda x, y: (x[0], x[1] + y[1]))
)

page_counts.print()

env.execute("Windowed Page View Count")
