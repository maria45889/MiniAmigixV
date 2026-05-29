import sys
import re

path = r'C:\Users\majo1\Documents\miniamigixv\static\js\musica.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'const floatPlayPauseBtn' not in content:
    content = content.replace("const playPauseBtn = document.getElementById('play-pause-btn');",
    "const playPauseBtn = document.getElementById('play-pause-btn');\n    const floatPlayPauseBtn = document.getElementById('float-play-pause-btn');\n    const floatPrevBtn = document.getElementById('float-prev-btn');\n    const floatNextBtn = document.getElementById('float-next-btn');\n    const openFloatBtn = document.getElementById('open-float-btn');\n    const floatSongInfo = document.getElementById('float-song-info');")

new_icon_func = '''    function updatePlayPauseIcon(isPlaying) {
        const iconHtml = isPlaying ? '<span class="material-icons-round">pause</span>' : '<span class="material-icons-round">play_arrow</span>';
        
        if (playPauseBtn) {
            playPauseBtn.innerHTML = iconHtml;
            if (isPlaying) {
                playPauseBtn.classList.add('playing');
            } else {
                playPauseBtn.classList.remove('playing');
            }
        }
        
        if (floatPlayPauseBtn) {
            floatPlayPauseBtn.innerHTML = iconHtml;
            if (isPlaying) {
                floatPlayPauseBtn.classList.add('playing');
            } else {
                floatPlayPauseBtn.classList.remove('playing');
            }
        }
    }'''

content = re.sub(r'function updatePlayPauseIcon\(isPlaying\) \{.*?\n    \}', new_icon_func, content, flags=re.DOTALL)

old_update_info = '''        // Update current song info (safe guard)
        if (currentSongInfo) {
            currentSongInfo.innerHTML = `
                <p class="song-title">${escapeHtml(song.name)}</p>
                <p class="song-artist">En reproducción</p>
            `;
        }'''
new_update_info = '''        // Update current song info (safe guard)
        if (currentSongInfo) {
            currentSongInfo.innerHTML = `
                <p class="song-title">${escapeHtml(song.name)}</p>
                <p class="song-artist">En reproducción</p>
            `;
        }
        if (floatSongInfo) {
            floatSongInfo.innerHTML = `
                <p class="song-title">${escapeHtml(song.name)}</p>
                <p class="song-artist">En reproducción</p>
            `;
        }'''
content = content.replace(old_update_info, new_update_info)

listeners = '''
        if (floatPlayPauseBtn) {
            floatPlayPauseBtn.addEventListener('click', () => {
                if (playPauseBtn) playPauseBtn.click();
            });
        }
        if (floatPrevBtn && prevBtn) floatPrevBtn.addEventListener('click', () => prevBtn.click());
        if (floatNextBtn && nextBtn) floatNextBtn.addEventListener('click', () => nextBtn.click());
        if (openFloatBtn) openFloatBtn.addEventListener('click', showFloatingPlayer);
'''

if 'floatPlayPauseBtn.addEventListener' not in content:
    content = content.replace("if(playPauseBtn) playPauseBtn.addEventListener('click', () => {", listeners + "\n        if(playPauseBtn) playPauseBtn.addEventListener('click', () => {")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('JS patched successfully!')
