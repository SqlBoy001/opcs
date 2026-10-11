"""Build the pilot from provider timing; no network or paid calls."""
import json, math, re, subprocess, wave, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'studio/public'
FPS, SR = 30, 48000
plan = json.loads((ROOT / 'content.json').read_text())['scenes']
content = {'schemaVersion': 1, 'fps': FPS, 'width': 1080, 'height': 1920,
           'brand': 'OPC / 实验记录', 'reviewStatus': 'pilot_pending_listening',
           'scenes': [], 'source': 'EXP-0001; v12 selected evidence',
           'costScope': 'User requested approximate video generation/modification spend; v2 limits retained in production records.'}
titles = ['为了这60秒', '时代不对，细节也不对', '这版，花了多少？', '先把错误拦下来']
cursor, ledger = 0, []
global_cues = []
audio_parts = []
for i, c in enumerate(plan):
    stem = ROOT / 'speech' / c['id']
    raw = json.loads(stem.with_suffix('.subtitles.json').read_text())
    words = [w for seg in raw for w in seg['timestamped_words']]
    assert ''.join(w['word'] for w in words) == c['text']
    wav = stem.with_suffix('.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(stem.with_suffix('.mp3')),
                    '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le', str(wav)], check=True)
    with wave.open(str(wav)) as f:
        pcm = f.readframes(f.getnframes())
    lead, tail = round(.12 * SR), round((.65 if i == 3 else .3) * SR)
    frames = math.ceil((lead + len(pcm)//2 + tail)/SR*FPS)
    length = frames * SR // FPS
    padded = bytes(lead*2) + pcm + bytes((length-lead-len(pcm)//2)*2)
    out = PUBLIC / ('voice-'+c['id']+'.wav')
    with wave.open(str(out), 'wb') as f:
        f.setparams((1,2,SR,0,'NONE','not compressed'));f.writeframes(padded)
    audio_parts.append(padded)
    captions = [{'text':w['word'], 'startMs':w['time_begin']+120,
                 'endMs':w['time_end']+120, 'timestampMs':None, 'confidence':None}
                for w in words]
    cues, current = [], []
    for token in captions:
        current.append(token)
        if re.search('[，。；：？！]', token['text']) or len(current)>=11:
            cues.append({'text':''.join(w['text'] for w in current),
                         'startMs':current[0]['startMs'], 'endMs':current[-1]['endMs'],
                         'words':current});current=[]
    if current:
        cues.append({'text':''.join(w['text'] for w in current),
                     'startMs':current[0]['startMs'], 'endMs':current[-1]['endMs'], 'words':current})
    # Keep a phrase visible through short pauses without changing word timings.
    for a,b in zip(cues,cues[1:]): a['displayEndMs']=b['startMs']
    cues[-1]['displayEndMs']=frames/FPS*1000
    scene={**c, 'title':c.get('title', titles[i]), 'startFrame':cursor, 'durationFrames':frames,
           'audio':'voice-'+c['id']+'.wav', 'captions':captions, 'cues':cues}
    content['scenes'].append(scene)
    for cue in cues:
        global_cues.append({'text':cue['text'],'start':cursor/FPS+cue['startMs']/1000,
                            'end':cursor/FPS+cue.get('displayEndMs',cue['endMs'])/1000})
    cursor += frames
    receipt=json.loads(stem.with_suffix('.receipt.json').read_text())
    ledger.append({'id':c['id'],'traceId':receipt['trace_id'],
                   'usageCharacters':receipt['extra_info']['usage_characters']})
content['durationFrames']=cursor
assert 15 <= cursor/FPS <= 20, ('pilot duration outside target', cursor/FPS)
for p in [ROOT/'content.json', ROOT/'studio/src/content.json']:
    p.write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')
with wave.open(str(ROOT/'voice.wav'),'wb') as f:
    f.setparams((1,2,SR,0,'NONE','not compressed'));f.writeframes(b''.join(audio_parts))
def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
(ROOT/'subtitles.srt').write_text('\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}\n' for i,c in enumerate(global_cues)))
cost={'provider':'MiniMax','calls':len(ledger),'requests':ledger,
      'usageCharacters':sum(c['usageCharacters'] for c in ledger),
      'actualCashCny':None,'rateCnyPer10000':3.5,'estimateSource':'https://platform.minimax.cn/docs/guides/pricing-paygo'}
cost['estimatedCny']=cost['usageCharacters']*3.5/10000
(ROOT/'cost-ledger.json').write_text(json.dumps(cost,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'durationSeconds':cursor/FPS,'captions':len(global_cues),'cost':cost},ensure_ascii=False))
