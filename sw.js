const CACHE = 'kruexchange-v22';

const STATIC = [
  '/index.html',
  '/my-saved-note.html',
  '/shared-cloud.html',
  '/kru-language-exchange.html',
  '/kru-exchange-vol2.html',
  '/kru-exchange-vol3.html',
  '/kru-exchange-vol4.html',
  '/kru-exchange-vol5.html',
  '/kru-exchange-vol6.html',
  '/kru-exchange-vol7.html',
  '/kru-exchange-vol8.html',
  '/kru-exchange-vol9.html',
  '/kru-exchange-vol12.html',
  '/kru-exchange-vol13.html',
  '/kru-exchange-vol14.html',
  '/kru-exchange-vol15.html',
  '/kru-exchange-vol16.html',
  '/kru-exchange-vol17.html',
  '/kru-exchange-vol19.html',
  '/kru-exchange-vol21.html',
  '/kru-exchange-vol22.html',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/thai-temple.png',
  '/manifest.json'
];

/* Install — pre-cache all static pages */
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(STATIC)).then(() => self.skipWaiting())
  );
});

/* Activate — clean up old caches */
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

/* Fetch strategy:
   - Firebase / Google APIs / CDN scripts → network only (live data)
   - Everything else → cache first, fall back to network, update cache */
self.addEventListener('fetch', e => {
  const url = e.request.url;
  if (
    url.includes('firebasedatabase.app') ||
    url.includes('firebaseio.com') ||
    url.includes('googleapis.com') ||
    url.includes('gstatic.com') ||
    url.includes('anthropic.com') ||
    url.includes('api.anthropic')
  ) {
    e.respondWith(fetch(e.request));
    return;
  }

  e.respondWith(
    caches.match(e.request).then(cached => {
      const network = fetch(e.request).then(res => {
        if (res.ok) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      });
      return cached || network;
    })
  );
});
