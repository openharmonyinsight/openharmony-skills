# smaps PSS Attribution

Use this parser pattern for per-library PSS attribution. The important rule is to reset the current mapping owner on every mapping header line.

```python
import re

current_lib = None
pss_by_lib = {}
for line in open("smaps.txt"):
    if re.match(r"[0-9a-f]+-[0-9a-f]+\s", line):
        m = re.search(r"(/system/lib\S*libmmi\S+\.so)", line)
        current_lib = m.group(1).split("/")[-1] if m else None
    m = re.match(r"Pss:\s+(\d+)\s+kB", line)
    if m and current_lib:
        pss_by_lib[current_lib] = pss_by_lib.get(current_lib, 0) + int(m.group(1))

for lib, pss in sorted(pss_by_lib.items()):
    print(f"{lib}\t{pss}")
```

For full loaded-library attribution, aggregate all `.so` mappings by complete path:

```python
import re
from collections import defaultdict

pss_by_so = defaultdict(int)
current_so = None
for line in open("smaps.txt"):
    if re.match(r"[0-9a-f]+-[0-9a-f]+\s", line):
        m = re.search(r"(/\S+\.so(?:\.\S+)*)$", line)
        current_so = m.group(1) if m else None
    m = re.match(r"Pss:\s+(\d+)\s+kB", line)
    if m and current_so:
        pss_by_so[current_so] += int(m.group(1))

for so, pss in sorted(pss_by_so.items(), key=lambda item: (-item[1], item[0])):
    print(f"{so}\t{pss}")
```

Earlier parser variants kept the last libmmi mapping after the next anonymous header. That can incorrectly add anonymous PSS to the previous library and overstate libmmi cost. Treat large unclassified deltas as residual until smaps, hidumper, and code-path evidence explain them.
