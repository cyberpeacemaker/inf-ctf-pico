# QR
https://zxing.org/w/decode.jspx

# shift
# Skip the first 3 characters and try again
cat xxd_str | cut -c 4- | xxd -r -p ; echo ""


# Header / Shift / Padding
### 3. How to detect padding/shifts in the "Real World"
In a professional forensic audit, we look for these clues:

1.  **Known Plaintext Attack:** We know the flag starts with `picoCTF`. We search the hex for those specific values. If we find them, we know the "Offset."
2.  **Repeated Patterns:** Look at your hex again: `ec 11 ec 11`. Seeing a two-byte pattern repeat at the very end is a massive red flag for **Padding**.
3.  **File Signatures:** As mentioned before, if a file starts with `41 c7 06`, and that doesn't match any known file type (like `89 50 4E 47` for PNG), we assume the first few bytes are a custom header or "junk" to hide the real data.
