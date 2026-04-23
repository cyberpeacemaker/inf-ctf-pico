#
- `binwalk`: tool for searching binary images for embedded files and executable code
- `foremost`: Recover files using their headers, footers, and data structures
- `steghide`: a steganography program

`PASS=$(exiftool img.jpg | grep -i "Comment" | awk -F': ' '{print $2}' | base64 -d | cut -d':' -f2 | base64 -d) && steghide extract -sf img.jpg -p "$PASS"`

#
### 1\. Metadata Analysis (EXIF Data)

The most common first step is to extract **EXIF (Exchangeable Image File Format)** data. This is "data about the data" embedded in the file.

* **What to look for:** Camera model, software used (e.g., Photoshop vs. an iPhone), timestamps, and—most importantly—**GPS coordinates**.
* **Tools:** `ExifTool` (command line) or online viewers like Jeffrey's Image Metadata Viewer.

---

### 2\. Reverse Image Searching

If you are trying to verify the source or location of an image, use the web to see where else it appears.

  * **Google Lens / Yandex Images:** Excellent for identifying landmarks, products, or people.
  * **TinEye:** Great for finding the "original" high-resolution version of a cropped or edited photo.
  * **Method:** This helps determine if an image is "repurposed" (e.g., a photo from a 2018 protest being used to claim something is happening today).

-----

### 3\. Error Level Analysis (ELA)

ELA identifies areas within an image that are at different compression levels. In a JPG, the entire image should ideally have a consistent "layer" of digital noise.

  * **How it works:** If a part of the image was digitally altered (e.g., a face swapped or text changed), that specific area will often show a different level of white/bright "noise" compared to the rest of the image.
  * **Tool:** [FotoForensics](https://www.google.com/search?q=http://fotoforensics.com/) is the industry standard for quick ELA checks.

-----

### 4\. Steganography Check

Steganography is the practice of hiding a file, message, or even another image inside a JPG.

  * **Strings Analysis:** Running the `strings` command in Linux can reveal hidden text or URLs buried in the binary code of the image.
  * **File Carving:** Tools like `Binwalk` or `Foremost` can check if there is a hidden ZIP or PDF appended to the end of the JPG file.
  * **Least Significant Bit (LSB):** Specialized tools like `StegSolve` can cycle through color planes to see if data is hidden in the pixels themselves.

-----

### 5\. Hexadecimal & Magic Bytes Verification

Every file type has a "signature." For a JPG, the file must start with specific bytes.

  * **The Signature:** A valid JPG always starts with `FF D8 FF` and ends with `FF D9`.
  * **Investigation:** Using a Hex Editor (like HxD), you can verify if a file is actually a JPG or if someone has renamed a malicious `.exe` file to `.jpg` to trick you into opening it.

-----

### Summary Checklist

| Phase | Action | Key Tool |
| :--- | :--- | :--- |
| **Origin** | Check GPS and timestamps | ExifTool |
| **Authenticity** | Check for edits/manipulation | FotoForensics (ELA) |
| **Context** | Find other copies online | Search by Image (Google/Yandex) |
| **Secrets** | Look for hidden files/text | Binwalk / Strings |
