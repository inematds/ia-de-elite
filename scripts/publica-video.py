#!/usr/bin/env python3
"""Publica o vídeo "IA de elite — 7 hábitos" (Explicavideos v2 viral, refazvideo 19/10/2026) neste repo.
Release video-v1.0.0 (MP4 com trilha + SRT) + videos/index.html (player com capítulos e legenda VTT) + videos/poster.jpg.
Não faz commit. Idempotente: sobe só o que mudou de tamanho.
Uso: python3 scripts/publica-video.py"""
import html, json, re, subprocess
from pathlib import Path

OUT = Path.home() / 'projetos/output/explica-He-NyJjzWM0/v2'
REPO = Path(__file__).resolve().parent.parent
GH = 'inematds/ia-de-elite'
TAG = 'video-v1.0.0'
BASE = f'https://github.com/{GH}/releases/download/{TAG}/'
NAME = 'ia-de-elite-pt-16x9'
TITLE = 'IA de elite: os 7 hábitos de quem usa IA no topo'
H1 = 'Use a IA como quem está <b>no topo</b>'
LEAD = ('Não é o modelo nem uma ferramenta secreta: é o jeito de conversar com a IA. Em 3 minutos e meio, os 7 hábitos, do mais simples ao mais ousado: fale em vez de digitar, IA na reunião, mostre em vez de contar, deixe a IA te entrevistar, peça falhas, teste você mesmo e mente aberta. No fim, o kit aberto e grátis.')


def sh(*a, **kw):
    return subprocess.run(a, check=True, text=True, capture_output=True, **kw).stdout


def main():
    rec = json.loads((OUT / 'verification/assembled-pt.json').read_text())
    full = OUT.parent / 'entrega/ia-de-elite.mp4'   # com trilha (som_viral); legenda do montado
    srt = Path(rec['file']).with_suffix('.srt')
    scenes = json.loads((OUT / 'docs/lesson-pt.json').read_text())
    chapters = [(int(c['time']), scenes[c['scene'] - 1]['title']) for c in rec['chapters']]
    d = rec['duration']; dd = f"{int(d // 60)}min{int(d % 60):02d}s"
    stage = OUT / 'release'; stage.mkdir(exist_ok=True)
    assets = []
    for src, ext in ((full, 'mp4'), (srt, 'srt')):
        dst = stage / f'{NAME}.{ext}'
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            dst.unlink(missing_ok=True); dst.hardlink_to(src)
        assets.append(dst)
    if subprocess.run(['gh', 'release', 'view', TAG, '--repo', GH], capture_output=True).returncode:
        sh('gh', 'release', 'create', TAG, '--repo', GH, '--title', f'{TITLE} (vídeo)', '--notes',
           f'{TITLE}: vídeo com avatar e voz do Nei, legendas em PT.\n\nAssistir: https://inematds.github.io/ia-de-elite/videos/')
    have = {a['name']: a['size'] for a in json.loads(sh('gh', 'release', 'view', TAG, '--repo', GH, '--json', 'assets'))['assets']}
    for f in assets:
        if have.get(f.name) != f.stat().st_size:
            print('upload', f.name, flush=True); sh('gh', 'release', 'upload', TAG, str(f), '--repo', GH, '--clobber')
    folder = REPO / 'videos'; folder.mkdir(exist_ok=True)
    (folder / 'pt.vtt').write_text('WEBVTT\n\n' + re.sub(r'(\d\d:\d\d:\d\d),(\d{3})', r'\1.\2', srt.read_text()))
    sh('ffmpeg', '-v', 'error', '-y', '-ss', '1.5', '-i', str(full), '-frames:v', '1', '-vf', 'scale=1280:-2', '-q:v', '4', str(folder / 'poster.jpg'))
    caps = ''.join(f'<button type="button" data-time="{s}">{s // 60:02d}:{s % 60:02d} · {html.escape(c)}</button>' for s, c in chapters)
    page = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TITLE)} · INEMA.CLUB</title><meta name="description" content="{html.escape(LEAD)}">
<meta property="og:image" content="https://inematds.github.io/ia-de-elite/videos/poster.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>:root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;background:#0c0c10;color:#f2f0ea;font:18px/1.6 Inter,system-ui,sans-serif}}main{{max-width:1100px;margin:auto;padding:32px 16px}}
a{{color:#FACC15}}h1{{font-family:Sora,sans-serif;font-size:clamp(1.8rem,5vw,2.8rem);line-height:1.15;margin:.4em 0}}h1 b{{color:#FACC15}}.lead{{color:#b9b6ad;max-width:780px}}
.card{{background:#15151c;border:1px solid #2a2a33;border-radius:16px;padding:20px;margin:28px 0}}.card h2{{font-family:Sora,sans-serif;margin:0 0 8px;font-size:1.3rem}}.card h2 span{{color:#8a877f;font-size:1rem;font-weight:500}}
video{{width:100%;aspect-ratio:16/9;background:#000;border-radius:12px}}
summary{{cursor:pointer;color:#FACC15;margin-top:8px}}button{{display:block;background:#0c0c10;color:#f2f0ea;border:1px solid #2a2a33;border-radius:8px;padding:10px 12px;margin:6px 0;text-align:left;cursor:pointer;width:100%;font:inherit}}
:focus-visible{{outline:3px solid #FACC15;outline-offset:3px}}footer{{color:#8a877f;font-size:15px;margin-top:40px}}</style></head>
<body><main><nav><a href="https://inema.club">INEMA.CLUB</a> · <a href="../guia/">Guia do kit</a> · <a href="https://github.com/{GH}">GitHub</a></nav>
<h1>{H1}</h1>
<p class="lead">{html.escape(LEAD)}</p>
<section class="card" id="pt"><h2>{html.escape(TITLE)} <span>{dd}</span></h2>
<video controls preload="metadata" playsinline poster="poster.jpg"><source src="{BASE}{NAME}.mp4" type="video/mp4"><track default kind="subtitles" src="pt.vtt" srclang="pt" label="Português"></video>
<p><a href="{BASE}{NAME}.mp4">Baixar MP4</a> · <a href="{BASE}{NAME}.srt">Baixar legendas</a> · <a href="../guia/">Kit aberto e grátis</a></p>
<details open><summary>Capítulos</summary>{caps}</details></section>
<footer>Produzido com o <a href="https://inematds.github.io/explicavideos/guia/">Explicavideos v2</a>. Conteúdo aberto e gratuito do <a href="https://inema.club">INEMA.CLUB</a>.</footer></main>
<script>document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{{const v=b.closest('.card').querySelector('video');v.currentTime=Number(b.dataset.time);v.play();}}));</script></body></html>
'''
    (folder / 'index.html').write_text(page)
    (folder / 'delivery.json').write_text(json.dumps({'pt': {'url': BASE + NAME + '.mp4', 'srt': BASE + NAME + '.srt', 'duration': round(d, 2)}}, indent=2) + '\n')
    print('OK', BASE + NAME + '.mp4', dd, len(chapters), 'capítulos')


if __name__ == '__main__':
    main()
