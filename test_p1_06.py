import time
from datetime import datetime, timedelta

from scanner.storage.event_repository import EventRepository
from scanner.storage.delivery_repository import DeliveryRepository
from scanner.storage.hash_generator import EventHashGenerator
from scanner.storage.ttl_cleaner import TTLCleaner
from scanner.storage.storage_guard import StorageGuard


# 1️⃣ Setup
event_repo = EventRepository()
delivery_repo = DeliveryRepository()
guard = StorageGuard(event_repo, delivery_repo)

ttl_cleaner = TTLCleaner(
    event_repo=event_repo,
    delivery_repo=delivery_repo,
    ttl_minutes=0,  # expire immediately for test
)

hasher = EventHashGenerator()

# 2️⃣ Create payload
payload = {
    "symbol": "VCB",
    "type": "OBSERVATION",
    "score": 0.82,
}

# 3️⃣ Store event
event_hash1 = guard.store_event(payload)
print("Stored Event Hash:", event_hash1)

# 4️⃣ Store same payload again (dedup)
event_hash2 = guard.store_event(payload)
print("Dedup Hash Same:", event_hash1 == event_hash2)

print("Event Count:", len(event_repo.list_all()))

# 5️⃣ Mark delivery
guard.mark_delivery(event_hash1, "u1")
print("Delivered to u1:", guard.has_been_delivered(event_hash1, "u1"))

# 6️⃣ Duplicate delivery (idempotent)
guard.mark_delivery(event_hash1, "u1")
print("Delivery Count:", len(delivery_repo.list_all()))

# 7️⃣ TTL cleanup
ttl_cleaner.clean_expired_events()

print("Event Count After TTL:", len(event_repo.list_all()))
print("Delivery Count After TTL:", len(delivery_repo.list_all()))

# 8️⃣ Attempt to access deleted event
try:
    event_repo.get(event_hash1)
except Exception as e:
    print("Access Deleted Event Blocked:", str(e))
