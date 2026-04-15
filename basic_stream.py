import csv

from pyflink.datastream import StreamExecutionEnvironment

# Create the execution environment
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

# Read data from the CSV file
data = []
with open("clicks.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:  # Ensure the row is not empty
            data.append((row[0], row[1], int(row[2]), int(row[3])))

# Load data into Flink - in production, this would be Kafka or similar
clicks = env.from_collection(data)

# Filter events where users spent more than 60 seconds
filtered_clicks = clicks.filter(lambda x: x[3] > 60)

# Print Results
filtered_clicks.print()

# Execute the job
env.execute("Simple Clickstream Analysis")
