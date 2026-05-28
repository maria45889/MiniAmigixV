document.addEventListener('DOMContentLoaded', function () {
    const openCreateBtn = document.getElementById('open-create-post');
    const modal = document.getElementById('create-post-modal');
    const closeModalBtn = modal ? modal.querySelector('.close-modal') : null;
    const form = document.getElementById('create-post-form');
    const postsGrid = document.querySelector('.posts-grid') || document.querySelector('.blog-main');

    const LOCAL_KEY = 'miniAmigixLocalPosts';

    function openModal() {
        if (!modal) return;
        modal.style.display = 'block';
    }
    function closeModal() {
        if (!modal) return;
        modal.style.display = 'none';
    }

    if (openCreateBtn) openCreateBtn.addEventListener('click', function (e) {
        e.preventDefault();
        openModal();
    });
    if (closeModalBtn) closeModalBtn.addEventListener('click', function () {
        closeModal();
    });
    window.addEventListener('click', function (e) {
        if (e.target === modal) closeModal();
    });

    function fetchJSON(url) {
        return fetch(url).then(r => {
            if (!r.ok) throw new Error('Network error');
            return r.json();
        });
    }

    function renderPost(post, opts = {}) {
        // opts.local -> indicates this is a client-only post
        const container = document.createElement('div');
        container.className = 'post-card';

        const header = document.createElement('div');
        header.className = 'post-header';
        const icon = document.createElement('span');
        icon.className = 'material-icons-round post-icon';
        icon.textContent = post.post_type === 'admin' ? 'announcement' : 'person';
        const h3 = document.createElement('h3');
        h3.textContent = post.titulo;
        header.appendChild(icon);
        header.appendChild(h3);

        const body = document.createElement('div');
        body.className = 'post-body';
        const excerpt = document.createElement('p');
        excerpt.className = 'post-excerpt';
        excerpt.textContent = (post.contenido || '').split(' ').slice(0, 20).join(' ') + (post.contenido && post.contenido.split(' ').length > 20 ? '…' : '');
        const meta = document.createElement('div');
        meta.className = 'post-meta';
        meta.innerHTML = `
            <span class="post-author"><span class="material-icons-round">person</span> ${post.autor || 'Anónimo'}</span>
            <span class="post-date"><span class="material-icons-round">calendar_today</span> ${post.fecha || ''}</span>
            <span class="post-read-time"><span class="material-icons-round">timer</span> ${post.lectura_min || 1} min de lectura</span>
            <span class="post-type-badge ${post.post_type === 'admin' ? 'admin' : 'personal'}">${post.post_type === 'admin' ? 'Oficial' : 'Personal'}</span>
        `;
        body.appendChild(excerpt);
        body.appendChild(meta);

        const footer = document.createElement('div');
        footer.className = 'post-footer';
        const readBtn = document.createElement('a');
        readBtn.className = 'btn-neon-sm';
        readBtn.href = '#';
        readBtn.textContent = 'Leer más';
        footer.appendChild(readBtn);

        container.appendChild(header);
        container.appendChild(body);
        container.appendChild(footer);

        if (opts.local) {
            const actions = document.createElement('div');
            actions.className = 'post-actions';
            const edit = document.createElement('button');
            edit.className = 'btn-neon-sm';
            edit.textContent = 'Editar';
            const del = document.createElement('button');
            del.className = 'btn-neon-sm danger';
            del.textContent = 'Eliminar';
            actions.appendChild(edit);
            actions.appendChild(del);
            footer.appendChild(actions);

            edit.addEventListener('click', function () {
                openModal();
                // populate form
                document.getElementById('post-title').value = post.titulo;
                document.getElementById('post-category').value = post.categoria || '';
                document.getElementById('post-content').value = post.contenido || '';
                document.getElementById('post-type').value = post.post_type || 'personal';
                document.getElementById('post-autor').value = post.autor || '';
                document.getElementById('post-lectura').value = post.lectura_min || 1;
                // mark as editing by storing editing id on form
                form.dataset.editingId = post._localId;
            });
            del.addEventListener('click', function () {
                if (!confirm('¿Eliminar publicación local?')) return;
                removeLocalPost(post._localId);
                container.remove();
            });
        }

        // prepend admin posts, append local/posts created now
        if (post.post_type === 'admin') {
            if (postsGrid && postsGrid.querySelector('.posts-grid')) {
                postsGrid.querySelector('.posts-grid').prepend(container);
            } else if (postsGrid) {
                postsGrid.prepend(container);
            }
        } else {
            if (postsGrid && postsGrid.querySelector('.posts-grid')) {
                postsGrid.querySelector('.posts-grid').appendChild(container);
            } else if (postsGrid) {
                postsGrid.appendChild(container);
            }
        }
    }

    function saveLocalPost(post) {
        const arr = JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');
        // assign simple local id
        post._localId = 'local-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
        arr.unshift(post);
        localStorage.setItem(LOCAL_KEY, JSON.stringify(arr));
        return post;
    }
    function loadLocalPosts() {
        try {
            const arr = JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');
            arr.forEach(p => renderPost(p, { local: true }));
        } catch (e) {
            console.warn('Failed to load local posts', e);
        }
    }
    function removeLocalPost(localId) {
        try {
            const arr = JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');
            const filtered = arr.filter(x => x._localId !== localId);
            localStorage.setItem(LOCAL_KEY, JSON.stringify(filtered));
        } catch (e) { }
    }

    function submitToServer(payload) {
        return fetch('/blog/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        }).then(r => r.json());
    }

    form && form.addEventListener('submit', function (e) {
        e.preventDefault();
        const data = {
            titulo: document.getElementById('post-title').value.trim(),
            categoria: document.getElementById('post-category').value,
            contenido: document.getElementById('post-content').value.trim(),
            autor: document.getElementById('post-autor').value.trim() || 'Anónimo',
            lectura_min: parseInt(document.getElementById('post-lectura').value, 10) || 1,
            post_type: document.getElementById('post-type').value || 'personal'
        };

        // If editing local post
        const editingId = form.dataset.editingId;
        if (editingId) {
            // update local storage and re-render
            const arr = JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');
            const idx = arr.findIndex(x => x._localId === editingId);
            if (idx > -1) {
                arr[idx] = Object.assign(arr[idx], data);
                localStorage.setItem(LOCAL_KEY, JSON.stringify(arr));
                // simple approach: reload the page area
                location.reload();
                return;
            }
        }

        submitToServer(data).then(resp => {
            if (resp && resp.success && resp.post && resp.post.id) {
                // server saved — append to UI
                data.fecha = resp.post.fecha || new Date().toLocaleString();
                renderPost(data, { local: false });
                closeModal();
                form.reset();
            } else {
                // fallback: save locally
                const local = saveLocalPost(Object.assign({ fecha: new Date().toLocaleString() }, data));
                renderPost(local, { local: true });
                closeModal();
                form.reset();
                alert('Publicación guardada localmente (sin conexión al servidor).');
            }
        }).catch(err => {
            console.warn('Create post failed', err);
            const local = saveLocalPost(Object.assign({ fecha: new Date().toLocaleString() }, data));
            renderPost(local, { local: true });
            closeModal();
            form.reset();
            alert('Publicación guardada localmente (error de red).');
        });
    });

    // Load admin posts from static JSON and local posts
    fetchJSON('/static/data/admin_posts.json').then(list => {
        if (Array.isArray(list)) list.forEach(p => renderPost(p));
    }).catch(() => { /* ignore */ });

    loadLocalPosts();
});
