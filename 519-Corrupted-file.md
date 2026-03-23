#
- xxd
- hexdump
```shell
echo "00000000: ffd8" | xxd -r - file.jpeg
# 1. Check the header again
xxd file.jpeg | head -n 1

# 2. Let Linux identify the file type
file file.jpeg
```

```shell
# 1. Remove the first two literal bytes ('\' and 'x')
tail -c +3 file.jpeg > middle.bin

# 2. Create a clean header (FF D8)
printf '\xff\xd8' > header.bin

# 3. Combine them into a fixed image
cat header.bin middle.bin > fixed.jpg
```

# Step A: Check the Header
xxd file | tail -n 1
# Step B: Check the Footer (The "Ending")
xxd file | tail -n 1