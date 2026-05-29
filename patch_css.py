import sys

css_code = """
/* Premium Player Container */
.premium-player-container {
    background: rgba(20, 10, 30, 0.65);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(0, 240, 255, 0.15);
    border-radius: 24px;
    padding: 24px 30px;
    box-shadow: 0 10px 40px rgba(0, 240, 255, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    gap: 20px;
    transition: all 0.3s ease;
}

.premium-player-container:hover {
    box-shadow: 0 15px 50px rgba(0, 240, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    border-color: rgba(0, 240, 255, 0.3);
}

.player-controls {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

/* Playback Buttons */
.playback-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 25px;
}

.control-btn {
    background: transparent;
    border: none;
    color: var(--text-main);
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 1.4rem;
}

.control-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--accent-cyan);
    transform: scale(1.1);
}

.control-btn.play-btn {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    color: #12131d;
    font-size: 2rem;
    box-shadow: 0 8px 25px rgba(0, 240, 255, 0.4);
    position: relative;
    z-index: 1;
}

.control-btn.play-btn::before {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-pink));
    border-radius: 50%;
    z-index: -1;
    filter: blur(8px);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.control-btn.play-btn:hover {
    transform: scale(1.08);
    box-shadow: 0 12px 35px rgba(0, 240, 255, 0.6);
}

.control-btn.play-btn:hover::before {
    opacity: 1;
}

@keyframes pulse-playing {
    0% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0.5); }
    70% { box-shadow: 0 0 0 15px rgba(0, 240, 255, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0); }
}

.control-btn.play-btn.playing {
    animation: pulse-playing 2s infinite;
}

/* Progress Bar Container */
.progress-container {
    display: flex;
    align-items: center;
    gap: 15px;
    width: 100%;
}

.time-display {
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 500;
    min-width: 45px;
    text-align: center;
}

.progress-bar-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    height: 24px;
    cursor: pointer;
}

.progress-bg {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    position: relative;
    overflow: visible;
    transition: height 0.2s ease;
}

.progress-bar-wrapper:hover .progress-bg {
    height: 8px;
}

.progress-fill {
    position: absolute;
    top: 0; left: 0;
    height: 100%;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-pink));
    border-radius: 4px;
    width: 0%;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
}

.progress-handle {
    position: absolute;
    top: 50%;
    right: -8px;
    transform: translateY(-50%) scale(0);
    width: 16px;
    height: 16px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
}

.progress-bar-wrapper:hover .progress-handle {
    transform: translateY(-50%) scale(1);
}

/* Volume and Tools */
.volume-and-tools {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 5px;
}

.volume-control {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-muted);
}

#volume-slider {
    width: 100px;
    height: 4px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 2px;
    outline: none;
    -webkit-appearance: none;
    transition: background 0.2s;
}

#volume-slider:hover {
    background: rgba(255, 255, 255, 0.25);
}

#volume-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 12px;
    height: 12px;
    background: var(--text-main);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
    transition: transform 0.2s;
}

#volume-slider::-webkit-slider-thumb:hover {
    transform: scale(1.3);
    background: var(--accent-cyan);
    box-shadow: 0 0 12px var(--accent-cyan);
}

.open-float-btn {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-main);
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s;
}

.open-float-btn:hover {
    background: rgba(0, 240, 255, 0.15);
    color: var(--accent-cyan);
    border-color: rgba(0, 240, 255, 0.3);
    transform: translateY(-2px);
}

/* Floating Player Premium Styles */
.floating-player.premium-float {
    background: rgba(12, 6, 20, 0.85);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border: 1px solid rgba(255, 79, 216, 0.2);
    border-radius: 24px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 20px rgba(255, 79, 216, 0.1);
    width: 340px;
    transition: opacity 0.3s, transform 0.3s;
    transform: translateY(10px);
    opacity: 0;
    pointer-events: none;
}

.floating-player.premium-float.active {
    transform: translateY(0);
    opacity: 1;
    pointer-events: all;
}

.floating-player .player-header {
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    background: rgba(255, 255, 255, 0.02);
}

.floating-player .player-header h3 {
    color: var(--accent-pink);
    font-size: 1.1rem;
    font-weight: 600;
}

.float-controls {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 15px;
}

.float-controls .control-btn.play-btn {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
}
"""

path = r'C:\Users\majo1\Documents\miniamigixv\static\css\musica.css'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert right before /* Responsive Design */
if '/* Responsive Design */' in content:
    content = content.replace('/* Responsive Design */', css_code + '\n/* Responsive Design */')
else:
    content += css_code

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('CSS Patched successfully!')
