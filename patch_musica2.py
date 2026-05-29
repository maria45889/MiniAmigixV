import sys

path = r'C:\Users\majo1\Documents\miniamigixv\static\js\musica.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Patches for embeddedPlayer
content = content.replace("function loadSongMedia(link, autoPlay = false, songIndex = null) {", "function loadSongMedia(link, autoPlay = false, songIndex = null) {\n    if (!embeddedPlayer) return;")
content = content.replace("function renderBlockedYouTubeMessage(videoID, message) {", "function renderBlockedYouTubeMessage(videoID, message) {\n    if (!embeddedPlayer) return;")

# Patches for lyricsContent
content = content.replace("function renderLyrics(lyrics, song) {", "function renderLyrics(lyrics, song) {\n    if (!lyricsContent) return;")

# For loadLyrics
old_load = '''        lyricsContent.innerHTML = `
            <div class="lyrics-loading">
                <p>Buscando letra para "${escapeHtml(song.name)}"...</p>
            </div>
        `;'''
new_load = '''        if (lyricsContent) {
            lyricsContent.innerHTML = `
                <div class="lyrics-loading">
                    <p>Buscando letra para "${escapeHtml(song.name)}"...</p>
                </div>
            `;
        }'''
content = content.replace(old_load, new_load)

# For deleteSong (clear player block)
old_delete = '''            // Clear player
            embeddedPlayer.innerHTML = `
                <div class="player-placeholder">
                    <span class="material-icons-round">music_note</span>
                </div>
            `;
            lyricsContent.innerHTML = `
                <p class="lyrics-placeholder">Selecciona una cancin para ver su letra aqu</p>
            `;
            currentSongInfo.innerHTML = `
                <p class="song-title">Ninguna cancin seleccionada</p>
                <p class="song-artist">Selecciona una cancin para comenzar</p>
            `;'''

new_delete = '''            // Clear player
            if (embeddedPlayer) {
                embeddedPlayer.innerHTML = `
                    <div class="player-placeholder">
                        <span class="material-icons-round">music_note</span>
                    </div>
                `;
            }
            if (lyricsContent) {
                lyricsContent.innerHTML = `
                    <p class="lyrics-placeholder">Selecciona una cancin para ver su letra aqu</p>
                `;
            }
            if (currentSongInfo) {
                currentSongInfo.innerHTML = `
                    <p class="song-title">Ninguna cancin seleccionada</p>
                    <p class="song-artist">Selecciona una cancin para comenzar</p>
                `;
            }'''
content = content.replace(old_delete, new_delete)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched successfully!')
