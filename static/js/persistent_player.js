// Persistent player: keeps audio playing across page navigations.
// Behavior:
// - Reads `miniamigixv_songs` and `miniamigixv_current_song_index` from localStorage.
// - If the current song link is a direct audio file (mp3/ogg/wav), plays it in the hidden <audio> element.
// - If it's a YouTube link, opens a small popup window with the embed URL to continue playback.

(function(){
    const playerEl = document.getElementById('persistent-player');
    const audioEl = document.getElementById('pp-audio');
    const trackEl = document.getElementById('pp-track');
    const playBtn = document.getElementById('pp-play');
    const prevBtn = document.getElementById('pp-prev');
    const nextBtn = document.getElementById('pp-next');
    const closeBtn = document.getElementById('pp-close');

    let songs = [];
    let currentIndex = null;
    let popup = null;

    function isYouTubeLink(url){
        return /(?:youtube.com\/watch\?|youtu.be\/)/i.test(url);
    }

    function extractYouTubeId(url){
        try{
            const u = new URL(url);
            let id = u.searchParams.get('v');
            if(!id){
                id = u.pathname.split('/').pop();
            }
            return id || null;
        }catch(e){
            // fallback for plain ids
            const m = url && url.match(/([A-Za-z0-9_-]{11})$/);
            return m ? m[1] : null;
        }
    }

    // YouTube IFrame API management
    let ytPlayer = null;
    let ytApiReady = false;
    let loadingYouTubeApi = false;

    function loadYouTubeAPI(cb){
        if(ytApiReady){ cb && cb(); return; }
        if(loadingYouTubeApi){
            // poll until ready
            const i = setInterval(()=>{ if(ytApiReady){ clearInterval(i); cb && cb(); } }, 150);
            return;
        }
        loadingYouTubeApi = true;
        const s = document.createElement('script');
        s.src = 'https://www.youtube.com/iframe_api';
        document.head.appendChild(s);
        window.onYouTubeIframeAPIReady = function(){ ytApiReady = true; loadingYouTubeApi = false; cb && cb(); };
    }

    function showBlockedMessage(text, withLink){
        const el = document.getElementById('pp-blocked-msg');
        const openBtn = document.getElementById('pp-open');
        if(el){
            el.style.display = '';
            el.innerHTML = `<div>${text}${withLink?'<a id="pp-blocked-open" href="#">Abrir en YouTube</a>':''}</div>`;
            const blockedOpen = document.getElementById('pp-blocked-open');
            if(blockedOpen){ blockedOpen.addEventListener('click',(ev)=>{ ev.preventDefault(); const s=songs[currentIndex]; if(s) window.open(s.link,'_blank','noopener'); }); }
        }
        if(openBtn) {
            openBtn.style.display = withLink ? '' : 'none';
        }
    }

    function clearBlockedMessage(){ const el = document.getElementById('pp-blocked-msg'); if(el) el.style.display='none'; }

    /* Progress helpers and YT polling */
    function formatTime(sec){ if(!isFinite(sec) || Number.isNaN(sec)) return '0:00'; sec = Math.max(0, Math.floor(sec)); const m = Math.floor(sec/60); const s = sec%60; return `${m}:${s.toString().padStart(2,'0')}`; }
    function progressFillEl(){ return document.getElementById('pp-progress-fill'); }
    function progressBarEl(){ return document.getElementById('pp-progress-bar'); }
    function timeCurrentEl(){ return document.getElementById('pp-time-current'); }
    function timeTotalEl(){ return document.getElementById('pp-time-total'); }

    let ytPollInterval = null;
    function startYTPoll(){ 
        stopYTPoll(); 
        const prog = document.getElementById('pp-progress'); 
        if(prog) prog.style.display='flex'; 
        ytPollInterval = setInterval(()=>{ 
            try{ 
                if(!ytPlayer) return; 
                const cur = ytPlayer.getCurrentTime()||0; 
                const dur = ytPlayer.getDuration()||0; 
                const fill = progressFillEl(); 
                if(fill) fill.style.width = (dur>0? (cur/dur*100) : 0) + '%'; 
                const curEl = timeCurrentEl(); 
                const totEl = timeTotalEl(); 
                if(curEl) curEl.textContent = formatTime(cur); 
                if(totEl) totEl.textContent = formatTime(dur); 
                localStorage.setItem('pp_time', cur);
            }catch(e){} 
        }, 500); 
    }
    function stopYTPoll(){ if(ytPollInterval){ clearInterval(ytPollInterval); ytPollInterval = null; } }

    function updateAudioProgress(){ 
        const cur = audioEl.currentTime || 0; 
        const dur = audioEl.duration || 0; 
        const fill = progressFillEl(); 
        if(fill) fill.style.width = (dur>0? (cur/dur*100) : 0) + '%'; 
        const curEl = timeCurrentEl(); 
        const totEl = timeTotalEl(); 
        if(curEl) curEl.textContent = formatTime(cur); 
        if(totEl) totEl.textContent = formatTime(dur); 
        localStorage.setItem('pp_time', cur);
    }

    function handleSeekEvent(ev){ const bar = progressBarEl(); if(!bar) return; const rect = bar.getBoundingClientRect(); const x = (ev.touches && ev.touches[0]) ? ev.touches[0].clientX : ev.clientX; const frac = Math.min(1, Math.max(0, (x - rect.left) / rect.width)); if(!isYouTubeLink((songs[currentIndex]||{}).link)){ const dur = audioEl.duration || 0; if(dur>0){ audioEl.currentTime = frac * dur; } } else { if(ytPlayer && typeof ytPlayer.seekTo === 'function'){ const dur = (typeof ytPlayer.getDuration === 'function') ? ytPlayer.getDuration() : 0; if(dur>0){ ytPlayer.seekTo(frac * dur, true); } } } const fill = progressFillEl(); if(fill) fill.style.width = (frac*100)+'%'; }

    function loadState(){
        try{
            songs = JSON.parse(localStorage.getItem('miniamigixv_songs')||'[]');
            // support both possible keys used by musica.js: 'miniamigixv_current_song' and 'miniamigixv_current_song_index'
            const idx1 = localStorage.getItem('miniamigixv_current_song_index');
            const idx2 = localStorage.getItem('miniamigixv_current_song');
            currentIndex = null;
            if(idx1!==null) currentIndex = parseInt(idx1);
            if((currentIndex===null || Number.isNaN(currentIndex)) && idx2!==null) currentIndex = parseInt(idx2);
            if(Number.isNaN(currentIndex)) currentIndex = null;
        }catch(e){songs=[]; currentIndex=null}
    }

    function saveState(){
        localStorage.setItem('miniamigixv_songs', JSON.stringify(songs));
        localStorage.setItem('miniamigixv_current_song_index', currentIndex);
    }

    function show(){ playerEl.setAttribute('aria-hidden','false'); playerEl.style.display='block'; }
    function hide(){ playerEl.setAttribute('aria-hidden','true'); playerEl.style.display='none'; }

    function updateUI(){
        if(currentIndex === null || !songs[currentIndex]){
            trackEl.textContent = '—';
            // hide thumb and UI when no song
            const thumb = document.getElementById('pp-thumb'); if(thumb) thumb.src = '/static/images/player-logo.svg';
            hide();
            return;
        }
        const s = songs[currentIndex];
        trackEl.textContent = s.name || s.link || 'Canción';
        // update thumbnail: if YouTube link, use yt thumbnail
        const thumb = document.getElementById('pp-thumb');
        if (thumb) {
            if (isYouTubeLink(s.link)) {
                const id = (function(){
                    try{ const u=new URL(s.link); let vid=u.searchParams.get('v'); if(!vid){ vid = u.pathname.split('/').pop(); } return vid; }catch(e){return null}
                })();
                if (id) thumb.src = `https://img.youtube.com/vi/${id}/mqdefault.jpg`;
                else thumb.src = '/static/images/player-logo.svg';
            } else {
                // fallback logo for non-youtube
                thumb.src = '/static/images/player-logo.svg';
            }
        }
        show();
    }

    function playCurrent(resumeTime = null){
        if(currentIndex===null || !songs[currentIndex]) return;
        const s = songs[currentIndex];
        localStorage.setItem('pp_playing', '1');
        
        if(resumeTime === null) {
            resumeTime = parseFloat(localStorage.getItem('pp_time') || '0');
        }
        if(isYouTubeLink(s.link)){
            // If the video was already detected as blocked for embedding, skip the YT player and show fallback immediately.
            if (s.blockedEmbed) {
                blockedYouTubeLink = s.link;
                showBlockedMessage('El video no permite reproducción dentro de otras páginas.', true);
                playBtn.textContent = '▶';
                return;
            }
            // Try to embed with IFrame API. If the video is blocked for embedding, show a friendly message.
            const openBtn = document.getElementById('pp-open');
            const embedContainer = document.getElementById('pp-embed');
            const ytId = extractYouTubeId(s.link);
            clearBlockedMessage();
            if(openBtn) openBtn.style.display = 'none';
            if(!ytId){
                showBlockedMessage('No se encontró el video de YouTube.');
                playBtn.textContent = '▶';
                return;
            }

            // attempt to load YT API and create a player
            loadYouTubeAPI(()=>{
                try{
                    // destroy previous player if exists
                    if(ytPlayer && typeof ytPlayer.destroy === 'function'){
                        try{ ytPlayer.destroy(); }catch(e){}
                        ytPlayer = null;
                    }
                    // ensure container visible
                    if(embedContainer) embedContainer.style.display = '';

                    const ytOrigin = (() => {
                        try {
                            const url = new URL(window.location.href);
                            return `${url.protocol}//${url.host}`;
                        } catch {
                            return window.location.origin || '';
                        }
                    })();
                    const normalizedYtOrigin = ytOrigin.replace(/\/+$/g, '');

                    const playerVars = {autoplay:1, rel:0, modestbranding:1, playsinline:1};
                    if (normalizedYtOrigin) {
                        playerVars.origin = normalizedYtOrigin;
                    }

                    ytPlayer = new YT.Player('pp-yt-player', {
                        height: '170', width: '100%', videoId: ytId,
                        playerVars,
                        events: {
                            onReady: function(event){
                                if (resumeTime > 0) {
                                    event.target.seekTo(resumeTime, true);
                                }
                                event.target.playVideo();
                                playBtn.textContent = '⏸';
                                // show progress and start polling for time/duration
                                const prog = document.getElementById('pp-progress'); if(prog) prog.style.display='flex';
                                startYTPoll();
                            },
                            onStateChange: function(ev){
                                // when playing
                                if(ev.data === YT.PlayerState.PLAYING){ 
                                    playBtn.textContent = '⏸'; 
                                    localStorage.setItem('pp_playing', '1');
                                }
                                if(ev.data === YT.PlayerState.PAUSED || ev.data === YT.PlayerState.ENDED){ 
                                    playBtn.textContent = '▶'; 
                                    if(ev.data === YT.PlayerState.PAUSED) localStorage.setItem('pp_playing', '0');
                                }
                            },
                            onError: function(err){
                                // error codes 101/150 indicate embedding disabled
                                console.warn('YouTube player error', err);
                                if(embedContainer) embedContainer.style.display = 'none';
                                stopYTPoll();
                                showBlockedMessage('El video no permite reproducción dentro de otras páginas.', true);
                                playBtn.textContent = '▶';
                            }
                        }
                    });
                }catch(e){
                    // if creating the player fails, fallback to friendly message
                    if(embedContainer) embedContainer.style.display = 'none';
                    showBlockedMessage('No es posible reproducir este video dentro de la página.');
                    playBtn.textContent = '▶';
                }
            });
            return;
        }
        audioEl.src = s.link;
        if (resumeTime > 0) {
            audioEl.currentTime = resumeTime;
        }
        audioEl.play().then(()=>{
            playBtn.textContent = '⏸';
            localStorage.setItem('pp_playing', '1');
        }).catch(()=>{
            playBtn.textContent = '▶';
            localStorage.setItem('pp_playing', '0');
        });
    }

    function pauseCurrent(){
        if(audioEl && !audioEl.paused){
            audioEl.pause();
        }
        if(ytPlayer && typeof ytPlayer.pauseVideo === 'function') {
            ytPlayer.pauseVideo();
        }
        playBtn.textContent = '▶';
        localStorage.setItem('pp_playing', '0');
    }

    playBtn.addEventListener('click', ()=>{
        const isPlaying = playBtn.textContent === '⏸';
        if(isPlaying){
            pauseCurrent();
        } else {
            playCurrent(null);
        }
    });

    prevBtn.addEventListener('click', ()=>{
        if(currentIndex===null) return;
        currentIndex = Math.max(0, currentIndex-1);
        saveState();
        updateUI();
        playCurrent();
    });
    nextBtn.addEventListener('click', ()=>{
        if(currentIndex===null) return;
        currentIndex = Math.min(songs.length-1, currentIndex+1);
        saveState();
        updateUI();
        playCurrent();
    });

    const toggleVideoBtn = document.getElementById('pp-toggle-video');
    if (toggleVideoBtn) {
        toggleVideoBtn.addEventListener('click', () => {
            playerEl.classList.toggle('show-video');
        });
    }

    closeBtn.addEventListener('click', ()=>{
        hide();
    });

    // Sync when other scripts update localStorage
    window.addEventListener('storage', (e)=>{
        if(e.key === 'miniamigixv_songs' || e.key === 'miniamigixv_current_song_index'){
            loadState();
            updateUI();
        }
    });

        // Initialize
    document.addEventListener('DOMContentLoaded', ()=>{
        loadState();
        updateUI();

        // Auto-resume playback if it was playing before page navigation
        if (localStorage.getItem('pp_playing') === '1' && currentIndex !== null) {
            // Un pequeño retraso para asegurar que los elementos estén listos
            setTimeout(() => {
                const pp = document.getElementById('persistent-player');
                if (pp) {
                    pp.setAttribute('aria-hidden', 'false');
                    pp.style.display = 'block';
                }
                playCurrent(null);
            }, 500);
        }

        // If user navigates within SPA (if implemented), try to keep popup alive.

        // expose a small API so musica.js can call this player
        window.PersistentPlayer = {
            playIndex(i){
                loadState();
                if(!Array.isArray(songs) || !songs[i]) return;
                currentIndex = i;
                saveState();
                updateUI();
                playCurrent();
            },
            pause(){ pauseCurrent(); },
            openPopupForCurrent(){ if(songs[currentIndex] && isYouTubeLink(songs[currentIndex].link)){ playCurrent(); } }
        };

        // Make the persistent player draggable and persist position
        (function(){
            const el = document.getElementById('persistent-player');
            const header = el && el.querySelector('.pp-header');
            if(!el || !header) return;
            let isDown=false, startX=0, startY=0, origX=0, origY=0;

            // restore position
            try{
                const pos = JSON.parse(localStorage.getItem('persistent_player_pos') || 'null');
                if(pos && typeof pos.x==='number' && typeof pos.y==='number'){
                    el.style.right = 'auto';
                    el.style.left = pos.x + 'px';
                    el.style.top = pos.y + 'px';
                    el.style.bottom = 'auto';
                }
            }catch(e){}

            header.addEventListener('mousedown', (ev)=>{
                isDown = true;
                el.classList.add('dragging');
                startX = ev.clientX; startY = ev.clientY;
                const rect = el.getBoundingClientRect();
                origX = rect.left; origY = rect.top;
                document.body.style.userSelect='none';
            });

            window.addEventListener('mousemove', (ev)=>{
                if(!isDown) return;
                const dx = ev.clientX - startX; const dy = ev.clientY - startY;
                const nx = Math.max(8, origX + dx); const ny = Math.max(8, origY + dy);
                el.style.left = nx + 'px'; el.style.top = ny + 'px'; el.style.right = 'auto'; el.style.bottom='auto';
            });

            window.addEventListener('mouseup', ()=>{
                if(!isDown) return; isDown=false; el.classList.remove('dragging'); document.body.style.userSelect='';
                try{ 
                    const rect = el.getBoundingClientRect();
                    localStorage.setItem('persistent_player_pos', JSON.stringify({x: Math.round(rect.left), y: Math.round(rect.top)}));
                }catch(e){}
            });
        })();

        // Progress event listeners for audio
        audioEl.addEventListener('timeupdate', ()=>{ updateAudioProgress(); });
        audioEl.addEventListener('loadedmetadata', ()=>{ const prog=document.getElementById('pp-progress'); if(prog) prog.style.display='flex'; updateAudioProgress(); });
        // Click/touch to seek
        (function(){ const bar=document.getElementById('pp-progress-bar'); if(bar){ bar.addEventListener('click', handleSeekEvent); bar.addEventListener('touchend', handleSeekEvent); } })();

        // If audio ends, auto-next
        audioEl.addEventListener('ended', ()=>{
            if(currentIndex===null) return;
            if(currentIndex < songs.length-1){ currentIndex++; saveState(); updateUI(); playCurrent(); }
        });
    });
})();
