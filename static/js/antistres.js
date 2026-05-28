document.addEventListener('DOMContentLoaded', () => {
    console.log("🧘‍♂️ MiniAmigixV Antiestrés: Online");
    
    // DOM Elements
    const gameCards = document.querySelectorAll('.game-card');
    const gameLaunches = document.querySelectorAll('.game-launch');
    
    // Game launch functionality
    gameLaunches.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const gameCard = button.closest('.game-card');
            const gameType = gameCard.dataset.game;
            
            // Visual feedback
            button.textContent = 'Cargando...';
            button.disabled = true;
            
            // Simulate loading
            setTimeout(() => {
                launchGame(gameType, gameCard);
                button.textContent = button.dataset.originalText || 'Jugar Ahora';
                button.disabled = false;
            }, 500);
        });
    });

    // Shared small button helper for game controls
    function btn(label, cls) {
        const b = document.createElement('button');
        b.className = cls || 'btn-neon-sm';
        b.textContent = label;
        return b;
    }
    
    function launchGame(gameType, gameCard) {
        // Add active class to selected game
        document.querySelectorAll('.game-card').forEach(card => {
            card.classList.remove('active');
        });
        gameCard.classList.add('active');
        
        // In a real implementation, this would load the specific game
        // For now, we'll show a modal or redirect to the game page
        showGameLaunchModal(gameType, gameCard);
    }
    
    function showGameLaunchModal(gameType, gameCard) {
        // Create modal container
        const modal = document.createElement('div');
        modal.className = 'game-launch-modal';

        modal.innerHTML = `
            <div class="game-launch-modal-content">
                <div class="game-launch-modal-header">
                    <h2>${getGameTitle(gameType)}</h2>
                    <span class="material-icons-round" id="close-modal">close</span>
                </div>
                <div class="game-launch-modal-body">
                    <div class="game-info">
                        <div class="game-icon">${getGameIcon(gameType)}</div>
                        <div class="game-details">
                            <h3>${getGameTitle(gameType)}</h3>
                            <p class="game-description">${getGameDescription(gameType)}</p>
                            <div class="game-features">
                                <h4>Características:</h4>
                                <ul>
                                    <li>${getGameFeature1(gameType)}</li>
                                    <li>${getGameFeature2(gameType)}</li>
                                    <li>${getGameFeature3(gameType)}</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="game-preview">
                        <div class="game-canvas" id="game-canvas"></div>
                        <div class="game-controls" id="game-controls"></div>
                    </div>
                </div>
                <div class="game-launch-modal-footer">
                    <button class="btn-neon-sm-outline" id="close-btn">Cerrar</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Close handlers
        modal.querySelector('#close-modal').addEventListener('click', () => closeModal());
        modal.querySelector('#close-btn').addEventListener('click', () => closeModal());

        function closeModal() {
            // stop any audio/animations if present
            if (modal._cleanup) modal._cleanup();
            document.body.removeChild(modal);
            gameCard.classList.remove('active');
        }

        // Render the game UI inside the preview area
        const canvasArea = modal.querySelector('#game-canvas');
        const controlsArea = modal.querySelector('#game-controls');
        renderGameUI(gameType, canvasArea, controlsArea, modal);
    }

    // Render the minimal playable UI for each gameType
    function renderGameUI(gameType, container, controls, modal) {
        // Clear
        container.innerHTML = '';
        controls.innerHTML = '';

        const cleaners = [];
        function registerCleanup(fn) { cleaners.push(fn); }
        modal._cleanup = () => cleaners.forEach(fn => { try { fn(); } catch(e){} });

        // Basic helper to create buttons
        function btn(label, cls) {
            const b = document.createElement('button');
            b.className = cls || 'btn-neon-sm';
            b.textContent = label;
            return b;
        }

        if (gameType === 'tic-tac-toe') initTicTacToe(container, controls, registerCleanup);
        else if (gameType === 'breathing') initBreathing(container, controls, registerCleanup);
        else if (gameType === 'bubbles') initBubbles(container, controls, registerCleanup);
        else if (gameType === 'memory') initMemory(container, controls, registerCleanup);
        else if (gameType === 'drawing') initDrawing(container, controls, registerCleanup);
        else if (gameType === 'meditation') initMeditation(container, controls, registerCleanup);
        else if (gameType === 'color-puzzle') initColorPuzzle(container, controls, registerCleanup);
        else if (gameType === 'maze') initMaze(container, controls, registerCleanup);
        else if (gameType === 'word-puzzle') initWordPuzzle(container, controls, registerCleanup);
        else if (gameType === 'aquarium') initAquarium(container, controls, registerCleanup);
        else if (gameType === 'balance') initBalance(container, controls, registerCleanup);
        else container.innerHTML = '<p>Juego no disponible todavía.</p>';
    }

    // ---- Game Implementations (lightweight) ----
    function initTicTacToe(container, controls, registerCleanup) {
        const grid = document.createElement('div');
        grid.className = 'tic-tac-toe-grid';
        container.appendChild(grid);

        let board = Array(9).fill(null);
        let current = 'X';
        let vsAI = true;

        function render() {
            grid.innerHTML = '';
            board.forEach((cell,i) => {
                const c = document.createElement('div');
                c.className = 'tic-tac-toe-cell';
                c.textContent = cell || '';
                c.addEventListener('click', () => play(i));
                grid.appendChild(c);
            });
        }

        function play(i) {
            if (board[i] || checkWinner()) return;
            board[i] = current;
            current = current === 'X' ? 'O' : 'X';
            render();
            const w = checkWinner();
            if (w) showMessage(w === 'draw' ? 'Empate' : `${w} gana`);
            else if (vsAI && current === 'O') setTimeout(aiMove, 350);
        }

        function aiMove() {
            const avail = board.map((v,i)=>v?null:i).filter(v=>v!==null);
            if (!avail.length) return;
            const choice = avail[Math.floor(Math.random()*avail.length)];
            play(choice);
        }

        function checkWinner() {
            const combos = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
            for (const [a,b,c] of combos) {
                if (board[a] && board[a] === board[b] && board[a] === board[c]) return board[a];
            }
            if (board.every(Boolean)) return 'draw';
            return null;
        }

        function showMessage(txt) {
            const msg = document.createElement('div');
            msg.style.position='absolute'; msg.style.bottom='12px'; msg.style.left='12px'; msg.style.padding='8px 12px'; msg.style.background='rgba(0,0,0,0.6)'; msg.style.borderRadius='8px'; msg.style.color='white'; msg.textContent=txt;
            container.appendChild(msg);
            setTimeout(()=>{ if (msg.parentNode) msg.parentNode.removeChild(msg); }, 2000);
        }

        // Controls
        const restart = btn('Reiniciar');
        const toggleAI = btn('Toggle vs AI','btn-neon-sm-outline');
        controls.appendChild(restart); controls.appendChild(toggleAI);
        restart.addEventListener('click', ()=>{ board = Array(9).fill(null); current='X'; render(); });
        toggleAI.addEventListener('click', ()=>{ vsAI = !vsAI; toggleAI.textContent = vsAI ? 'vs AI: Sí' : 'vs AI: No'; });

        render();
    }

    function initBreathing(container, controls, registerCleanup) {
        const circle = document.createElement('div');
        circle.className = 'breathing-circle';
        circle.textContent = 'Pulsa comenzar';
        container.appendChild(circle);

        let intervalId = null;
        let phase = 0; // 0 inhale,1 hold,2 exhale
        let inh=4, hold=4, exh=6; // default

        const startBtn = btn('Comenzar');
        const stopBtn = btn('Detener','btn-neon-sm-outline');
        controls.appendChild(startBtn); controls.appendChild(stopBtn);

        startBtn.addEventListener('click', ()=>{
            if (intervalId) return;
            phase=0; circle.textContent='Inhala'; animateCircle(1);
            intervalId = setInterval(step, 1000);
        });
        stopBtn.addEventListener('click', ()=>{ clearInterval(intervalId); intervalId=null; circle.style.transform='scale(1)'; circle.textContent='Pausa'; });

        function step(){
            if (phase===0){ circle.textContent=`Inhala (${inh}s)`; animateCircle(1 + 0.3); setTimeout(()=>{}, 0); phase=1; setTimeout(()=>{ phase=2; }, inh*1000); }
        }

        // Simple gentle CSS transform pulse
        function animateCircle(scale){ circle.style.transition='transform 1s ease-in-out'; circle.style.transform=`scale(${scale})`; }

        registerCleanup(()=>{ clearInterval(intervalId); });
    }

    function initBubbles(container, controls, registerCleanup) {
        const canvas = document.createElement('canvas');
        canvas.className = 'bubbles-canvas';
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        container.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        const bubbles = [];
        let running = true;

        function spawn(){
            const r = 10 + Math.random()*30;
            bubbles.push({x: Math.random()*canvas.width, y: canvas.height + r, r, vy: -0.5 - Math.random()*1.2, a: Math.random()*0.6+0.2});
        }

        function loop(){
            if (!running) return;
            ctx.clearRect(0,0,canvas.width,canvas.height);
            if (Math.random() < 0.1) spawn();
            for (let i=bubbles.length-1;i>=0;i--){ const b=bubbles[i]; b.y += b.vy; ctx.beginPath(); ctx.fillStyle = `rgba(255,255,255,${b.a})`; ctx.arc(b.x,b.y,b.r,0,Math.PI*2); ctx.fill(); if (b.y + b.r < 0) bubbles.splice(i,1); }
            requestAnimationFrame(loop);
        }

        canvas.addEventListener('click', (e)=>{
            const rect = canvas.getBoundingClientRect(); const x = e.clientX - rect.left; const y = e.clientY - rect.top;
            for (let i=bubbles.length-1;i>=0;i--){ const b=bubbles[i]; const d = Math.hypot(b.x-x,b.y-y); if (d < b.r){ bubbles.splice(i,1); popSound(); break; } }
        });

        function popSound(){ try{ const aCtx = new (window.AudioContext||window.webkitAudioContext)(); const o=aCtx.createOscillator(); const g=aCtx.createGain(); o.type='sine'; o.frequency.value=600; g.gain.value=0.0001; o.connect(g); g.connect(aCtx.destination); o.start(); g.gain.exponentialRampToValueAtTime(0.02,aCtx.currentTime+0.01); g.gain.exponentialRampToValueAtTime(0.00001,aCtx.currentTime+0.25); setTimeout(()=>{ o.stop(); aCtx.close(); },300); }catch(e){}
        }

        loop();
        registerCleanup(()=>{ running=false; });
    }

    function initMemory(container, controls, registerCleanup) {
        const grid = document.createElement('div'); grid.className='memory-grid'; container.appendChild(grid);
        const emojis = ['🍃','🌸','🌞','🌊','🌙','🍂','🕊️','🌿'];
        const cards = shuffle([...emojis,...emojis]);
        let flipped = [];

        function render(){ grid.innerHTML=''; cards.forEach((c,i)=>{ const el=document.createElement('div'); el.className='memory-card'; el.dataset.index=i; el.textContent = flipped.includes(i) || cards[i].found ? cards[i] : '?'; el.addEventListener('click', ()=>flip(i,el)); grid.appendChild(el); }); }

        function flip(i,el){ if (flipped.length===2 || cards[i].found) return; flipped.push(i); render(); if (flipped.length===2){ const [a,b]=flipped; if (cards[a]===cards[b]){ cards[a].found = cards[b].found = true; setTimeout(()=>{ flipped=[]; render(); checkWin(); }, 600); } else { setTimeout(()=>{ flipped=[]; render(); }, 800); } } }

        function checkWin(){ if (cards.every(c=>c.found)) showMsg('¡Completado!'); }
        function showMsg(t){ const m=document.createElement('div'); m.style.position='absolute'; m.style.bottom='10px'; m.style.left='10px'; m.style.background='rgba(0,0,0,0.6)'; m.style.padding='8px 12px'; m.style.color='white'; m.style.borderRadius='8px'; m.textContent=t; container.appendChild(m); setTimeout(()=>m.remove(),1500); }

        const restart = btn('Reiniciar'); controls.appendChild(restart); restart.addEventListener('click', ()=>{ for (let k in cards) delete cards[k].found; const newCards = shuffle([...emojis,...emojis]); for (let i=0;i<newCards.length;i++) cards[i]=newCards[i]; flipped=[]; render(); });
        render();

        function shuffle(a){ for (let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
    }

    function initDrawing(container, controls, registerCleanup) {
        const canvas = document.createElement('canvas'); canvas.className='drawing-canvas'; canvas.width = container.clientWidth - 40; canvas.height = 380; container.appendChild(canvas);
        const ctx = canvas.getContext('2d'); ctx.fillStyle='white'; ctx.fillRect(0,0,canvas.width,canvas.height);
        let drawing=false; let color='#6ee7b7'; let size=4;
        canvas.addEventListener('pointerdown', e=>{ drawing=true; ctx.beginPath(); ctx.moveTo(e.offsetX,e.offsetY); });
        canvas.addEventListener('pointermove', e=>{ if(!drawing) return; ctx.lineTo(e.offsetX,e.offsetY); ctx.strokeStyle=color; ctx.lineWidth=size; ctx.lineCap='round'; ctx.stroke(); });
        canvas.addEventListener('pointerup', ()=>{ drawing=false; });

        const colorInput = document.createElement('input'); colorInput.type='color'; colorInput.value='#6ee7b7'; colorInput.addEventListener('input', e=>{ color=e.target.value; });
        const clearBtn = btn('Limpiar','btn-neon-sm-outline'); const saveBtn = btn('Descargar');
        controls.appendChild(colorInput); controls.appendChild(clearBtn); controls.appendChild(saveBtn);
        clearBtn.addEventListener('click', ()=>{ ctx.fillStyle='white'; ctx.fillRect(0,0,canvas.width,canvas.height); });
        saveBtn.addEventListener('click', ()=>{ const a=document.createElement('a'); a.href=canvas.toDataURL('image/png'); a.download='dibujo.png'; a.click(); });
    }

    function initMeditation(container, controls, registerCleanup) {
        const box = document.createElement('div'); box.style.padding='12px'; box.style.color='var(--text-main)'; box.innerHTML = '<p>Sesión de meditación breve: 3 minutos</p><div id="med-timer" style="font-size:2rem">03:00</div>';
        container.appendChild(box);
        let duration = 180; let timerId=null;
        const start = btn('Iniciar'); const stop = btn('Detener','btn-neon-sm-outline'); controls.appendChild(start); controls.appendChild(stop);
        let audioCtx, o, g;
        start.addEventListener('click', ()=>{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            o = audioCtx.createOscillator(); g = audioCtx.createGain(); o.type='sine'; o.frequency.value=220; g.gain.value=0.0001; o.connect(g); g.connect(audioCtx.destination); o.start(); g.gain.exponentialRampToValueAtTime(0.02,audioCtx.currentTime+1);
            let t=duration; updateTimer(t); timerId=setInterval(()=>{ t--; if (t<=0){ clearInterval(timerId); timerId=null; g.gain.exponentialRampToValueAtTime(0.00001,audioCtx.currentTime+0.5); setTimeout(()=>{ o.stop(); audioCtx.close(); audioCtx=null; },600); } updateTimer(t); },1000);
        });
        stop.addEventListener('click', ()=>{ if (timerId){ clearInterval(timerId); timerId=null; } if (audioCtx){ try{ g.gain.exponentialRampToValueAtTime(0.00001,audioCtx.currentTime+0.2); setTimeout(()=>{ o.stop(); audioCtx.close(); audioCtx=null; },300); }catch(e){} } });
        function updateTimer(s){ const m=Math.floor(s/60).toString().padStart(2,'0'); const sec=(s%60).toString().padStart(2,'0'); box.querySelector('#med-timer').textContent = `${m}:${sec}`; }
    }

    function initColorPuzzle(container, controls, registerCleanup) {
        const size = 4; const panel = document.createElement('div'); panel.style.display='grid'; panel.style.gridTemplateColumns=`repeat(${size},1fr)`; panel.style.gap='6px'; panel.style.width='360px'; container.appendChild(panel);
        const base = []; for (let i=0;i<size*size;i++){ base.push(i/(size*size)); }
        const colors = base.map(v=>`hsl(${Math.round(v*360)},70%,60%)`);
        let cells = shuffle(colors.slice());
        let first = null;
        function render(){ panel.innerHTML=''; cells.forEach((c,i)=>{ const d=document.createElement('div'); d.style.background=c; d.style.height='80px'; d.style.borderRadius='8px'; d.addEventListener('click', ()=>{ if (!first) first=i; else { [cells[first],cells[i]]=[cells[i],cells[first]]; first=null; render(); } }); panel.appendChild(d); }); }
        const restart = btn('Reiniciar'); controls.appendChild(restart); restart.addEventListener('click', ()=>{ cells=shuffle(colors.slice()); render(); }); render(); function shuffle(a){ for (let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
    }

    function initMaze(container, controls, registerCleanup) {
        const canvas = document.createElement('canvas'); canvas.width = 540; canvas.height = 360; canvas.style.borderRadius='8px'; container.appendChild(canvas); const ctx = canvas.getContext('2d');
        const cols = 15, rows = 10; const cellW = canvas.width/cols, cellH=canvas.height/rows;
        // simple random walk maze: generate open cells with perlin-like smoothing
        const grid = Array(rows).fill(0).map(()=>Array(cols).fill(1));
        for (let r=1;r<rows-1;r++) for (let c=1;c<cols-1;c++) grid[r][c] = Math.random()>0.3?0:1;
        // smoothing
        for (let k=0;k<3;k++) for (let r=1;r<rows-1;r++) for (let c=1;c<cols-1;c++){ let n=0; [[1,0],[-1,0],[0,1],[0,-1]].forEach(([dr,dc])=>{ if (grid[r+dr][c+dc]===1) n++; }); if (n<2) grid[r][c]=0; }
        const start = {r:1,c:1}; const exit = {r:rows-2,c:cols-2}; let player = {r:start.r,c:start.c};
        function draw(){ ctx.clearRect(0,0,canvas.width,canvas.height); for (let r=0;r<rows;r++) for (let c=0;c<cols;c++){ ctx.fillStyle = grid[r][c]===1? 'rgba(40,40,40,1)':'rgba(200,240,230,0.06)'; ctx.fillRect(c*cellW,r*cellH,cellW,cellH); }
            // player
            ctx.fillStyle='rgba(255,120,120,0.9)'; ctx.fillRect(player.c*cellW+4,player.r*cellH+4,cellW-8,cellH-8);
            ctx.fillStyle='rgba(120,255,180,0.9)'; ctx.fillRect(exit.c*cellW+6,exit.r*cellH+6,cellW-12,cellH-12);
        }
        function move(dr,dc){ const nr=player.r+dr, nc=player.c+dc; if (nr<0||nr>=rows||nc<0||nc>=cols) return; if (grid[nr][nc]===1) return; player.r=nr; player.c=nc; draw(); if (player.r===exit.r && player.c===exit.c) showMsg('Salida encontrada'); }
        function showMsg(t){ const m=document.createElement('div'); m.style.position='absolute'; m.style.bottom='10px'; m.style.left='10px'; m.style.background='rgba(0,0,0,0.6)'; m.style.padding='8px 12px'; m.style.color='white'; m.style.borderRadius='8px'; m.textContent=t; container.appendChild(m); setTimeout(()=>m.remove(),1500); }
        draw();
        function keyHandler(e){ if (e.key==='ArrowUp') move(-1,0); if (e.key==='ArrowDown') move(1,0); if (e.key==='ArrowLeft') move(0,-1); if (e.key==='ArrowRight') move(0,1); }
        window.addEventListener('keydown', keyHandler); registerCleanup(()=>{ window.removeEventListener('keydown', keyHandler); });
    }

    function initWordPuzzle(container, controls, registerCleanup) {
        const words = ['PAZ','RESPIRA','CALMA','SONRISA','SOL','MAR'];
        const size=10; const grid = Array.from({length:size},()=>Array(size).fill(''));
        // place words horizontally for simplicity
        words.forEach((w,i)=>{ const r = i%size; let start = Math.floor(Math.random()*(size - w.length)); for (let j=0;j<w.length;j++) grid[r][start+j]=w[j]; });
        // fill rest with random letters
        const letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'; for (let r=0;r<size;r++) for (let c=0;c<size;c++) if (!grid[r][c]) grid[r][c]=letters[Math.floor(Math.random()*letters.length)];
        const panel = document.createElement('div'); panel.className='wordsearch-grid'; container.appendChild(panel);
        for (let r=0;r<size;r++) for (let c=0;c<size;c++){ const cell=document.createElement('div'); cell.className='wordsearch-cell'; cell.textContent=grid[r][c]; panel.appendChild(cell); }
        const help = btn('Mostrar Palabras','btn-neon-sm-outline'); controls.appendChild(help); help.addEventListener('click', ()=>{ alert('Palabras: ' + words.join(', ')); });
    }

    function initAquarium(container, controls, registerCleanup) {
        const canvas = document.createElement('canvas'); canvas.className='aquarium-canvas'; canvas.width = container.clientWidth - 40; canvas.height = 360; container.appendChild(canvas); const ctx = canvas.getContext('2d');
        const fishes = []; for (let i=0;i<8;i++) fishes.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height, vx:(Math.random()-0.5)*1.2, vy:(Math.random()-0.5)*0.6, size:10+Math.random()*20});
        let running=true; function loop(){ if(!running) return; ctx.clearRect(0,0,canvas.width,canvas.height); // water
            ctx.fillStyle='rgba(20,60,100,0.3)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            fishes.forEach(f=>{ f.x+=f.vx; f.y+=f.vy; if (f.x<0||f.x>canvas.width) f.vx*=-1; if (f.y<0||f.y>canvas.height) f.vy*=-1; ctx.beginPath(); ctx.fillStyle='rgba(255,200,120,0.9)'; ctx.ellipse(f.x,f.y,f.size,f.size*0.6,0,0,Math.PI*2); ctx.fill(); }); requestAnimationFrame(loop); }
        canvas.addEventListener('click', ()=>{ // feed: add particles
            for (let i=0;i<6;i++){ fishes.push({x:Math.random()*canvas.width,y:0+Math.random()*50, vx:(Math.random()-0.5)*1, vy:Math.random()*1+0.2, size:6}); }
        }); loop(); registerCleanup(()=>{ running=false; });
    }

    function initBalance(container, controls, registerCleanup) {
        const box = document.createElement('div'); box.className='balance-area'; container.appendChild(box);
        const emotions = ['Triste','Frustrado','Contento','Calmado','Ansioso','Motivado'];
        const chips = emotions.map(e=>{ const d=document.createElement('div'); d.className='emotion-chip'; d.textContent=e; d.draggable=true; return d; });
        const pos = document.createElement('div'); pos.style.minWidth='120px'; pos.style.minHeight='120px'; pos.style.border='1px dashed rgba(255,255,255,0.06)'; pos.style.borderRadius='8px'; pos.style.padding='8px'; pos.textContent='Positivo';
        const neg = pos.cloneNode(true); neg.textContent='Negativo'; box.appendChild(...chips); box.appendChild(pos); box.appendChild(neg);
        chips.forEach(c=>{ c.addEventListener('dragstart', e=>{ e.dataTransfer.setData('text/plain', c.textContent); }); });
        [pos,neg].forEach(target=>{ target.addEventListener('dragover', e=>e.preventDefault()); target.addEventListener('drop', e=>{ e.preventDefault(); const txt=e.dataTransfer.getData('text/plain'); const el = chips.find(x=>x.textContent===txt); if (el && el.parentNode!==target){ target.appendChild(el); } }); });
    }

    
    // Helper functions for game data
    function getGameIcon(gameType) {
        const icons = {
            'tic-tac-toe': 'toc',
            'breathing': 'air',
            'color-puzzle': 'palette',
            'maze': 'map',
            'bubbles': 'circle',
            'memory': 'memory',
            'drawing': 'brush',
            'meditation': 'psychology',
            'word-puzzle': 'title',
            'aquarium': 'aquarium',
            'balance': 'timeline'
        };
        return `<span class="material-icons-round" style="font-size: 3rem;">${icons[gameType] || 'psychology'}</span>`;
    }
    
    function getGameTitle(gameType) {
        const titles = {
            'tic-tac-toe': 'Tres en Raya',
            'breathing': 'Respiración Guiada',
            'color-puzzle': 'Rompecabezas de Colores',
            'maze': 'Laberinto Zen',
            'bubbles': 'Burbujas Relajantes',
            'memory': 'Memoria Visual',
            'drawing': 'Dibujo Terapéutico',
            'meditation': 'Meditación Breve',
            'word-puzzle': 'Sopa de Letras Calma',
            'aquarium': 'Acuario Virtual',
            'balance': 'Equilibrio Emocional'
        };
        return titles[gameType] || 'Juego Antiestrés';
    }
    
    function getGameDescription(gameType) {
        const descriptions = {
            'tic-tac-toe': 'Clásico juego de estrategia para dos jugadores. Perfecto para enfocar la mente y tomar un breve descanso.',
            'breathing': 'Ejercicio de respiración profunda para reducir el estrés y la ansiedad en pocos minutos.',
            'color-puzzle': 'Ordena los colores degradados para crear una transición suave. Excelente para la concentración y percepción visual.',
            'maze': 'Encuentra la salida en laberintos generados aleatoriamente con música ambiental suave.',
            'bubbles': 'Haz clic en las burbujas que aparecen en pantalla para liberar tensión con efectos visuales y sonoros calmantes.',
            'memory': 'Encuentra las parejas de imágenes idénticas para ejercitar la memoria de forma lúdica y relajante.',
            'drawing': 'Libera tu creatividad con herramientas de dibujo simples y colores relajantes sin presión de resultado.',
            'meditation': 'Sesiones guiadas de 3-5 minutos para reducir el estrés y mejorar la concentración.',
            'word-puzzle': 'Encuentra palabras relacionadas con bienestar y relajación en una sopa de letras temática.',
            'aquarium': 'Observa y interactúa con peces virtuales en un ambiente acuático tranquilizador con sonidos de agua.',
            'balance': 'Mantén el balancín estable mientras aparecen emociones que debes clasificar como positivas o negativas.'
        };
        return descriptions[gameType] || 'Juego diseñado para reducir el estrés y promover la relajación.';
    }
    
    function getGameFeature1(gameType) {
        const features1 = {
            'tic-tac-toe': 'Modo un jugador contra IA o dos jugadores',
            'breathing': 'Guía visual y sonora para ritmo perfecto',
            'color-puzzle': 'Miles de combinaciones de colores posibles',
            'maze': 'Laberintos generados proceduralmente',
            'bubbles': 'Efectos de sonido y visuales tranquilizantes',
            'memory': 'Mejora la memoria visual y concentración',
            'drawing': 'Libera creatividad sin juicio ni presión',
            'meditation': 'Sesiones de 3, 5 y 10 minutos disponibles',
            'word-puzzle': 'Vocabulario enfocado en bienestar y paz',
            'aquarium': 'Múltiples escenas acuáticas para elegir',
            'balance': 'Desarrolla inteligencia emocional mientras juegas'
        };
        return features1[gameType] || 'Diseño pensado para la relajación';
    }
    
    function getGameFeature2(gameType) {
        const features2 = {
            'tic-tac-toe': 'Dificultad ajustable de la IA',
            'breathing': 'Personaliza los tiempos de inhalación/exhalación',
            'color-puzzle': 'Modo contrarreloj o juego libre',
            'maze': 'Música ambiental y sonidos de naturaleza',
            'bubbles': 'Modo desafío con puntuación',
            'memory': 'Niveles de dificultad creciente',
            'drawing': 'Variedad de herramientas y colores',
            'meditation': 'Diferentes técnicas de meditación guiada',
            'word-puzzle': 'Pistas disponibles si te atas',
            'aquarium': 'Interactúa con los peces y el ambiente',
            'balance': 'Retroalimentación inmediata sobre tus decisiones'
        };
        return features2[gameType] || 'Mecánicas simples y intuitivas';
    }
    
    function getGameFeature3(gameType) {
        const features3 = {
            'tic-tac-toe': 'Estadísticas de victorias/derrotas/empates',
            'breathing': 'Registro de sesiones y progreso',
            'color-puzzle': 'Guarda tus mejores tiempos',
            'maze': 'Tablas de líderes por tiempo de completion',
            'bubbles': 'Modo zen sin límite de tiempo',
            'memory': 'Modo contrarreloj disponible',
            'drawing': 'Opción de guardar y compartir tus dibujos',
            'meditation': 'Recordatorios para practicar diariamente',
            'word-puzzle': 'Nuevos rompecabezas diarios',
            'aquarium': 'Información sobre las especies de peces',
            'balance': 'Niveles que aumentan en complejidad emocional'
        };
        return features3[gameType] || 'Interfaz limpia y libre de distracciones';
    }
    
    // Add hover effect to game cards
    gameCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            if (!card.classList.contains('active')) {
                card.style.transform = 'translateY(-3px)';
                card.style.boxShadow = '0 10px 25px rgba(0, 240, 255, 0.2)';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (!card.classList.contains('active')) {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.4)';
            }
        });
    });
    
    // Initialize original button texts
    gameLaunches.forEach(button => {
        if (!button.dataset.originalText) {
            button.dataset.originalText = button.textContent;
        }
    });
    
    console.log("🧘‍♂️ Antiestrés module initialized");
});