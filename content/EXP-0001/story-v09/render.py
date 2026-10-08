"""Story edit using real media, cached layouts and frame-aligned captions."""
import argparse,importlib.util,json,subprocess
from pathlib import Path
from functools import lru_cache
from PIL import Image,ImageDraw,ImageOps
HERE=Path(__file__).resolve().parent;OUT=HERE/'output';OUT.mkdir(exist_ok=True)
D=json.loads((HERE.parent/'content.json').read_text())['story_v09'];CH={c['id']:c for c in D['chapters']}
spec=importlib.util.spec_from_file_location('v08',HERE.parent/'recap-v08/render.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
old=base.old;BIN=base.BIN;txt=base.txt;font=base.font
SOURCE=HERE.parent/'recap-v08/output/OPC-2-v08-recap-180s.mp4'
class Reader:
 def __init__(self,path,start,duration,w=720,h=660):
  self.w=w;self.h=h
  self.p=subprocess.Popen([str(BIN/'ffmpeg'),'-v','error','-threads','2','-ss',str(start),'-t',str(duration),'-i',str(path),'-an','-vf',f'fps=24,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 def read(self):
  b=self.p.stdout.read(self.w*self.h*3)
  assert len(b)==self.w*self.h*3,'Short decoded frame'
  return Image.frombytes('RGB',(self.w,self.h),b)
 def close(self):self.p.stdout.close();self.p.terminate();self.p.wait();self.p.stderr.close()
def photo(im,key,bounds,crop=None,contain=False):
 src=Image.open(D['assets'][key]['path']).convert('RGB')
 if crop:src=src.crop(crop)
 x,y,x1,y1=bounds;w,h=x1-x,y1-y
 if contain:
  fit=ImageOps.contain(src,(w,h),Image.Resampling.LANCZOS);ImageDraw.Draw(im).rectangle(bounds,fill='#E8E8E8');im.paste(fit,(x+(w-fit.width)//2,y+(h-fit.height)//2))
 else:im.paste(ImageOps.fit(src,(w,h),Image.Resampling.LANCZOS),(x,y))
@lru_cache(None)
def sub(index):
 c=D['captions'][index];im=old.bg(CH[c['chapter']]['palette']).crop((0,1104,720,1280)).convert('RGB');dr=ImageDraw.Draw(im);s=c['display_text'];size=36
 while dr.textlength(s,font=font(size))>648:size-=1
 assert size>=31,(s,size)
 dr.text(((720-dr.textlength(s,font=font(size)))/2,70),s,font=font(size),fill='white',stroke_width=1,stroke_fill='#122034');return im
@lru_cache(None)
def layout(kind,stage=0):
 s=next(s for s in D['shots'] if s['kind']==kind);im=old.bg(CH[s['chapter']]['palette']).convert('RGB');ac='#76E4E0'
 txt(im,(36,42),'一个人的 OPC 实验 / AI 漫剧',22,ac)
 headings={'hook_costume':'古装押送兵，\n怎么穿成了这样？','hook_shackle':'衣服改了，\n脚镣又大成这样','hook_result':'为了做出这 60 秒','hook_promise':'怎么做 · 哪里翻车\n又花了多少钱？','earned_result':'折腾到这里，\n留下了这版 60 秒','startup':'第一次熟悉制作','episode':'后面这版 60 秒','connected':'每一步，都要接起来','lesson_replay':'先修设定，也能换镜头讲','closing':'前面的小错误，\n可能变成后面的返工'}
 txt(im,(33,126),headings[kind],48)
 if kind=='hook_costume':
  photo(im,'wrong_soldier',(150,300,570,1050),(900,80,1530,1440),True)
 elif kind=='hook_shackle':
  photo(im,'bad_shackle',(0,320,720,1040),(900,530,1750,1420))
 elif kind=='hook_promise':
  photo(im,'02-projects-after',(30,325,690,705))
  photo(im,'08-film-at-07s',(30,725,353,1025),(480,20,1090,720))
  photo(im,'09-film-at-54s',(373,725,690,1025),(540,0,1160,720))
 elif kind=='startup':
  photo(im,'02-projects-after',(30,320,690,900),contain=True)
 elif kind=='connected':
  photo(im,'03-ai-create',(30,315,690,610),contain=True)
  photo(im,'05-storyboard',(30,630,690,1010),(232,112,1000,813),True)
 elif kind in ('lesson_replay','closing') and stage==0:
  photo(im,'wrong_soldier',(24,300,348,1000),(900,80,1530,1440),True)
  photo(im,'first_pass',(372,300,696,1000),(0,3120,240,3640),True)
 return im

def banner(im,main,small='',y=907,color='#78E1E0'):
 lay=Image.new('RGBA',(660,142),(0,0,0,0));ImageDraw.Draw(lay).rounded_rectangle((0,0,659,141),radius=20,fill=(8,21,35,236))
 size=36
 while ImageDraw.Draw(lay).textlength(main,font=font(size))>612:size-=1
 assert size>=24,main
 txt(lay,(24,17),main,size,color)
 if small:txt(lay,(24,82),small,23,'#D0DAE7')
 im.paste(lay,(30,y),lay)
def frame(s,n,video=None):
 k=s['kind'];t=n/24;stage=int(t>=4) if k=='lesson_replay' else int(t>=3) if k=='closing' else 0
 im=layout(k,stage).copy()
 if video:im.paste(video,(0,310))
 if k=='hook_costume':
  im=im.convert('RGBA');old.callout(im,(315,310,422,375),'帽檐',(29,350),t,0,'#FFAA8A');old.callout(im,(305,445,431,634),'立领 / 双排扣',(385,706),t,.6,'#FFAA8A');im=im.convert('RGB')
 elif k=='hook_shackle':
  im=im.convert('RGBA');old.callout(im,(110,790,649,1029),'脚镣比例失真',(155,668),t,0,'#FFAA8A');im=im.convert('RGB')
 elif k=='hook_result':banner(im,'搭工作台，再一轮轮返工','本次真实成片片段 / 60秒检查版')
 elif k=='earned_result':banner(im,'这一轮的产物：60秒检查版','本次真实产物 / 60秒检查版')
 elif k=='startup':banner(im,'前期先充 ¥200','火山节省计划 · 搭建 / 调接口 / 跑测试')
 elif k=='episode':banner(im,'本次生成与修改 ≈ ¥75','DeepSeek、MiniMax 尚未计入')
 elif k=='connected':
  labels=['故事 / 人物','参考 / 分镜','生成视频','剪辑']
  # A compact process ribbon over real workbench imagery, not a new checklist page.
  idx=min(3,int(t/2));banner(im,' → '.join(labels[max(0,idx-1):min(4,idx+2)]),'从设定到成片，逐步检查再往下走')
 elif k=='lesson_replay':banner(im,'先核对设定，再同步下游' if not stage else '动作不顺，也可以换镜头讲','真实重制前后' if not stage else '取刀剪辑片段 / 改善来自剪辑')
 elif k=='closing':banner(im,'把错误拦在下一步之前','少把错误参考，带进下一次付费生成')
 return im

def streams_for(s):
 k=s['kind'];a=D['assets'];dur=s['duration']
 if k=='hook_result':return [Reader(a['final']['path'],7,2),Reader(a['final']['path'],50,2)]
 if k=='earned_result':return [Reader(a['final']['path'],49,dur)]
 if k=='episode':return [Reader(a['final']['path'],35,dur)]
 if k=='lesson_replay':return [Reader(a['edit']['path'],0,4)]
 if k=='closing':return [Reader(a['final']['path'],50,4)]
 return []
def get_video(s,n,readers):
 if not readers:return None
 if s['kind']=='hook_result':return readers[int(n>=48)].read()
 if s['kind']=='lesson_replay':return readers[0].read() if n>=96 else None
 if s['kind']=='closing':return readers[0].read() if n>=72 else None
 return readers[0].read()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 cue=0;previous=None
 enc=None
 if not args.preview:enc=subprocess.Popen([str(BIN/'ffmpeg'),'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','24','-i','-','-an','-c:v','libx264','-threads','4','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'OPC-2-v09-story-185s.mp4')],stdin=subprocess.PIPE)
 body=None
 for s in D['shots']:
  middle=s['chapter'] in ('02','03','04','05','06','07')
  if args.preview and middle:continue
  if middle and body is None:body=Reader(SOURCE,10,120,720,1280)
  rs=[] if middle else streams_for(s)
  lead=None
  if middle and s['kind']=='prep':
   # Skip the old opener's dissolve remnants while preserving frame count.
   for _ in range(13):lead=body.read()
  limit=min(s['duration']*24,49 if s['chapter']=='01' else 145) if args.preview else s['duration']*24
  for n in range(limit):
   im=(lead.copy() if lead is not None and n<13 else body.read()) if middle else frame(s,n,get_video(s,n,rs))
   absolute=s['start_frame']+n
   while absolute>=D['captions'][cue]['end_frame']:cue+=1
   im.paste(sub(cue),(0,1104))
   # Hook uses clean cuts. Later newly composed scenes dissolve for 8 frames.
   if previous is not None and n<8 and ((not middle and s['chapter']!='01') or s['kind']=='prep'):im=Image.blend(previous,im,old.ease(n/7))
   if enc:enc.stdin.write(im.tobytes())
   if n==min(limit-1,48 if s['chapter']=='01' else 144):im.save(OUT/(s['id']+'.png'))
  previous=im.copy()
  for r in rs:r.close()
  print('rendered',s['id'],flush=True)
 if body:body.close()
 if enc:enc.stdin.close();assert enc.wait()==0
if __name__=='__main__':main()
