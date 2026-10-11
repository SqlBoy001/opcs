import json, sqlite3, urllib.request, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent
DB = pathlib.Path('/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/data/drama_generator.db')
API = 'https://api.minimax.cn/v1/t2a_v2'
VOICE = 'Chinese (Mandarin)_Unrestrained_Young_Man'

def generate(chapter):
    name = chapter['id']
    dst = ROOT / 'speech' / name
    if dst.with_suffix('.receipt.json').exists():
        print(name, 'cached', flush=True)
        return
    if dst.with_suffix('.attempt.json').exists():
        raise SystemExit('Existing request attempt without completion; inspect before paid retry: '+name)
    body = dict(model='speech-2.8-hd', text=chapter['text'], stream=False,
        voice_setting=dict(voice_id=chapter.get('voice',VOICE), speed=chapter.get('speed',1.12), vol=1, pitch=0),
        audio_setting=dict(sample_rate=32000, bitrate=128000, format='mp3', channel=1),
        language_boost='Chinese', subtitle_enable=True, subtitle_type='word',
        output_format='hex')
    if chapter.get('emotion'): body['voice_setting']['emotion']=chapter['emotion']
    dst.with_suffix('.request.json').write_text(json.dumps(body, ensure_ascii=False, indent=2))
    db=sqlite3.connect('file:'+str(DB)+'?mode=ro', uri=True)
    row=db.execute("SELECT api_key FROM ai_service_configs WHERE id=7 AND service_type='tts' AND provider='minimax'").fetchone()
    db.close()
    if not row or not row[0]: raise SystemExit('No configured MiniMax key')
    req=urllib.request.Request(API, data=json.dumps(body, ensure_ascii=False).encode(), headers={'Content-Type':'application/json','Authorization':'Bearer '+row[0]}, method='POST')
    dst.with_suffix('.attempt.json').write_text(json.dumps({'at':time.time(),'endpoint':API,'chapter':name}))
    try:
        with urllib.request.urlopen(req, timeout=180) as r: result=json.load(r)
    except Exception as e:
        print('Request failed:',type(e).__name__,flush=True); raise SystemExit(1)
    status=result.get('base_resp',{})
    receipt={'base_resp':status,'trace_id':result.get('trace_id'),'extra_info':result.get('extra_info'),'model':body['model'],'voice':body['voice_setting']['voice_id'],'speed':body['voice_setting']['speed'],'emotion':body['voice_setting'].get('emotion','auto')}
    dst.with_suffix('.response-meta.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    if status.get('status_code') != 0: raise SystemExit(str(status))
    data=result.get('data',{}); blob=bytes.fromhex(data['audio'])
    dst.with_suffix('.mp3').write_bytes(blob)
    sub_url=data.get('subtitle_file')
    if not sub_url: raise SystemExit('Audio received but subtitle_file missing')
    with urllib.request.urlopen(sub_url,timeout=40) as r: sub=r.read()
    dst.with_suffix('.subtitles.json').write_bytes(sub)
    dst.with_suffix('.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    print(name, json.dumps(receipt,ensure_ascii=False),flush=True)

if __name__=='__main__':
    plan=json.loads((ROOT/'speech-plan.json').read_text())
    for c in plan:
        if len(sys.argv)<2 or c['id'] in sys.argv[1:]: generate(c)
