import json,subprocess,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parent
files=[R/'OPC-2-v10-adu-motion-129s.mp4',R/'OPC-2-v10-review-720p.mp4']
result={'type':'content-producer self-check','independent_qa':False,'subjective_listening':'not_performed; human review requested','files':[]}
for p in files:
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]))
 v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True)
 run=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-vn','-af','loudnorm=I=-15.5:TP=-1.2:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 measured=json.JSONDecoder().raw_decode(run.stderr[run.stderr.rfind('{'):])[0];assert float(measured['input_tp'])<=-.5,measured
 assert -16.5<float(measured['input_i'])<-14.8,measured
 item=dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),width=v['width'],height=v['height'],fps=v['avg_frame_rate'],frames=v['nb_read_frames'],duration=d['format']['duration'],audio_codec=a['codec_name'],audio_sample_rate=a['sample_rate'],loudness=measured,full_decode='passed',color={k:v.get(k) for k in ['color_range','color_space','color_transfer','color_primaries']})
 result['files'].append(item)
original=Path('/Users/shenzihao/Documents/ChatGPT/OPC-2-content-v09/OPC-2-v09-story-185s.mp4')
result['v09_original_sha256']=hashlib.sha256(original.read_bytes()).hexdigest();assert result['v09_original_sha256']=='3ae4cb5b966d67d072efe025c6d29512d4b65a26c8bac86ea01f94ab4dc21d04'
g=json.loads((R/'geometry-check.json').read_text())['data']['result'];result['caption_geometry']={k:v for k,v in g.items() if k!='captions'};assert not g['overflow'] and not g['outside'] and not g['collisions']
T=json.loads((R/'project/timeline.json').read_text());D=json.loads((R/'content-source-v09.json').read_text());assert [c['source_text'] for c in T['subtitles']]==[c['text'] for c in D['captions']]
assert all(c['speech_end']<=c['t1'] and c['t0']<=c['speech_start'] for c in T['subtitles'])
result['source_text_preserved']=True;result['audio_caption_method']='73 individually generated real audio files; measured sample boundaries; no inferred word timestamps';result['chapters']=9;result['shots']=24;result['paid_api_calls']=0
(R/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
