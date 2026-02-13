import time
from datetime import datetime, timedelta

from scanner.observation.lifecycle_manager import ObservationLifecycleManager
from scanner.observation.state_transition import ObservationState
from scanner.observation.update_detector import ObservationUpdateDetector
from scanner.observation.expiry_handler import ObservationExpiryHandler
from scanner.observation.close_handler import ObservationCloseHandler


# 1️⃣ Setup components
manager = ObservationLifecycleManager()
detector = ObservationUpdateDetector()
expiry = ObservationExpiryHandler(expiry_minutes=0)  # expire immediately for test
closer = ObservationCloseHandler()


# 2️⃣ Create observation
record = manager.create("obs1")
print("Initial State:", record.state.value)


# 3️⃣ Transition OPEN → UPDATED
manager.transition("obs1", ObservationState.UPDATED)
print("After Update:", record.state.value)


# 4️⃣ Meaningful change detection
prev = {"rsi": 50}
curr = {"rsi": 55}
print("Meaningful Change (should True):", detector.has_meaningful_change(prev, curr))

curr2 = {"rsi": 50.2}
print("Minor Change (should False):", detector.has_meaningful_change(prev, curr2))


# 5️⃣ Expiry test (force immediate expiry)
expiry.apply_expiry(record)
print("After Expiry:", record.state.value)


# 6️⃣ Close explicitly
closer.close(record)
print("After Close:", record.state.value)


# 7️⃣ Attempt reopen (should fail)
try:
    manager.transition("obs1", ObservationState.OPEN)
except Exception as e:
    print("Reopen Blocked:", str(e))


# 8️⃣ Attempt invalid transition from CLOSED
try:
    manager.transition("obs1", ObservationState.UPDATED)
except Exception as e:
    print("Closed Transition Blocked:", str(e))


# 9️⃣ Attempt double close
try:
    closer.close(record)
except Exception as e:
    print("Double Close Blocked:", str(e))
