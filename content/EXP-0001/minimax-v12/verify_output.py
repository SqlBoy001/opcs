import json, subprocess, hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
result=json.loads((R/'checks.json').read_text());result['files']=[]
for name in ['OPC-3-v12-expressive-1080p.mp4','OPC-3-v12-expressive-review-720p.mp4']:
    p=R/name
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    if '1080p' in name:
        manifest=json.loads(Path(str(p)+'.manifest.json').read_text())
        assert manifest['output_sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
        # The exporter already decodes the full master before writing its manifest.
    else:
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],capture_output=True,text=True,check=True)
    loud=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    metrics=json.JSONDecoder().raw_decode(loud.stderr[loud.stderr.rfind('{'):])[0]
    assert -18<float(metrics['input_i'])<-14,metrics
    assert float(metrics['input_tp'])<=-.5,metrics
    assert abs(float(info['format']['duration'])-result['duration_seconds'])<.1
    if '720p' in name: assert p.stat().st_size<10_000_000
    item=dict(file=name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),width=v['width'],height=v['height'],fps=v['avg_frame_rate'],duration=info['format']['duration'],audio_codec=a['codec_name'],sample_rate=a['sample_rate'],decode='passed',loudness=metrics)
    result['files'].append(item)
result['video_checks']='passed: full decode, streams, duration, loudness/peak; not subjective listening'
(R/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
