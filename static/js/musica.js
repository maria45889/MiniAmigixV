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
    const floatPlayPauseBtn = document.getElementById('float-play-pause-btn');
    const floatPrevBtn = document.getElementById('float-prev-btn');
    const floatNextBtn = document.getElementById('float-next-btn');
    const openFloatBtn = document.getElementById('open-float-btn');
    const floatSongInfo = document.getElementById('float-song-info');
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
    let youtubePlayer = null;
    let youTubeApiReadyPromise = null;
    let youTubeProgressTimer = null;
    let isYouTubePlaying = false;
    let isYouTubeBlocked = false;
    let blockedYouTubeLink = '';
    
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
    if (floatingPlayer && localStorage.getItem('miniamigixv_floating_player_visible') === 'true') {
        floatingPlayer.classList.add('active');
    }
    
    function loadFloatingPlayerPosition() {
        if (!floatingPlayer) return;
        if (floatingPosition.top && floatingPosition.left) {
            floatingPlayer.style.top = floatingPosition.top + 'px';
            floatingPlayer.style.left = floatingPosition.left + 'px';
            floatingPlayer.style.bottom = 'auto';
            floatingPlayer.style.right = 'auto';
        }
    }
    
    function saveFloatingPlayerPosition() {
        if (!floatingPlayer) return;
        const rect = floatingPlayer.getBoundingClientRect();
        localStorage.setItem('miniamigixv_floating_player', JSON.stringify({
            top: rect.top,
            left: rect.left
        }));
    }

    function setYouTubeBlockedState(blocked, link = '') {
        isYouTubeBlocked = blocked;
        blockedYouTubeLink = blocked ? link : '';
        if (playPauseBtn) {
            playPauseBtn.disabled = blocked;
        }
        if (blocked) {
            updatePlayPauseIcon(false);
            stopYouTubeSync();
            if (currentSongInfo) {
                const artistNode = currentSongInfo.querySelector('.song-artist');
                if (artistNode) {
                    artistNode.textContent = 'No se puede reproducir aquí. Abre el enlace de YouTube.';
                }
            }
        }
    }

    function startYouTubeSync() {
        stopYouTubeSync();
        if (!youtubePlayer || !isYouTubePlaying) return;
        youTubeProgressTimer = setInterval(() => {
            updateYouTubeProgress();
        }, 500);
    }

    function stopYouTubeSync() {
        if (youTubeProgressTimer) {
            clearInterval(youTubeProgressTimer);
            youTubeProgressTimer = null;
        }
    }

    function updateYouTubeProgress() {
        if (!youtubePlayer || !isYouTubePlaying) return;
        try {
            const currentTime = youtubePlayer.getCurrentTime();
            const duration = youtubePlayer.getDuration();
            if (!duration || duration <= 0) return;

            const progress = (currentTime / duration) * 100;
            progressFill.style.width = progress + '%';
            progressHandle.style.left = progress + '%';
            currentTimeSpan.textContent = formatTime(currentTime);
            totalTimeSpan.textContent = formatTime(duration);
            syncLyrics(currentTime, duration);
        } catch (error) {
            // ignore if YT player not ready yet
        }
    }

    function renderBlockedYouTubeMessage(videoID, message) {
    if (!embeddedPlayer) return;
        const link = blockedYouTubeLink || `https://www.youtube.com/watch?v=${videoID}`;
        embeddedPlayer.innerHTML = `
            <div class="alert alert-warning youtube-blocked-message">
                <div class="blocked-header">
                    <span class="material-icons-round">block</span>
                    <div>
                        <p class="blocked-title">Este video no se puede reproducir aquí.</p>
                        <p class="blocked-subtitle">YouTube bloquea este video para reproducción embebida.</p>
                    </div>
                </div>
                <p>${escapeHtml(message)}</p>
                <a href="${link}" target="_blank" rel="noopener noreferrer" class="btn-neon youtube-open-button">
                    Abrir directamente en YouTube
                </a>
            </div>
        `;
    }
    
    function startInlineEdit(index, songItem) {
        if (!songItem || index < 0 || index >= songs.length) return;
        if (songItem.classList.contains('editing')) return;

        const song = songs[index];
        const songInfo = songItem.querySelector('.song-info');
        if (!songInfo) return;

        songItem.classList.add('editing');
        songInfo.style.display = 'none';

        const editForm = document.createElement('form');
        editForm.className = 'song-edit-form';
        editForm.innerHTML = `
            <input type="text" name="songName" class="song-edit-name" value="${escapeHtml(song.name)}" placeholder="Nombre de la canción" required />
            <input type="url" name="songLink" class="song-edit-link" value="${escapeHtml(song.link)}" placeholder="Enlace de la canción" required />
            <div class="edit-buttons">
                <button type="submit" class="edit-save">Guardar</button>
                <button type="button" class="edit-cancel">Cancelar</button>
            </div>
        `;

        editForm.addEventListener('click', (e) => e.stopPropagation());
        editForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const updatedName = editForm.elements.songName.value.trim();
            const updatedLink = editForm.elements.songLink.value.trim();

            if (!updatedName || !updatedLink) {
                alert('El nombre y el enlace son obligatorios.');
                return;
            }

            songs[index] = {
                ...song,
                name: updatedName,
                link: updatedLink
            };

            localStorage.setItem('miniamigixv_songs', JSON.stringify(songs));
            renderSongList();

            if (index === currentSongIndex) {
                selectSong(index, false);
            }
        });

        editForm.querySelector('.edit-cancel').addEventListener('click', (e) => {
            e.preventDefault();
            songItem.classList.remove('editing');
            songInfo.style.display = '';
            editForm.remove();
        });

        songItem.insertBefore(editForm, songItem.querySelector('.song-actions'));
    };

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
            songItem.className = `song-item ${index === currentSongIndex ? 'active' : ''} ${song.blockedEmbed ? 'blocked' : ''}`;
            songItem.dataset.index = index;
            
                const blockedBadge = song.blockedEmbed ? '<span class="song-badge blocked">Bloqueado</span>' : '';
            const lyricsBadge = song.lyrics ? '<span class="song-badge lyrics">Letra</span>' : '';
            const openYoutubeButton = song.blockedEmbed ? `
                <button type="button" class="action-btn open-youtube" title="Abrir en YouTube">
                    <span class="material-icons-round">open_in_new</span>
                </button>
            ` : '';

            songItem.innerHTML = `
                <div class="song-info">
                    <div class="song-title">
                        ${escapeHtml(song.name)}
                        ${blockedBadge}
                        ${lyricsBadge}
                    </div>
                    <div class="song-link">${song.link}</div>
                </div>
                <div class="song-actions">
                    ${openYoutubeButton}
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
        
        // Update current song info (safe guard)
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
        }
        
        // Load the song (audio or iframe)
        loadSongMedia(song.link, autoPlay, index);
        
        // Load lyrics for the selected song
        loadLyrics(song);
        
        if (autoPlay) {
            // Save songs and current index for the persistent player
            try {
                localStorage.setItem('miniamigixv_songs', JSON.stringify(songs));
                localStorage.setItem('miniamigixv_current_song', currentSongIndex);
                localStorage.setItem('miniamigixv_current_song_index', currentSongIndex);
            } catch (e) { console.warn('localStorage write failed', e); }

            // If the persistent player API exists, use it so playback survives navigation
            if (window.PersistentPlayer && typeof window.PersistentPlayer.playIndex === 'function') {
                window.PersistentPlayer.playIndex(currentSongIndex);
            } else {
                // Fallback to local player
                playSong();
            }
        } else {
            // No siempre existen controles locales en el template (play/pause, etc.).
            // Evitamos cualquier update de UI cuando falten.
            try {
                updatePlayPauseIcon(false);
            } catch (e) {
                // ignore
            }
        }

        
        // Show floating player
        showFloatingPlayer();
        
        // Save current song index to localStorage
        localStorage.setItem('miniamigixv_current_song', currentSongIndex);
    }
    
    function loadSongMedia(link, autoPlay = false, songIndex = null) {
    if (!embeddedPlayer) return;
        // Clear previous content
        embeddedPlayer.innerHTML = '';
        youtubePlayerIframe = null;
        youtubePlayer = null;
        isYouTubePlaying = false;
        stopYouTubeSync();
        setYouTubeBlockedState(false);
        if (audioPlayer) {
            audioPlayer.pause();
            audioPlayer.src = '';
        }

        const currentSong = songIndex !== null ? songs[songIndex] : null;
        if (currentSong?.blockedEmbed && isYouTubeLink(link)) {
            const videoId = extractYouTubeVideoId(link);
            blockedYouTubeLink = link;
            renderBlockedYouTubeMessage(videoId, 'Este video está marcado como bloqueado para reproducción embebida.');
            setYouTubeBlockedState(true, blockedYouTubeLink);
            return;
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
                embeddedPlayer.dataset.sourceUrl = link;
                crearPlayer(videoId, embeddedPlayer, autoPlay);
                const created = embeddedPlayer && embeddedPlayer.querySelector('#youtube-player');
                youtubePlayerIframe = created;
                isYouTubePlaying = autoPlay;
                setYouTubeBlockedState(false);
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

function loadYouTubeIframeApi() {
    if (window.YT && window.YT.Player) {
        return Promise.resolve(window.YT);
    }
    if (youTubeApiReadyPromise) {
        return youTubeApiReadyPromise;
    }

    youTubeApiReadyPromise = new Promise((resolve, reject) => {
        const tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        tag.async = true;
        tag.onerror = () => reject(new Error('No se pudo cargar la API de YouTube'));
        document.head.appendChild(tag);

        window.onYouTubeIframeAPIReady = () => {
            resolve(window.YT);
        };
    });

    return youTubeApiReadyPromise;
}

function getYouTubeEmbedParams(link, autoPlay = false) {
    const params = {
        rel: 0,
        playsinline: 1,
        enablejsapi: 1,
        origin: window.location.origin,
        modestbranding: 1
    };

    if (autoPlay) {
        params.autoplay = 1;
    }

    return params;
}

async function crearPlayer(videoID, contenedor, autoPlay = false) {
    contenedor.innerHTML = '<div id="youtube-player"></div>';
    youtubePlayerIframe = null;
    youtubePlayer = null;

    const embedParams = getYouTubeEmbedParams(contenedor.dataset.sourceUrl || '', autoPlay);
    console.log('[musica] crearPlayer init', { videoID, sourceUrl: contenedor.dataset.sourceUrl, autoPlay, embedParams });

    try {
        const YT = await loadYouTubeIframeApi();
        console.log('[musica] YouTube API ready', { hasYT: !!YT, hasPlayer: !!YT?.Player });

        youtubePlayer = new YT.Player('youtube-player', {
            height: '315',
            width: '100%',
            videoId: videoID,
            playerVars: embedParams,
            events: {
                onReady: (event) => {
                    youtubePlayerIframe = event.target.getIframe();
                    console.log('[musica] onReady', {
                        videoID,
                        iframeSrc: youtubePlayerIframe?.src,
                        iframeExists: !!youtubePlayerIframe,
                        autoPlay
                    });
                    if (autoPlay) {
                        event.target.playVideo();
                        console.log('[musica] onReady autoplay triggered');
                    }
                },
                onStateChange: (event) => {
                    console.log('[musica] onStateChange', { videoID, state: event.data });
                    if (event.data === 1) {
                        const song = songs[currentSongIndex];
                        if (song) {
                            loadLyrics(song);
                        }
                    }
                },
                onError: (event) => {
                    const code = event?.data;
                    console.error('[musica] onError', { videoID, sourceUrl: contenedor.dataset.sourceUrl, errorCode: code, event });
                    let message = 'No se pudo cargar el video.';
                    if (code === 100) {
                        message = 'El video no está disponible.';
                    } else if (code === 101 || code === 150 || code === 153) {
                        message = 'La reproducción está bloqueada para este video en sitios externos.';
                        if (songs[currentSongIndex]) {
                            songs[currentSongIndex].blockedEmbed = true;
                            localStorage.setItem('miniamigixv_songs', JSON.stringify(songs));
                            renderSongList();
                        }
                    }
                    blockedYouTubeLink = contenedor.dataset.sourceUrl || `https://www.youtube.com/watch?v=${videoID}`;
                    renderBlockedYouTubeMessage(videoID, message);
                    setYouTubeBlockedState(true, blockedYouTubeLink);
                    youtubePlayer = null;
                    youtubePlayerIframe = null;
                    isYouTubePlaying = false;
                    updatePlayPauseIcon(false);
                }
            }
        });
    } catch (error) {
        console.error('[musica] YouTube API load error:', { videoID, sourceUrl: contenedor.dataset.sourceUrl, error });
        contenedor.innerHTML = `
            <div class="alert alert-warning">
                ⚠️ No se pudo cargar la API de YouTube.
                <br>Abre el video directamente en YouTube si deseas reproducirlo.
                <br><br>
                <a href="https://www.youtube.com/watch?v=${videoID}"
                   target="_blank" rel="noopener noreferrer">
                    Abrir directamente en YouTube
                </a>
            </div>
        `;
    }
}

function sendYouTubeCommand(command) {
    if (youtubePlayer && typeof youtubePlayer[command] === 'function') {
        youtubePlayer[command]();
        return;
    }
    if (!youtubePlayerIframe || !youtubePlayerIframe.contentWindow) return;
    if (!youtubePlayerIframe.src) return;

    youtubePlayerIframe.contentWindow.postMessage(
        JSON.stringify({
            event: 'command',
            func: command,
            args: []
        }),
        '*'
    );
}




    
    function generateLyricsForSong(song) {
        const title = song?.name ? escapeHtml(song.name) : 'Tu canción';
        const description = song?.blockedEmbed
            ? 'Letra sugerida disponible porque este video está bloqueado para reproducción embebida.'
            : 'Letra asociada automáticamente al video seleccionado.';

        const baseLines = [
            `Letra de "${title}"`,
            `🎵 ${description}`,
            `Esta letra se muestra automáticamente sin importar el idioma del video.`,
            `Siente el ritmo y deja que el texto te guíe.`,
            `Mientras suena la melodía, la letra se recorre.`,
            `Cada verso acompaña el pulso de la canción.`,
            `Disfruta del momento y siente el compás.`
        ];

        return baseLines.map((line, index) => ({
            text: line,
            timestamp: index * 8
        }));
    }

    function renderLyrics(lyrics, song) {
    if (!lyricsContent) return;
        const displayLines = lyrics.split(/\r?\n/).filter(line => line.trim());
        currentLyrics = displayLines.map((line, index) => ({
            text: line,
            timestamp: index * 8
        }));

        lyricsContent.innerHTML = `
            <div class="lyrics-meta">
                <p class="lyrics-heading">Letra de "${escapeHtml(song?.name || 'Tu canción')}"</p>
                <p class="lyrics-note">Letra cargada automáticamente para el video seleccionado.</p>
            </div>
            ${displayLines.map((line, index) => `
                <p class="lyrics-line" data-index="${index}">${escapeHtml(line)}</p>
            `).join('')}
        `;

        if (audioPlayer && !audioPlayer.paused) {
            syncLyrics(audioPlayer.currentTime, audioPlayer.duration);
        } else if (youtubePlayer && isYouTubePlaying) {
            updateYouTubeProgress();
        }
    }

    async function fetchLyricsFromApi(song) {
        if (!song?.name) return null;

        const raw = song.name.trim();
        // Try splitting by ' - ' first, then by '|'
        let parts = raw.replace(/—|–/g, ' - ').split(' - ').map(p => p.trim()).filter(Boolean);
        if (parts.length < 2) {
            // Try splitting by '|'
            parts = raw.split('|').map(p => p.trim()).filter(Boolean);
        }
        if (parts.length < 2) return null;

        // Clean up common suffixes from title like "(Cover Español)", "(Lyrics)", "(Extended VERSION)"
        const artist = encodeURIComponent(parts[0]);
        const titleRaw = parts.slice(1).join(' ').replace(/\(.*?\)/g, '').trim();
        const title = encodeURIComponent(titleRaw);
        const url = `https://api.lyrics.ovh/v1/${artist}/${title}`;

        try {
            const response = await fetch(url);
            if (!response.ok) return null;
            const data = await response.json();
            return data?.lyrics ? data.lyrics.trim() : null;
        } catch (error) {
            console.warn('No se pudo obtener la letra automáticamente:', error);
            return null;
        }
    }

    async function loadLyrics(song, songIndex = null) {
        if (!song) return;

        if (song.lyrics) {
            renderLyrics(song.lyrics, song);
            return;
        }

        if (lyricsContent) {
            lyricsContent.innerHTML = `
                <div class="lyrics-loading">
                    <p>Buscando letra para "${escapeHtml(song.name)}"...</p>
                </div>
            `;
        }

        const lyrics = await fetchLyricsFromApi(song);
        if (lyrics) {
            song.lyrics = lyrics;
            if (songIndex !== null && Number.isInteger(songIndex)) {
                songs[songIndex] = song;
                localStorage.setItem('miniamigixv_songs', JSON.stringify(songs));
                renderSongList();
            }
            renderLyrics(lyrics, song);
            return;
        }

        renderLyrics(generateLyricsForSong(song).map(line => line.text).join('\n'), song);
    }

    function syncLyrics(currentTime, duration) {
        if (!currentLyrics.length) return;
        let progress = 0;
        if (typeof currentTime === 'number' && typeof duration === 'number' && duration > 0) {
            progress = currentTime / duration;
        } else if (audioPlayer && audioPlayer.duration) {
            progress = audioPlayer.currentTime / audioPlayer.duration;
        } else {
            return;
        }
        const index = Math.min(currentLyrics.length - 1, Math.floor(progress * currentLyrics.length));
        document.querySelectorAll('.lyrics-line').forEach((node) => {
            node.classList.toggle('active', Number(node.dataset.index) === index);
        });
    }
    
    function playSong() {
        const currentSong = songs[currentSongIndex];
        if (!currentSong) return;

        if (isYouTubeLink(currentSong.link)) {
            if (isYouTubeBlocked) {
                alert('Este video no se puede reproducir embebido. Usa el enlace directo que se muestra en el reproductor.');
                return;
            }
            if (youtubePlayer && typeof youtubePlayer.playVideo === 'function') {
                youtubePlayer.playVideo();
            } else {
                sendYouTubeCommand('playVideo');
            }
            isYouTubePlaying = true;
            updatePlayPauseIcon(true);
            startYouTubeSync();
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
            if (isYouTubeBlocked) {
                return;
            }
            if (youtubePlayer && typeof youtubePlayer.pauseVideo === 'function') {
                youtubePlayer.pauseVideo();
            } else {
                sendYouTubeCommand('pauseVideo');
            }
            isYouTubePlaying = false;
            stopYouTubeSync();
            updatePlayPauseIcon(false);
            return;
        }
        
        audioPlayer.pause();
        updatePlayPauseIcon(false);
    }
    
        function updatePlayPauseIcon(isPlaying) {
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
            if (!volumeSlider) return;
            const volume = parseInt(volumeSlider.value, 10);
            const volumeFraction = volume / 100;

            // Update percentage display
            const pctEl = document.getElementById('volume-pct');
            if (pctEl) pctEl.textContent = volume + '%';

            // Update volume icon
            const iconEl = document.getElementById('volume-icon');
            if (iconEl) {
                if (volume === 0) iconEl.textContent = 'volume_off';
                else if (volume < 40) iconEl.textContent = 'volume_down';
                else iconEl.textContent = 'volume_up';
            }

            // Audio player volume
            if (audioPlayer) audioPlayer.volume = volumeFraction;

            // YouTube player volume (works even when embedded)
            if (youtubePlayer && typeof youtubePlayer.setVolume === 'function') {
                youtubePlayer.setVolume(volume);
            }
        } catch (e) {
            console.warn('updateVolume error', e);
        }
    }
    
    function updateProgress() {
        const currentSong = songs[currentSongIndex];
        if (!currentSong || isProgressDragging) return;
        if (isYouTubeLink(currentSong.link)) {
            updateYouTubeProgress();
            return;
        }
        
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
        // Continue even if some elements are missing

        // Add song form
        if(addSongForm) addSongForm.addEventListener('submit', (e) => {
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

        // Song list actions (delegated)
        if(songList) songList.addEventListener('click', (e) => {
            const songItem = e.target.closest('.song-item');
            if (!songItem) return;

            const index = Number(songItem.dataset.index);
            if (Number.isNaN(index)) return;

            if (e.target.closest('.action-btn.delete')) {
                deleteSong(index);
                return;
            }

            if (e.target.closest('.action-btn.open-youtube')) {
                const song = songs[index];
                if (song && song.link) {
                    window.open(song.link, '_blank', 'noopener');
                }
                return;
            }

            if (e.target.closest('.action-btn.edit')) {
                startInlineEdit(index, songItem);
                return;
            }

            if (e.target.closest('.action-btn')) {
                return;
            }

            selectSong(index);
        });
        
        // Audio player events
        if(audioPlayer) audioPlayer.addEventListener('timeupdate', updateProgress);
        if(audioPlayer) audioPlayer.addEventListener('timeupdate', syncLyrics);
        if(audioPlayer) audioPlayer.addEventListener('ended', () => {
            // Auto-play next song
            nextSong();
        });
        if(audioPlayer) audioPlayer.addEventListener('loadedmetadata', () => {
            // Duration is now available
            updateProgress();
            syncLyrics();
        });
        
        // Progress bar
        if(progressBg) progressBg.addEventListener('mousedown', (e) => {
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
        if(volumeSlider) volumeSlider.addEventListener('input', updateVolume);
        
        // Play/pause button
        
        if (floatPlayPauseBtn) {
            floatPlayPauseBtn.addEventListener('click', () => {
                if (playPauseBtn) playPauseBtn.click();
            });
        }
        if (floatPrevBtn && prevBtn) floatPrevBtn.addEventListener('click', () => prevBtn.click());
        if (floatNextBtn && nextBtn) floatNextBtn.addEventListener('click', () => nextBtn.click());
        if (openFloatBtn) openFloatBtn.addEventListener('click', showFloatingPlayer);

        if(playPauseBtn) playPauseBtn.addEventListener('click', () => {
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
        if(nextBtn) nextBtn.addEventListener('click', nextSong);
        if(prevBtn) prevBtn.addEventListener('click', prevSong);
        
        // Close floating player
        if(closeFloatBtn) closeFloatBtn.addEventListener('click', () => {
            floatingPlayer.classList.remove('active');
            localStorage.setItem('miniamigixv_floating_player_visible', 'false');
        });
        
        // Refresh lyrics
        if(refreshLyricsBtn) refreshLyricsBtn.addEventListener('click', () => {
            const currentSong = songs[currentSongIndex];
            if (currentSong) {
                loadLyrics(currentSong, currentSongIndex);
            }
        });
        
        // Make floating player draggable
        if(floatingPlayer) makeDraggable(floatingPlayer);
        
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
        if (!floatingPlayer) return;
        floatingPlayer.classList.add('active');
        localStorage.setItem('miniamigixv_floating_player_visible', 'true');
    }
    
    function updateFloatingPlayerVisibility() {
        if (!floatingPlayer) return;
        if (localStorage.getItem('miniamigixv_floating_player_visible') === 'true') {
            floatingPlayer.classList.add('active');
        } else {
            floatingPlayer.classList.remove('active');
        }
    }
    
    function editSong(index) {
        if (index < 0 || index >= songs.length) return;
        const song = songs[index];
        const updatedName = prompt('Editar nombre de la canción:', song.name);
        if (updatedName === null) return;
        const updatedLink = prompt('Editar enlace de la canción:', song.link);
        if (updatedLink === null) return;

        song.name = updatedName.trim() || song.name;
        song.link = updatedLink.trim() || song.link;
        songs[index] = song;
        localStorage.setItem('miniamigixv_songs', JSON.stringify(songs));
        renderSongList();

        if (index === currentSongIndex) {
            selectSong(index, false);
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
    if (volumeSlider) {
        volumeSlider.value = 70;
        updateVolume();
    }
    
    console.log("🎵 Music module initialized");
});
