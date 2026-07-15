import re

file_path = r'C:\Users\majo1\Desktop\MiniAmigixV\templates\chat.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the style block
new_style = '''<style>
    /* ── TOKENS ─────────────────────────────────────────────── */
    :root {
        --purple:        #8b5cf6;
        --purple-light:  #a78bfa;
        --purple-dark:   #6d28d9;
        --cyan:          #06b6d4;
        --bg:            #0a0a0f;
        --surface:       rgba(255,255,255,0.04);
        --surface-hov:   rgba(255,255,255,0.07);
        --border:        rgba(139,92,246,0.18);
        --border-hov:    rgba(139,92,246,0.45);
        --text:          #f1f5f9;
        --muted:         #94a3b8;
        --radius:        24px;
        --shadow-purple: 0 0 40px rgba(139,92,246,0.18);
        --glow:          0 0 18px rgba(139,92,246,0.5);
    }

    /* ── RESET & BASE ───────────────────────────────────────── */
    .chat-page * { box-sizing: border-box; }
    .chat-page {
        min-height: 100vh;
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', system-ui, sans-serif;
        padding-bottom: 40px;
        position: relative;
        overflow: hidden;
    }

    /* orb blobs */
    .chat-orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
    }
    .chat-orb-1 {
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(139,92,246,0.2) 0%, transparent 70%);
        top: -100px; left: -100px;
        animation: orbFloat1 10s ease-in-out infinite;
    }
    .chat-orb-2 {
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%);
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

    .chat-hero {
        position: relative;
        z-index: 1;
        text-align: center;
        padding: 40px 20px 20px;
        animation: fadeSlideUp 0.5s ease both;
    }
    .chat-hero h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 30%, var(--purple-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0 5px;
    }
    .chat-hero p { color: var(--muted); margin: 0; }

    /* ── LAYOUT ─────────────────────────────────────────────── */
    .chat-wrapper {
        display: flex !important;
        height: calc(100vh - 220px) !important;
        max-width: 1400px !important;
        margin: 0 auto 20px !important;
        background: var(--surface) !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        overflow: hidden !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: var(--shadow-purple) !important;
        position: relative;
        z-index: 1;
        animation: fadeSlideUp 0.5s 0.2s ease both;
    }
    .chat-list {
        width: 320px !important;
        border-right: 1px solid var(--border) !important;
        display: flex !important;
        flex-direction: column !important;
        background: rgba(0,0,0,0.2) !important;
        flex-shrink: 0 !important;
    }
    .chat-list-header {
        padding: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-weight: 700;
    }
    .new-chat-btn {
        background: linear-gradient(135deg, var(--purple), var(--cyan)) !important;
        border: none !important; color: #fff !important; padding: 8px 16px !important; border-radius: 50px !important;
        cursor: pointer !important; display: flex !important; align-items: center !important; gap: 6px !important;
        font-weight: 600 !important; font-size: 0.85rem !important;
        transition: all 0.3s !important;
        box-shadow: none !important;
    }
    .new-chat-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(139,92,246,0.4) !important;
    }
    .chat-search {
        padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex; align-items: center; gap: 10px;
    }
    .chat-search input {
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 50px; padding: 8px 16px; width: 100%; color: var(--text);
        outline: none; transition: all 0.3s;
    }
    .chat-search input:focus {
        border-color: var(--purple); background: rgba(139,92,246,0.05);
    }
    #chat-list-items { overflow-y: auto; flex: 1; }
    .chat-item {
        padding: 15px 20px; display: flex; align-items: center; gap: 12px;
        cursor: pointer; transition: all 0.2s;
        border-left: 3px solid transparent;
    }
    .chat-item:hover { background: rgba(255,255,255,0.03); }
    .chat-item.active {
        background: rgba(139,92,246,0.1);
        border-left-color: var(--purple);
    }
    .chat-item-name { font-weight: 600; font-size: 0.95rem; }
    .chat-item-preview { font-size: 0.8rem; color: var(--muted); margin-top: 4px; }
    
    .chat-panel { flex: 1; display: flex; flex-direction: column; background: rgba(0,0,0,0.1); }
    .chat-topbar {
        padding: 20px; border-bottom: 1px solid var(--border);
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(255,255,255,0.02);
    }
    .chat-title { font-weight: 700; font-size: 1.1rem; }
    .chat-title-label { color: var(--purple-light); }
    
    .chat-area { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 20px; scroll-behavior: smooth; }
    
    .msg { display: flex; gap: 15px; max-width: 85%; }
    .msg.user { align-self: flex-end; flex-direction: row-reverse; }
    .avatar {
        width: 40px; height: 40px; border-radius: 50%; display: flex;
        align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;
    }
    .avatar.bot { background: rgba(255,255,255,0.1); color: var(--cyan); }
    .avatar.user { background: linear-gradient(135deg, var(--purple), var(--cyan)); color: #fff; }
    
    .bubble {
        padding: 16px 20px; border-radius: 20px; font-size: 0.95rem; line-height: 1.5;
        position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .bubble.bot {
        background: rgba(255,255,255,0.05) !important; border: 1px solid var(--border) !important;
        border-radius: 20px 20px 20px 4px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
    }
    .bubble.user {
        background: linear-gradient(135deg, rgba(139,92,246,0.8), rgba(6,182,212,0.8)) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 20px 20px 4px 20px !important; color: #fff !important;
        box-shadow: 0 8px 32px rgba(139,92,246,0.2) !important;
    }
    
    .input-bar {
        padding: 20px; border-top: 1px solid var(--border);
        display: flex; gap: 10px; align-items: center; background: rgba(0,0,0,0.2);
    }
    .msg-input {
        flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 50px; padding: 14px 20px; color: var(--text); outline: none;
        transition: all 0.3s;
    }
    .msg-input:focus { border-color: var(--purple); background: rgba(139,92,246,0.05); }
    
    .icon-btn {
        background: transparent; border: none; color: var(--muted); font-size: 1.2rem;
        cursor: pointer; padding: 10px; border-radius: 50%; transition: all 0.2s;
    }
    .icon-btn:hover { color: var(--purple-light); background: rgba(255,255,255,0.05); }
    
    .send-btn {
        background: linear-gradient(135deg, var(--purple), var(--cyan)) !important;
        color: #fff !important; border: none !important; width: 48px !important; height: 48px !important; border-radius: 50% !important;
        display: flex !important; align-items: center !important; justify-content: center !important; font-size: 1.2rem !important;
        cursor: pointer !important; transition: all 0.3s !important; box-shadow: var(--glow) !important;
    }
    .send-btn:hover { transform: scale(1.05) !important; filter: brightness(1.1) !important; }
    
    .welcome-screen { text-align: center; margin: auto; padding: 40px; }
    .welcome-icon { font-size: 4rem !important; margin-bottom: 20px !important; filter: drop-shadow(0 0 20px var(--purple)) !important; }
    .suggestion-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 30px; }
    .suggestion-card {
        background: rgba(255,255,255,0.05); border: 1px solid var(--border);
        padding: 15px; border-radius: 15px; color: var(--text); cursor: pointer;
        transition: all 0.3s; display: flex; align-items: center; gap: 10px;
    }
    .suggestion-card:hover { background: rgba(139,92,246,0.1); border-color: var(--purple); transform: translateY(-2px); }
</style>'''

content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)

if '<div class="chat-page">' not in content:
    content = content.replace('<div class="chat-wrapper">', '''<div class="chat-page">
    <div class="chat-orb chat-orb-1"></div>
    <div class="chat-orb chat-orb-2"></div>
    <div class="chat-hero">
        <span style="font-size:3rem;">💬</span>
        <h1>Chat IA</h1>
        <p>Conversa con MiniAmigixV y resuelve tus dudas al instante.</p>
    </div>
    <div class="chat-wrapper">''')
    
    content = content.replace('</div>\n{% endblock %}', '</div>\n</div>\n{% endblock %}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
