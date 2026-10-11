import hashlib,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parent/'studio/public/fonts/NotoSansSC.ttf'
expected='a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da'
url='https://raw.githubusercontent.com/google/fonts/9710da1eacb3be272583c3224dcb70f9da6eadbb/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf'
if p.exists():
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,'Existing font differs; not overwriting'
 print('Font checksum verified; no download')
else:
 with urllib.request.urlopen(url,timeout=60) as r:data=r.read()
 assert hashlib.sha256(data).hexdigest()==expected,'Font download checksum mismatch'
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 print('Pinned font restored and checksum verified')
