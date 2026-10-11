"""Optional same-script candidate. --check is offline and never charges."""
import argparse, base64, hashlib, json, os, time, urllib.request, urllib.error, urllib.parse
from pathlib import Path

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--check',action='store_true')
parser.add_argument('--voice-id',default=os.getenv('ELEVENLABS_VOICE_ID'))
parser.add_argument('--model',default='eleven_v4')
args=parser.parse_args()
key=os.getenv('ELEVENLABS_API_KEY')
status={'provider':'ElevenLabs','key_configured':bool(key),'voice_id_configured':bool(args.voice_id),
        'ready':bool(key and args.voice_id),'network_called':False}
if args.check:
    print(json.dumps(status));raise SystemExit(0)
if not status['ready']:
    raise SystemExit('Configure ELEVENLABS_API_KEY and a Mandarin ELEVENLABS_VOICE_ID locally; never put the key in chat or source.')
text=''.join(c['text'] for c in json.loads((ROOT/'content.json').read_text())['scenes'])
body={'text':text,'model_id':args.model,'language_code':'zh',
      'voice_settings':{'stability':.5,'similarity_boost':.75}}
run=hashlib.sha256(json.dumps([args.voice_id,body],ensure_ascii=False).encode()).hexdigest()[:12]
dest=ROOT/'elevenlabs-comparison'/run
if dest.exists():raise SystemExit('This candidate already has an attempt; inspect it before any paid retry.')
dest.mkdir(parents=True)
(dest/'request.json').write_text(json.dumps(body,ensure_ascii=False,indent=2))
(dest/'attempt.json').write_text(json.dumps({'time':time.time(),'voice_id':args.voice_id,'max_calls':1}))
url='https://api.elevenlabs.io/v1/text-to-speech/'+urllib.parse.quote(args.voice_id,safe='')+'/with-timestamps?output_format=mp3_44100_128'
request=urllib.request.Request(url,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','xi-api-key':key},method='POST')
try:
    with urllib.request.urlopen(request,timeout=120) as response:
        data=json.load(response)
        receipt={'request_id':response.headers.get('request-id'),'character_count':response.headers.get('x-character-count'),'http_status':response.status,'actual_charge':None}
except urllib.error.HTTPError as e:
    (dest/'failure.json').write_text(json.dumps({'status':e.code,'automatic_retry':False}))
    raise SystemExit('ElevenLabs request failed, HTTP '+str(e.code)+'; no automatic retry.')
(dest/'candidate.mp3').write_bytes(base64.b64decode(data['audio_base64']))
(dest/'alignment.json').write_text(json.dumps({k:v for k,v in data.items() if k!='audio_base64'},ensure_ascii=False,indent=2))
(dest/'receipt.json').write_text(json.dumps(receipt,indent=2))
print('Saved candidate in '+str(dest))
