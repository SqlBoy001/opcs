"""Check the delivered local edit, without rerunning product QA or generation."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'output'
BIN = Path('/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/tools/ffmpeg')
D = json.loads((HERE.parent / 'content.json').read_text())['recap_v08']
movie = OUT / 'OPC-2-v08-recap-180s.mp4'
probe = json.loads(subprocess.check_output([
    str(BIN / 'ffprobe'), '-v', 'error', '-show_streams', '-show_format',
    '-of', 'json', str(movie)]))
streams = probe['streams']
assert len(streams) == 1 and streams[0]['codec_type'] == 'video'
v = streams[0]
assert (v['width'], v['height'], v['r_frame_rate'], int(v['nb_frames'])) == (720, 1280, '24/1', 4320)
assert abs(float(probe['format']['duration']) - 180) < .05
decode = subprocess.run([str(BIN / 'ffmpeg'), '-v', 'error', '-i', str(movie),
    '-f', 'null', '-'], capture_output=True)
assert decode.returncode == 0 and not decode.stderr, decode.stderr.decode()
end = 0
shots = {s['kind']: s for s in D['shots']}
for shot in D['shots']:
    assert shot['start_frame'] == end
    end += shot['duration'] * 24
assert end == 4320
end = 0
srt = (HERE / 'subtitles.srt').read_text()
voice = (HERE / 'voiceover.md').read_text()
for cue in D['captions']:
    assert cue['start_frame'] == end
    end = cue['end_frame']
    shot = shots[cue['shot']]
    assert shot['start_frame'] <= cue['start_frame'] < end <= shot['start_frame'] + shot['duration'] * 24
    assert cue['display_text'] in srt and cue['text'] in voice
    assert len(cue['text']) <= 40
assert end == 4320
verified = []
for key, asset in D['assets'].items():
    if asset.get('sha256'):
        assert hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest() == asset['sha256'], key
        verified.append(key)
result = {
    'duration_seconds': 180, 'resolution': [720, 1280], 'fps': 24,
    'frames': 4320, 'audio': 'silent_review_draft',
    'shots': len(D['shots']), 'captions': len(D['captions']),
    'full_decode': 'passed', 'subtitle_coverage_and_shot_alignment': 'passed',
    'source_hashes_verified': verified,
    'bytes': movie.stat().st_size,
    'sha256': hashlib.sha256(movie.read_bytes()).hexdigest(),
    'cost_basis': D['billing'],
    'subtitle_style': D['subtitle_style'],
    'scope': 'local_content_edit_self_check; not independent product QA',
}
(OUT / 'checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
