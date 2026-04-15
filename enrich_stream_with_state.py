import csv

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import KeyedProcessFunction, RuntimeContext
from pyflink.datastream.state import ValueStateDescriptor


class SessionTracker(KeyedProcessFunction):
    """
    Tracks user sessions and detects cart abandonment.
    Maintains state for each user's last action.
    """

    def open(self, runtime_context: RuntimeContext):
        # Initialize state to track last page visited
        state_descriptor = ValueStateDescriptor("last_page", Types.STRING())
        self.last_page_state = runtime_context.get_state(state_descriptor)

    def process_element(self, value, ctx):
        user_id, page, timestamp = value
        last_page = self.last_page_state.value()

        # Detect cart abandonment
        if last_page == "cart" and page not in ["cart", "checkout"]:
            yield (user_id, "CART_ABANDONED", timestamp)

        # Update state with current page
        self.last_page_state.update(page)
        yield (user_id, page, timestamp)


env = StreamExecutionEnvironment.get_execution_environment()

data = []
with open("user_journeys.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            data.append((row[0], row[1], int(row[2])))

# Simulate user clickstream
# user_clicks = env.from_collection(
#     [
#         ("user1", "home", 1634567890),
#         ("user1", "products", 1634567895),
#         ("user1", "cart", 1634567900),
#         ("user1", "home", 1634567905),  # Cart abandoned!
#         ("user2", "products", 1634567910),
#         ("user2", "cart", 1634567915),
#         ("user2", "checkout", 1634567920),  # Successful checkout
#     ]
# )
user_clicks = env.from_collection(
    collection=data,
    type_info=Types.TUPLE([Types.STRING(), Types.STRING(), Types.INT()]),
)

# Process with stateful function
results = user_clicks.key_by(lambda x: x[0]).process(SessionTracker())  # Key by user_id

results.print()

env.execute("Cart Abandonment Detection")
