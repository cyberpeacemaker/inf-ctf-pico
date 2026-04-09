
tshark -r myNetworkTraffic.pcap -T fields -e frame.time_relative -e tcp.payload

- xxd -r -p

# pcap

- timestamp, TCP seq no., TCP Window Size

# TCP Retransmission
This happens because Wireshark sees multiple SYN packets with the same sequence number.

### 3. How to target the Tab explicitly
If you want to be explicit with `cut` (which is sometimes necessary in scripts), you can't just type a Tab key into the terminal easily. You usually use the `$'\t'` syntax:

```bash
cut -d$'\t' -f2
```

### Summary: Which one should you use?
* **Use `awk`** when you are working interactively. It is shorter to type and handles spaces, tabs, and weird alignment automatically.
* **Use `cut`** only when you are 100% certain the file is strictly Tab-separated (TSV) or Comma-separated (CSV) and you want a tiny bit more speed.