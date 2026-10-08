import copy,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'explained-v06'))
from prepare import split_sentences,stamp

def main():
 p=HERE.parent/'content.json';data=json.loads(p.read_text());d=copy.deepcopy(data['recap_v08'])
 chs=[dict(id='01',duration=15,title='一个人做60秒AI漫剧，\n为什么总在返工？',short='真实失败开场',palette='navy',
 narration=['古装押送兵，怎么穿成这样？','衣服改了，脚镣又大成这样。','做这六十秒，我搭工作台、反复返工。','怎么做、哪里翻车、花了多少？这次都讲清楚。'],shots=[['hook_costume',3],['hook_shackle',3],['hook_result',4],['hook_promise',5]])]
 chs+=copy.deepcopy(data['motion_v07']['chapters'][1:7])
 chs[1]['narration'][0]='先说开工前。故事冲突、人物场景、生成工具，还有预算。'
 chs += [dict(id='08',duration=27,title='这60秒，\n是这样做出来的',short='做出了什么，又付出了什么',palette='blue',
 narration=['折腾到这里，总算留下了这版六十秒漫剧。','第一次熟悉流程，搭工作台、调接口、跑测试，我先充了两百元火山节省计划。','这版视频生成和修改，又花了大概七十五元。DeepSeek、MiniMax还没算。转场和打斗想更自然，还得再投入。'],shots=[['earned_result',5],['startup',10],['episode',12]]),
 dict(id='09',duration=23,title='生成之后，\n才开始真正做判断',short='这一轮留下的经验',palette='navy',
 narration=['这次让我明白，故事、人物、分镜到视频和剪辑，要一步步接起来。','前面的设定先核对好，改完同步下游；动作不顺，也可以换个镜头讲。','否则，前面一个小错误，到了视频阶段，就可能变成又一次付费重做。'],shots=[['connected',8],['lesson_replay',8],['closing',7]])]
 groups={'01':[[0],[1],[2],[3]],'02':[[0],[1,2]],'03':[[0],[1]],'04':[[0,1],[2],[3]],'05':[[0,1],[2]],'06':[[0],[1],[2,3]],'07':[[0,1],[2,3]],'08':[[0],[1],[2]],'09':[[0],[1],[2]]}
 cursor=0;shots=[];cues=[]
 for ch in chs:
  ch['start_frame']=cursor;ch['end_frame']=cursor+ch['duration']*24
  for (kind,dur),indices in zip(ch['shots'],groups[ch['id']]):
   phrases=[s for i in indices for s in split_sentences(ch['narration'][i],20)];weights=[max(7,len(s)) for s in phrases];a=0;cc=cursor
   for phrase,w in zip(phrases,weights):
    a+=w;end=cursor+round(dur*24*a/sum(weights));cues.append(dict(start_frame=cc,end_frame=end,text=phrase,display_text=re.sub(r'[，。？！：；、\s]+$','',phrase),chapter=ch['id'],shot=kind));cc=end
   shots.append(dict(id=f'{len(shots)+1:02}-{kind}',kind=kind,duration=dur,start_frame=cursor,chapter=ch['id']));cursor+=dur*24
  assert cursor==ch['end_frame']
 assert cursor==4440
 d.update(chapters=chs,shots=shots,captions=cues,duration_seconds=185,status='review_draft',user_authorization='2026-10-08用户明确授权按讨论的钩子和叙事收尾方案修改',positioning='个人OPC实验复盘：一个人尝试AI漫剧，展示真实结果、返工与投入',title='一个人做60秒AI漫剧，为什么总在返工？')
 d['edit_structure']={'opening':'0–15秒：错服装→巨型脚镣→两个成片镜头→流程/踩坑/费用承诺','middle':'15–135秒：原v08的10–130秒内容，字幕同步更新并加过渡句','ending':'135–185秒：成片→前期充值/本次费用→案例回顾与返工收获；删除三张目录式总结卡'}
 data['story_v09']=d;data['latest_draft']='story_v09';p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (HERE/'subtitles.srt').write_text('\n'.join(f"{i}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame'])}\n{c['display_text']}\n" for i,c in enumerate(cues,1)))
 voice=['# v09 口播稿\n',d['title']+'\n','185秒静音审阅稿。\n']
 for c in chs:voice.extend([f"## {c['start_frame']/24:g}–{c['end_frame']/24:g}秒｜{c['short']}\n",'\n\n'.join(c['narration'])+'\n'])
 (HERE/'voiceover.md').write_text('\n'.join(voice));print({'seconds':185,'shots':len(shots),'captions':len(cues)})
if __name__=='__main__':main()
