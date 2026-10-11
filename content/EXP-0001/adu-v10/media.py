import json,sys,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P=ROOT/'project'
SK=Path('/Users/shenzihao/.hifox/organizations/040a2449-fbf3-4ec1-b87e-18aeaed0d2a4/runs/2026/09/d5cdf3e3-63cc-42cb-9cd2-65a1e2551c6a/codex-home/skills/adu-motion-video')
sys.path.insert(0,str(SK/'scripts'));from color_management import image_plan
D=json.loads((ROOT/'content-source-v09.json').read_text());timeline=json.loads((P/'timeline.json').read_text());shot={x['kind']:x for x in timeline['shots']}
video={};colors=[]
for key,src,offset,length in [('resultA','final',7,4),('resultB','final',49,16),('resultC','final',32,18),('raw','raw',0,6),('edit','edit',0,6)]:
 path=D['assets'][src]['path'];plan=image_plan(Path(path));out=P/'sc'/key;out.mkdir(exist_ok=True)
 vf=plan['filter'] if 'filter' in plan else None
 print(key,plan,flush=True)
 if not vf:raise RuntimeError('No color filter')
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(offset),'-i',path,'-t',str(length),'-an','-vf',vf+',fps=24,scale=1080:-2','-q:v','3',str(out/'f_%04d.jpg')],check=True)
 n=len(list(out.glob('*.jpg')));video[key]=dict(n=n,fps=24,offset=offset,source=path,length=n/24)
 colors.append(dict(key=key,plan=plan,source=D['assets'][src],offset=offset,frameCount=n))
(P/'media.js').write_text('window.MEDIA='+json.dumps(video)+';')
(ROOT/'media-color.json').write_text(json.dumps(colors,ensure_ascii=False,indent=2))
