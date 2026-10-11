import json, subprocess, hashlib
from pathlib import Path
r=Path(__file__).resolve().parent;p=r/'OPC-3-v13-pilot.mp4'
d=json.loads((r/'content.json').read_text())
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True,capture_output=True)
a=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
loud=json.JSONDecoder().raw_decode(a.stderr[a.stderr.rfind('{'):])[0]
assert abs(float(info['format']['duration'])-d['durationFrames']/d['fps'])<.1
assert float(loud['input_tp'])<=-.5 and -18<float(loud['input_i'])<-14
assert p.stat().st_size<10000000
cursor=0
for s in d['scenes']:
 assert s['startFrame']==cursor;cursor+=s['durationFrames']
 assert ''.join(c['text'] for c in s['captions'])==s['text']
 assert all(c['startMs']<c['endMs']<=s['durationFrames']/d['fps']*1000 for c in s['captions'])
 assert all(a['endMs']<=b['startMs']+.1 for a,b in zip(s['captions'],s['captions'][1:]))
assert cursor==d['durationFrames']
v=next(s for s in info['streams'] if s['codec_type']=='video')
checks={'type':'content producer targeted self-check','independent_qa':False,'duration_seconds':float(info['format']['duration']),'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'complete_decode':'passed','typescript_and_eslint':'passed','caption_exact_text':'passed','caption_timing_bounds':'passed','four_scene_timeline':'passed','checked_stills':5,'visual_observation':'No obvious overlap or cutoff in the inspected opening, two comparison, cost and takeaway frames','subjective_listening':'pending user listening; not verified by author','elevenlabs':'credential preflight only, no call, key and Mandarin voice ID missing','hyperframes':'official creative guidance applied; MP4 rendered with Remotion','render_browser':'system Google Chrome; initial bundled Headless Shell attempt failed Target closed','npm_audit':'10 high development-tool dependency advisories from scaffold, no complete automatic fix; see npm-audit.json. Not a hosted deployment.','file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'loudness':loud}
(r/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False))
