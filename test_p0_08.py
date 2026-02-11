from scanner.ta_engine.context import TAContext
from scanner.optimization.pipeline_guard import OptimizationGuard
from scanner.fa_gate.store import FAStatus


# 1️⃣ Setup
context = TAContext(max_length=200)
guard = OptimizationGuard()

symbol = "TEST"


# 2️⃣ Case A — Data Insufficient (should early drop)
fa_status = FAStatus.FA_PASS
is_session_active = True

print("Case A (insufficient data):",
      guard.should_process(symbol, context, fa_status, is_session_active))


# 3️⃣ Add enough candles
for i in range(25):
    candle = {
        "open": 10 + i * 0.1,
        "high": 10 + i * 0.1 + 0.2,
        "low": 10 + i * 0.1 - 0.2,
        "close": 10 + i * 0.1,
        "volume": 1000 + i * 10,
    }
    context.add_candle(candle)


# 4️⃣ Case B — FA_FAIL (should early drop)
print("Case B (FA_FAIL):",
      guard.should_process(symbol, context, FAStatus.FA_FAIL, True))


# 5️⃣ Case C — Session inactive (should early drop)
print("Case C (Session inactive):",
      guard.should_process(symbol, context, FAStatus.FA_PASS, False))


# 6️⃣ Case D — Valid processing allowed
print("Case D (valid process):",
      guard.should_process(symbol, context, FAStatus.FA_PASS, True))


# 7️⃣ Regime Cache Test
regime1 = guard.get_regime(symbol, context)
regime2 = guard.get_regime(symbol, context)

print("Regime First Call:", regime1.value)
print("Regime Second Call (cached):", regime2.value)
print("Regime cache stable:", regime1 == regime2)
