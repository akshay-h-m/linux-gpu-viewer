import re

def load_pci_ids(path="data/pci.ids"):
    ids = {}
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = re.match(r'^([0-9a-f]{4})\s+(.+)$', line, re.I)
            if m:
                ids[m.group(1).lower()] = m.group(2)
    return ids
