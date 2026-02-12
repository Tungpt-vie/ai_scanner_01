from scanner.ops.resume_manager import ResumeManager
from scanner.ops.state_snapshot import StateSnapshot
from scanner.ops.recovery_guard import RecoveryGuard
from scanner.ops.internet_watchdog import InternetWatchdog
from scanner.ops.auto_start import AutoStartController


# 1️⃣ Test Snapshot
snapshot = StateSnapshot()
snapshot.capture(
    last_symbol="TEST",
    last_regime="TRENDING",
    last_filter_state="STANDARD",
    session_active=True,
)

state = snapshot.get_state()
print("Snapshot Captured:", state)


# 2️⃣ Test Recovery Guard
guard = RecoveryGuard()
resume_allowed = guard.allow_resume(state)
print("Resume Allowed:", resume_allowed)
print("Replay Allowed (should be False):", guard.allow_replay())


# 3️⃣ Test Resume Manager
manager = ResumeManager()
manager.capture_state(
    last_symbol="TEST",
    last_regime="TRENDING",
    last_filter_state="STANDARD",
    session_active=True,
)

resume_ok = manager.attempt_resume()
print("Resume Attempt OK:", resume_ok)
print("In Resume Mode:", manager.in_resume_mode())


# 4️⃣ Test Internet Watchdog (non-blocking check)
watchdog = InternetWatchdog()
print("Internet Online (True/False acceptable):", watchdog.check_connection())


# 5️⃣ Test AutoStartController
controller = AutoStartController()
started = controller.start()
print("AutoStart Started:", started)
print("Controller Started State:", controller.is_started())
