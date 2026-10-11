const captionBase=window.OVERLAY;
window.OVERLAY=t=>{captionBase(t);const shot=TIMELINE.shots.find(s=>t>=s.t0&&t<s.t1);const light=shot?.chapter==='02';document.querySelectorAll('.native-subtitles .sz').forEach(el=>{el.style.color=light?'#132E37':'#FFFFFF';el.style.webkitTextStroke=light?'0px transparent':'2px rgba(10,16,22,.85)';});};
