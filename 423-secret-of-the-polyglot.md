
dd if=flag2of2-final.pdf of=hidden_image.png bs=1 count=914

---

#

Ah, I see the confusion! You were expecting a nice `output.png` and `output.pdf` to just appear in the folder. It feels like `binwalk` did a "half-job," but there’s a very logical (and slightly annoying) reason why it only gave you the Zlib stuff.

### 1. Why no `.png` or `.pdf` file?
`binwalk` is a bit "picky" about how it extracts. 

* **The PNG (Offset 0):** Because the PNG starts at the very beginning of the file (Offset 0), `binwalk` often views the *entire* `flag2of2-final.pdf` as the PNG. It doesn't usually create a second copy of the "whole file" inside the extraction folder unless it thinks the PNG is "embedded" later on.
* **The PDF (Offset 914):** `binwalk` is great at finding headers, but it often struggles to find the "End of File" marker for PDFs. Because it doesn't know exactly where the PDF *ends*, it sometimes skips the extraction of the PDF container itself and moves straight to the "inner" compressed data (the Zlib).



### 2. The "Zlib" is the "Innards"
Think of the PDF as a cardboard box. The **Zlib compressed data** is the actual bubble wrap inside the box. 
* `binwalk` saw the box (PDF at 914).
* `binwalk` saw the bubble wrap (Zlib at 1149).
* It decided the bubble wrap was the most "extractable" thing and pulled that out.

### 3. How to get your PNG and PDF manually
Since `-e` didn't give you the clean files you wanted, we can use the "Surgery" method with `dd`. This is actually more reliable in CTFs because you control the exact byte counts.

**To get the PNG (from byte 0 to 914):**
```bash
dd if=flag2of2-final.pdf of=extracted_image.png bs=1 count=914
```

**To get the PDF (from byte 914 to the end):**
```bash
dd if=flag2of2-final.pdf of=extracted_document.pdf bs=1 skip=914
```



### 4. What to do now?
1.  **Check the PNG:** Use the `dd` command above to get `extracted_image.png`. Since it's only 50x50, it might be a tiny QR code or a small string of text.
2.  **Check the Zlib:** Look at that `47D` file again. If `binwalk` extracted it, that is the *content* of the PDF.
    * Try: `strings _flag2of2-final.pdf.extracted/47D`
    * Try: `cat _flag2of2-final.pdf.extracted/47D`

**Why the Zlib matters:** In many PDF forensic challenges, the flag is hidden in a "Stream." A PDF stream is almost always compressed with Zlib. By extracting the Zlib, `binwalk` has basically "unwrapped" the PDF for you.

Did you try running `strings` on that `47D` file yet? The flag might be staring at you in there!