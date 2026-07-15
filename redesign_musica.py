import re

file_path = r'C:\Users\majo1\Desktop\MiniAmigixV\templates\musica.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_style = '''<style>
    /* ── TOKENS ─────────────────────────────────────────────── */
    :root {
        --emerald:         #10b981;
        --emerald-light:   #34d399;
        --emerald-dark:    #059669;
        --bg:              #0a0a0f;
        --surface:         rgba(255,255,255,0.04);
        --surface-hov:     rgba(255,255,255,0.07);
        --border:          rgba(16,185,129,0.18);
        --border-hov:      rgba(16,185,129,0.45);
        --text:            #f1f5f9;
        --muted:           #94a3b8;
        --radius:          24px;
        --shadow-emerald:  0 0 40px rgba(16,185,129,0.18);
        --glow:            0 0 18px rgba(16,185,129,0.5);
    }

    /* ── RESET & BASE ───────────────────────────────────────── */
    .musica-page * { box-sizing: border-box; }
    .musica-page {
        min-height: 100vh;
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', system-ui, sans-serif;
        padding-bottom: 40px;
        position: relative;
        overflow: hidden;
    }

    /* orb blobs */
    .musica-orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
    }
    .musica-orb-1 {
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(16,185,129,0.2) 0%, transparent 70%);
        top: -100px; left: -100px;
        animation: orbFloat1 10s ease-in-out infinite;
    }
    .musica-orb-2 {
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(52,211,153,0.15) 0%, transparent 70%);
        bottom: -50px; right: -50px;
        animation: orbFloat2 12s ease-in-out infinite;
    }

    @keyframes orbFloat1 {
        0%,100% { transform: translate(0,0) scale(1); }
        50%      { transform: translate(40px,40px) scale(1.1); }
    }
    @keyframes orbFloat2 {
        0%,100% { transform: translate(0,0) scale(1); }
        50%      { transform: translate(-40px,-40px) scale(0.9); }
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .musica-hero {
        position: relative;
        z-index: 1;
        text-align: center;
        padding: 40px 20px 20px;
        animation: fadeSlideUp 0.5s ease both;
    }
    .musica-hero h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 30%, var(--emerald-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0 5px;
    }
    .musica-hero p { color: var(--muted); margin: 0; }

    /* ── LAYOUT ─────────────────────────────────────────────── */
    .music-wrapper {
        max-width: 1400px !important;
        margin: 0 auto !important;
        position: relative;
        z-index: 1;
        animation: fadeSlideUp 0.5s 0.2s ease both;
        padding: 0 20px;
    }
    
    .music-section {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 24px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: var(--shadow-emerald) !important;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .music-section:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 40px rgba(16,185,129,0.3) !important;
        border-color: var(--border-hov) !important;
    }
    
    .playlist-card, .track-item {
        background: rgba(0,0,0,0.2) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        transition: all 0.3s;
    }
    .playlist-card:hover, .track-item:hover {
        border-color: var(--emerald) !important;
        background: rgba(16,185,129,0.05) !important;
    }
    
    .play-btn-glow {
        background: linear-gradient(135deg, var(--emerald), var(--emerald-light)) !important;
        box-shadow: var(--glow) !important;
        color: #fff !important;
        border: none !important; border-radius: 50% !important;
    }
    .play-btn-glow:hover { transform: scale(1.1); filter: brightness(1.1); }
</style>'''

if '{% block content %}' in content:
    content = content.replace('{% block content %}', '{% block content %}\n' + new_style)

if '<div class="music-wrapper">' in content and '<div class="musica-page">' not in content:
    content = content.replace('<div class="music-wrapper">', '''<div class="musica-page">
    <div class="musica-orb musica-orb-1"></div>
    <div class="musica-orb musica-orb-2"></div>
    <div class="musica-hero">
        <span style="font-size:3rem;">🎵</span>
        <h1>Música</h1>
        <p>Tu banda sonora perfecta para cada momento.</p>
    </div>
    <div class="music-wrapper">''')
    content = content.replace('</div>\n{% endblock %}', '</div>\n</div>\n{% endblock %}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Musica updated!")
