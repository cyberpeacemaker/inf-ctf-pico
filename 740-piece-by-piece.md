# SSH Login
ssh ctf-player@dolphin-cove.picoctf.net -p 56454

# File Split and Merge
It looks like you've moved past the "printer" networking phase and are now in the **file reconstruction** phase. You have a series of fragmented files (`part_aa` through `part_ae`) that need to be stitched back together to form a valid ZIP archive.

### 1. Combine the Fragments
In Linux, the `cat` (concatenate) command is perfect for this. Since the files are named alphabetically (`aa`, `ab`, `ac`, etc.), a wildcard will pull them in the correct order.

Run this command to merge them into a single zip file:
```bash
cat part_a* > flag.zip
```

### 2. Verify the File
Before trying to unzip it, verify that the combined file is actually recognized as a ZIP archive:
```bash
file flag.zip
```
> **Expected Output:** `flag.zip: Zip archive data, at least v2.0 to extract...`

### 3. Unzip with the Password
Now, use the password provided in the `instructions.txt` (**supersecret**) to extract the contents.

Run:
```bash
unzip flag.zip
```
When prompted for the password, type: `supersecret`
