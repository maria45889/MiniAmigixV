import re
import os

configs = [
    {
        'file': r'C:\Users\majo1\Desktop\MiniAmigixV\templates\juegos.html',
        'color': '#ef4444',
        'color_light': '#f87171',
        'color_dark': '#b91c1c',
        'emoji': '🎮',
        'title': 'Juegos Arena',
        'subtitle': 'Pon a prueba tu mente y diviértete con nuestros mini-juegos.',
        'page_class': 'juegos-page',
        'orb_class': 'juegos-orb',
        'hero_class': 'juegos-hero',
        'target_wrapper': '<div class="games-page-background">',
        'name': 'Juegos'
    },
    {
        'file': r'C:\Users\majo1\Desktop\MiniAmigixV\templates\traductor\traductor.html',
        'color': '#14b8a6',
        'color_light': '#2dd4bf',
        'color_dark': '#0f766e',
        'emoji': '🌍',
        'title': 'Traductor Inteligente',
        'subtitle': 'Traduce y comunícate sin barreras en múltiples idiomas.',
        'page_class': 'traductor-page',
        'orb_class': 'traductor-orb',
        'hero_class': 'traductor-hero',
        'target_wrapper': '<div class="translator-container">',
        'name': 'Traductor'
    },
    {
        'file': r'C:\Users\majo1\Desktop\MiniAmigixV\templates\entretenimiento.html',
        'color': '#8b5cf6',
        'color_light': '#a78bfa',
        'color_dark': '#6d28d9',
        'emoji': '🍿',
        'title': 'Entretenimiento',
        'subtitle': 'Descubre las mejores películas, series y recomendaciones.',
        'page_class': 'entretenimiento-page',
        'orb_class': 'entretenimiento-orb',
        'hero_class': 'entretenimiento-hero',
        'target_wrapper': '<div class="entertainment-wrapper">',
        'name': 'Entretenimiento'
    },
    {
        'file': r'C:\Users\majo1\Desktop\MiniAmigixV\templates\soporte\index.html',
        'color': '#3b82f6',
        'color_light': '#60a5fa',
        'color_dark': '#1d4ed8',
        'emoji': '🛠️',
        'title': 'Soporte Técnico',
        'subtitle': 'Encuentra ayuda y reporta problemas fácilmente.',
        'page_class': 'soporte-page',
        'orb_class': 'soporte-orb',
        'hero_class': 'soporte-hero',
        'target_wrapper': '<div class="dashboard">',
        'name': 'Soporte'
    },
    {
        'file': r'C:\Users\majo1\Desktop\MiniAmigixV\templates\panel_admin.html',
        'color': '#f43f5e',
        'color_light': '#fb7185',
        'color_dark': '#be123c',
        'emoji': '⚙️',
        'title': 'Panel de Administración',
        'subtitle': 'Control total sobre la plataforma MiniAmigixV.',
        'page_class': 'admin-page',
        'orb_class': 'admin-orb',
        'hero_class': 'admin-hero',
        'target_wrapper': '<div class="dashboard">',
        'name': 'Panel Admin'
    }
]

def generate_style(cfg):
    return f'''<style>
    :root {{
        --accent:         {cfg['color']};
        --accent-light:   {cfg['color_light']};
        --accent-dark:    {cfg['color_dark']};
        --bg:            #0a0a0f;
        --surface:       rgba(255,255,255,0.04);
        --surface-hov:   rgba(255,255,255,0.07);
        --border:        rgba(255,255,255,0.1);
        --border-hov:    {cfg['color']}50;
        --text:          #f1f5f9;
        --muted:         #94a3b8;
        --radius:        24px;
        --shadow-accent: 0 0 40px {cfg['color']}30;
        --glow:          0 0 18px {cfg['color']}80;
    }}

    .{cfg['page_class']} * {{ box-sizing: border-box; }}
    .{cfg['page_class']} {{
        min-height: 100vh;
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', system-ui, sans-serif;
        padding-bottom: 40px;
        position: relative;
        overflow: hidden;
    }}

    .{cfg['orb_class']} {{
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
    }}
    .{cfg['orb_class']}-1 {{
        width: 400px; height: 400px;
        background: radial-gradient(circle, {cfg['color']}33 0%, transparent 70%);
        top: -100px; left: -100px;
        animation: orbFloat1 10s ease-in-out infinite;
    }}
    .{cfg['orb_class']}-2 {{
        width: 350px; height: 350px;
        background: radial-gradient(circle, {cfg['color_light']}26 0%, transparent 70%);
        bottom: -50px; right: -50px;
        animation: orbFloat2 12s ease-in-out infinite;
    }}

    @keyframes orbFloat1 {{
        0%,100% {{ transform: translate(0,0) scale(1); }}
        50%      {{ transform: translate(40px,40px) scale(1.1); }}
    }}
    @keyframes orbFloat2 {{
        0%,100% {{ transform: translate(0,0) scale(1); }}
        50%      {{ transform: translate(-40px,-40px) scale(0.9); }}
    }}
    @keyframes fadeSlideUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    .{cfg['hero_class']} {{
        position: relative;
        z-index: 1;
        text-align: center;
        padding: 40px 20px 20px;
        animation: fadeSlideUp 0.5s ease both;
    }}
    .{cfg['hero_class']} h1 {{
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 30%, var(--accent-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0 5px;
    }}
    .{cfg['hero_class']} p {{ color: var(--muted); margin: 0; }}

    /* Glassmorphism Overrides */
    .{cfg['page_class']} > div:not(.{cfg['hero_class']}):not(.{cfg['orb_class']}) {{
        position: relative;
        z-index: 1;
        animation: fadeSlideUp 0.5s 0.2s ease both;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 20px;
    }}
    
    .games-hero-banner, .translator-header, .movies-header, .stats-cards, .games-grid, .ticket-list, .translator-layout {{
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: var(--shadow-accent) !important;
        margin-bottom: 24px;
        transition: transform 0.3s, box-shadow 0.3s;
    }}
    
    .game-card, .movie-card, .series-card, .ticket-card, .translator-box {{
        background: rgba(0,0,0,0.2) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 16px !important;
        transition: all 0.3s;
    }}
    
    .game-card:hover, .movie-card:hover, .series-card:hover, .ticket-card:hover {{
        border-color: var(--accent) !important;
        background: {cfg['color']}0D !important;
        transform: translateY(-4px) !important;
    }}
    
    .hero-continue-btn, .btn-primary, .translate-btn {{
        background: linear-gradient(135deg, var(--accent), var(--accent-light)) !important;
        color: #fff !important;
        border: none !important;
        box-shadow: var(--glow) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
    }}
</style>'''

for cfg in configs:
    if os.path.exists(cfg['file']):
        with open(cfg['file'], 'r', encoding='utf-8') as f:
            content = f.read()
            
        style = generate_style(cfg)
        
        # Inject style
        if '{% block content %}' in content:
            content = content.replace('{% block content %}', '{% block content %}\n' + style)
            
        # Replace wrapper
        if cfg['target_wrapper'] in content and f'class="{cfg["page_class"]}"' not in content:
            replacement = f'''<div class="{cfg['page_class']}">
    <div class="{cfg['orb_class']} {cfg['orb_class']}-1"></div>
    <div class="{cfg['orb_class']} {cfg['orb_class']}-2"></div>
    <div class="{cfg['hero_class']}">
        <span style="font-size:3rem;">{cfg['emoji']}</span>
        <h1>{cfg['title']}</h1>
        <p>{cfg['subtitle']}</p>
    </div>
    {cfg['target_wrapper']}'''
            content = content.replace(cfg['target_wrapper'], replacement, 1)
            content = content.replace('</div>\n{% endblock %}', '</div>\n</div>\n{% endblock %}')
            
        with open(cfg['file'], 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {cfg['name']}")
    else:
        print(f"File not found: {cfg['file']}")
