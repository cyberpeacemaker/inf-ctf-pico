
# decuplication
```python
def extract_unique_binary(filename):
    with open(filename, 'r') as f:
        # Load and remove all whitespace/newlines
        data = f.read().strip().replace(" ", "").replace("\n", "")

    # The noise pattern you identified
    pattern = "01000101000101000000000001010001"

    # Step 1: Strip the noise
    unique_data = data.replace(pattern, "")
    
    # OUTPUT UNIQUE DATA FIRST as requested
    print("--- RAW UNIQUE BINARY ---")
    print(unique_data)
    print(f"\nLength of unique binary: {len(unique_data)} bits")
    print("-" * 25 + "\n")

    # Step 2: Attempt Decoding
    try:
        # Check if length is divisible by 8 (Standard Byte)
        if len(unique_data) % 8 != 0:
            print(f"Warning: Binary length ({len(unique_data)}) is not a multiple of 8.")
            print("This usually means there is a hidden 'offset' or extra bits.\n")

        # Convert to bytes using the 'int' method (handles large numbers)
        # bit invet? big/little ?
        num = int(unique_data, 2)
        raw_bytes = num.to_bytes((num.bit_length() + 7) // 8, 'big')
        
        print("--- RAW BYTES OUTPUT ---")
        print(raw_bytes)
        
        # Try to see it as a string
        print("\n--- STRING DECODE ---")
        print(raw_bytes.decode('utf-8', errors='ignore'))

    except Exception as e:
        print(f"Error during byte conversion: {e}")

extract_unique_binary('digits.bin')
```

# know text
```python
def find_pico_pattern(filename):
    with open(filename, 'r') as f:
        # Load and clean the file
        data = f.read().strip().replace(" ", "").replace("\n", "")

    # The "Signature" we are hunting for
    # 1. Bit Iversion 2. Big/Little Endian
    target = "01110000011010010110001101101111" # 'pico'
    "01110000011010010110001101101111"
    
    # Search for the pattern
    index = data.find(target)
    
    if index != -1:
        print(f"[+] Found 'pico' signature at bit index: {index}")
        # Extract everything from 'pico' onwards
        flag_binary = data[index:]
        
        # Now, let's decode from that exact spot
        chunks = [flag_binary[i:i+8] for i in range(0, len(flag_binary), 8)]
        decoded = "".join([chr(int(c, 2)) for c in chunks if len(c) == 8])
        print(f"\n[!] Flag Found: {decoded}")
    else:
        print("[-] 'pico' not found. Checking for 'pico' in Caesar/ROT...")
        # If 'pico' isn't there, the binary itself might be shifted or XORed
        # Let's look for any 32-bit block that has a similar structure
        print("    Try searching for common headers like 'CTF{' or 'flag' next.")

find_pico_pattern('digits.bin')
```