
grep "$(cat sum)" checksum.txt

sha256sum <directory>/*

# Real world
```shell
sha256sum files/* > manifest.txt
sha256sum -c manifest.txt
```

# hash

| Algorithm | Command | Use Case |
| :--- | :--- | :--- |
| **MD5** | `md5sum` | Legacy, fast, but no longer cryptographically secure (prone to collisions). |
| **SHA-1** | `sha1sum` | Older standard, widely used in Git, but also considered weak now. |
| **SHA-256** | `sha256sum` | **The current standard** for file integrity and security. |
| **SHA-512** | `sha512sum` | Extremely secure, often used for password hashing in `/etc/shadow`. |
