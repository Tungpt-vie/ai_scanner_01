from scanner.data_feed.fake_feed import FakeFeed
from scanner.data_feed.manager import FeedManager

feed1 = FakeFeed("VCB", 5)
feed2 = FakeFeed("VCB", 5)  # giả làm nguồn failover

manager = FeedManager(
    feeds=[feed1, feed2],
    timeframe_minutes=5
)

for i in range(6):
    candle = manager.get_latest_valid_candle()
    print("CANDLE:", candle)
