// Empty service worker to disable workbox in development
self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', () => {
  self.clients.claim();
});

// Do nothing for all other events
self.addEventListener('fetch', (event) => {
  // Let the browser handle all requests normally
}); 