"""Build the complete timeline from source text and MiniMax word timestamps."""
import json, math, subprocess, wave, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUB = ROOT / 'studio/public'
FPS, SR = 30, 48000
content = json.loads((ROOT / 'content.json').read_text())
chapters = content['chapters']
titles = {
 'hook_costume':'古装押送兵\n怎么穿成这样？', 'hook_shackle':'衣服改了\n脚镣又大成这样',
 'hook_result':'为了做出这 60 秒', 'hook_promise':'怎么做、哪里翻车\n又花了多少钱？',
 'prep':'开工前，先想清楚', 'tools':'把工具，接成流程',
 'build_before':'从现有项目出发', 'build_after':'继续搭建工作台',
 'era_sample':'时代错了\n细节会暴露问题', 'era_prompt':'问题已写进提示词',
 'era_compare':'先修时代，再换参考', 'sync':'人物改了\n分镜却没跟上',
 'warning':'改完，还要同步下游', 'state':'脸像了，处境却不对',
 'state_detail':'服装之外，还要看状态', 'shackle':'修好一个问题\n又出现一个新问题',
 'compare':'同一个动作\n换一种镜头讲法', 'action':'切反应，再接持刀结果',
 'earned_result':'折腾到这里\n留下这版 60 秒', 'startup':'九月账户支出',
 'episode':'这版，花了多少？', 'connected':'从设定，一步步接到成片',
 'lesson_replay':'这一轮留下的经验', 'closing':'把错误\n拦在下一步之前',
}
names = ['真实失败开场','开工准备','搭建工作台','服装与时代','资料与依赖','人物处境','动作与剪辑','结果与投入','本次收获']
all_shots, all_captions, parts, ledger = [], [], [], []
cursor = 0
for c in chapters:
    stem = ROOT / 'speech' / c['id']
    request = json.loads(stem.with_suffix('.request.json').read_text())
    assert request['text'] == c['text']
    assert request['voice_setting']['voice_id'] == content['voice_id']
    subs = json.loads(stem.with_suffix('.subtitles.json').read_text())
    words = [w for s in subs for w in s['timestamped_words']]
    assert ''.join(w['word'] for w in words) == c['text']
    wav = stem.with_suffix('.wav')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(stem.with_suffix('.mp3')),'-ar',str(SR),'-ac','1','-c:a','pcm_s16le',str(wav)],check=True)
    with wave.open(str(wav)) as f: pcm=f.readframes(f.getnframes())
    lead = int(.1*SR) if cursor == 0 else 0
    tail = int((.8 if c == chapters[-1] else .18)*SR)
    chapter_frames=math.ceil((lead+len(pcm)//2+tail)/SR*FPS)
    total_samples=chapter_frames*SR//FPS
    parts.append(bytes(lead*2)+pcm+bytes((total_samples-lead-len(pcm)//2)*2))
    offset_ms=cursor/FPS*1000+lead/SR*1000
    word_caps=[{'text':w['word'],'startMs':offset_ms+w['time_begin'],'endMs':offset_ms+w['time_end'],'timestampMs':None,'confidence':None} for w in words]
    all_captions.extend(word_caps)
    chapter_shots=[]; char_cursor=0
    for source_shot in c['shots']:
        cues=[]
        for source_cue in source_shot['captions']:
            end_char=char_cursor+len(source_cue['text'])
            ww=[(w, cap) for w,cap in zip(words,word_caps) if w['word_begin']<end_char and w['word_end']>char_cursor]
            assert ''.join(w['word'] for w,_ in ww)==source_cue['text']
            cues.append({'text':source_cue['text'],'startMs':ww[0][1]['startMs'],'endMs':ww[-1][1]['endMs'],'words':[cap for _,cap in ww]})
            char_cursor=end_char
        start=round(cues[0]['startMs']/1000*FPS)
        chapter_shots.append({'id':source_shot['id'],'kind':source_shot['kind'],'chapter':c['id'],'chapterName':names[int(c['id'])-1],'title':titles[source_shot['kind']],'startFrame':start,'cues':cues})
    assert char_cursor==len(c['text'])
    chapter_shots[0]['startFrame']=cursor
    for i,shot in enumerate(chapter_shots):
        end=chapter_shots[i+1]['startFrame'] if i+1<len(chapter_shots) else cursor+chapter_frames
        shot['durationFrames']=end-shot['startFrame']
        assert shot['durationFrames']>0
        for j,cue in enumerate(shot['cues']):
            cue['displayEndMs']=shot['cues'][j+1]['startMs'] if j+1<len(shot['cues']) else end/FPS*1000
    all_shots.extend(chapter_shots)
    cursor+=chapter_frames
    rec=json.loads(stem.with_suffix('.receipt.json').read_text())
    ledger.append({'chapter':c['id'],'voice':rec['voice'],'usage_characters':rec['extra_info']['usage_characters'],'trace_id':rec['trace_id']})
with wave.open(str(ROOT/'voice.wav'),'wb') as f:
    f.setparams((1,2,SR,0,'NONE','not compressed'));f.writeframes(b''.join(parts))
subprocess.run(['ffmpeg','-y','-v','error','-i',str(ROOT/'voice.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar',str(SR),'-c:a','pcm_s16le',str(PUB/'full-voice.wav')],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(PUB/'full-voice.wav'),'-c:a','libmp3lame','-b:a','160k',str(ROOT/'OPC-3-v14-F-口播.mp3')],check=True)
timeline={'fps':FPS,'durationFrames':cursor,'voice':content['voice_id'],'shots':all_shots,'captions':all_captions}
for dst in [ROOT/'timeline.json',ROOT/'studio/src/full-content.json']:
    dst.write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
def stamp(t):
    m=round(t); return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
cues=[cue for s in all_shots for cue in s['cues']]
(ROOT/'subtitles.srt').write_text('\n'.join(f'{i+1}\n{stamp(c["startMs"])} --> {stamp(c["displayEndMs"])}\n{c["text"]}\n' for i,c in enumerate(cues)))
(ROOT/'voiceover.txt').write_text('\n\n'.join(c['text'] for c in chapters))
cost={'calls':len(ledger),'usage_characters':sum(r['usage_characters'] for r in ledger),'requests':ledger,'rate_cny_per_10000':3.5,'activation_fee':'no new voice; same voice activated earlier','actual_cash_cny':None}
cost['estimated_tts_cny']=cost['usage_characters']*3.5/10000
(ROOT/'cost-ledger.json').write_text(json.dumps(cost,ensure_ascii=False,indent=2))
print(json.dumps({'seconds':cursor/FPS,'shots':len(all_shots),'captions':len(cues),'tts_cny_estimate':cost['estimated_tts_cny']},ensure_ascii=False))
