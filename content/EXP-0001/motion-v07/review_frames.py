"""Extract one representative encoded frame for each shot for visual review."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / 'output'
shots = json.loads((HERE.parent / 'content.json').read_text())['motion_v07']['shots']
ffmpeg = '/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/tools/ffmpeg/ffmpeg'
frames = [s['start_frame'] + min(144, s['duration'] * 24 - 1) for s in shots]
select = '+'.join(f'eq(n\\,{n})' for n in frames)
subprocess.run([ffmpeg, '-v', 'error', '-y', '-i', str(OUT / 'OPC-2-v07-motion-180s.mp4'),
    '-vf', 'select=' + select + ',scale=288:512', '-vsync', '0',
    str(OUT / 'encoded-%02d.jpg')], check=True)
for offset in (0, 10):
    board = Image.new('RGB', (1500, 1120), '#222222')
    draw = ImageDraw.Draw(board)
    for i, shot in enumerate(shots[offset:offset+10]):
        x, y = i % 5 * 300, i // 5 * 560
        board.paste(Image.open(OUT / f'encoded-{offset+i+1:02d}.jpg'), (x, y+30))
        draw.text((x+5, y+5), shot['id'], fill='white')
    board.save(OUT / f'encoded-board-{offset//10+1}.jpg')
print('20 encoded frames extracted into two review boards')
