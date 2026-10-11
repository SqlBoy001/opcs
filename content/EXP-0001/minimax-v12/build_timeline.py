import json, math, pathlib, subprocess, wave
ROOT=pathlib.Path(__file__).resolve().parent
P=ROOT/'project'; SR=48000; FPS=60
plan=json.loads((ROOT/'speech-plan.json').read_text())
subs=[]; shots=[]; audio=[]; cursor=0; ledger=[]
for chapter in plan:
    id=chapter['id']; prefix=ROOT/'speech'/id
    raw=json.loads(prefix.with_suffix('.subtitles.json').read_text())
    words=[w for seg in raw for w in seg['timestamped_words']]
    joined=''.join(seg['text'] for seg in raw)
    assert joined==chapter['text'],(id,'subtitle text mismatch')
    assert ''.join(w['word'] for w in words)==chapter['text'],(id,'word coverage mismatch')
    dst=prefix.with_suffix('.wav')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(prefix.with_suffix('.mp3')),'-ar',str(SR),'-ac','1','-c:a','pcm_s16le',str(dst)],check=True)
    with wave.open(str(dst),'rb') as f: data=f.readframes(f.getnframes())
    count=len(data)//2
    lead=round(.15*SR) if not audio else 0
    offset=(cursor+lead)/SR
    current_text=0
    local_shots=[]
    for source in chapter['shots']:
        cues=[]
        for cap in source['captions']:
            end_text=current_text+len(cap['text'])
            ws=[w for w in words if w['word_begin']<end_text and w['word_end']>current_text]
            assert ws,(id,cap)
            t0=offset+ws[0]['time_begin']/1000
            t1=offset+ws[-1]['time_end']/1000
            assert t0<t1<=offset+count/SR+.05,(id,t0,t1)
            cue=dict(id=len(subs),zh=cap['display_text'],t0=t0,t1=t1,source_text=cap['text'],shot=source['kind'],speech_start=t0,speech_end=t1,alignment='MiniMax word timestamps')
            subs.append(cue);cues.append(cue);current_text=end_text
        shot={k:v for k,v in source.items() if k!='captions'}
        shot.update(t0=cues[0]['t0'],t1=cues[-1]['t1'],cues=cues)
        local_shots.append(shot)
    assert current_text==len(chapter['text'])
    pad=math.ceil((cursor+lead+count+SR*.18)/(SR/FPS))*int(SR/FPS)-(cursor+lead+count)
    local_shots[0]['t0']=cursor/SR
    for a,b in zip(local_shots,local_shots[1:]):
        cut=round(b['t0']*FPS)/FPS
        a['t1']=cut;b['t0']=cut
    cursor+=lead+count+pad
    local_shots[-1]['t1']=cursor/SR
    shots+=local_shots;audio.append(bytes(lead*2)+data+bytes(pad*2))
    receipt=json.loads(prefix.with_suffix('.receipt.json').read_text())
    ledger.append(dict(chapter=id,trace_id=receipt['trace_id'],usage_characters=receipt['extra_info']['usage_characters'],audio_length_ms=receipt['extra_info']['audio_length'],voice=receipt['voice'],speed=receipt['speed'],emotion=receipt['emotion']))
audio.append(bytes(SR*2));cursor+=SR;shots[-1]['t1']=cursor/SR
with wave.open(str(P/'voice.wav'),'wb') as f:
    f.setparams((1,2,SR,0,'NONE','not compressed'));f.writeframes(b''.join(audio))
end=cursor/SR
t=dict(end=end,fps=FPS,shots=shots,subtitles=subs)
(P/'timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2))
(P/'timeline.js').write_text('window.TIMELINE='+json.dumps(dict(end=end,shots=shots),ensure_ascii=False)+';')
(P/'subs.js').write_text('window.SUBS='+json.dumps(subs,ensure_ascii=False)+';')
cfg=json.loads((P/'config.js').read_text().split('=',1)[1].rstrip('; \n'));cfg['end']=end
(P/'config.js').write_text('window.CONFIG='+json.dumps(cfg,ensure_ascii=False)+';')
def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
(ROOT/'subtitles.srt').write_text('\n'.join(f'{i+1}\n{stamp(s["t0"])} --> {stamp(s["t1"])}\n{s["zh"]}\n' for i,s in enumerate(subs)))
(ROOT/'voiceover.txt').write_text('\n\n'.join(c['text'] for c in plan))
cost=dict(provider='MiniMax',model='speech-2.8-hd',voice=ledger[0]['voice'],speed=ledger[0]['speed'],calls=len(ledger),usage_characters=sum(r['usage_characters'] for r in ledger),rate_cny_per_10000=3.5,rate_source='https://platform.minimax.cn/docs/guides/pricing-paygo',currency='CNY',actual_account_charge=None,account_charge_note='No readable billing reconciliation obtained; calculated amount is published-rate estimate, not verified cash charge',requests=ledger)
extras=[]
for f in (ROOT/'speech').glob('*.receipt.json'):
    if f.stem.split('.')[0] not in {c['id'] for c in plan}:
        x=json.loads(f.read_text());extras.append(dict(sample=f.stem,trace_id=x['trace_id'],usage_characters=x['extra_info']['usage_characters'],voice=x['voice'],speed=x['speed'],emotion=x['emotion']))
cost['additional_samples']=extras
cost['narration_calls']=len(ledger)
cost['calls']+=len(extras)
cost['usage_characters']+=sum(x['usage_characters'] for x in extras)
cost['estimated_cny']=round(cost['usage_characters']*3.5/10000,6)
(ROOT/'cost-ledger.json').write_text(json.dumps(cost,ensure_ascii=False,indent=2))
print(json.dumps(dict(duration=end,shots=len(shots),captions=len(subs),cost=cost['estimated_cny']),ensure_ascii=False))
