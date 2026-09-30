"""Render an editorial video layout using existing evidence, with full captions."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE=Path(__file__).resolve().parent
OUT=HERE/'output'; OUT.mkdir(exist_ok=True)
FF=Path('/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/tools/ffmpeg/ffmpeg')
FONT='/System/Library/Fonts/STHeiti Medium.ttc'
DATA=json.loads((HERE.parent/'content.json').read_text())['explained_v06']
BG='#F3F0E8'; INK='#203332'; TEAL='#167D77'; MUTED='#67746D'; ORANGE='#C46336'; WHITE='#FFFFFF'

def f(size): return ImageFont.truetype(FONT,size)
def txt(im,x,y,value,size=30,fill=INK):
    ImageDraw.Draw(im).multiline_text((x,y),value,font=f(size),fill=fill,spacing=12)
def card(im,box,fill=WHITE,outline=None,r=22):
    ImageDraw.Draw(im).rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=2)
def photo(im,key,box,crop=None):
    src=Image.open(DATA['assets'][key]['path']).convert('RGB') if key in DATA['assets'] else Image.open(key).convert('RGB')
    if crop: src=src.crop(crop)
    x,y,x1,y1=box
    fitted=ImageOps.contain(src,(x1-x,y1-y),Image.Resampling.LANCZOS)
    card(im,box,'#E3E7E1')
    im.paste(fitted,(x+(x1-x-fitted.width)//2,y+(y1-y-fitted.height)//2))
def base(ch,note):
    im=Image.new('RGB',(720,1280),BG)
    d=ImageDraw.Draw(im)
    d.rectangle((0,0,12,1280),fill=TEAL)
    txt(im,38,49,'AI 漫剧实验笔记',24,TEAL)
    txt(im,575,51,f"{int(ch['id']):02} / 09",21,MUTED)
    txt(im,38,106,ch['label'],21,MUTED)
    txt(im,35,155,ch['title'],47)
    txt(im,38,942,ch['takeaway'],29,TEAL)
    txt(im,38,991,note,17,MUTED)
    card(im,(30,1036,690,1194),'#FAF8F3')
    d.line((46,1045,674,1045),fill='#D7DCD4',width=2)
    txt(im,38,1224,'未发布 · 静音审阅稿 / 口播字幕',18,MUTED)
    d.rectangle((38,1260,682,1264),fill='#D7DCD4')
    d.rectangle((38,1260,38+int(644*int(ch['id'])/9),1264),fill=TEAL)
    return im

def getframe(key,second):
    dest=OUT/f'{key}-{second}.jpg'
    if not dest.exists():
        run(['-ss',str(second),'-i',DATA['assets'][key]['path'],'-frames:v','1',str(dest)])
    return str(dest)

def slide(ch,kind):
    note='流程示意 · 根据本次实验归纳'
    if kind in {'hero','state','state_detail','result'}: note='真实检查版素材 · 静帧不证明动作或声音合格'
    if kind in {'before_after','create','warning'}: note='用户提供的历史截图 · 非当前实时操作'
    if kind=='shackle': note='真实失败候选 · 不作为合格产物展示'
    if kind in {'era','era_fix'}: note='时代问题来自开发记录 · 未提供旧军服错图'
    if kind.startswith('cost'): note='v2 验证报告及制作记录 · 金额为历史快照'
    im=base(ch,note)
    if kind=='hero':
        photo(im,'09-film-at-54s',(36,328,684,695))
        txt(im,48,747,'我想验证的三个问题',24,MUTED)
        for i,(a,b) in enumerate([('01','做出什么？'),('02','哪里返工？'),('03','花费多少？')]):
            x=37+i*224;card(im,(x,797,x+205,910));txt(im,x+16,814,a,22,ORANGE);txt(im,x+16,856,b,27)
    elif kind=='prep':
        items=[('01','故事冲突','先能讲清一段故事'),('02','人物场景','时代、身份、状态'),('03','生成工具','文字 → 图像 → 视频'),('04','预算验收','失败和返工也要算')]
        for i,(n,title,sub) in enumerate(items):
            x=37+(i%2)*330;y=334+(i//2)*289
            card(im,(x,y,x+312,y+263))
            txt(im,x+20,y+23,n,47,ORANGE);txt(im,x+20,y+99,title,35);txt(im,x+20,y+182,sub,23,MUTED)
    elif kind=='tools':
        for i,(n,title,sub) in enumerate([('01','文字 / 整理设定','本次记录：DeepSeek'),('02','图像 / 参考与修正','Seedream 4.5、图片工具'),('03','视频 / 生成镜头','v06 记录：Seedance 2.5')]):
            y=330+i*195;card(im,(38,y,682,y+177));txt(im,58,y+31,n,40,ORANGE);txt(im,145,y+29,title,34);txt(im,145,y+99,sub,24,MUTED)
    elif kind=='before_after':
        txt(im,40,304,'改版前',23,ORANGE);photo(im,'01-projects-before',(36,345,684,601))
        txt(im,40,620,'改版后',23,TEAL);photo(im,'02-projects-after',(36,656,684,913),crop=(0,0,1440,600))
    elif kind=='create':
        photo(im,'03-ai-create',(36,337,684,855),crop=(190,85,1060,633))
        txt(im,49,880,'先说想法，再明确制作方向',26)
    elif kind=='era':
        card(im,(36,332,684,490),'#F1DED3');txt(im,56,357,'故事要求',23,ORANGE);txt(im,56,409,'古代 / 押送官兵',39)
        txt(im,42,532,'润色后的提示词却出现……',29,MUTED)
        for i,value in enumerate(['立领','双排扣','帽檐','裤中缝']):
            x=38+(i%2)*330;y=600+(i//2)*144;card(im,(x,y,x+312,y+120));txt(im,x+24,y+38,value,36,ORANGE)
    elif kind=='era_fix':
        photo(im,'first_pass',(36,338,684,709),crop=(0,3120,900,3640))
        txt(im,40,731,'重制首轮角色图 / 古代官兵设定',22,MUTED)
        card(im,(36,785,684,911));txt(im,56,808,'交领右衽 · 札甲 · 布巾包髻',31);txt(im,56,859,'这是后续图例，不是缺失的旧错图',22,MUTED)
    elif kind=='dependency':
        for y,title,sub,col in [(333,'人物卡：新版','外貌与衣服已修改',TEAL),(531,'分镜提示词：旧版','仍带着历史描述',ORANGE),(729,'旧素材：待重审','同步文字后，还要重新检查图片',ORANGE)]:
            card(im,(38,y,682,y+160));txt(im,65,y+28,title,34,col);txt(im,65,y+98,sub,24,MUTED)
        txt(im,330,500,'↓',25,ORANGE);txt(im,330,698,'↓',25,ORANGE)
    elif kind=='warning':
        txt(im,40,306,'真实工作台里的版本提醒',25,TEAL)
        photo(im,'05-storyboard',(36,353,684,416),crop=(370,111,870,156))
        photo(im,'05-storyboard',(36,457,684,905),crop=(237,155,1000,690))
    elif kind=='state':
        photo(im,'08-film-at-07s',(36,337,684,706))
        card(im,(36,755,684,911));txt(im,56,781,'同一个角色，也有不同的场景状态',30);txt(im,56,844,'押送中：污痕、磨损、疲态',26,MUTED)
    elif kind=='state_detail':
        photo(im,'08-film-at-07s',(36,337,350,700),crop=(530,180,1040,710))
        photo(im,'09-film-at-54s',(370,337,684,700),crop=(850,120,1190,720))
        txt(im,47,727,'女主：脏痕与脚镣',24);txt(im,380,727,'周雎：木枷与囚衣',24)
        card(im,(36,796,684,911));txt(im,58,828,'按角色身份处理，不能统一“加脏”',30)
    elif kind=='shackle':
        photo(im,'bad_shackle',(36,329,684,887),crop=(900,580,1750,1430))
        # Highlight the already-present giant ring, never alter the underlying evidence.
        ImageDraw.Draw(im).ellipse((160,688,594,864),outline=ORANGE,width=6)
        card(im,(53,838,385,890),'#F1DED3');txt(im,72,851,'异常：脚镣比例失真',25,ORANGE)
    elif kind=='action_explain':
        for y,key,t,label in [(318,'raw',1,'接近刀柄'),(521,'edit',2.7,'切反应'),(724,'edit',5,'持刀结果')]:
            txt(im,43,y+76,label,25,TEAL);photo(im,getframe(key,t),(203,y,683,y+180))
    elif kind=='compare':
        # Source videos are inserted later; no subtitle/label is taken from a stale prior cut.
        ImageDraw.Draw(im).rectangle((25,280,695,1030),fill=BG)
        txt(im,40,275,'原片 / S007',22,ORANGE);txt(im,315,278,'原速播放后定格，便于对照',19,MUTED)
        txt(im,40,655,'剪辑版 / 同一镜头',22,TEAL)
    elif kind=='cost_scope':
        for i,(title,sub) in enumerate([('工作台搭建','联调测试、工具试用'),('角色重制','时代冲突、服装与场景状态'),('镜头返工','分镜图、视频小样、重试'),('隐性投入','文字工具、剪辑、人工时间')]):
            y=327+i*147;card(im,(38,y,682,y+128));txt(im,58,y+22,title,30,TEAL);txt(im,270,y+34,sub,22,MUTED)
    elif kind=='cost_calls':
        txt(im,43,324,'仅“全员押送状态 v04”这一轮',26,MUTED)
        card(im,(38,385,682,641));txt(im,70,420,'18',120,ORANGE);txt(im,276,474,'次图片工具调用',32);txt(im,74,586,'调用次数已记录 / 金额未知',26,MUTED)
        txt(im,50,690,'7 角色初版 ＋ 2 角色修正',30)
        txt(im,50,754,'3 新分镜 ＋ 6 分镜局部修正',30)
        txt(im,50,851,'不是整个项目的调用总数',26,ORANGE)
    elif kind=='cost_cash':
        card(im,(38,324,682,573));txt(im,62,347,'9 月账户现金快照 / 出账中',24,MUTED)
        txt(im,59,395,'¥274.92',78,TEAL);txt(im,62,506,'含 ¥200 套餐 ＋ ¥74.92 按量费用',26)
        card(im,(38,605,682,809));txt(im,62,627,'9 月 28 日筛选账单',25,MUTED);txt(im,60,673,'¥74.92',65,ORANGE);txt(im,62,763,'已包含在月度金额中，不能重复相加',24)
        txt(im,45,852,'项目排他归因、其他工具、人工：未齐',26,ORANGE)
    elif kind=='result':
        photo(im,'09-film-at-54s',(36,337,684,706))
        card(im,(36,757,684,911));txt(im,58,779,'60 秒  /  720p  /  检查版',40,TEAL);txt(im,58,853,'原声音色、情绪、口型仍待主观复核',23,MUTED)
    elif kind=='next':
        for i,(n,title,sub) in enumerate([('01','听完整段原声','台词 / 情绪 / 口型'),('02','让观众复述冲突','看懂了吗？还想继续看吗？'),('03','补齐成本归因','再判断是否值得继续投入')]):
            y=328+i*197;card(im,(38,y,682,y+180));txt(im,60,y+38,n,45,ORANGE);txt(im,160,y+34,title,33);txt(im,160,y+107,sub,23,MUTED)
    else: raise ValueError(kind)
    return im

def run(args):
    subprocess.run([str(FF),'-hide_banner','-loglevel','error','-y',*args],check=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--slides-only',action='store_true');ap.add_argument('--reuse',action='store_true');opts=ap.parse_args()
    for name,asset in DATA['assets'].items():
        assert hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest()==asset['sha256'],name
    chapter={ch['id']:ch for ch in DATA['chapters']}
    clips=[]
    for s in DATA['shots']:
        art=OUT/(s['id']+'.png');dest=OUT/(s['id']+'.mp4')
        slide(chapter[s['chapter']],s['kind']).save(art)
        if opts.slides_only: continue
        if not (opts.reuse and dest.exists()):
            inputs=['-loop','1','-framerate','24','-i',str(art)]
            filters=[]
            if s['kind']=='compare':
                for key in ('raw','edit'): inputs+=['-i',DATA['assets'][key]['path']]
                filters=['-filter_complex','[1:v]fps=24,scale=600:338,tpad=stop_mode=clone:stop_duration=6[a];[2:v]fps=24,scale=600:338,tpad=stop_mode=clone:stop_duration=6[b];[0:v][a]overlay=60:308[v1];[v1][b]overlay=60:690[v]', '-map','[v]']
            if s['kind']=='result':
                inputs+=['-ss','49','-i',DATA['assets']['final']['path']]
                filters=['-filter_complex','[1:v]fps=24,scale=648:365[a];[0:v][a]overlay=36:337[v]','-map','[v]']
            run([*inputs,*filters,'-an','-frames:v',str(s['duration']*24),'-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p',str(dest)])
        clips.append(dest);print(s['id'],flush=True)
    if opts.slides_only: return
    (OUT/'concat.txt').write_text(''.join(f"file '{p.name}'\n" for p in clips))
    run(['-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-c','copy',str(OUT/'base.mp4')])
    run(['-i',str(OUT/'base.mp4'),'-vf',f"ass={HERE/'subtitles.ass'}:fontsdir=/System/Library/Fonts",'-an','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'OPC-2-explained-v06-180s-captioned.mp4')])

if __name__=='__main__': main()
