#!/usr/bin/env python3
"""
inject_features_v1.py
=====================
Injects three features into every in-scope Kru Exchange volume:

  1. TTS speak buttons  — EN button on every .e line, TH button on every .t line
  2. Bookmark button    — bottom-right of every card, saves to localStorage
  3. Pill nav update    — adds "All Volumes" + "My Notes" action rows to pill popover

Run from the directory containing the HTML files:
    python3 inject_features_v1.py

Or point SRC to the folder:
    SRC = "/path/to/your/html/files"
"""

import os, re

# ── CONFIGURE THIS ────────────────────────────────────────────────────────────
SRC = "."          # folder containing the HTML files (change if needed)
# ─────────────────────────────────────────────────────────────────────────────

INJECTION_MARKER = "/* KRU-FEATURES-v1 */"   # prevents double-injection

# In-scope files  →  (vol_id, vol_label)
FILES = {
    "kru-language-exchange.html": ("1",  "Vol. 1"),
    "kru-exchange-vol2.html":     ("2",  "Vol. 2"),
    "kru-exchange-vol3.html":     ("3",  "Vol. 3"),
    "kru-exchange-vol4.html":     ("4",  "Vol. 4"),
    "kru-exchange-vol5.html":     ("5",  "Vol. 5"),
    "kru-exchange-vol6.html":     ("6",  "Vol. 6"),
    "kru-exchange-vol7.html":     ("7",  "Vol. 7"),
    "kru-exchange-vol8.html":     ("8",  "Vol. 8"),
    "kru-exchange-vol9.html":     ("9",  "Vol. 9"),
    "kru-exchange-vol12.html":    ("12", "Vol. 12"),
    "kru-exchange-vol13.html":    ("13", "Vol. 13"),
    "kru-exchange-vol14.html":    ("14", "Vol. 14"),
    "kru-exchange-vol15.html":    ("15", "Vol. 15"),
    "kru-exchange-vol16.html":    ("16", "Vol. 16"),
    "kru-exchange-vol17.html":    ("17", "Vol. 17"),
    "kru-exchange-vol18.html":    ("18", "Vol. 18"),
    "kru-exchange-vol19.html":    ("19", "Vol. 19"),
    "kru-exchange-vol20.html":    ("20", "Vol. 20"),
    "kru-exchange-vol21.html":    ("21", "Vol. 21"),
    "kru-exchange-vol22.html":    ("22", "Vol. 22"),
}

# ── CSS ───────────────────────────────────────────────────────────────────────
FEATURES_CSS = """
  /* KRU-FEATURES-v1 — TTS + Bookmark — do not remove this comment */

  /* ── BOOKMARK ── */
  .num { display: none; }

  .bm-btn {
    position: absolute;
    bottom: 0.75rem; right: 1rem;
    width: 26px; height: 26px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 6px;
    border: 1.5px solid var(--border);
    background: transparent;
    cursor: pointer;
    transition: all 0.18s;
    color: var(--muted);
    padding: 0;
    z-index: 2;
  }

  .bm-btn:hover {
    border-color: var(--gold, #b87820);
    color: var(--gold, #b87820);
    background: rgba(184,120,32,0.07);
  }

  .bm-btn.saved {
    border-color: var(--gold, #b87820);
    color: var(--gold, #b87820);
    background: rgba(184,120,32,0.1);
  }

  .bm-btn svg { width: 13px; height: 13px; }

  @keyframes bmPop {
    0%   { transform: scale(1) rotate(0deg); }
    35%  { transform: scale(1.55) rotate(-12deg); }
    65%  { transform: scale(0.88) rotate(6deg); }
    100% { transform: scale(1) rotate(0deg); }
  }

  @keyframes particleFly {
    0%   { transform: translate(0,0) scale(1); opacity: 1; }
    100% { transform: translate(var(--dx), var(--dy)) scale(0); opacity: 0; }
  }

  .bm-btn.popping { animation: bmPop 0.42s cubic-bezier(0.34,1.56,0.64,1) forwards; }

  .bm-particle {
    position: fixed; border-radius: 50%;
    pointer-events: none; z-index: 9999;
  }

  .bm-toast {
    position: fixed;
    bottom: 2rem; left: 50%; transform: translateX(-50%) translateY(10px);
    background: var(--ink, #1c1710);
    color: rgba(250,247,242,0.9);
    font-size: 0.76rem; font-weight: 500;
    padding: 0.55rem 1.1rem;
    border-radius: 99px;
    border: 1px solid rgba(255,255,255,0.1);
    opacity: 0; transition: all 0.22s;
    pointer-events: none; z-index: 999;
    white-space: nowrap; font-family: 'Outfit', sans-serif;
  }

  .bm-toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }

  /* ── TTS SPEAK BUTTONS ── */
  .card { padding-bottom: 2.2rem; }

  .speak-line {
    display: flex; align-items: flex-start;
    justify-content: space-between; gap: 0.5rem;
  }

  .speak-text { flex: 1; }

  .speak-btn {
    flex-shrink: 0;
    display: inline-flex; align-items: center; justify-content: center;
    gap: 3px; padding: 3px 8px;
    border-radius: 20px; border: 1.5px solid;
    background: transparent; cursor: pointer;
    font-size: 0.7rem; font-weight: 600;
    font-family: 'Outfit', sans-serif; letter-spacing: 0.04em;
    transition: all 0.15s; white-space: nowrap;
    margin-top: 2px; min-height: 26px; min-width: 44px;
  }

  .speak-btn.eng { color: var(--eng, #2a5c8a); border-color: rgba(42,92,138,0.35); }
  .speak-btn.eng:hover { background: rgba(42,92,138,0.08); border-color: var(--eng, #2a5c8a); }
  .speak-btn.tha { color: var(--thai, #8a2040); border-color: rgba(138,32,64,0.35); }
  .speak-btn.tha:hover { background: rgba(138,32,64,0.08); border-color: var(--thai, #8a2040); }

  .speak-btn.speaking { animation: speakPulse 0.9s ease-in-out infinite; }
  .speak-btn.eng.speaking { background: rgba(42,92,138,0.12); border-color: var(--eng, #2a5c8a); }
  .speak-btn.tha.speaking { background: rgba(138,32,64,0.12); border-color: var(--thai, #8a2040); }

  @keyframes speakPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.6; transform: scale(0.95); }
  }

  .speak-btn svg { width: 11px; height: 11px; flex-shrink: 0; }

  /* pill nav additions */
  .pp-foot {
    border-top: 1px solid rgba(255,255,255,0.07);
    padding: 4px 0;
  }
  .pp-foot .pp-lnk { color: rgba(200,148,58,0.8) !important; font-weight: 700 !important; }
  .pp-foot .pp-lnk:hover { color: rgba(200,148,58,1) !important; }
"""

# ── TOAST HTML ────────────────────────────────────────────────────────────────
TOAST_HTML = '\n<div id="bmToast" class="bm-toast"></div>'

# ── TTS JS ────────────────────────────────────────────────────────────────────
TTS_JS = """
<script>
/* ── TTS · Web Speech API · en-GB + th-TH ── */
var _ttsActiveBtn = null;
var _speakerSVG = '<svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2 5.5h2.5L8 2.5v11L4.5 10.5H2V5.5z" fill="currentColor"/><path d="M10.5 5.5c1.1 0.7 1.8 1.9 1.8 3.5s-0.7 2.8-1.8 3.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><path d="M12.5 3.5C14.2 4.7 15.2 6.2 15.2 8s-1 3.3-2.7 4.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>';

function _makeBtn(lang, cls, label) {
  var btn = document.createElement('button');
  btn.className = 'speak-btn ' + cls;
  btn.dataset.lang = lang;
  btn.setAttribute('aria-label', 'Listen in ' + label);
  btn.innerHTML = _speakerSVG + '<span>' + label + '</span>';
  btn.addEventListener('click', function(e) { e.stopPropagation(); _speakBtn(this); });
  return btn;
}

function _speakBtn(btn) {
  if (!window.speechSynthesis) return;
  if (_ttsActiveBtn && _ttsActiveBtn !== btn) _ttsActiveBtn.classList.remove('speaking');
  window.speechSynthesis.cancel();
  window.speechSynthesis.resume();
  var textEl = btn.closest('.speak-line').querySelector('.speak-text');
  var text = textEl ? textEl.textContent.trim() : '';
  if (!text) return;
  var lang = btn.dataset.lang;
  setTimeout(function() {
    var utt = new SpeechSynthesisUtterance(text);
    utt.lang = lang;
    utt.rate = lang === 'th-TH' ? 0.82 : 0.92;
    var voices = window.speechSynthesis.getVoices();
    var voice = voices.find(function(v) { return v.lang === lang; })
             || voices.find(function(v) { return v.lang.startsWith(lang.split('-')[0]); });
    if (voice) utt.voice = voice;
    _ttsActiveBtn = btn;
    btn.classList.add('speaking');
    utt.onend = function() { btn.classList.remove('speaking'); _ttsActiveBtn = null; };
    utt.onerror = function() { btn.classList.remove('speaking'); _ttsActiveBtn = null; };
    window.speechSynthesis.speak(utt);
  }, 60);
}

function _injectSpeakButtons() {
  document.querySelectorAll('.e, .dt .e').forEach(function(el) {
    if (el.querySelector('.speak-btn')) return;
    var wrap = document.createElement('div'); wrap.className = 'speak-line';
    var span = document.createElement('span'); span.className = 'speak-text';
    span.innerHTML = el.innerHTML; el.innerHTML = '';
    wrap.appendChild(span); wrap.appendChild(_makeBtn('en-GB','eng','EN'));
    el.appendChild(wrap);
  });
  document.querySelectorAll('.t, .dt .t').forEach(function(el) {
    if (el.querySelector('.speak-btn')) return;
    var wrap = document.createElement('div'); wrap.className = 'speak-line';
    var span = document.createElement('span'); span.className = 'speak-text';
    span.innerHTML = el.innerHTML; el.innerHTML = '';
    wrap.appendChild(span); wrap.appendChild(_makeBtn('th-TH','tha','TH'));
    el.appendChild(wrap);
  });
}

if (!window.speechSynthesis) {
  console.warn('TTS not available');
} else {
  var _v = window.speechSynthesis.getVoices();
  if (_v.length > 0) { _injectSpeakButtons(); }
  else {
    window.speechSynthesis.addEventListener('voiceschanged', function() { _injectSpeakButtons(); }, { once: true });
    setTimeout(_injectSpeakButtons, 400);
  }
}
</script>"""

# ── BOOKMARK JS (template — vol_id and vol_label are substituted per file) ────
BOOKMARK_JS_TPL = """
<script>
/* ── BOOKMARKS · localStorage · My Notes ── */
var _BM_KEY   = 'kruexchange_saved_cards';
var _BM_VOL   = '{vol_id}';
var _BM_LABEL = '{vol_label}';

var _bmOutline = '<svg viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2 2.5A1.5 1.5 0 0 1 3.5 1h7A1.5 1.5 0 0 1 12 2.5V14l-5-2.5L2 14V2.5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>';
var _bmFilled  = '<svg viewBox="0 0 14 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M2 2.5A1.5 1.5 0 0 1 3.5 1h7A1.5 1.5 0 0 1 12 2.5V14l-5-2.5L2 14V2.5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>';

function _bmLoad() { try { return JSON.parse(localStorage.getItem(_BM_KEY) || '[]'); } catch(e) { return []; } }
function _bmWrite(a) { try { localStorage.setItem(_BM_KEY, JSON.stringify(a)); } catch(e) {} }

function _bmCardId(card) {
  var sec = card.closest('.section'); var num = card.querySelector('.num');
  return 'vol' + _BM_VOL + '_' + (sec ? sec.id : 'x') + '_' + (num ? num.textContent.trim() : '0');
}

function _bmCardData(card) {
  var sec   = card.closest('.section');
  var secId = sec ? sec.id : 'unknown';
  var label = secId.charAt(0).toUpperCase() + secId.slice(1).replace(/-/g,' ');
  var eng   = card.querySelector('.e .speak-text')
            ? card.querySelector('.e .speak-text').textContent.trim()
            : (card.querySelector('.e') ? card.querySelector('.e').textContent.trim() : '');
  var thai  = card.querySelector('.t .speak-text')
            ? card.querySelector('.t .speak-text').textContent.trim()
            : (card.querySelector('.t') ? card.querySelector('.t').textContent.trim() : '');
  var rom   = card.querySelector('.r') ? card.querySelector('.r').textContent.trim() : '';
  return {
    id: _bmCardId(card), vol: _BM_VOL, volLabel: _BM_LABEL,
    topic: secId, topicLabel: label,
    eng: eng, thai: thai, roman: rom,
    savedAt: new Date().toISOString()
  };
}

var _bmToastTimer = null;
function _bmToast(msg) {
  var t = document.getElementById('bmToast');
  if (!t) return;
  t.textContent = msg; t.classList.add('show');
  clearTimeout(_bmToastTimer);
  _bmToastTimer = setTimeout(function() { t.classList.remove('show'); }, 2200);
}

function _bmFireParticles(btn) {
  var r = btn.getBoundingClientRect();
  var cx = r.left + r.width/2, cy = r.top + r.height/2;
  var colors = ['#b87820','#c05828','#e8b030','#d4943a','#f0c060','#a05020'];
  for (var i = 0; i < 12; i++) {
    (function(i) {
      var angle = (i/12)*Math.PI*2 + (Math.random()-0.5)*0.6;
      var dist  = 22 + Math.random()*22;
      var dx    = Math.cos(angle)*dist, dy = Math.sin(angle)*dist;
      var size  = 6 + Math.random()*7;
      var color = colors[Math.floor(Math.random()*colors.length)];
      var delay = Math.random()*60, dur = 480 + Math.random()*140;
      var p = document.createElement('span');
      p.className = 'bm-particle';
      p.style.cssText = [
        'left:'+(cx-size/2)+'px','top:'+(cy-size/2)+'px',
        'width:'+size+'px','height:'+size+'px','background:'+color,
        '--dx:'+dx.toFixed(1)+'px','--dy:'+dy.toFixed(1)+'px',
        'animation:particleFly '+dur+'ms '+delay+'ms ease-out forwards'
      ].join(';');
      document.body.appendChild(p);
      setTimeout(function() { if (p.parentNode) p.parentNode.removeChild(p); }, dur+delay+80);
    })(i);
  }
}

function _injectBookmarks() {
  var saved = _bmLoad(); var savedIds = saved.map(function(c) { return c.id; });
  document.querySelectorAll('.card').forEach(function(card) {
    if (card.querySelector('.bm-btn')) return;
    var id  = _bmCardId(card);
    var btn = document.createElement('button');
    btn.className = 'bm-btn' + (savedIds.indexOf(id) !== -1 ? ' saved' : '');
    btn.innerHTML = savedIds.indexOf(id) !== -1 ? _bmFilled : _bmOutline;
    btn.setAttribute('aria-label','Save to My Notes');
    btn.setAttribute('title','Save to My Notes');
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var arr = _bmLoad(); var ids = arr.map(function(c){return c.id;}); var isSaved = ids.indexOf(id) !== -1;
      if (isSaved) {
        arr = arr.filter(function(c){return c.id!==id;});
        btn.classList.remove('saved'); btn.innerHTML = _bmOutline;
        _bmWrite(arr); _bmToast('Removed from My Notes');
      } else {
        var data = _bmCardData(card);
        arr.push(data); btn.classList.add('saved'); btn.innerHTML = _bmFilled;
        _bmWrite(arr); _bmToast('Saved to My Notes · ' + data.topicLabel);
        btn.classList.add('popping');
        setTimeout(function(){ btn.classList.remove('popping'); }, 500);
        _bmFireParticles(btn);
      }
    });
    card.appendChild(btn);
  });
}

_injectBookmarks();
</script>"""

# ── PILL FOOTER HTML ──────────────────────────────────────────────────────────
PILL_FOOT = """  <div class="pp-foot">
    <a class="pp-lnk" href="index.html">&#8592; All Volumes</a>
    <a class="pp-lnk" href="my-saved-note.html">&#128278; My Notes</a>
  </div>"""


# ── HELPERS ───────────────────────────────────────────────────────────────────
def inject_css(html, css):
    """Inject CSS before the LAST </style> tag."""
    pos = html.rfind('</style>')
    if pos == -1:
        print("    ⚠  No </style> found — skipping CSS injection")
        return html
    return html[:pos] + css + '\n</style>' + html[pos+8:]

def fix_fonts_async(html):
    """Make Google Fonts load non-blocking so page renders immediately."""
    import re
    if 'rel="preload" as="style"' in html:
        return html  # already fixed
    pattern = re.compile(r'<link href="(https://fonts\.googleapis\.com[^"]+)" rel="stylesheet">')
    m = pattern.search(html)
    if not m:
        return html
    url = m.group(1)
    replacement = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="preload" as="style" href="' + url + '" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
        '<noscript><link href="' + url + '" rel="stylesheet"></noscript>'
    )
    return html.replace(m.group(0), replacement, 1)

def inject_pill_footer(html):
    """Add My Notes + All Volumes rows to the existing pill popover."""
    if 'pp-foot' in html:
        return html   # already done
    # The pill pop ends with </div> just before the pill button
    # Pattern: last </div> before <button class="pill-btn"
    pattern = re.compile(r'(</div>)(\s*\n\s*<button[^>]*pill-btn)', re.IGNORECASE)
    m = pattern.search(html)
    if m:
        insert_pos = m.start(1)
        html = html[:insert_pos] + '\n' + PILL_FOOT + '\n' + html[insert_pos:]
    else:
        print("    ⚠  Pill popover closing tag not found — pill footer skipped")
    return html


# ── MAIN ──────────────────────────────────────────────────────────────────────
ok, skipped, missing = [], [], []

for fname, (vol_id, vol_label) in FILES.items():
    fpath = os.path.join(SRC, fname)

    if not os.path.exists(fpath):
        missing.append(fname)
        print(f"  ✗  {fname}  (not found)")
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    if INJECTION_MARKER in html:
        skipped.append(fname)
        print(f"  ↷  {fname}  (already injected)")
        continue

    print(f"  ✦  {fname}  ({vol_label})")

    # 0 — async fonts
    html = fix_fonts_async(html)

    # 1 — CSS
    html = inject_css(html, FEATURES_CSS)

    # 2 — pill footer
    html = inject_pill_footer(html)

    # 3 — toast div + TTS + Bookmark JS  (before </body>)
    bookmark_js = BOOKMARK_JS_TPL.replace('{vol_id}', vol_id).replace('{vol_label}', vol_label)
    injection = TOAST_HTML + '\n' + TTS_JS + '\n' + bookmark_js + '\n'
    html = html.replace('</body>', injection + '</body>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

    ok.append(fname)

print()
print(f"{'='*52}")
print(f"  Done  ✅  {len(ok)} files updated")
if skipped: print(f"  Skipped  ↷  {len(skipped)} already injected")
if missing: print(f"  Missing  ✗   {len(missing)}: {', '.join(missing)}")
print(f"{'='*52}")
