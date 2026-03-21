#
- wc
- file
- head -c 8 decoded-output | xxd
- echo "7069636F4354467B666F72656E736963735F616E616C797369735F69735F616D617A696E675F62396163346362397D" | xxd -r -p

# Magic Byte
The "Magic Bytes" check: Run head -c 8 image.png | xxd. A real PNG always starts with 89 50 4E 47 0D 0A 1A 0A.

# Zlib
In a PNG file, Zlib compressed data is a perfectly normal part of the file structure. It’s what contains the actual pixel data (the IDAT chunks).

# TODO
extract string from img?


### Forensic Summary of your Journey:
2.  **Decoding:** You found a 1.5MB file with "long lines" which was actually a **Base64** encoded PNG.
3.  **Discovery:** You analyzed the PNG and found a **Hex string** (likely via `strings` or by visually looking at the image).
4.  **Final Step:** You converted the Hex to ASCII to get the flag.
