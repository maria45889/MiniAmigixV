const CACHE_NAME = 'miniamigixv-v6';
const urlsToCache = [
    '/',
    '/static/css/core/style.css',
    '/static/css/core/sidebar-neon.css',
    '/static/imagenes/logo.png',
    '/static/favicon.ico'
].filter(url => {
    // Validate URLs before caching
    try {
        new URL(url, window.location.origin);
        return true;
    } catch (e) {
        console.warn('Invalid URL in cache list:', url);
        return false;
    }
});

// Instalación del service worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache for:', CACHE_NAME);
                return cache.addAll(urlsToCache.map(url => {
                    console.log('Caching:', url);
                    return url;
                })).catch(error => {
                    console.error('Failed to cache some URLs:', error);
                    // Continue even if some URLs fail to cache
                    return Promise.resolve();
                });
            })
    );
    self.skipWaiting();
});

// Activación del service worker
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch de recursos
self.addEventListener('fetch', event => {
    // No cachear llamadas a la API
    if (event.request.url.includes('/api/') || event.request.url.includes('/clima/')) {
        event.respondWith(fetch(event.request));
        return;
    }

    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Cache hit - return response
                if (response) {
                    return response;
                }
                return fetch(event.request).then(
                    response => {
                        // Check if valid response
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        // Clone response
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME)
                            .then(cache => {
                                cache.put(event.request, responseToCache);
                            }).catch(err => {
                                console.warn('Failed to cache response:', err);
                            });
                        return response;
                    }
                ).catch(error => {
                    console.error('Fetch failed:', error);
                    return new Response('Network error occurred', { status: 503 });
                });
            })
    );
});
