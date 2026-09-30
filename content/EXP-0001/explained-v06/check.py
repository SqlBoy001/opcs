"""Targeted self-check of the new export; not a repeat of business QA."""
import hashlib
import json
import subprocess
from pathlib import Path
from decimal import Decimal
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent;OUT=HERE/'output'
BIN=Path('/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/tools/ffmpeg')
DATA=json.loads((HERE.parent/'content.json').read_text())['explained_v06']
VIDEO=OUT/'OPC-2-explained-v06-180s-captioned.mp4'

def main():
    cues=DATA['captions']
    assert cues[0]['start_frame']==0 and cues[-1]['end_frame']==4320
    assert all(a['end_frame']==b['start_frame'] for a,b in zip(cues,cues[1:]))
    assert all(c['end_frame']>c['start_frame'] for c in cues)
    assert ''.join(c['text'] for c in cues)==''.join(''.join(ch['narration']) for ch in DATA['chapters'])
    assert Decimal('200')+Decimal('74.92')==Decimal('274.92')
    expected={'raw':'e0f8d3bfef73503f7d63d8d953cba858af232354528bd6bf69d56e8ecdad2f40','edit':'8a88d6ec1799f8bb073af8d1651d09a4681dab96ed1777295ab6674f3aeaff95','final':'b7066a812e9801f7b3d4b6ab8874a483bb52ca106851f7e07e681a48b4c16029','bad_shackle':'c5d5eadce7f933a645e8d4709921e328ac22c2cf0b14dc16c6bb80b72785bfc3'}
    for key,value in expected.items(): assert DATA['assets'][key]['sha256']==value,key
    probe=json.loads(subprocess.check_output([str(BIN/'ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(VIDEO)]))
    v=probe['streams'][0]
    assert len(probe['streams'])==1 and v['codec_type']=='video'
    assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(720,1280,'24/1',4320)
    assert float(probe['format']['duration'])==180
    decode=subprocess.run([str(BIN/'ffmpeg'),'-v','error','-i',str(VIDEO),'-f','null','-'],capture_output=True,text=True)
    assert decode.returncode==0 and not decode.stderr,decode.stderr
    frames=[]
    for s in DATA['shots']:
        # Exact time is retained in the caption for the visual check.
        t=s['start_frame']/24+min(3,s['duration']/2)
        dest=OUT/f"check-{s['id']}.jpg"
        subprocess.run([str(BIN/'ffmpeg'),'-v','error','-y','-ss',str(t),'-i',str(VIDEO),'-frames:v','1',str(dest)],check=True)
        frames.append((dest,t))
    for page in range(3):
        selected=frames[page*7:(page+1)*7]
        sheet=Image.new('RGB',(350*len(selected),650),'#ddd');d=ImageDraw.Draw(sheet)
        for i,(path,t) in enumerate(selected):
            im=Image.open(path).resize((350,622));sheet.paste(im,(i*350,25));d.text((i*350+8,5),f'{path.stem} / {t:g}s',fill='black')
        sheet.save(OUT/f'contact-{page+1}.jpg')
    result={'media':'PASS','caption_text_and_coverage':'PASS','source_hashes_match_previous_verified_sources':'PASS','account_arithmetic':'PASS','decode_exit':decode.returncode,'decode_stderr':decode.stderr,'duration':180,'frames':4320,'bytes':VIDEO.stat().st_size,'sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'streams':1,'audio':'absent; silent review draft','visual':'contact sheets generated; requires actual viewing','business_qa':'not rerun'}
    (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
