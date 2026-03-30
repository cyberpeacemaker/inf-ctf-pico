#
- ROT13
- URL
- Hex
- Base64

# ROT
```python
import sys

def caesar_cipher(text, shift):
    result = ""
    
    for char in text:
        # Handle Uppercase
        if char.isupper():
            # Shift within A-Z (ASCII 65-90)
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Handle Lowercase
        elif char.islower():
            # Shift within a-z (ASCII 97-122)
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            # Keep symbols/numbers/spaces as they are
            result += char
            
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 rotate.py 'your text' [shift_number]")
    else:
        user_text = sys.argv[1]
        user_shift = int(sys.argv[2])
        print(caesar_cipher(user_text, user_shift))
```

# Plus Bruteforce
```python
# Replace the 'if __name__' block with this to see everything
text_to_crack = "cvpbPGS{arfgrq_rap0qvat_s3n24s73}"

for i in range(1, 26):
    print(f"Shift {i:2}: {caesar_cipher(text_to_crack, i)}")
```

```bash
#!/bin/bash

# Usage: ./rotate.sh "text" shift_number
input=$1
shift=$2

# Create the alphabet
alphabet="abcdefghijklmnopqrstuvwxyz"

# Calculate the wrap-around point
# Cut the alphabet at the shift point and swap the pieces
shifted_alphabet=$(echo $alphabet | sed -E "s/(.{$shift})(.*)/\2\1/")

# Do the same for Uppercase
alphabet_upper=$(echo $alphabet | tr 'a-z' 'A-Z')
shifted_upper=$(echo $shifted_alphabet | tr 'a-z' 'A-Z')

# Perform the translation
echo "$input" | tr "${alphabet}${alphabet_upper}" "${shifted_alphabet}${shifted_upper}"
```

# xxd
xxd: make a hexdump or do the reverse

xxd -r[evert] [options] [infile [outfile]]
#

base64 (-d)

# URL
%3d <-> =

# tr
tr: translate or delete characters