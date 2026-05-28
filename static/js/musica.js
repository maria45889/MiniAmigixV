document.addEventListener('DOMContentLoaded', () => {
    console.log("🎵 MiniAmigixV Música: Online");
    
    // DOM Elements
    const addSongForm = document.getElementById('add-song-form');
    const songNameInput = document.getElementById('song-name');
    const songLinkInput = document.getElementById('song-link');
    const songList = document.getElementById('song-list');
    const embeddedPlayer = document.getElementById('embedded-player');
    const lyricsContent = document.getElementById('lyrics-content');
    const currentSongInfo = document.getElementById('current-song-info');
    const floatingPlayer = document.getElementById('floating-player');
    const closeFloatBtn = document.getElementById('close-float');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const volumeSlider = document.getElementById('volume-slider');
    const progressFill = document.getElementById('progress-fill');
    const progressHandle = document.getElementById('progress-handle');
    const progressBg = document.querySelector('.progress-bg');
    const currentTimeSpan = document.getElementById('current-time');
    const totalTimeSpan = document.getElementById('total-time');
    const refreshLyricsBtn = document.getElementById('refresh-lyrics');
    
    // Audio element (hidden)
    const audioPlayer = document.getElementById('audio-player');
    
    // State
    let songs = JSON.parse(localStorage.getItem('miniamigixv_songs') || '[]');
    let currentSongIndex = -1;
    let currentLyrics = [];
    let isDragging = false;
    let isProgressDragging = false;
    let floatingPosition = JSON.parse(localStorage.getItem('miniamigixv_floating_player') || '{}');
    let youtubePlayerIframe = null;
    let isYouTubePlaying = false;
    
    // Initialize
    if (floatingPlayer && floatingPlayer.parentElement !== document.body) {
        document.body.appendChild(floatingPlayer);
        floatingPlayer.style.position = 'fixed';
    }

    loadFloatingPlayerPosition();
    renderSongList();

    const savedCurrentSong = parseInt(localStorage.getItem('miniamigixv_current_song'), 10);
    if (!Number.isNaN(savedCurrentSong) && savedCurrentSong >= 0 && savedCurrentSong < songs.length) {
        currentSongIndex = savedCurrentSong;
        selectSong(currentSongIndex, false);
    }

    setupEventListeners();
    updateFloatingPlayerVisibility();
    
    // Load saved floating player state
    if (localStorage.getItem('miniamigixv_floating_player_visible') === 'true') {
        floatingPlayer.classList.add('active');
    }
    
    function loadFloatingPlayerPosition() {
        if (floatingPosition.top && floatingPosition.left) {
            floatingPlayer.style.top = floatingPosition.top + 'px';
            floatingPlayer.style.left = floatingPosition.left + 'px';
            floatingPlayer.style.bottom = 'auto';
            floatingPlayer.style.right = 'auto';
        }
    }
    
    function saveFloatingPlayerPosition() {
        const rect = floatingPlayer.getBoundingClientRect();
        localStorage.setItem('miniamigixv_floating_player', JSON.stringify({
            top: rect.top,
            left: rect.left
        }));
    }
    
    function renderSongList() {
        if (!songList) return;
        songList.innerHTML = '';
        
        if (songs.length === 0) {
            songList.innerHTML = `
                <div class="empty-state">
                    <p>No tienes canciones aún. ¡Agrega tu primera canción arriba!</p>
                </div>
            `;
            return;
        }
        
        songs.forEach((song, index) => {
            const songItem = document.createElement('div');
            songItem.className = `song-item ${index === currentSongIndex ? 'active' : ''}`;
            songItem.dataset.index = index;
            
            songItem.innerHTML = `
                <div class="song-info">
                    <div class="song-title">${escapeHtml(song.name)}</div>
                    <div class="song-link">${song.link}</div>
                </div>
                <div class="song-actions">
                    <button class="action-btn edit" title="Editar">
                        <span class="material-icons-round">edit</span>
                    </button>
                    <button class="action-btn delete" title="Eliminar">
                        <span class="material-icons-round">delete</span>
                    </button>
                </div>
            `;
            
            songList.appendChild(songItem);
        });
        
        // Add event listeners to song items
        document.querySelectorAll('.song-item').forEach(item => {
            item.addEventListener('click', (e) => {
                // Prevent action buttons from triggering song selection
                if (e.target.closest('.action-btn')) return;
                
                const index = parseInt(item.dataset.index);
                selectSong(index);
            });
            
            // Delete button
            const deleteBtn = item.querySelector('.action-btn.delete');
            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const index = parseInt(item.dataset.index);
                deleteSong(index);
            });
            
            // Edit button (placeholder - in a real app would open edit form)
            const editBtn = item.querySelector('.action-btn.edit');
            editBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                alert('No disponible: edición de canciones (pendiente)');
            });
        });
    }
    
    function selectSong(index, autoPlay = true) {
        console.log('[musica] selectSong', { index, autoPlay, songsLen: songs.length });
        if (index < 0 || index >= songs.length) return;
        
        currentSongIndex = index;
        const song = songs[index] || {};
        
        // Update UI
        document.querySelectorAll('.song-item').forEach(item => {
            item.classList.remove('active');
        });
        const selectedItem = document.querySelector(`.song-item[data-index="${index}"]`);
        if (selectedItem) {
            selectedItem.classList.add('active');
        }
        
        // Update current song info in floating player
        currentSongInfo.innerHTML = `
            <p class="song-title">${escapeHtml(song.name)}</p>
            <p class="song-artist">En reproducción</p>
        `;
        
        // Load the song (audio or iframe)
        loadSongMedia(song.link, autoPlay);
        
        // Load lyrics (simulated)
        loadLyrics(song.name);
        
        if (autoPlay) {
            playSong();
        } else {
            updatePlayPauseIcon(false);
        }
        
        // Show floating player
        showFloatingPlayer();
        
        // Save current song index to localStorage
        localStorage.setItem('miniamigixv_current_song', currentSongIndex);
    }
    
    function loadSongMedia(link, autoPlay = false) {
        // Clear previous content
        embeddedPlayer.innerHTML = '';
        youtubePlayerIframe = null;
        isYouTubePlaying = false;
        if (audioPlayer) {
            audioPlayer.pause();
            audioPlayer.src = '';
        }

        if (!link) {
            embeddedPlayer.innerHTML = `
                <div class="player-placeholder">
                    <span class="material-icons-round">warning</span>
                    <p>Enlace no válido o vacío</p>
                </div>
            `;
            return;
        }

        if (isYouTubeLink(link)) {
            const videoId = extractYouTubeVideoId(link);
            console.log('[musica] loadSongMedia YouTube', { link, videoId, embeddedPlayerExists: !!embeddedPlayer });
            if (videoId) {
                crearPlayer(videoId, embeddedPlayer, autoPlay);
                const created = embeddedPlayer && embeddedPlayer.querySelector('#youtube-player');
                youtubePlayerIframe = created;
                isYouTubePlaying = autoPlay;
                console.log('[musica] iframe created?', { hasYoutubePlayer: !!created });
            } else {
                embeddedPlayer.innerHTML = `
                    <div class="player-placeholder">
                        <span class="material-icons-round">warning</span>
                        <p>Enlace de YouTube no válido</p>
                    </div>
                `;
            }
        } else if (isSpotifyLink(link)) {
            const embedUrl = getSpotifyEmbedUrl(link);
            if (embedUrl) {
                const iframe = document.createElement('iframe');
                iframe.width = "100%";
                iframe.height = "100%";
                iframe.src = embedUrl;
                iframe.title = "Spotify embed player";
                iframe.frameBorder = "0";
                iframe.allow = "encrypted-media";
                embeddedPlayer.appendChild(iframe);
            } else {
                embeddedPlayer.innerHTML = `
                    <div class="player-placeholder">
                        <span class="material-icons-round">warning</span>
                        <p>Enlace de Spotify no válido</p>
                    </div>
                `;
            }
        } else if (isDirectAudioFile(link)) {
            audioPlayer.src = link;
            audioPlayer.load();
            embeddedPlayer.innerHTML = `
                <div class="player-placeholder">
                    <span class="material-icons-round">music_note</span>
                    <p>Reproductor de audio activado</p>
                </div>
            `;
        } else {
            const iframe = document.createElement('iframe');
            iframe.width = "100%";
            iframe.height = "100%";
            iframe.src = link;
            iframe.title = "Reproductor embebido";
            iframe.frameBorder = "0";
            iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
            embeddedPlayer.appendChild(iframe);
        }
    }
    
    function isYouTubeLink(link) {
        return link && (link.includes('youtube.com') || link.includes('youtu.be'));
    }
    
    function isSpotifyLink(link) {
        return link && (link.includes('open.spotify.com') || link.includes('spotify:track:'));
    }

    function getSpotifyEmbedUrl(link) {
        try {
            if (link.includes('open.spotify.com')) {
                const url = new URL(link);
                const parts = url.pathname.split('/');
                if (parts[1] === 'track' && parts[2]) {
                    return `https://open.spotify.com/embed/track/${parts[2]}`;
                }
            }
            if (link.startsWith('spotify:track:')) {
                const trackId = link.split(':').pop();
                return `https://open.spotify.com/embed/track/${trackId}`;
            }
        } catch (e) {
            return null;
        }
        return null;
    }

    function isDirectAudioFile(link) {
        return /\.(mp3|wav|ogg|m4a|flac)$/i.test(link);
    }

function extractYouTubeVideoId(url) {
    try {
        if (!url) return null;
        const trimmed = String(url).trim();

        // Already an embed URL
        // https://www.youtube.com/embed/VIDEO_ID
        const embedMatch = trimmed.match(/\/(embed|v)\/([^?&/]+)/i);
        if (embedMatch && embedMatch[2]) return embedMatch[2];

        // https://youtu.be/VIDEO_ID
        const shortMatch = trimmed.match(/youtu\.be\/([^?&/]+)/i);
        if (shortMatch && shortMatch[1]) return shortMatch[1];

        // https://www.youtube.com/shorts/VIDEO_ID
        const shortsMatch = trimmed.match(/\/shorts\/([^?&/]+)/i);
        if (shortsMatch && shortsMatch[1]) return shortsMatch[1];

        // https://www.youtube.com/watch?v=VIDEO_ID&list=...&start_radio=...
        if (trimmed.includes('watch?v=')) {
            return trimmed.split('watch?v=')[1].split('&')[0];
        }

        // Fallback: try URL parsing
        const u = new URL(trimmed);
        if (u.hostname.includes('youtube.com')) {
            const v = u.searchParams.get('v');
            if (v) return v;
        }

        return null;
    } catch (error) {
        console.error('Error extrayendo ID:', error);
        return null;
    }
}

function crearPlayer(videoID, contenedor, autoPlay = false) {
    const params = new URLSearchParams({
        rel: '0',
        playsinline: '1',
        enablejsapi: '1',
        origin: window.location.origin
    });

    if (autoPlay) {
        params.set('autoplay', '1');
    }

    contenedor.innerHTML = `
        <iframe
            id="youtube-player"
            width="100%"
            height="315"
            src="https://www.youtube-nocookie.com/embed/${videoID}?${params.toString()}"
            frameborder="0"
            allow="autoplay; encrypted-media; picture-in-picture"
            allowfullscreen>
        </iframe>
    `;

    const iframe = document.getElementById("youtube-player");
    youtubePlayerIframe = iframe;

    iframe.onerror = function () {
        contenedor.innerHTML = `
            <div class="alert alert-warning">
                ⚠️ No se pudo cargar el video.
                <br>• El propietario bloqueó la incrustación.
                <br>• El video no está disponible en tu región.
                <br>• Alguna extensión del navegador lo bloquea.
                <br><br>
                <a href="https://www.youtube.com/watch?v=${videoID}"
                   target="_blank">
                    Abrir directamente en YouTube
                </a>
            </div>
        `;
    };
}

    function sendYouTubeCommand(command) {
        if (!youtubePlayerIframe || !youtubePlayerIframe.contentWindow) return;
        if (!youtubePlayerIframe.src) return;

        // Use '*' to avoid browser strict origin mismatch errors.
        // YouTube iframe reads the message via its internal handler.
        // In practice this eliminates the recurring console error.
        youtubePlayerIframe.contentWindow.postMessage(
            JSON.stringify({
                event: 'command',
                func: command,
                args: []
            }),
            '*'
        );
    }




    
    function loadLyrics(songName) {
        const normalized = escapeHtml(songName || 'Tu canción');
        const baseLines = [
            `Letra de "${normalized}"`,
            `🎵 Aquí comienza tu historia musical.`,
            `Siente el ritmo y deja que el texto te guíe.`,
            `Mientras suena la melodía, la letra se recorre.`,
            `Cada verso acompaña el pulso de la canción.`,
            `Disfruta del momento y siente el compás.`
        ];
        
        currentLyrics = baseLines.map((line, index) => ({
            text: line,
            timestamp: index * 8
        }));
        
        lyricsContent.innerHTML = currentLyrics.map((line, index) => `
            <p class="lyrics-line" data-index="${index}">${line.text}</p>
        `).join('');
        
        if (audioPlayer && !audioPlayer.paused) {
            syncLyrics();
        }
    }

    function syncLyrics() {
        if (!currentLyrics.length || !audioPlayer || !audioPlayer.duration) return;
        const progress = audioPlayer.currentTime / audioPlayer.duration;
        const index = Math.min(currentLyrics.length - 1, Math.floor(progress * currentLyrics.length));
        document.querySelectorAll('.lyrics-line').forEach((node) => {
            node.classList.toggle('active', Number(node.dataset.index) === index);
        });
    }
    
    function playSong() {
        const currentSong = songs[currentSongIndex];
        if (!currentSong) return;

        if (isYouTubeLink(currentSong.link)) {
            sendYouTubeCommand('playVideo');
            isYouTubePlaying = true;
            updatePlayPauseIcon(true);
            return;
        }
        
        if (audioPlayer.src) {
            audioPlayer.play().catch(e => {
                console.error("Error al reproducir audio:", e);
                alert("No se pudo reproducir la canción. Verifique que el enlace sea un archivo de audio válido.");
            });
            updatePlayPauseIcon(true);
        }
    }
    
    function pauseSong() {
        const currentSong = songs[currentSongIndex];
        if (!currentSong) return;

        if (isYouTubeLink(currentSong.link)) {
            sendYouTubeCommand('pauseVideo');
            isYouTubePlaying = false;
            updatePlayPauseIcon(false);
            return;
        }
        
        audioPlayer.pause();
        updatePlayPauseIcon(false);
    }
    
    function updatePlayPauseIcon(isPlaying) {
        if (isPlaying) {
            playPauseBtn.innerHTML = '<span class="material-icons-round">pause</span>';
        } else {
            playPauseBtn.innerHTML = '<span class="material-icons-round">play_arrow</span>';
        }
        
        // Also update in floating player (same element)
    }
    
    function nextSong() {
        if (songs.length === 0) return;
        
        currentSongIndex = (currentSongIndex + 1) % songs.length;
        selectSong(currentSongIndex);
    }
    
    function prevSong() {
        if (songs.length === 0) return;
        
        currentSongIndex = (currentSongIndex - 1 + songs.length) % songs.length;
        selectSong(currentSongIndex);
    }
    
    function updateVolume() {
        try {
            if (!volumeSlider || typeof currentSongIndex !== 'number' || !Number.isInteger(currentSongIndex)) return;
            if (currentSongIndex < 0 || currentSongIndex >= songs.length) return;
            const currentSong = songs[currentSongIndex];
            if (!currentSong || typeof currentSong !== 'object') return;
            const volume = volumeSlider.value / 100;
            if (currentSong?.link && isYouTubeLink(currentSong.link)) {
                // YouTube iframe volume control requires the YouTube Player API.
                return;
            }
            if (audioPlayer) {
                audioPlayer.volume = volume;
            }
        } catch (e) {
            console.warn('updateVolume error', e);
        }
    }
    
    function updateProgress() {
        const currentSong = songs[currentSongIndex];
        if (!currentSong || isProgressDragging) return;
        if (isYouTubeLink(currentSong.link)) return;
        
        if (!audioPlayer.src) return;
        
        const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
        progressFill.style.width = progress + '%';
        progressHandle.style.left = progress + '%';
        
        // Update time display
        currentTimeSpan.textContent = formatTime(audioPlayer.currentTime);
        if (!isNaN(audioPlayer.duration)) {
            totalTimeSpan.textContent = formatTime(audioPlayer.duration);
        }
    }
    
    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    function setupEventListeners() {
        if (!addSongForm || !songNameInput || !songLinkInput || !songList || !floatingPlayer || !playPauseBtn || !prevBtn || !nextBtn || !volumeSlider || !progressBg || !currentTimeSpan || !totalTimeSpan || !closeFloatBtn || !refreshLyricsBtn || !audioPlayer) {
            return;
        }

        // Add song form
        addSongForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = songNameInput.value.trim();
            const link = songLinkInput.value.trim();
            
            if (name && link) {
                songs.push({ name, link });
                localStorage.setItem('miniamigixv_songs', JSON.stringify(songs));
                renderSongList();
                addSongForm.reset();
                
                // Auto-select the newly added song
                selectSong(songs.length - 1);
            }
        });
        
        // Audio player events
        audioPlayer.addEventListener('timeupdate', updateProgress);
        audioPlayer.addEventListener('timeupdate', syncLyrics);
        audioPlayer.addEventListener('ended', () => {
            // Auto-play next song
            nextSong();
        });
        audioPlayer.addEventListener('loadedmetadata', () => {
            // Duration is now available
            updateProgress();
            syncLyrics();
        });
        
        // Progress bar
        progressBg.addEventListener('mousedown', (e) => {
            isProgressDragging = true;
            const rect = progressBg.getBoundingClientRect();
            const percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
            audioPlayer.currentTime = percent * audioPlayer.duration;
        });
        
        document.addEventListener('mousemove', (e) => {
            if (!isProgressDragging) return;
            const rect = progressBg.getBoundingClientRect();
            let percent = (e.clientX - rect.left) / rect.width;
            percent = Math.max(0, Math.min(1, percent));
            audioPlayer.currentTime = percent * audioPlayer.duration;
        });
        
        document.addEventListener('mouseup', () => {
            isProgressDragging = false;
        });
        
        // Volume slider
        volumeSlider.addEventListener('input', updateVolume);
        
        // Play/pause button
        playPauseBtn.addEventListener('click', () => {
            const currentSong = songs[currentSongIndex];
            if (!currentSong) return;

            if (isYouTubeLink(currentSong.link)) {
                if (isYouTubePlaying) pauseSong();
                else playSong();
            } else {
                if (audioPlayer.paused) {
                    playSong();
                } else {
                    pauseSong();
                }
            }
        });
        
        // Next/previous buttons
        nextBtn.addEventListener('click', nextSong);
        prevBtn.addEventListener('click', prevSong);
        
        // Close floating player
        closeFloatBtn.addEventListener('click', () => {
            floatingPlayer.classList.remove('active');
            localStorage.setItem('miniamigixv_floating_player_visible', 'false');
        });
        
        // Refresh lyrics
        refreshLyricsBtn.addEventListener('click', () => {
            const currentSong = songs[currentSongIndex];
            if (currentSong) {
                loadLyrics(currentSong.name);
            }
        });
        
        // Make floating player draggable
        makeDraggable(floatingPlayer);
        
        // Hide floating player when ESC key pressed
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                floatingPlayer.classList.remove('active');
                localStorage.setItem('miniamigixv_floating_player_visible', 'false');
            }
        });
    }
    
    function makeDraggable(element) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        
        element.querySelector('.player-header').onmousedown = dragMouseDown;
        
        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            // Get the mouse cursor position at startup:
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            // Call a function whenever the cursor moves:
            document.onmousemove = elementDrag;
        }
        
        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            // Calculate the new cursor position:
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            // Set the element's new position:
            const newTop = element.offsetTop - pos2;
            const newLeft = element.offsetLeft - pos1;
            
            // Keep within viewport
            const maxTop = window.innerHeight - element.offsetHeight;
            const maxLeft = window.innerWidth - element.offsetWidth;
            element.style.top = Math.max(0, Math.min(maxTop, newTop)) + 'px';
            element.style.left = Math.max(0, Math.min(maxLeft, newLeft)) + 'px';
            
            // Remove bottom/right settings
            element.style.bottom = 'auto';
            element.style.right = 'auto';
        }
        
        function closeDragElement() {
            // Stop moving when mouse button is released:
            document.onmouseup = null;
            document.onmousemove = null;
            saveFloatingPlayerPosition();
        }
    }
    
    function showFloatingPlayer() {
        floatingPlayer.classList.add('active');
        localStorage.setItem('miniamigixv_floating_player_visible', 'true');
    }
    
    function updateFloatingPlayerVisibility() {
        if (localStorage.getItem('miniamigixv_floating_player_visible') === 'true') {
            floatingPlayer.classList.add('active');
        } else {
            floatingPlayer.classList.remove('active');
        }
    }
    
    function deleteSong(index) {
        if (index < 0 || index >= songs.length) return;
        
        songs.splice(index, 1);
        localStorage.setItem('miniamigixv_songs', JSON.stringify(songs));
        
        // Adjust current song index if needed
        if (currentSongIndex >= songs.length) {
            currentSongIndex = songs.length - 1;
        }
        
        if (songs.length === 0) {
            currentSongIndex = -1;
            // Clear player
            embeddedPlayer.innerHTML = `
                <div class="player-placeholder">
                    <span class="material-icons-round">music_note</span>
                    <p>Selecciona una canción para ver el reproductor aquí</p>
                </div>
            `;
            lyricsContent.innerHTML = `
                <p class="lyrics-placeholder">Selecciona una canción para ver su letra aquí</p>
            `;
            currentSongInfo.innerHTML = `
                <p class="song-title">Ninguna canción seleccionada</p>
                <p class="song-artist">Selecciona una canción para comenzar</p>
            `;
            if (!isYouTubeLink(songs[currentSongIndex]?.link || '')) {
                audioPlayer.pause();
                updatePlayPauseIcon(false);
            }
        }
        
        renderSongList();
        
        // If we deleted the currently playing song, play the next one or stop
        if (index === currentSongIndex && songs.length > 0) {
            // Select the next song (or previous if we deleted the last one)
            const newIndex = Math.min(index, songs.length - 1);
            selectSong(newIndex);
        } else if (index < currentSongIndex) {
            // If we deleted a song before the current one, adjust index
            currentSongIndex--;
        }
    }
    
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
    
    // Initialize volume
    volumeSlider.value = 70;
    updateVolume();
    
    console.log("🎵 Music module initialized");
});
