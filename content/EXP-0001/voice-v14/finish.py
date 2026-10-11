"""Create a bounded-size chat copy and inspect actual encoded output."""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
master=ROOT/'OPC-3-v14-F-1080p.mp4'
delivery=ROOT/'OPC-3-v14-F-完整版.mp4'
def run(args): subprocess.run(args,check=True)
def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
run(['ffmpeg','-v','error','-i',str(master),'-f','null','-'])
print('Master decode passed',flush=True)
common=['ffmpeg','-v','error','-y','-i',str(master),'-vf','scale=720:1280:flags=lanczos','-c:v','libx264','-b:v','530k','-preset','fast','-pix_fmt','yuv420p','-passlogfile',str(ROOT/'delivery-pass')]
run(common+['-pass','1','-an','-f','null','/dev/null'])
run(common+['-pass','2','-c:a','aac','-b:a','96k','-ar','48000','-movflags','+faststart',str(delivery)])
assert delivery.stat().st_size<10_000_000
run(['ffmpeg','-v','error','-i',str(delivery),'-f','null','-'])
run(['ffmpeg','-v','error','-y','-ss','39.5','-i',str(delivery),'-frames:v','1','-update','1',str(ROOT/'prompt-final.jpg')])
report={'master':{},'chat_copy':{},'self_check':True,'human_full_listening':'pending','targeted_checks_only':True}
for name,path in [('master',master),('chat_copy',delivery)]:
    pp=probe(path);v=next(s for s in pp['streams'] if s['codec_type']=='video');a=next(s for s in pp['streams'] if s['codec_type']=='audio')
    assert v['nb_frames']=='3617'
    assert abs(float(v['duration'])-float(a['duration']))<0.1
    report[name]={'path':str(path),'bytes':path.stat().st_size,'duration_seconds':float(pp['format']['duration']),'dimensions':[v['width'],v['height']],'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'fps':v['r_frame_rate'],'frames':int(v['nb_frames']),'decode':'passed','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(ROOT/'output-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False),flush=True)
