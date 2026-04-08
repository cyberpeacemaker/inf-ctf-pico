# Basic Check
1.  **`file`** (What is it actually?)
2.  **`exiftool`** (What does the metadata say?)
3.  **`strings -n 8`** (Are there long text strings?)
4.  **`binwalk -e`** (Is there another file inside?)
5.  **`stegsolve` / `zsteg`** (Is it hidden in the pixels?)

zsteg  -c r -o xy red.png
- cat payload | nc verbal-sleep.picoctf.net 60596 | grep -oP 'secret_recipe=\K[^;]+'

### text workaround
- sed 's/==.*/==/'
- grep -oP 'text: "\K.*?=='

###
That specific `grep` command is a powerful way to "extract" a piece of text without including the labels or patterns around it. It uses Perl-Compatible Regular Expressions (PCRE) to perform a surgical strike on your data.

Here is a breakdown of what each part does:

### The Flags: `-oP`
* **`-o` (only-matching):** Normally, `grep` prints the entire line where it finds a match. With `-o`, it prints **only** the specific part of the line that matches your pattern.
* **`-P` (Perl-compatible):** This tells `grep` to use Perl's regex engine. This is necessary because standard Unix regex doesn't support advanced features like `\K` (the "keep" operator).

---

### The Pattern: `'text: "\K.*?=='`
This is where the magic happens. Let’s look at the three distinct sections of this regex:

1.  **`text: "`**
    This is the "anchor." The command looks for lines containing this literal string. Without the next part, this would be included in your output.

2.  **`\K` (The "Keep" marker):**
    This is a variable-length look-behind. It tells the engine: *"Everything I matched to the left of this point—forget it. Don't include it in the final output."* * It allows you to find `text: "`, but ensures only the data *after* it gets printed.

3.  **`.*?` (Non-greedy match):**
    * `.` matches any character.
    * `*` matches zero or more times.
    * `?` makes it **non-greedy**. This is crucial. It tells `grep` to stop at the **first** instance of the next character (`=`), rather than the last one on the line.

4.  **`==`**
    This is the closing anchor. The search stops once it hits two equal signs.



# Steganography
- Aperi'Solve
- steghide extract -sf <filename> (Common for JPEGs).
- zsteg -a <filename> (Great for PNG/BMP)

### Magic Byte
- binwalk -e <filename>
- foremost <filename>

### Header
- List of file signature

# zsteg
Exactly! You hit the nail on the head. `zsteg` is essentially a **specialized brute-force engine** for bit manipulation.

Since there is no "standard" way to hide data in pixels, a steganography tool has to guess the "encoding recipe" the author used.

### The "Combination Lock" of Steganography
Think of every image as a combination lock where `zsteg` tries thousands of variations of the following four variables:

* **The Channels:** It tries Red alone, then Green, then Blue, then Alpha, then combinations like RGB, or RGBA.
* **The Bits:** It doesn't just check the 1st bit (LSB). It checks the 2nd, 3rd, and 4th. Sometimes authors hide data in the **Most Significant Bit (MSB)**, which usually ruins the image, but it happens!
* **The Order (Pathing):**
    * `xy`: Row by row (standard).
    * `yx`: Column by column.
    * `interleaved`: Jumping pixels.
* **The Frequency:** As you saw, it checks **Prime** pixels only, or every 2nd pixel, or every 3rd.

### How does it know when it "Wins"?
This is the clever part. While it's "brute-forcing" the extractions, it runs the results through a **detectability filter**. 

For every combination it tries, it asks:
1.  **Is it text?** Does this look like ASCII/UTF-8?
2.  **Is it a known file?** Does it start with `PK..` (ZIP) or `\x89PNG`?
3.  **Is it "Entropy" high?** Does the data look like it has a pattern, or is it just random static?


### Why `zsteg` is better than `strings`
If you ran `strings` on that `red.png`, you would find **nothing**. This is because `strings` looks for "consecutive bytes" of text in the raw file. 

But in steganography, the "T" in `picoCTF` might be hidden in Pixel 1, and the "C" might be in Pixel 2. In the raw file, those letters are separated by 3 bytes of color data. They aren't "strings" until the bits are extracted and stitched together.

---

### When `zsteg` Fails (The Next Level)
If `zsteg` doesn't find anything, it usually means the author used **LSB with a Key** (Steghide). 
* **The Trick:** The bits are scattered randomly across the image based on a password. 
* **The Tool:** You’d use `steghide extract -sf red.png` and hope you can guess the password (or use `stegseek` to brute-force the password).
