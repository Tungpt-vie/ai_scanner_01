from datetime import datetime

from scanner.ta_engine.context import TAContext
from scanner.ta_engine.evaluator import TAEvaluator
from scanner.ta_filter.filter_pipeline import TAFilterPipeline
from scanner.fa_gate.store import FAStatus
from scanner.event_generator.factory import TAEventFactory
from scanner.phrase_engine.renderer import PhraseRenderer


# 1️⃣ Setup
context = TAContext(max_length=200)
evaluator = TAEvaluator()
pipeline = TAFilterPipeline()
factory = TAEventFactory()
renderer = PhraseRenderer()

symbol = "TEST"
timestamp = datetime.utcnow()


# 2️⃣ Deterministic trending dataset
prices = [
    10, 10.2, 10.4, 10.6, 10.8,
    11, 11.2, 11.4, 11.6, 11.8,
    12, 12.2, 12.4, 12.6, 12.8,
    13, 13.2, 13.4, 13.6, 13.8,
    14, 14.2, 14.4, 14.6, 14.8,
    15, 15.2, 15.4, 15.6, 15.8,
]

volumes = [
    1000, 1100, 1050, 1200, 1300,
    1250, 1400, 1500, 1550, 1600,
    1700, 1800, 1900, 2000, 2100,
    2200, 2300, 2400, 2500, 2600,
    2700, 2800, 2900, 3000, 3200,
    3500, 3800, 4000, 4200, 4500,
]

for i in range(len(prices)):
    candle = {
        "open": prices[i],
        "high": prices[i] + 0.2,
        "low": prices[i] - 0.2,
        "close": prices[i],
        "volume": volumes[i],
    }
    context.add_candle(candle)


# 3️⃣ Evaluate signal
signal = evaluator.evaluate(context)

# 4️⃣ Apply filter
filter_state = pipeline.process(signal, FAStatus.FA_PASS)

# 5️⃣ Create event
event = factory.create_event(
    symbol=symbol,
    timestamp=timestamp,
    signal=signal,
    filter_state=filter_state,
)

# 6️⃣ Render phrase
output = renderer.render(event)

print("Rendered Output:\n")
print(output)


# 7️⃣ Lint negative test (manual injection)
bad_text = "You should buy now. This will rise."
print("\nLint Test (should be False):", renderer.lint.validate(bad_text))
