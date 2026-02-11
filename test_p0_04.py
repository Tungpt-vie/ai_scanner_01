from scanner.ta_engine.engine import TAEngine


engine = TAEngine()

# Tạo dữ liệu giả lập giá tăng dần
prices = [
    10, 10.2, 10.4, 10.6, 10.8,
    11, 11.2, 11.4, 11.6, 11.8,
    12, 12.2, 12.4, 12.6, 12.8,
    13, 13.2, 13.4, 13.6, 13.8,
    14, 14.2, 14.4, 14.6, 14.8
]

for p in prices:
    candle = {
        "open": p,
        "high": p + 0.1,
        "low": p - 0.1,
        "close": p,
        "volume": 1000
    }

    result = engine.process_candle(candle)

print("Final TA Result:")
print(result)
