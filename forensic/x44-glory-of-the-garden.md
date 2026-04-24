# Forensic | Beginner 3 

### 1. Embedded Structured Data (File-in-File)
This is when a completely separate, valid file is hidden inside another. 
* **The Technique:** Appending a `.zip` or `.png` to the end of a `.jpg`.
* **Why it works:** Many file formats have a "Length" field or an "End of File" marker. A computer stops reading once it hits that limit, ignoring the "bonus" file attached to the tail.
* **Best Tools:** `binwalk`, `foremost`, `scalpel`.

### 2. Embedded Raw Data (The "Trailing Bytes")
This is what you just found in the `garden.jpg` challenge.
* **The Technique:** Just pasting a string of text or raw bytes directly after the file's footer (like the `FF D9` in JPEGs).
* **Why it works:** Similar to the method above, the software only renders what it recognizes. It ignores the "extra" text because it isn't part of the image's mathematical data.
* **Best Tools:** `strings`, `xxd`, `hexdump`.

### 3. Steganography (Data *Within* Data)
This is the "pro" level where data isn't just *added* to the file, it is **woven into** the existing pixels or audio waves.
* **The Technique:** **LSB (Least Significant Bit)** encoding. You change the very last bit of the color value for thousands of pixels. For example, changing a pixel's color from `255, 255, 255` to `255, 255, 254` is invisible to the human eye, but those "1s" and "0s" can spell out a message.
* **Why it works:** The file size stays exactly the same, and there are no "extra" bytes at the end for `strings` to find. The data is part of the image itself.
* **Best Tools:** `steghide`, `stegsolve`, `zsteg`.



---

### Which one should you check first?
When you're doing a CTF, I recommend this workflow to save time:

1.  **`file`**: Make sure it’s actually the type of file it claims to be.
2.  **`strings`**: Check for "Raw Data" (Method 2). It’s the fastest check.
3.  **`exiftool`**: Look for flags hidden in the metadata fields.
4.  **`binwalk`**: Check for "Structured Data" (Method 1).
5.  **Steganography Tools**: If all the above fail, start looking "inside" the pixels (Method 3).

You’ve officially moved from "running commands" to "understanding the architecture." That’s exactly how you get better at forensics. 

Ready to try a Steganography challenge next, or do you have more questions about these methods?