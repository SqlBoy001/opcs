"""Reuse approved v07 front section; replace all captions and the last 50 seconds."""
import argparse, importlib.util, json, subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;OUT=HERE/'output';OUT.mkdir(exist_ok=True)
D=json.loads((HERE.parent/'content.json').read_text())['recap_v08'];CH={c['id']:c for c in D['chapters']}
BIN=Path('/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/tools/ffmpeg')
FONT='/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc'
spec=importlib.util.spec_from_file_location('prior_renderer',HERE.parent/'motion-v07/render.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
SOURCE=HERE.parent/'motion-v07/output/OPC-2-v07-motion-180s.mp4'
@lru_cache(None)
def font(size):return ImageFont.truetype(FONT,size,index=11)
def txt(im,xy,value,size=30,color='#F5F8FF'):
 ImageDraw.Draw(im).multiline_text(xy,value,font=font(size),fill=color,spacing=14)
def image(im,key,bounds,crop=None):
 src=Image.open(D['assets'][key]['path']).convert('RGB')
 if crop:src=src.crop(crop)
 x,y,x1,y1=bounds;im.paste(ImageOps.fit(src,(x1-x,y1-y),Image.Resampling.LANCZOS),(x,y))
@lru_cache(None)
def caption(index):
 c=D['captions'][index];pal=CH[c['chapter']]['palette'];lay=old.bg(pal).crop((0,1104,720,1280)).convert('RGB')
 # No card: the chapter background continues behind bold, compact captions.
 dr=ImageDraw.Draw(lay);s=c['display_text'];size=36
 while dr.textlength(s,font=font(size))>648:size-=1
 assert size>=31,(s,size)
 w=dr.textlength(s,font=font(size));dr.text(((720-w)/2,70),s,font=font(size),fill='white',stroke_width=1,stroke_fill='#122034')
 return lay
@lru_cache(None)
def canvas(kind,phase=0):
 shot=next(s for s in D['shots'] if s['kind']==kind);ch=CH[shot['chapter']];im=old.bg(ch['palette']).convert('RGB');ac=old.PALETTES[ch['palette']][2]
 txt(im,(36,38),'OPC / AI 漫剧创作实录',20,ac);txt(im,(580,38),f"{ch['id']} / 09",20,'#ABBCD1')
 ImageDraw.Draw(im).line((36,86,684,86),fill='#426478',width=1)
 txt(im,(36,113),ch['short'],23,ac);txt(im,(33,162),ch['title'],46)
 if kind=='startup':
  image(im,'02-projects-after',(36,323,684,755))
  txt(im,(42,799),'¥200',86,ac);txt(im,(344,823),'前期入门调试',28)
  txt(im,(45,923),'先充火山节省计划',32)
  txt(im,(45,985),'搭工作台 · 调接口 · 跑测试',26,'#BBCBDD')
 elif kind=='episode':
  txt(im,(43,753),'≈ ¥75',90,ac);txt(im,(420,790),'这次 60 秒',30)
  txt(im,(45,904),'生成 + 修改',32)
  txt(im,(45,970),'DeepSeek、MiniMax 尚未计入',26,'#BBCBDD')
  txt(im,(45,1026),'转场、打斗再打磨，还要继续投入',25,ac)
 elif kind=='flow':
  image(im,'03-ai-create',(36,320,684,620),crop=(160,70,1190,600))
  labels=['故事 / 人物设定','参考图 / 分镜','视频生成','剪辑 / 输出']
  for i,label in enumerate(labels):
   y=665+i*96;active=i<=phase
   txt(im,(47,y),f'0{i+1}',29,ac if active else '#485A66');txt(im,(116,y),label,33,'#F5F8FF' if active else '#485A66')
   if active:ImageDraw.Draw(im).line((46,y+70,674,y+70),fill='#35566B',width=1)
 elif kind=='lessons':
  # Real wrong costume / first corrected reference, with full bodies preserved.
  for key,bounds,crop in [('wrong_soldier',(35,320,346,810),(900,80,1530,1440)),('first_pass',(374,320,685,810),(0,3120,240,3640))]:
   src=Image.open(D['assets'][key]['path']).convert('RGB').crop(crop);fit=ImageOps.contain(src,(bounds[2]-bounds[0],bounds[3]-bounds[1]),Image.Resampling.LANCZOS)
   ImageDraw.Draw(im).rectangle(bounds,fill='#E8E8E8');im.paste(fit,(bounds[0]+(bounds[2]-bounds[0]-fit.width)//2,bounds[1]+(bounds[3]-bounds[1]-fit.height)//2))
  for i,label in enumerate(['先核对时代、人物与处境','修改后同步下游参考','动作不顺，也能换镜头讲']):txt(im,(46,856+i*76),label,30,ac if i==phase else '#F5F8FF')
 elif kind=='closing':
  txt(im,(40,943),'流程跑一遍',29,ac);txt(im,(388,943),'错误逐步改',29,ac)
  txt(im,(40,1011),'费用分开算，优化留预算',33)
 return im
class Reader:
 def __init__(self,path,start,duration,w,h):
  self.w=w;self.h=h
  self.p=subprocess.Popen([str(BIN/'ffmpeg'),'-v','error','-threads','2','-ss',str(start),'-t',str(duration),'-i',str(path),'-an','-vf',f'fps=24,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 def read(self):
  b=self.p.stdout.read(self.w*self.h*3)
  assert len(b)==self.w*self.h*3,'Unexpected short media frame'
  return Image.frombytes('RGB',(self.w,self.h),b)
 def close(self):self.p.stdout.close();self.p.terminate();self.p.wait()
def phase_for(kind,t):return min(3,int(t/2)) if kind=='flow' else min(2,int(t/2.3)) if kind=='lessons' else 0
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 if args.preview:
  r=Reader(SOURCE,45,1,720,1280);im=r.read();r.close();idx=next(i for i,c in enumerate(D['captions']) if c['start_frame']<=1080<c['end_frame']);im.paste(caption(idx),(0,1104));im.save(OUT/'preview-subtitle.png')
  for s in D['shots'][15:]:
   im=canvas(s['kind'],3 if s['kind']=='flow' else 1).copy()
   if s['kind'] in ('episode','closing'):
    w,h=(648,365) if s['kind']=='episode' else (720,570);r=Reader(D['assets']['final']['path'],47,1,w,h);im.paste(r.read(),(36,330) if s['kind']=='episode' else (0,320));r.close()
   idx=next(i for i,c in enumerate(D['captions']) if c['start_frame']<=s['start_frame']+96<c['end_frame']);im.paste(caption(idx),(0,1104));im.save(OUT/(s['id']+'.png'))
  return
 enc=subprocess.Popen([str(BIN/'ffmpeg'),'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','24','-i','-','-an','-c:v','libx264','-threads','4','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'OPC-2-v08-recap-180s.mp4')],stdin=subprocess.PIPE)
 r=Reader(SOURCE,0,130,720,1280);cue=0;last=None
 for n in range(3120):
  im=r.read()
  while n>=D['captions'][cue]['end_frame']:cue+=1
  im.paste(caption(cue),(0,1104));enc.stdin.write(im.tobytes());last=im
  if n%720==0:print(f'front {n//24}/130s',flush=True)
 r.close()
 for s in D['shots'][15:]:
  kind=s['kind'];r=None
  if kind in ('episode','closing'):
   w,h=(648,365) if kind=='episode' else (720,570);r=Reader(D['assets']['final']['path'],35 if kind=='episode' else 47,s['duration'],w,h)
  for n in range(s['duration']*24):
   im=canvas(kind,phase_for(kind,n/24)).copy()
   if r:im.paste(r.read(),(36,330) if kind=='episode' else (0,320))
   absolute=s['start_frame']+n
   while absolute>=D['captions'][cue]['end_frame']:cue+=1
   im.paste(caption(cue),(0,1104))
   if n<10:im=Image.blend(last,im,old.ease(n/9))
   enc.stdin.write(im.tobytes())
   if n==96:im.save(OUT/(s['id']+'.png'))
  last=im
  if r:r.close()
  print('rendered',s['id'],flush=True)
 enc.stdin.close();assert enc.wait()==0
if __name__=='__main__':main()
