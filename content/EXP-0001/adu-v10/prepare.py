import json,subprocess,hashlib,shutil,math,wave,re
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent; P=ROOT/'project'; FPS=60; SR=48000
SRC=Path('/Users/shenzihao/.hifox/organizations/040a2449-fbf3-4ec1-b87e-18aeaed0d2a4/runs/2026/09/d5cdf3e3-63cc-42cb-9cd2-65a1e2551c6a/workdir/opcs/content/EXP-0001/content.json')
D=json.loads(SRC.read_text())['story_v09']; (ROOT/'content-source-v09.json').write_text(json.dumps(D,ensure_ascii=False,indent=2))
V=P/'voice-parts';V.mkdir(exist_ok=True)
FF='/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/tools/ffmpeg/ffmpeg'
segments=[]; subs=[]; cursor=0; shots=[]
for shot in D['shots']:
 start=cursor
 for c in [c for c in D['captions'] if c['shot']==shot['kind']]:
  i=len(subs);a=V/f'{i:03}.aiff';w=V/f'{i:03}.wav'
  if not a.exists():subprocess.run(['say','-v','Eddy (中文（中国大陆）)','-r','220','-o',str(a),c['text']],check=True)
  subprocess.run([FF,'-v','error','-y','-i',str(a),'-ac','1','-ar',str(SR),str(w)],check=True)
  with wave.open(str(w),'rb') as f: data=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()
  # Generated each complete caption separately: boundaries measured from real files, not character ratios.
  lead=5760 if i==0 else 0
  pad=math.ceil((len(data)+lead+3840)/(SR/FPS))*int(SR/FPS)-len(data)-lead
  seg=np.concatenate([np.zeros(lead,dtype=np.int16),data,np.zeros(pad,dtype=np.int16)])
  subs.append(dict(id=i,zh=c['display_text'],t0=cursor/SR,t1=(cursor+lead+len(data))/SR,shot=shot['kind'],source_text=c['text'],speech_start=(cursor+lead)/SR,speech_end=(cursor+lead+len(data))/SR))
  segments.append(seg);cursor+=len(seg)
 end=cursor
 shots.append(dict(**shot,t0=start/SR,t1=end/SR,cues=[s for s in subs if s['shot']==shot['kind']]))
 print('voice',shot['kind'],round((end-start)/SR,2),flush=True)
# Leave an intentional end hold after the last spoken line.
segments.append(np.zeros(SR,dtype=np.int16));cursor+=SR;shots[-1]['t1']=cursor/SR
voice=np.concatenate(segments)
with wave.open(str(P/'voice.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes(voice.tobytes())
END=cursor/SR
(P/'timeline.json').write_text(json.dumps(dict(end=END,fps=FPS,shots=shots,subtitles=subs),ensure_ascii=False,indent=2))
(P/'timeline.js').write_text('window.TIMELINE='+json.dumps(dict(end=END,shots=shots),ensure_ascii=False)+';\n')
(P/'subs.js').write_text('window.SUBS='+json.dumps(subs,ensure_ascii=False)+';\n')
def stamp(t):
 m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
(ROOT/'subtitles.srt').write_text('\n'.join(f'{i+1}\n{stamp(s["t0"])} --> {stamp(s["t1"])}\n{s["zh"]}\n' for i,s in enumerate(subs)))
(ROOT/'voiceover.txt').write_text('\n'.join(c['text'] for c in D['captions']))
# Only crop/resize true evidence. Keep originals untouched and preserve source hashes.
crops={'soldier':('wrong_soldier',(900,80,1530,1440)), 'prompt':('wrong_soldier',(0,85,880,1470)), 'correct':('first_pass',(0,3120,240,3640)), 'shackle':('bad_shackle',(900,530,1750,1420)), 'storyboard':('05-storyboard',(232,112,1000,813)), 'state':('08-film-at-07s',(440,15,1210,720)), 'stateleg':('08-film-at-07s',(560,100,1020,715)), 'statecollar':('09-film-at-54s',(730,70,1070,720))}
for key in ['01-projects-before','02-projects-after','03-ai-create','04-review-workbench','05-storyboard','06-dark-theme','08-film-at-07s','09-film-at-54s']:crops[key]=(key,None)
media=[]
for name,(key,crop) in crops.items():
 im=Image.open(D['assets'][key]['path']).convert('RGB')
 if crop:im=im.crop(crop)
 im.thumbnail((1600,1600),Image.Resampling.LANCZOS);im.save(P/'assets'/f'{name}.jpg',quality=94)
 media.append(dict(file=f'assets/{name}.jpg',source=D['assets'][key],crop=crop))
(ROOT/'media-provenance.json').write_text(json.dumps(media,ensure_ascii=False,indent=2))
config=dict(brand='OPC 实验记录',demo=False,fps=FPS,width=1080,height=1920,end=END,subtitles=True,subtitlePreset='standard',subtitleStyle=dict(zhSize=48),subtitlePosition=dict(bottomRatio=.12,leftRatio=.085,rightRatio=.085),race=dict(labels=[],keys=[]))
(P/'config.js').write_text('window.CONFIG='+json.dumps(config,ensure_ascii=False)+';')
print('TOTAL',END,'captions',len(subs),flush=True)
