import re

file_path = r'C:\Users\majo1\Desktop\MiniAmigixV\templates\estudio.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_style = '''<style>
    /* ── TOKENS ─────────────────────────────────────────────── */
    :root {
        --amber:         #f59e0b;
        --amber-light:   #fbbf24;
        --amber-dark:    #b45309;
        --bg:            #0a0a0f;
        --surface:       rgba(255,255,255,0.04);
        --surface-hov:   rgba(255,255,255,0.07);
        --border:        rgba(245,158,11,0.18);
        --border-hov:    rgba(245,158,11,0.45);
        --text:          #f1f5f9;
        --muted:         #94a3b8;
        --radius:        24px;
        --shadow-amber:  0 0 40px rgba(245,158,11,0.18);
        --glow:          0 0 18px rgba(245,158,11,0.5);
    }

    /* ── RESET & BASE ───────────────────────────────────────── */
    .estudio-page * { box-sizing: border-box; }
    .estudio-page {
        min-height: 100vh;
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', system-ui, sans-serif;
        padding-bottom: 40px;
        position: relative;
        overflow: hidden;
    }

    /* orb blobs */
    .estudio-orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
    }
    .estudio-orb-1 {
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(245,158,11,0.2) 0%, transparent 70%);
        top: -100px; left: -100px;
        animation: orbFloat1 10s ease-in-out infinite;
    }
    .estudio-orb-2 {
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(251,191,36,0.15) 0%, transparent 70%);
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

    .estudio-hero {
        position: relative;
        z-index: 1;
        text-align: center;
        padding: 40px 20px 20px;
        animation: fadeSlideUp 0.5s ease both;
    }
    .estudio-hero h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 30%, var(--amber-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0 5px;
    }
    .estudio-hero p { color: var(--muted); margin: 0; }

    /* ── LAYOUT ─────────────────────────────────────────────── */
    .dashboard {
        max-width: 1400px !important;
        margin: 0 auto !important;
        position: relative;
        z-index: 1;
        animation: fadeSlideUp 0.5s 0.2s ease both;
        padding: 0 20px;
    }
    
    .summary-panel {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 24px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: var(--shadow-amber) !important;
        margin-bottom: 24px;
    }
    .summary-stats {
        display: flex; gap: 20px; flex-wrap: wrap; margin-top: 15px;
    }
    .stat-item {
        flex: 1; min-width: 200px;
        background: rgba(0,0,0,0.2) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 16px !important;
        padding: 16px !important; display: flex; align-items: center; gap: 15px;
        transition: all 0.3s;
    }
    .stat-item:hover { border-color: var(--amber); background: rgba(245,158,11,0.05) !important; }
    
    .quick-actions {
        display: flex; gap: 15px; margin-bottom: 24px; flex-wrap: wrap;
    }
    .quick-action-btn {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        padding: 12px 24px !important; border-radius: 50px !important;
        display: flex; align-items: center; gap: 8px; cursor: pointer;
        transition: all 0.3s !important; backdrop-filter: blur(12px); font-weight: 600;
    }
    .quick-action-btn:hover {
        background: linear-gradient(135deg, var(--amber), var(--amber-light)) !important;
        color: #000 !important;
        border-color: transparent !important;
        box-shadow: var(--glow) !important;
    }
    
    .nota-card, .calendario-card, .grafico-card, .pomodoro-card {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 24px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: var(--shadow-amber) !important;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .nota-card:hover, .calendario-card:hover, .grafico-card:hover, .pomodoro-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 40px rgba(245,158,11,0.3) !important;
        border-color: var(--border-hov) !important;
    }
    
    textarea, input[type="text"], input[type="number"], select {
        background: rgba(0,0,0,0.2) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: var(--text) !important; border-radius: 12px !important;
        padding: 12px !important; width: 100%; outline: none; transition: all 0.3s;
    }
    textarea:focus, input[type="text"]:focus, input[type="number"]:focus, select:focus {
        border-color: var(--amber) !important; background: rgba(245,158,11,0.05) !important;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, var(--amber), var(--amber-light)) !important;
        color: #000 !important; border: none !important; font-weight: 700 !important;
        padding: 12px 24px !important; border-radius: 12px !important; cursor: pointer;
        transition: all 0.3s !important; margin-top: 15px; display: inline-block;
    }
    .btn-primary:hover {
        transform: translateY(-2px); box-shadow: var(--glow) !important;
    }
    
    #timer-display { font-size: 4rem !important; font-weight: 800 !important; color: var(--amber-light) !important; }
</style>'''

# Add CSS block at the end of extra_css or right before content
if '{% block content %}' in content:
    content = content.replace('{% block content %}', '{% block content %}\n' + new_style)

# Wrap the dashboard with the page container
if '<div class="dashboard">' in content and '<div class="estudio-page">' not in content:
    content = content.replace('<div class="dashboard">', '''<div class="estudio-page">
    <div class="estudio-orb estudio-orb-1"></div>
    <div class="estudio-orb estudio-orb-2"></div>
    <div class="estudio-hero">
        <span style="font-size:3rem;">📖</span>
        <h1>Estudio</h1>
        <p>Tu espacio de aprendizaje y concentración.</p>
    </div>
    <div class="dashboard">''')
    content = content.replace('</div>\n{% endblock %}', '</div>\n</div>\n{% endblock %}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Estudio updated!")
