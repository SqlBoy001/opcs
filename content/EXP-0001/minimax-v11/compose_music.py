"""Original restrained 84 BPM underscore, composed for this edit. Not ADu's retired score.
Dm9 / Bbmaj7 / Fmaj9 / Cadd9. Soft felt-key arpeggios, pad, quiet brushed pulse.
No samples, copyrighted recordings, API or external music downloads.
"""
import json,wave,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent;P=R/'project';sr=48000;duration=json.loads((P/'timeline.json').read_text())['end']
out=np.zeros((round(duration*sr),2),np.float32);rng=np.random.default_rng(31);beat=60/84
chords=[[50,57,60,64,69],[46,53,57,60,65],[41,53,57,60,67],[48,55,60,62,67]]
def add(sig,at,amp=.1,pan=0):
 i=round(at*sr);n=min(len(sig),len(out)-i)
 if n<=0:return
 out[i:i+n,0]+=sig[:n]*amp*np.sqrt((1-pan)/2);out[i:i+n,1]+=sig[:n]*amp*np.sqrt((1+pan)/2)
def key(note,dur):
 t=np.arange(round(dur*sr))/sr;f=440*2**((note-69)/12);env=(1-np.exp(-t*65))*np.exp(-t*2.0)*np.clip((dur-t)/.16,0,1)
 return (np.sin(2*np.pi*f*t)+.24*np.sin(2*np.pi*f*2*t)+.055*np.sin(2*np.pi*f*3*t))*env
bars=int(np.ceil(duration/(beat*4)))
for bar in range(bars):
 at=bar*4*beat;ch=chords[(bar//2)%4]
 dur=4*beat+.7;t=np.arange(round(dur*sr))/sr;env=np.minimum(t/.7,1)*np.minimum((dur-t)/1.2,1)
 pad=sum(np.sin(2*np.pi*440*2**((n-69)/12)*t) for n in ch[:4])/4*env
 add(pad,at,.05,(-.15 if bar%2 else .15))
 # Four alternating, gently varying musical phrases, with space under speech.
 offsets=[0,1.5,2.5] if bar%4<2 else [.5,2,3.25]
 order=[2,4,3] if bar%2 else [1,3,4]
 for j,b in enumerate(offsets):add(key(ch[order[j]]+12,1.6),at+b*beat,.04 if bar<4 else .035,[-.35,.3,-.1][j])
 if 4<=bar<bars-3:
  t=np.arange(round(.12*sr))/sr;tap=rng.normal(0,1,len(t));tap=np.diff(tap,prepend=0)*np.exp(-t*65)
  for b in [1,3]:add(tap,at+b*beat,.0017,0)
# Soft delay as atmosphere. Delays don't reset at visual cuts.
for delay,g in [(round(.23*sr),.13),(round(.41*sr),.08)]:out[delay:]+=out[:-delay].copy()*g
x=np.arange(len(out))/sr;out*=np.minimum(x/1.4,1)[:,None]*np.clip((duration-x)/2,0,1)[:,None]
with wave.open(str(P/'assets/original-underscore.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes(np.clip(out*32767,-32768,32767).astype('<i2').tobytes())
(R/'music-provenance.json').write_text(json.dumps(dict(type='original procedural composition for this edit',tempo=84,source='compose_music.py',license='Original project composition; no third-party samples',sha256=hashlib.sha256((P/'assets/original-underscore.wav').read_bytes()).hexdigest(),subjective_listening='pending'),indent=2))
