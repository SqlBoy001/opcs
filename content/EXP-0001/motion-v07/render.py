"""Motion-led evidence video. All visual alterations are compositing/annotations."""
import argparse, json, math, subprocess
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

HERE=Path(__file__).resolve().parent; OUT=HERE/'output';OUT.mkdir(exist_ok=True)
BIN=Path('/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/tools/ffmpeg')
D=json.loads((HERE.parent/'content.json').read_text())['motion_v07']
CH={c['id']:c for c in D['chapters']};W,H,FPS=720,1280,24
FONT='/System/Library/Fonts/STHeiti Medium.ttc';WHITE='#F5F8FF';MUTED='#ABBCD1'
PALETTES={'navy':('#071222','#215A73','#70E6E0'),'violet':('#110F28','#403B75','#C2AAFF'),
 'blue':('#091626','#174D80','#79BEFF'),'red':('#25121D','#773F42','#FF9A7D'),
 'green':('#091E20','#235A51','#78E1B7'),'amber':('#1C1714','#64502D','#FFD280')}

@lru_cache(None)
def font(s):return ImageFont.truetype(FONT,s)
def text(im,xy,value,s=30,color=WHITE,anchor=None):
    ImageDraw.Draw(im).multiline_text(xy,value,font=font(s),fill=color,spacing=12,anchor=anchor)
def box(im,bounds,fill=(24,39,58,255),outline=None,r=22):
    ImageDraw.Draw(im).rounded_rectangle(bounds,radius=r,fill=fill,outline=outline,width=2)
def ease(x):x=max(0,min(1,x));return 1-(1-x)**3
def rgb(h):return tuple(int(h[n:n+2],16) for n in (1,3,5))

@lru_cache(None)
def bg(palette):
    a,b,accent=PALETTES[palette];a=np.array(rgb(a));b=np.array(rgb(b))
    y,x=np.mgrid[0:H,0:W];g=np.exp(-((x-620)**2/(650**2)+(y-390)**2/(730**2)))[:,:,None]*.77
    im=Image.fromarray((a*(1-g)+b*g).astype('uint8')).convert('RGBA')
    lines=Image.new('RGBA',(W,H),(0,0,0,0));dr=ImageDraw.Draw(lines)
    for n in range(10):dr.line((n*145-330,0,n*145+470,H),fill=(*rgb(accent),18),width=1)
    return Image.alpha_composite(im,lines)

def shell(ch):
    im=bg(ch['palette']).copy();accent=PALETTES[ch['palette']][2]
    text(im,(36,40),'OPC / AI 漫剧创作实录',20,accent)
    text(im,(586,40),f"{int(ch['id']):02} / 09",20,MUTED)
    ImageDraw.Draw(im).line((36,86,684,86),fill=(*rgb(accent),100),width=1)
    text(im,(36,113),ch['short'],23,accent)
    text(im,(33,160),ch['title'],48)
    return im

@lru_cache(None)
def source(key,crop=None):
    p=D['assets'][key]['path'] if key in D['assets'] else key
    im=Image.open(p).convert('RGB')
    if crop:im=im.crop(crop)
    im.thumbnail((1600,1800),Image.Resampling.LANCZOS)
    return im

def photo(im,key,bounds,t=0,dur=10,crop=None,motion=True,contain=False):
    x,y,x1,y1=bounds;bw,bh=x1-x,y1-y
    src=source(key,crop)
    if contain:
        fitted=ImageOps.contain(src,(bw,bh),Image.Resampling.LANCZOS)
        ImageDraw.Draw(im).rectangle(bounds,fill='#E8E8E8')
        im.paste(fitted,(x+(bw-fitted.width)//2,y+(bh-fitted.height)//2))
        return
    # Slow crop movement never changes image identity or paints over evidence.
    z=1.0+(0.045*min(1,t/dur) if motion else 0)
    fitted=ImageOps.fit(src,(round(bw*z),round(bh*z)),Image.Resampling.BICUBIC)
    cx=(fitted.width-bw)//2;cy=(fitted.height-bh)//2
    fitted=fitted.crop((cx,cy,cx+bw,cy+bh))
    im.paste(fitted,(x,y))
    ImageDraw.Draw(im).rounded_rectangle((x,y,x1,y1),radius=10,outline=(255,255,255,70),width=2)

def plate(im,xy,title,sub,t,delay,accent,width=620):
    progress=ease((t-delay)/.55)
    if not progress:return
    lay=Image.new('RGBA',(width,144),(0,0,0,0));box(lay,(0,0,width-1,143),(15,29,48,238),(*rgb(accent),120))
    text(lay,(25,23),title,34,accent);text(lay,(25,91),sub,23,MUTED)
    lay.putalpha(lay.getchannel('A').point(lambda v:int(v*progress)))
    im.alpha_composite(lay,(xy[0],xy[1]+round(36*(1-progress))))

def callout(im,bounds,label,label_xy,t,delay,accent):
    p=ease((t-delay)/.6)
    if not p:return
    dr=ImageDraw.Draw(im);x0,y0,x1,y1=bounds
    dr.arc(bounds,-90,-90+359*p,fill=accent,width=5)
    lx,ly=label_xy;tw=int(dr.textlength(label,font=font(25)))+32
    dr.line((lx+tw//2,ly+48,(x0+x1)//2,(y0+y1)//2),fill=(*rgb(accent),int(210*p)),width=2)
    layer=Image.new('RGBA',(tw,51),(0,0,0,0));box(layer,(0,0,tw-1,50),(10,18,31,245),accent,r=12);text(layer,(16,11),label,25,accent)
    layer.putalpha(layer.getchannel('A').point(lambda v:int(v*p)))
    im.alpha_composite(layer,(lx,ly-round((1-p)*18)))

def note(im,value):text(im,(36,1071),value,17,MUTED)
def footer(im,ch,t,scene):
    # Full narration, separate from annotations. No implied audio synchrony.
    absframe=scene['start_frame']+int(round(t*24))
    cue=next((c for c in D['captions'] if c['start_frame']<=absframe<c['end_frame']),None)
    layer=Image.new('RGBA',(W,168),(0,0,0,0));box(layer,(24,3,696,164),(4,10,18,227),r=18)
    if cue:
        s=cue['text'];lines=[s] if len(s)<=20 else [s[:20],s[20:]]
        for n,line in enumerate(lines):
            width=ImageDraw.Draw(layer).textlength(line,font=font(30));text(layer,((W-width)/2,48+n*42-(18 if len(lines)>1 else 0)),line,30)
    im.alpha_composite(layer,(0,1104))
    ImageDraw.Draw(im).rectangle((24,1269,696,1272),fill=(60,75,94))
    ImageDraw.Draw(im).rectangle((24,1269,24+int(672*absframe/4320),1272),fill=PALETTES[ch['palette']][2])

class Video:
    def __init__(self,key,start,duration,width,height):
        self.width=width;self.height=height;self.last=None
        self.proc=subprocess.Popen([str(BIN/'ffmpeg'),'-v','error','-ss',str(start),'-t',str(duration),'-i',D['assets'][key]['path'],'-an','-vf',f'fps=24,scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    def read(self):
        need=self.width*self.height*3;data=self.proc.stdout.read(need)
        if len(data)==need:self.last=Image.frombytes('RGB',(self.width,self.height),data)
        return self.last
    def close(self):
        self.proc.stdout.close();self.proc.terminate();self.proc.wait()

def scene_frame(s,t,vids=None):
    ch=CH[s['chapter']];im=shell(ch);ac=PALETTES[ch['palette']][2];kind=s['kind'];dur=s['duration'];vids=vids or {}
    if kind=='hero':
        photo(im,'09-film-at-54s',(0,320,720,930),t,dur,crop=(220,0,1060,720))
        plate(im,(40,889),'先不买课，先自己跑一遍','这是一轮真实实验，不是收益教学',t,.4,ac)
    elif kind=='prep':
        items=[('故事','先讲清冲突'),('人物','时代、身份、处境'),('工具','文字、图像、视频'),('预算','失败和重制也要算')]
        for n,(title,sub) in enumerate(items):
            p=ease((t-n*.7)/.55);x=36+n%2*336;y=334+n//2*339
            if p:
                lay=Image.new('RGBA',(312,305));box(lay,(0,0,311,304),(21,24,51,245),(*rgb(ac),150))
                text(lay,(22,20),f'0{n+1}',28,ac);text(lay,(22,89),title,58);text(lay,(22,228),sub,23,MUTED)
                lay.putalpha(lay.getchannel('A').point(lambda a:int(a*p)));im.alpha_composite(lay,(x+round(75*(1-p)),y))
    elif kind=='tools':
        for n,(title,sub) in enumerate([('写 / 文字模型','DeepSeek：整理角色资料'),('画 / 图像工具','Seedream + 图片工具：参考与修正'),('动 / 视频模型','本轮视频：Seedance 2.5')]):plate(im,(50,337+n*230),title,sub,t,n*.8,ac)
        note(im,'本次实际工具分工 · 不是通用最优组合')
    elif kind in ('build_before','build_after'):
        key='01-projects-before' if kind=='build_before' else '02-projects-after'
        photo(im,key,(28,344,692,840),t,dur,crop=None)
        plate(im,(38,882),'改版前' if kind=='build_before' else '整理创作入口与制作流程','基于 LocalMiniDrama 继续开发',t,.4,ac)
        note(im,'历史工作台截图 · 此处只展示界面整理')
    elif kind=='era_sample':
        photo(im,'wrong_soldier',(171,299,569,1044),t,dur,crop=(900,80,1530,1440),motion=False,contain=True)
        callout(im,(324,309,420,367),'帽檐',(38,339),t,.8,ac)
        callout(im,(320,406,412,473),'立领',(530,431),t,2.6,ac)
        callout(im,(316,470,416,615),'双排扣',(32,601),t,4.5,ac)
        note(im,'旧项目5真实角色图 · 2026-09-26 13:14')
    elif kind=='era_prompt':
        photo(im,'wrong_soldier',(26,319,359,993),t,dur,crop=(0,85,880,1470))
        box(im,(382,358,695,984),(18,20,35,245),(*rgb(ac),130))
        text(im,(404,390),'问题已写进\n提示词',34,ac)
        for n,word in enumerate(['立领','双排扣','帽檐','裤中缝']):text(im,(410,556+n*87),word,38,WHITE if n<min(4,int(t)+1) else '#544E58')
        note(im,'右侧摘录该图真实生成提示词 · 非事后编造')
    elif kind=='era_compare':
        photo(im,'wrong_soldier',(30,340,347,1008),t,dur,crop=(900,80,1530,1440),motion=False,contain=True)
        photo(im,'first_pass',(372,340,690,1008),t,dur,crop=(0,3120,240,3640),motion=False,contain=True)
        text(im,(45,295),'重制前 / 时代违和',23,'#FF9A7D');text(im,(380,295),'重制首轮 / 古代设定',23,'#78E1B7')
        callout(im,(425,505,661,741),'札甲 / 古代服制',(401,937),t,1,'#78E1B7')
        note(im,'真实前后版本 · 这里只对比时代与服制')
    elif kind=='sync':
        for n,(title,sub) in enumerate([('人物卡已经换新','脸、发型和服装设定已更新'),('分镜还保留旧答案','旧描述 → 旧图 → 继续往下生成'),('让改动真正传下去','同步依赖，失效旧引用，再核对')]):plate(im,(50,333+n*230),title,sub,t,n*1.0,ac if n!=1 else '#FF9A7D')
        note(im,'流程示意 · 对应真实旧描述问题')
    elif kind=='warning':
        photo(im,'05-storyboard',(28,333,692,935),t,dur,crop=(232,112,1000,813),motion=False)
        callout(im,(152,336,403,368),'角色已更新，旧素材要核对',(82,960),t,.7,ac)
        note(im,'真实历史截图 · 裁出版本提醒与图片区域')
    elif kind=='state':
        photo(im,'08-film-at-07s',(0,320,720,1020),t,dur,crop=(440,15,1210,720))
        callout(im,(353,500,505,716),'衣料有磨损 / 脏痕',(26,395),t,1.0,ac)
        note(im,'检查版真实画面 · 押送状态')
    elif kind=='state_detail':
        photo(im,'08-film-at-07s',(24,336,350,964),t,dur,crop=(560,100,1020,715))
        photo(im,'09-film-at-54s',(370,336,697,964),t,dur,crop=(730,70,1070,720),motion=False)
        callout(im,(395,402,642,535),'周雎 / 木枷',(448,558),t,.5,ac)
        callout(im,(62,797,300,940),'女主 / 脚镣',(43,962),t,1.4,ac)
        note(im,'身份相同之外，还要符合这一场的处境')
    elif kind=='shackle':
        photo(im,'bad_shackle',(20,310,700,1024),t,dur,crop=(900,530,1750,1420),motion=False)
        callout(im,(147,780,625,1000),'新问题：脚镣比例失真',(101,634),t,.5,'#FF9A7D')
        note(im,'真实失败候选 · 原图未修改')
    elif kind=='compare':
        text(im,(35,300),'原片 / S007',24,'#FF9A7D');text(im,(35,677),'剪辑版 / S007',24,ac)
        for key,y in [('raw',337),('edit',712)]:
            frame=vids[key].read()
            if frame:im.paste(frame,(40,y))
        note(im,'同速对照 · 播放后定格供讲解')
    elif kind=='action':
        key='edit';frame=vids[key].read()
        if frame:im.paste(frame,(36,348))
        labels=['接近刀柄','切对方反应','回到持刀结果']
        for n,label in enumerate(labels):
            x=32+n*232;p=ease((t-n*1.3)/.5)
            if p:
                box(im,(x,801,x+218,981),(28,34,45,240),ac);text(im,(x+17,832),f'0{n+1}',30,ac);text(im,(x+17,919),label,24)
        note(im,'前6秒原速播放，随后定格拆解 · 改善来自剪辑')
    elif kind=='cost_scope':
        text(im,(44,343),'09 / 26',70,ac);text(im,(44,435),'13:00 起',43)
        plate(im,(45,541),'旧项目 5 ＋ 重制版 6','把重制前的错误也算进来',t,.3,ac)
        plate(im,(45,738),'72 条图片 / 11 条视频记录','记录数不是收费次数，也不是可用率',t,1.1,ac)
        note(im,'本地只读记录 · 北京时间筛选')
    elif kind=='cost_cash':
        text(im,(44,337),'可核实的火山按量现金',30,MUTED)
        value=74.92*ease(t/1.1)
        text(im,(37,411),f'¥{value:.2f}',103,ac)
        text(im,(45,560),'已有账单快照 / 不是全成本',27)
        plate(im,(44,646),'同规格视频原价：约 ¥9.14 / 次','6秒 · 720p · Seedance 2.5',t,.2,ac)
        plate(im,(44,836),'套餐购买、其他工具、人工另计','不用整个账户月费硬摊到这一集',t,1.2,ac)
        note(im,'已保存账单：9/30快照 · 实时区间复核待登录')
    elif kind=='budget':
        text(im,(43,328),'继续优化：先留',31,MUTED)
        text(im,(31,394),'¥40–60',105,ac)
        text(im,(43,540),'情景预算 · 尚未花费',27)
        plate(im,(45,615),'2–3 个问题镜头 × 最多 2 次','S005 踢击 / S007 取刀 / 可选 S009',t,.2,ac)
        plate(im,(45,805),'保留其他镜头，只改最不自然的部分','预算不等于保证变自然',t,1.1,ac)
        note(im,'视频原价＋4–6张Seedream参考图；不含人工')
    elif kind in ('result','closing'):
        frame=vids['final'].read()
        if frame:im.paste(frame,(0,330))
        if kind=='result':plate(im,(45,900),'这次留下：60 秒漫剧检查版','生成 → 找错 → 重做 / 改镜头',t,.4,ac)
        else:plate(im,(45,900),'下一轮只修最不自然的几镜','不是无限抽卡，是带着问题再试',t,.4,ac)
        note(im,'本次真实产物片段 · 未发布复盘草稿')
    else:raise ValueError(kind)
    footer(im,ch,t,s)
    return im

def videos(s):
    k=s['kind']
    if k=='compare':return {v:Video(v,0,6.1,640,360) for v in ('raw','edit')}
    if k=='action':return {'edit':Video('edit',0,6.1,648,365)}
    if k in ('result','closing'):return {'final':Video('final',48 if k=='result' else 7,s['duration'],720,550)}
    return {}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--only');ap.add_argument('--reuse',action='store_true');args=ap.parse_args()
    scenes=[s for s in D['shots'] if not args.only or s['kind']==args.only]
    previous=None
    for s in scenes:
        target=OUT/(s['id']+'.mp4')
        if args.reuse and target.exists():continue
        vs=videos(s)
        if args.preview:
            t=min(6,s['duration']-.1)
            # Videos are advanced to the same illustrative time for previews.
            for v in vs.values():
                for _ in range(round(t*24)):v.read()
            scene_frame(s,t,vs).convert('RGB').save(OUT/(s['id']+'.png'))
            for v in vs.values():v.close()
            continue
        cmd=[str(BIN/'ffmpeg'),'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','24','-i','-','-an','-c:v','libx264','-threads','4','-preset','veryfast','-crf','27','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        first=None
        for n in range(s['duration']*24):
            im=scene_frame(s,n/24,vs).convert('RGB')
            if n==0:first=im.copy()
            # Alternate chapter cross-dissolves and image wipes, 12 frames.
            if previous is not None and n<12:
                p=ease(n/11)
                if int(s['chapter'])%2:
                    im=Image.blend(previous,im,p)
                else:
                    reveal=round(W*p);mix=previous.copy();mix.paste(im.crop((0,0,reveal,H)),(0,0));im=mix
            proc.stdin.write(im.tobytes())
            if n==min(144,s['duration']*24-1):im.save(OUT/(s['id']+'.png'))
        previous=im.copy()
        proc.stdin.close();assert proc.wait()==0,s['id']
        for v in vs.values():v.close()
        print('rendered',s['id'],flush=True)
    if not args.preview and not args.only:
        manifest=OUT/'concat.txt';manifest.write_text(''.join(f"file '{s['id']}.mp4'\n" for s in D['shots']))
        subprocess.run([str(BIN/'ffmpeg'),'-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy','-movflags','+faststart',str(OUT/'OPC-2-v07-motion-180s.mp4')],check=True)

if __name__=='__main__':main()
