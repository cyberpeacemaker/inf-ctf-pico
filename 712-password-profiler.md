# Profiler, Combinator
CUPP (Common User Passwords Profiler)
Hashcat (-attack mode)

```python
names = ["Alice", "Johnson", "AJ", "Bob", "Charlie"]
years = ["1990", "90", "15", "07", "1507", "0715"]
# symbols = ["!", "@", "#"]

# Simple nested loop combination
for name in names:
    for year in years:
        # for sym in symbols:
            # print(f"{name}{year}{sym}")
        print(f"{name}{year}")
```