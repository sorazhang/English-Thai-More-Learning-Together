# KruExchange · Claude Code Handoff
**Date:** 2026-04-13  
**Session:** 6.1.4

---

## Project Overview

A bilingual English-Thai language exchange website built around a Muay Thai training context. Two characters: a Thai Muay Thai coach (kru) learning English, and Sora (student) learning Thai.

**Live site:** https://sorazhang.github.io/English-Thai-More-Learning-Together/

---

## File Structure

```
/
├── index.html                  ← Main library page (rebuilt this session)
├── my-saved-note.html          ← Personal notes app (built this session)
├── kru-language-exchange.html  ← Vol 1
├── kru-exchange-vol2.html      ← Vol 2
├── kru-exchange-vol3.html      ← ...
├── kru-exchange-vol4.html      ← Vol 4 (pilot — already has TTS + bookmark)
│   ...
├── kru-exchange-vol22.html     ← Vol 22
└── inject_features_v1.py       ← Run this to update all 22 vols
```

---

## What Was Built This Session

### 1. `index.html` — rebuilt
- Dark `#0a0906` bg, Cormorant Garamond, pixel art Muay Thai fighter (bobbing)
- Sticky search bar with live filtering + category pills (All · Gym · Food · Culture · Travel · Daily Life)
- **🔖 My Notes** button in search bar row
- All 22 volumes with correct `data-cat` attributes
- 🥊 Volumes pill nav (bottom-right) with My Notes in footer
- Async font loading (non-blocking)

### 2. `my-saved-note.html` — new page
Same arcade aesthetic as KruVocab POC. Login screen on first visit (name + API key + role).

**Three sections:**
- **📌 My Topics** — bookmarked cards from vol pages (from `kruexchange_saved_cards` localStorage)
- **📖 My Words** — words searched + saved via Anthropic API (from `kruexchange_my_words` localStorage)  
- **🌐 Word Cloud** — built from My Words only (API-searched words)

**Features:** API word lookup (Anthropic), TTS on cards, tag filter pills, search, remove buttons, settings sheet (change name/key/role), logout.

### 3. `inject_features_v1.py` — run locally
```bash
cd /path/to/your/html/files
python3 inject_features_v1.py
```
Injects into all 22 vol files:
- TTS buttons (EN on `.e` lines, TH on `.t` lines)
- Bookmark button (bottom-right of each card, gold fireworks on save)
- Pill footer with `← All Volumes` and `🔖 My Notes` links
- Async font loading fix

### 4. `kru-exchange-vol4-tts.html` — pilot
Vol 4 already has all features injected. Use as reference for what other vols will look like after running the inject script.

---

## localStorage Keys

| Key | Contents |
|-----|----------|
| `kruexchange_saved_cards` | Bookmarked cards from vol pages |
| `kruexchange_my_words` | Words added via API lookup |
| `kruexchange_session` | User session (name, API key, role) |

---

## Design System

### KruExchange vol pages
- Fonts: Fraunces (headers), Outfit (body), Noto Sans Thai
- Colors: `--bg: #faf7f2` · `--eng: #2a5c8a` · `--thai: #8a2040` · `--roman: #2a6640` · `--accent: #c05828`

### index.html
- Fonts: Cormorant Garamond (display), Jost (body), Noto Sans Thai
- Colors: `--bg: #0a0906` · `--gold: #c8943a` · `--cream: #f0e8d8`

### my-saved-note.html
- Fonts: Press Start 2P (pixel/arcade), Outfit, Noto Sans Thai
- Colors: `--bg: #0a0a12` · `--cyan: #00e5ff` · `--orange: #ff6d00` · `--yellow: #ffd600`

---

## Immediate Next Tasks

### Priority 1 — Floating 🔖 My Notes pill
Add a second floating pill (bottom-left) on **every page** — index + all 22 vols. Links to `my-saved-note.html`. Should be always visible, opposite side from the 🥊 Volumes pill.

Add to `index.html` manually, add to `inject_features_v1.py` so vols get it on next run.

```css
/* suggested CSS — add alongside existing pill styles */
.notes-pill {
  position: fixed; bottom: 1.6rem; left: 1.6rem;
  background: rgba(184,120,32,0.15);
  border: 1px solid rgba(184,120,32,0.4);
  color: #c8943a;
  border-radius: 99px;
  padding: 0.55rem 1.05rem;
  font-size: 0.72rem; font-weight: 700;
  text-decoration: none;
  z-index: 300;
  transition: all 0.2s;
}
.notes-pill:hover { background: rgba(184,120,32,0.25); }
```

```html
<a class="notes-pill" href="my-saved-note.html">🔖 My Notes</a>
```

### Priority 2 — Run inject script
```bash
python3 inject_features_v1.py
```
Verify on 2–3 vols: TTS buttons appear, bookmark saves to localStorage, pill footer has My Notes link.

### Priority 3 — Verify My Notes flow
1. Open a vol → bookmark a card → pill → My Notes
2. Check My Topics shows the bookmarked card
3. Open My Notes → + → search a word → save → check My Words and Word Cloud

---

## Known Issues / Watch Out For

- `inject_features_v1.py` uses `INJECTION_MARKER = "/* KRU-FEATURES-v1 */"` to detect already-injected files — safe to re-run
- TTS only works when opened as a **local file in Chrome** (`file:///...`) — blocked in sandboxed iframes
- Web Speech API: Chrome needs `speechSynthesis.cancel()` + `resume()` + 50ms delay (already in the code)
- Anthropic API key must start with `sk-` — the setup screen validates this
- Non-ASCII characters in pasted API keys can silently break auth — the code filters to ASCII 32–126
- `</style>` closing tag sometimes gets silently dropped during HTML injection — always verify after inject

---

## Vol Pages In Scope (for inject script)

`kru-language-exchange.html` · `kru-exchange-vol2` through `vol22` (note: vol10, vol11 not in the index)

---

## Out of Scope (experimental files — do not inject)

`wisdom-index.html` · `wisdom-mockup-v3.html` · `kru-combinations.html` · `kru-exchange-vol4-comic.html`
