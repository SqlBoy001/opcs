import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PUB=ROOT/'studio/public/assets'
for name,source in json.loads((ROOT/'media-source.json').read_text()).items():
    clip=PUB/(name+'.mp4')
    if not clip.exists():
        subprocess.run(['ffmpeg','-v','error','-n','-ss',str(source['offset']),'-i',source['source'],'-t',str(source['length']),'-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(clip)],check=True)
    still=PUB/(name+'-end.jpg')
    if not still.exists():
        subprocess.run(['ffmpeg','-v','error','-n','-sseof','-0.08','-i',str(clip),'-frames:v','1','-update','1',str(still)],check=True)
    print(name,clip.stat().st_size,flush=True)
