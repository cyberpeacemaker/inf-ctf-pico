import re

filename = 'heapdump-1774328682578.heapsnapshot'

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# This regex finds the flag and any surrounding whitespace/newlines
# and replaces it with a single comma to keep the array valid.
pattern = r',?\s*picoCTF\{.*?\}+?\s*,?'
cleaned_content = re.sub(pattern, ',', content)

with open('heap_fixed.heapsnapshot', 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print("Patch complete. Try loading 'heap_fixed.heapsnapshot' in DevTools.")