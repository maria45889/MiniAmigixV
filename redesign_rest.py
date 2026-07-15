import re
import os

configs = [
    {
        'file': r'C:\Users\majo1\Desktop\MiniAmigixV\templates\clima\clima.html',
        'color': '#06b6d4',
        'color_light': '#22d3ee',
        'color_dark': '#0891b2',
        'emoji': '⛅',
        'title': 'Clima Global',
        'subtitle': 'Consulta el pronóstico del tiempo en tiempo real en cualquier parte del mundo.',
        'page_class': 'clima-page',
        'orb_class': 'clima-orb',
        'hero_class': 'clima-hero',
        'target_wrapper': '<div class="weather-dashboard">',
        'name': 'Clima'
    },
    {
        'file': r'C:\Users\majo1\Desktop\MiniAmigixV\templates\notificaciones\lista_notificaciones.html',
        'color': '#f472b6',
        'color_light': '#f9a8d4',
        'color_dark': '#db2777',
        'emoji': '🔔',
        'title': 'Notificaciones',
        'subtitle': 'Mantente al día con todas las novedades y actualizaciones.',
        'page_class': 'notificaciones-page',
        'orb_class': 'notificaciones-orb',
        'hero_class': 'notificaciones-hero',
        'target_wrapper': '<div class="notifications-container">',
        'name': 'Notificaciones'
    },
    {
        'file': r'C:\Users\majo1\Desktop\MiniAmigixV\templates\perfil\index.html',
        'color': '#eab308',
        'color_light': '#fde047',
        'color_dark': '#ca8a04',
        'emoji': '👤',
        'title': 'Mi Perfil',
        'subtitle': 'Gestiona tu información, personaliza tu experiencia y mira tus estadísticas.',
        'page_class': 'perfil-page',
        'orb_class': 'perfil-orb',
        'hero_class': 'perfil-hero',
        'target_wrapper': '<div class="dashboard">',
        'name': 'Perfil'
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
    
    .weather-dashboard, .notifications-container, .profile-card, .profile-stats, .profile-recent-activity, .weather-current, .weather-details, .weather-forecast, .notification-card {{
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: var(--shadow-accent) !important;
        margin-bottom: 24px;
        transition: transform 0.3s, box-shadow 0.3s;
    }}
    
    .weather-current:hover, .weather-details:hover, .weather-forecast:hover, .notification-card:hover {{
        border-color: var(--accent) !important;
        background: {cfg['color']}0D !important;
        transform: translateY(-4px) !important;
    }}
    
    .btn-primary, .mark-all-read, .edit-profile-btn {{
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
