gunzip disko-1.dd.gz
strings disko-1.dd | grep "picoCTF{"

---

Yes, you should **definitely unzip it first.**

The `.gz` extension stands for Gzip, and while `exiftool` is smart enough to read the metadata *of the compressed package itself*, it cannot "see through" the compression to analyze the actual disk sectors inside.

### Why you need to unzip
1.  **ExifTool Output:** The `Archived File Name : disko-1.dd` line you see is just a metadata "label" inside the Gzip header telling you what's inside. It’s like reading the label on a cardboard box—you know there's a "disko-1.dd" in there, but you haven't opened the box to look at the data yet.
2.  **File Size:** Forensics images (like `.dd` files) are often much larger once uncompressed. Commands like `strings` or `binwalk` need access to the raw bytes of that large file to find your flag.

#### 3. If that fails (The Deep Dive)
If a simple string search doesn't work, the flag might be inside a file *on* the disk image. You can use the **Sleuth Kit** tools to list the files without mounting it:
```bash
# List all files on the disk
fls -r disko-1.dd
```
Look for suspicious file names (like `flag.txt` or `secret.txt`). If you find one, note its **inode number** (the number at the start of the line) and use `icat` to read it:
```bash
# Replace 12345 with the actual inode number you found
icat disko-1.dd 12345
```
