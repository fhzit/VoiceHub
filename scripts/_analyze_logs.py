import json
from collections import Counter

data = json.load(open('/opt/data/cache/documents/doc_7b2cec5a4c4e_message.txt'))
print('entries:', len(data))

levels = Counter()
versions = Counter()
paths = Counter()
errors = []

for e in data:
    src = e.get('source', {})
    lvl = src.get('level', '?')
    levels[lvl] += 1
    msg = src.get('message', '')
    w = e.get('$workers', {})
    v = (w.get('scriptVersion') or {}).get('id', '?')
    versions[v] += 1
    req = (w.get('event') or {}).get('request') or {}
    p = req.get('path', req.get('url', '?'))
    paths[p] += 1
    if lvl in ('error', 'warn'):
        errors.append((e.get('timestamp'), lvl, p, msg[:300]))

print('levels:', dict(levels))
print('versions:', dict(versions))
print()
print('--- error/warn entries:', len(errors))
for ts, lvl, p, msg in errors:
    print(f'[{lvl}] {ts} {p}')
    print(f'    {msg}')
    print()

print('--- top paths:')
for p, n in paths.most_common(15):
    print(f'{n:3d}  {p}')
