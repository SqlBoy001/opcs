"""One factual source supplies narration, captions, edit decisions and handoff."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/shenzihao/Documents/ChatGPT/AI_Drama')
BASE = ROOT / 'backend-node/data/storage/projects/0006_20260926_亡国公主·全角色重制版'

chapters = [
    dict(id='01', duration=12, title='一个人做 AI 漫剧，\n究竟要准备什么？', label='起点 / 不报班，自己试',
         takeaway='先跑一遍，再判断值不值得', evidence=['用户个人观察；新包09图仅作本实验画面'],
         narration=['刷到不少AI漫剧副业内容，我决定先不报班。', '自己跑一遍：要准备什么，又会在哪里返工？'],
         shots=[('hero', 12)]),
    dict(id='02', duration=20, title='先准备的，\n不只是生成工具', label='准备 / 四件事',
         takeaway='故事、参考、工具、验收', evidence=['编辑归纳；复盘稿一、四'],
         narration=['我先拆成四件事：故事冲突、人物场景、生成工具，还有预算和验收。',
                    '文字模型整理资料，图像工具做参考，视频模型生成镜头。',
                    '但每一步，都要有人判断能不能往下走。'],
         shots=[('prep', 10), ('tools', 10)]),
    dict(id='03', duration=14, title='为什么还要\n搭一个工作台？', label='搭建 / 从入口到制作',
         takeaway='把上下文、版本和审核串起来', evidence=['复盘稿一、四；新包01/02/03'],
         narration=['我基于LocalMiniDrama继续搭建工作台，把想法、角色、分镜和审核串起来。',
                    '入口能变清楚，但界面改好了，画面也未必就对。'],
         shots=[('before_after', 7), ('create', 7)]),
    dict(id='04', duration=20, title='第一关：古装故事，\n人物却穿错时代', label='问题 01 / 先校准设定',
         takeaway='先改时代与服制，再往下生成', evidence=['docs/progress.md 2026-09-26 押送兵时代错配；复盘稿二/四'],
         narration=['重制前，古装押送兵竟然跑出了近现代军服。',
                    '查记录才发现，润色后的提示词混进了立领、双排扣这些描述。',
                    '所以先校准时代和服制，错误参考也要撤下，不能直接接着做视频。'],
         shots=[('era', 11), ('era_fix', 9)]),
    dict(id='05', duration=20, title='第二关：人物改了，\n分镜为什么没变？', label='问题 02 / 上下游同步',
         takeaway='资料同步之后，旧图仍要重审', evidence=['docs/progress.md 2026-09-28 角色下游同步；新包05'],
         narration=['人物卡更新了，分镜却还沿用旧衣服、旧描述。',
                    '这次的问题，是上下游各存了一份资料，改动没有传下去。',
                    '后来补上依赖同步和旧素材失效；文字改了，旧图也不能自动算合格。'],
         shots=[('dependency', 10), ('warning', 10)]),
    dict(id='06', duration=22, title='第三关：人物像了，\n处境还不对', label='问题 03 / 押送状态',
         takeaway='这个人是谁 ≠ 此刻经历了什么', evidence=['qc-cast-v04.md；v2 E07；新包08/09；真实异常脚镣图'],
         narration=['同一张脸、同一套衣服，还不够。押送中的囚犯，怎么会干干净净？',
                    '要补衣料磨损和脏痕，还得逐人处理木枷、脚镣和官兵的行军状态。',
                    '重生图也会冒出巨型脚镣。图片不对，就先停在图片阶段。'],
         shots=[('state', 8), ('state_detail', 7), ('shackle', 7)]),
    dict(id='07', duration=22, title='第四关：动作不顺，\n一定要反复重生？', label='问题 04 / 动作与剪辑',
         takeaway='换镜头设计，也是一次取舍', evidence=['v2 E04/E06；qc-action-v06.md S007'],
         narration=['到了动作，取刀也没有稳定连起来。这里是原片和剪辑版对照。',
                    '最后切到对方的反应，再回到持刀结果，用分切交代动作。',
                    '故事能往下讲了，但这不等于模型完成了连续、准确的取刀。'],
         shots=[('compare', 12), ('action_explain', 10)]),
    dict(id='08', duration=34, title='最后算账：\n不能只看最后一天', label='费用 / 整个实验的范围',
         takeaway='记录不全，就不报完整总价', evidence=['v2 E11/E12/Cost；qc-cast-v04；docs/progress.md 测试与返工记录'],
         narration=['成本也要重算范围：搭工作台的测试，重制前的角色问题，以及图片、视频返工，都该算。',
                    '光全员押送状态这一轮，就记录了十八次图片工具调用，金额仍未知。',
                    '现有快照里，九月账户现金二百七十四点九二元，包含两百元套餐；九月二十八日是七十四点九二元。',
                    '两笔不能相加，也都不是本集总成本。文字、图片工具、人工和套餐分摊还没对齐。'],
         shots=[('cost_scope', 11), ('cost_calls', 8), ('cost_cash', 15)]),
    dict(id='09', duration=16, title='做出了检查版，\n下一步还要验证', label='结果 / 先把问题讲清楚',
         takeaway='先听审，再看观众是否看懂', evidence=['v2 E03/Quality/Next Experiment'],
         narration=['现在留下的是六十秒、七百二十P检查版，原声还没完成主观听审。',
                    '这次最大的收获，是把错误拦在下一步之前。接下来先听审，再找观众验证。'],
         shots=[('result', 8), ('next', 8)]),
]

def stamp(frames, ass=False):
    total_ms = round(frames * 1000 / 24)
    h, rem = divmod(total_ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f'{h}:{m:02}:{s:02}.{ms//10:02}' if ass else f'{h:02}:{m:02}:{s:02},{ms:03}'

def split_sentences(value, limit=24):
    import re
    pieces = re.findall(r'[^，：；。？！]+[，：；。？！]?', value)
    result=[]
    for piece in pieces:
        while len(piece)>limit:
            result.append(piece[:limit]); piece=piece[limit:]
        if piece: result.append(piece)
    return result

def main():
    assets = {}
    for path in sorted((HERE/'assets').glob('*.png')):
        assets[path.stem] = dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(), kind='provided_historical_image')
    for key,path in {
        'raw':BASE/'videos/vg_46_ecfddff9.mp4',
        'edit':BASE/'videos/s007-action-v05-editorial.mp4',
        'final':BASE/'exports/action-v06/jinyang-EP01-action-v06c-720p.mp4',
        'bad_shackle':BASE/'images/ig_c179b089.jpg',
        'first_pass':ROOT/'backend-node/data/production/jinyang-rebuild-v01/contact-first-pass.jpg',
    }.items():
        assets[key] = dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),kind='original_production_media')
    start=0; cues=[]; shots=[]
    for ch in chapters:
        ch['start_frame']=start; ch['end_frame']=start+ch['duration']*24
        phrases=[p for line in ch['narration'] for p in split_sentences(line)]
        weights=[max(9,len(p)) for p in phrases]
        cursor=start; accum=0
        for p,w in zip(phrases,weights):
            accum+=w
            end=start+round(ch['duration']*24*accum/sum(weights))
            cues.append(dict(start_frame=cursor,end_frame=end,text=p,chapter=ch['id']))
            cursor=end
        cursor=start
        for kind,duration in ch['shots']:
            shots.append(dict(id=f'{len(shots)+1:02}-{kind}',kind=kind,duration=duration,chapter=ch['id'],start_frame=cursor))
            cursor+=duration*24
        assert cursor==ch['end_frame']
        start=cursor
    assert start==4320
    data=json.loads((HERE.parent/'content.json').read_text())
    data['explained_v06']=dict(status='unpublished_silent_review_draft',duration_seconds=180,
        duration_basis='编辑假设；用户要求更丰富讲解、更长问题停留。非用户确认的精确时长。',
        chapters=chapters,shots=shots,captions=cues,assets=assets,
        art_policy='用户提供真实图片＋本地排版示意；无新AI配图、无新录屏',
        cost_scope='工作台测试、旧角色时代问题、重制及各轮返工均纳入；归因不全，不报准确总额',
        cost_cash_snapshot={'month':'2026-09','account_cny':274.92,'included_plan_cny':200,'included_sep28_cny':74.92,'project_total_cny':None,'status':'9月出账中快照，非最终账单'},
        cost_records={'image_tool_documented_attempts':{'escort_v03':9,'cast_v04':18,'action_v05':4,'action_v06':2,'subtotal':33,'scope':'仅所列四轮；包含无输出尝试，非项目全部次数或收费笔数'},'account_cash_arithmetic':'200.00 + 74.92 = 274.92','known_missing':['全搭建期最终账单','图片/文字/TTS账单或权益消耗','套餐与跨项目分摊','人工时间与Agent运行费用']},
        voiceover_status='仅口播稿和逐句字幕；无配音，无原声听审',
        supplied_zip_attachment='01a0f172-4617-7eb4-94bf-6708bbaaf4f9')
    data['latest_draft']='explained_v06'
    (HERE.parent/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    srt=[]; ass=[]
    for n,c in enumerate(cues,1):
        value=c['text']; wrapped=value if len(value)<=20 else value[:20]+'\n'+value[20:]
        srt.append(f"{n}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame'])}\n{wrapped}\n")
        ass.append(f"Dialogue: 0,{stamp(c['start_frame'],True)},{stamp(c['end_frame'],True)},Default,,0,0,0,,"+wrapped.replace('\n',r'\N'))
    (HERE/'subtitles.srt').write_text('\n'.join(srt))
    header='''[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Heiti SC,30,&H0023201B,&H0023201B,&H00F7F5F0,&H00F7F5F0,0,0,0,0,100,100,0,0,1,0,0,2,48,48,119,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    (HERE/'subtitles.ass').write_text(header+'\n'.join(ass)+'\n')
    voice=['# v06 完整口播稿\n','约3分钟，静音审阅稿；未配音。字幕逐句覆盖以下全文，实际录音后需重新校时。\n']
    board=['# v06 分镜与证据\n','工作台截图均为历史记录；无新录屏。\n']
    for ch in chapters:
        title=ch['title'].replace('\n','')
        voice += [f"## {ch['start_frame']/24:g}–{ch['end_frame']/24:g} 秒｜{title}\n",'\n\n'.join(ch['narration'])+'\n']
        board += [f"## {ch['id']}｜{title}（{ch['duration']}秒）\n",f"画面：{ch['shots']}\n",f"口播：{''.join(ch['narration'])}\n",f"依据：{'；'.join(ch['evidence'])}\n"]
    (HERE/'voiceover.md').write_text('\n'.join(voice));(HERE/'storyboard.md').write_text('\n'.join(board))
    print(json.dumps({'duration':180,'chapters':len(chapters),'shots':len(shots),'cues':len(cues),'narration_chars':sum(len(''.join(ch['narration'])) for ch in chapters),'max_cue_chars_per_second':max(len(c['text'])/((c['end_frame']-c['start_frame'])/24) for c in cues)},ensure_ascii=False))

if __name__=='__main__': main()
