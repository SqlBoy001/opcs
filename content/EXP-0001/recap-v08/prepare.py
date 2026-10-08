"""Keep factual content in the experiment's shared content.json."""
import copy, json, re, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'explained-v06'))
from prepare import split_sentences,stamp

def main():
 p=HERE.parent/'content.json';data=json.loads(p.read_text());d=copy.deepcopy(data['motion_v07'])
 d['chapters']=d['chapters'][:7]
 d['chapters'] += [
  dict(id='08',duration=28,title='第一次入门，\n和这一集分别花多少？',short='费用 / 简单算两笔',palette='blue',
   narration=['第一次熟悉AI漫剧制作，搭工作台、调接口、跑测试，我先充了两百元火山节省计划。','后面这版六十秒视频，生成和修改大概七十五元。DeepSeek、MiniMax还没算。转场和打斗想再自然些，还得继续花钱。'],shots=[['startup',14],['episode',14]],start_frame=3120,end_frame=3792),
  dict(id='09',duration=22,title='这一轮，\n带走三件事',short='回顾 / 流程 · 注意项 · 成本',palette='navy',
   narration=['这次跑通的流程是：故事和人物设定，参考图和分镜，再生成视频，最后剪辑。','注意三件事：先对时代和人物，改完同步下游，动作不顺时也可以换镜头讲。','第一次入门要算调试成本；做一集要算生成和返工，想更好，还要留优化预算。'],shots=[['flow',8],['lessons',7],['closing',7]],start_frame=3792,end_frame=4320)
 ]
 d['shots']=[s for s in d['shots'] if s['start_frame']<3120]
 d['captions']=[c for c in d['captions'] if c['end_frame']<=3120]
 cursor=3120
 for ch in d['chapters'][7:]:
  for (kind,duration),narration in zip(ch['shots'],ch['narration']):
   phrases=split_sentences(narration,20);weights=[max(8,len(s)) for s in phrases];a=0;cc=cursor
   for phrase,w in zip(phrases,weights):
    a+=w;end=cursor+round(duration*24*a/sum(weights))
    d['captions'].append(dict(start_frame=cc,end_frame=end,text=phrase,chapter=ch['id'],shot=kind));cc=end
   d['shots'].append(dict(id=f'{len(d["shots"])+1:02}-{kind}',kind=kind,duration=duration,start_frame=cursor,chapter=ch['id']));cursor+=duration*24
 assert cursor==4320
 d['status']='review_draft';d['user_authorization']='2026-10-08用户明确采用粗略个人经历口径，修改字幕与最后费用总结'
 d['source_feedback']=['01a11993-d9e8-70f0-8bea-ce0e6e87dfb3','01a11993-d9fa-7387-afee-55e280e6b952','01a11993-da37-78d9-a289-997cdbb82ea0']
 d['billing']={'source':'2026-10-08用户确认＋2026-09-30保存的v2账单','startup_plan_paid_cny':200,'episode_video_cash_approx_cny':75,'episode_duration_seconds':60,'excluded':['DeepSeek','MiniMax','人工及其他未归因费用'],'scope':'前期先充值200元用于熟悉制作和搭建测试；不声称200全部已经消耗。约75元为本次火山视频现金粗估，不是所有工具全成本，不是每集固定报价。','live_refresh':'not_performed_not_required_for_user_requested_rough_recap'}
 d.pop('budget',None)
 d['removed']+=['费用记录条数','精确单次价格和40–60元试验预算卡','实时账单登录提示','整段费用审计式讲述']
 d['subtitle_style']={'family':'PingFang SC','weight':'Semibold','font_collection_index':11,'size_px':36,'min_size_px':31,'layout':'短句居中，白字细描边，无黑色卡片，去句尾标点','max_width_px':648}
 d['attachment_observations']={'deepseek':'近30天消费2.91元；9/26提示0.19元；范围不等于本实验','minimax':'两条为9/16与9/21，标价0.0389/0.5068，券后均0；不能归为本轮费用','treatment':'保留未计入口径，不把全账户/历史金额直接摊本片'}
 # Onscreen captions omit trailing punctuation; prose keeps natural punctuation.
 for c in d['captions']:c['display_text']=re.sub(r'[，。？！：；、\s]+$','',c['text'])
 data['recap_v08']=d;data['latest_draft']='recap_v08';p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (HERE/'subtitles.srt').write_text('\n'.join(f"{i}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame'])}\n{c['display_text']}\n" for i,c in enumerate(d['captions'],1)))
 voice=['# v08 口播稿\n','180秒静音审阅稿，费用按本次经历粗估。\n']
 for ch in d['chapters']:voice.extend([f"## {ch['start_frame']/24:g}–{ch['end_frame']/24:g}秒｜{ch['short']}\n",'\n\n'.join(ch['narration'])+'\n'])
 (HERE/'voiceover.md').write_text('\n'.join(voice))
 print({'seconds':180,'shots':len(d['shots']),'captions':len(d['captions'])})
if __name__=='__main__':main()
