# Identity Spoofing
```
git config user.name "root"
git config user.email "root@picoctf"
# Verify
git config --list
# Commit and push
git add flag.txt
git commit -m "Update flag.txt"
git push origin main
```