import sys

path = r'C:\Users\majo1\Documents\miniamigixv\static\js\musica.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''    function setupEventListeners() {
        if (!addSongForm || !songNameInput || !songLinkInput || !songList || !floatingPlayer || !playPauseBtn || !prevBtn || !nextBtn || !volumeSlider || !progressBg || !currentTimeSpan || !totalTimeSpan || !closeFloatBtn || !refreshLyricsBtn || !audioPlayer) {
            return;
        }'''

new_code = '''    function setupEventListeners() {
        // Continue even if some elements are missing'''

content = content.replace(old_code, new_code)

content = content.replace("addSongForm.addEventListener('submit',", "if(addSongForm) addSongForm.addEventListener('submit',")
content = content.replace("songList.addEventListener('click',", "if(songList) songList.addEventListener('click',")
content = content.replace("audioPlayer.addEventListener(", "if(audioPlayer) audioPlayer.addEventListener(")
content = content.replace("progressBg.addEventListener(", "if(progressBg) progressBg.addEventListener(")
content = content.replace("volumeSlider.addEventListener(", "if(volumeSlider) volumeSlider.addEventListener(")
content = content.replace("playPauseBtn.addEventListener(", "if(playPauseBtn) playPauseBtn.addEventListener(")
content = content.replace("nextBtn.addEventListener(", "if(nextBtn) nextBtn.addEventListener(")
content = content.replace("prevBtn.addEventListener(", "if(prevBtn) prevBtn.addEventListener(")
content = content.replace("closeFloatBtn.addEventListener(", "if(closeFloatBtn) closeFloatBtn.addEventListener(")
content = content.replace("refreshLyricsBtn.addEventListener(", "if(refreshLyricsBtn) refreshLyricsBtn.addEventListener(")
content = content.replace("makeDraggable(floatingPlayer);", "if(floatingPlayer) makeDraggable(floatingPlayer);")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched successfully!')
