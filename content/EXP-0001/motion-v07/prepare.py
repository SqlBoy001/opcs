import hashlib
import json
import sys
from pathlib import Path
from decimal import Decimal

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'explained-v06'))
from prepare import split_sentences, stamp

def main():
    path=HERE.parent/'content.json';data=json.loads(path.read_text());old=data['explained_v06']
    assets=dict(old['assets'])
    soldier=Path('/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/data/storage/projects/0005_20260926_亡国公主醒来，先杀押送官/characters/ig_f4a32585.jpg')
    assets['wrong_soldier']={'path':str(soldier),'sha256':hashlib.sha256(soldier.read_bytes()).hexdigest(),'kind':'original_production_media','record_id':91,'character_id':19,'project_id':5,'created_at_utc':'2026-09-26T05:14:58.121Z'}
    chapters=[
      dict(id='01',duration=10,title='不报班，\n一个人做 AI 漫剧',short='先自己试一次',palette='navy',
           narration=['刷到不少AI漫剧副业内容，我决定先不报班。','自己跑一遍：能做出什么，又会在哪里返工？'],shots=[('hero',10)]),
      dict(id='02',duration=18,title='开工前，\n先拆成四件事',short='先备什么？',palette='violet',
           narration=['故事冲突、人物场景、生成工具，还有预算。','文字模型整理资料，图像工具做参考，视频模型生成镜头。','难点是把这些环节接起来。'],shots=[('prep',9),('tools',9)]),
      dict(id='03',duration=12,title='把工具，\n串成一个工作台',short='从想法到制作',palette='blue',
           narration=['我在LocalMiniDrama基础上，继续搭建工作台。','创作入口和制作流程顺了，画面的问题才刚开始。'],shots=[('build_before',6),('build_after',6)]),
      dict(id='04',duration=24,title='古装押送兵，\n怎么穿成了这样？',short='第一处返工：时代错了',palette='red',
           narration=['这就是重制前的押送兵。看帽檐、立领，还有胸前的双排扣。','古装故事里混进这套服装，一眼就违和。','查提示词才发现，润色时已经写进了近现代服制。','先纠正时代，再换人物参考，不能把错误继续传给分镜。'],shots=[('era_sample',10),('era_prompt',6),('era_compare',8)]),
      dict(id='05',duration=20,title='人物改了，\n分镜还在穿旧衣服',short='第二处返工：旧资料没换',palette='blue',
           narration=['人物卡已经更新，分镜却还在用旧衣服、旧描述。','上游改了，下游没有一起变。','后来补上依赖同步，让旧素材失效，再逐镜核对新的参考。'],shots=[('sync',10),('warning',10)]),
      dict(id='06',duration=22,title='脸像了，\n剧情处境还不对',short='第三处返工：押送状态',palette='green',
           narration=['押送中的囚犯，脸和衣服怎么会干干净净？','要补污痕和磨损，还要逐人处理木枷、脚镣和官兵状态。','可重生图又冒出了巨型脚镣。','一个问题修好，并不代表下一张图就不会出新问题。'],shots=[('state',6),('state_detail',8),('shackle',8)]),
      dict(id='07',duration=24,title='动作不顺，\n换一种镜头讲法',short='第四处返工：取刀动作',palette='amber',
           narration=['接下来是取刀。上面是原片，下面是剪辑版。','原片没有把连续动作交代清楚。','最后切到对方的反应，再回到持刀结果。','故事接上了，但这个改善来自剪辑，并不是模型把动作做完美了。'],shots=[('compare',12),('action',12)]),
      dict(id='08',duration=34,title='这一轮花了多少？\n继续抽卡还要多少？',short='把账算到具体镜头',palette='blue',
           narration=['从九月二十六日下午一点起，把旧角色和重制记录一起算进来。',
                      '按已有火山账单快照，可核实的按量现金是七十四点九二元。套餐购买、其他工具和人工另计。',
                      '继续优化，我会先重试踢击和取刀，必要时再修出鞘。每镜最多两次，先留四十到六十元。',
                      '这是试错预算，不是花完就一定自然。'],shots=[('cost_scope',6),('cost_cash',12),('budget',16)]),
      dict(id='09',duration=16,title='60 秒漫剧背后，\n是一轮轮纠错',short='这次 OPC 创作经历',palette='navy',
           narration=['最后留下的是这一版六十秒漫剧检查版。','最费劲的是找出哪里不对，再决定重做还是换个讲法。','下一轮只修最不自然的几镜，其他先保留。'],shots=[('result',10),('closing',6)]),
    ]
    cursor=0;shots=[];cues=[]
    groups={'01':[[0,1]],'02':[[0],[1,2]],'03':[[0],[1]],'04':[[0,1],[2],[3]],'05':[[0,1],[2]],'06':[[0],[1],[2,3]],'07':[[0,1],[2,3]],'08':[[0],[1],[2,3]],'09':[[0,1],[2]]}
    for ch in chapters:
        ch['start_frame']=cursor;ch['end_frame']=cursor+ch['duration']*24
        for (kind,duration),indices in zip(ch['shots'],groups[ch['id']]):
            phrases=[p for idx in indices for p in split_sentences(ch['narration'][idx])]
            weights=[max(9,len(p)) for p in phrases];a=0;cc=cursor
            for phrase,w in zip(phrases,weights):
                a+=w;end=cursor+round(duration*24*a/sum(weights))
                cues.append(dict(start_frame=cc,end_frame=end,text=phrase,chapter=ch['id'],shot=kind));cc=end
            shots.append(dict(id=f'{len(shots)+1:02}-{kind}',kind=kind,duration=duration,start_frame=cursor,chapter=ch['id']))
            cursor+=duration*24
        assert cursor==ch['end_frame']
    assert cursor==4320
    budget={'currency':'CNY','video_model':'doubao-seedance-2-5-260628','spec':'720p/24fps，无视频输入；复用或修正首尾参考',
      'price_per_million_tokens':70,'six_seconds_tokens':130500,'seven_seconds_tokens':152100,
      'six_seconds_list_cny':9.135,'seven_seconds_list_cny':10.647,
      'low':{'shots':['S005','S007'],'tries_each':2,'image_allowance_count':4,'image_price':0.25,'video_cny':36.54,'image_cny':1,'subtotal':37.54},
      'high':{'shots':['S005','S007','S009'],'tries_each':2,'image_allowance_count':6,'image_price':0.25,'video_cny':57.834,'image_cny':1.5,'subtotal':59.334},
      'suggested_reserve_cny':[40,60],'not_guaranteed_quality':True,'actual_new_requests':0,
      'source':'v2供应商用量；2026-09-30官网模型价格；价格为刊例，不预设未来套餐剩余或优惠'}
    assert Decimal('9.135')*4+Decimal('10.647')*2+Decimal('1.5')==Decimal('59.334')
    data['motion_v07']=dict(status='review_draft_billing_live_refresh_pending',duration_seconds=180,chapters=chapters,shots=shots,captions=cues,assets=assets,
      billing={'window_start_local':'2026-09-26T13:00:00+08:00','window_start_utc':'2026-09-26T05:00:00Z','project_ids':[5,6],'image_records':72,'video_records':11,'video_completed':10,'video_failed':1,'known_account_cash_snapshot_cny':74.92,'snapshot_date':'2026-09-30','live_refresh':'requires_user_login','scope_note':'账户按量现金，不是完整项目成本；套餐购买、外部工具与人工另计；无逐请求排他账单映射'},
      budget=budget,art_policy='现有真实图像与源视频；本地动态构图、圈注、推近与章节转场',audio='silent_review_draft',removed=['结尾听审评估清单','观众偏好验证步骤','整屏价格未知卡'],
      user_authorization='2026-09-30四项定向修改',source_feedback=['01a0f199-be98-7a76-acdc-921d5f3c51bf','01a0f199-bebb-72da-8150-d14b42d8d45e'])
    data['latest_draft']='motion_v07';path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    srt=[]
    for n,c in enumerate(cues,1):
        t=c['text'];t=t if len(t)<=20 else t[:20]+'\n'+t[20:]
        srt.append(f"{n}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame'])}\n{t}\n")
    (HERE/'subtitles.srt').write_text('\n'.join(srt))
    voice=['# v07 口播稿\n','180秒静音审阅稿；字幕与本稿同源。费用采用已有账单快照，实时复核待登录。\n']
    for ch in chapters:
        voice.extend([f"## {ch['start_frame']/24:g}–{ch['end_frame']/24:g} 秒｜{ch['short']}\n",'\n\n'.join(ch['narration'])+'\n'])
    (HERE/'voiceover.md').write_text('\n'.join(voice))
    (HERE/'budget.json').write_text(json.dumps(budget,ensure_ascii=False,indent=2)+'\n')
    print({'seconds':180,'shots':len(shots),'cues':len(cues),'characters':sum(len(c['text']) for c in cues)})

if __name__=='__main__':main()
