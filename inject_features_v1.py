#!/usr/bin/env python3
"""
inject_features_v1.py — inject TTS buttons, bookmark buttons, and floating
🔖 My Notes pill into all KruExchange vol HTML files.

Usage:
    cd /path/to/html/files
    python3 inject_features_v1.py

Safe to re-run — already-injected files are skipped via INJECTION_MARKER.
"""

import os
import re
import html as htmllib

INJECTION_MARKER = "/* KRU-FEATURES-v1 */"

TARGET_FILES = [
    "kru-language-exchange.html",
    "kru-exchange-vol2.html",
    "kru-exchange-vol3.html",
    "kru-exchange-vol4.html",
    "kru-exchange-vol5.html",
    "kru-exchange-vol6.html",
    "kru-exchange-vol7.html",
    "kru-exchange-vol8.html",
    "kru-exchange-vol9.html",
    "kru-exchange-vol12.html",
    "kru-exchange-vol13.html",
    "kru-exchange-vol14.html",
    "kru-exchange-vol15.html",
    "kru-exchange-vol16.html",
    "kru-exchange-vol17.html",
    "kru-exchange-vol19.html",
    "kru-exchange-vol21.html",
    "kru-exchange-vol22.html",
]

# ── CSS injected before </style> ──────────────────────────────────────────────

INJECT_CSS = """
/* KRU-FEATURES-v1 */

/* ── TTS BUTTONS ── */
.tts-btn {
  background: none;
  border: 1px solid rgba(42,92,138,0.3);
  border-radius: 99px;
  padding: 0.13rem 0.55rem;
  font-size: 0.62rem;
  cursor: pointer;
  color: rgba(42,92,138,0.65);
  transition: all 0.15s;
  margin-left: 0.45rem;
  vertical-align: middle;
  white-space: nowrap;
  line-height: 1.6;
}
.tts-btn.thai {
  border-color: rgba(138,32,64,0.3);
  color: rgba(138,32,64,0.65);
}
.tts-btn:hover { opacity: 0.85; transform: scale(1.05); }
.tts-btn.speaking { opacity: 0.5; }

/* ── BOOKMARK BUTTON ── */
.card { position: relative !important; }
.bookmark-btn {
  position: absolute;
  bottom: 0.6rem; right: 0.7rem;
  background: none;
  border: 1px solid rgba(184,120,32,0.3);
  border-radius: 99px;
  padding: 0.18rem 0.6rem;
  font-size: 0.68rem;
  cursor: pointer;
  color: rgba(184,120,32,0.5);
  transition: all 0.2s;
  z-index: 10;
}
.bookmark-btn:hover { color: #c8943a; border-color: rgba(184,120,32,0.6); }
.bookmark-btn.saved { color: #c8943a; border-color: #c8943a; }

/* ── FLOATING NOTES PILL ── */
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
"""

# ── HTML + JS injected before </body> ─────────────────────────────────────────

INJECT_BEFORE_BODY = """
<!-- KRU-FEATURES-v1 -->
<a class="notes-pill" href="my-saved-note.html">\U0001f516 My Notes</a>

<script>
(function() {
  /* ── TTS ── */
  function ttsSpeak(text, lang) {
    if (!window.speechSynthesis) return;
    speechSynthesis.cancel();
    setTimeout(function() {
      if (speechSynthesis.paused) speechSynthesis.resume();
      var u = new SpeechSynthesisUtterance(text);
      u.lang  = lang;
      u.rate  = 0.9;
      speechSynthesis.speak(u);
    }, 50);
  }

  document.querySelectorAll('.tts-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var me = this;
      me.classList.add('speaking');
      ttsSpeak(me.dataset.text, me.dataset.lang);
      setTimeout(function() { me.classList.remove('speaking'); }, 2500);
    });
  });

  /* ── BOOKMARK ── */
  function getCards() {
    try { return JSON.parse(localStorage.getItem('kruexchange_saved_cards') || '[]'); }
    catch (e) { return []; }
  }
  function saveCards(arr) {
    localStorage.setItem('kruexchange_saved_cards', JSON.stringify(arr));
  }

  function fireworks(btn) {
    var rect = btn.getBoundingClientRect();
    var cx = rect.left + rect.width / 2;
    var cy = rect.top  + rect.height / 2;
    for (var i = 0; i < 8; i++) {
      (function(i) {
        var spark = document.createElement('span');
        spark.textContent = '\u2726';
        spark.style.cssText =
          'position:fixed;left:' + cx + 'px;top:' + cy + 'px;pointer-events:none;' +
          'color:#c8943a;font-size:0.9rem;z-index:9999;' +
          'transition:all 0.6s ease-out;opacity:1;';
        document.body.appendChild(spark);
        var angle = (i / 8) * 2 * Math.PI;
        var dist  = 40 + Math.random() * 20;
        var dx    = Math.cos(angle) * dist;
        var dy    = Math.sin(angle) * dist;
        requestAnimationFrame(function() {
          spark.style.transform = 'translate(' + dx + 'px,' + dy + 'px)';
          spark.style.opacity   = '0';
          setTimeout(function() { spark.remove(); }, 650);
        });
      })(i);
    }
  }

  document.querySelectorAll('.bookmark-btn').forEach(function(btn) {
    var id    = btn.dataset.id;
    var saved = getCards();
    if (saved.some(function(c) { return c.id === id; })) {
      btn.classList.add('saved');
      btn.textContent = '\u2605 Saved';
    }
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var cards = getCards();
      var idx   = cards.findIndex(function(c) { return c.id === id; });
      if (idx >= 0) {
        cards.splice(idx, 1);
        btn.classList.remove('saved');
        btn.textContent = '\u2606 Save';
      } else {
        var card = btn.closest('.card');
        function txt(a, b) {
          var el = card.querySelector(a) || card.querySelector(b);
          return el ? el.textContent.trim() : '';
        }
        cards.push({
          id:    id,
          eng:   txt('.e',  '.eng'),
          thai:  txt('.t',  '.thai-script'),
          roman: txt('.r',  '.roman'),
          vol:   document.title,
          saved: Date.now()
        });
        btn.classList.add('saved');
        btn.textContent = '\u2605 Saved';
        fireworks(btn);
      }
      saveCards(cards);
    });
  });
})();
</script>
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def attr_escape(text):
    """Escape text for use in a double-quoted HTML attribute."""
    return htmllib.escape(text.strip(), quote=True)


def inject_tts(html):
    """Add TTS buttons after text content in .e/.eng and .t/.thai-script divs."""

    def en_sub(m):
        cls, text = m.group(1), m.group(2)
        btn = ' <button class="tts-btn" data-text="{}" data-lang="en-US">\U0001f50a EN</button>'.format(
            attr_escape(text))
        return '<div class="{}">{}{}</div>'.format(cls, text, btn)

    def th_sub(m):
        cls, text = m.group(1), m.group(2)
        btn = ' <button class="tts-btn thai" data-text="{}" data-lang="th-TH">\U0001f50a TH</button>'.format(
            attr_escape(text))
        return '<div class="{}">{}{}</div>'.format(cls, text, btn)

    # Single-line divs only (.*? does not cross newlines by default)
    html = re.sub(r'<div class="(e|eng)">(.*?)</div>',   en_sub, html)
    html = re.sub(r'<div class="(t|thai-script)">(.*?)</div>', th_sub, html)
    return html


def inject_bookmarks(html, vol_slug):
    """
    Insert a bookmark button before the closing </div> of every .card div.
    Uses a depth-counter to find the correct closing tag even with nested divs.
    """
    out = []
    card_count = 0
    i = 0
    n = len(html)

    while i < n:
        card_pos = html.find('<div class="card"', i)
        if card_pos == -1:
            out.append(html[i:])
            break

        # Append everything before this card
        out.append(html[i:card_pos])

        # Walk forward counting <div depth to find the matching </div>
        depth = 0
        j = card_pos
        found_close = -1
        while j < n:
            next_open  = html.find('<div', j)
            next_close = html.find('</div>', j)

            if next_open == -1 and next_close == -1:
                break

            use_open = (next_open != -1) and (next_close == -1 or next_open < next_close)
            if use_open:
                depth += 1
                j = next_open + 4        # skip past '<div'
            else:
                depth -= 1
                if depth == 0:
                    found_close = next_close
                    break
                j = next_close + 6       # skip past '</div>'

        if found_close == -1:
            # Couldn't find closing tag — append rest as-is
            out.append(html[card_pos:])
            break

        card_count += 1
        uid = '{}-card{:03d}'.format(vol_slug, card_count)
        card_body = html[card_pos:found_close]
        btn = '\n      <button class="bookmark-btn" data-id="{}">\u2606 Save</button>'.format(uid)
        out.append(card_body)
        out.append(btn)
        out.append('\n    </div>')
        i = found_close + len('</div>')

    return ''.join(out)


def make_font_async(html):
    """
    Convert blocking Google Fonts <link> to async (print-swap trick).
    Skips links that are already async.
    """
    def replace_link(m):
        url = m.group(1)
        return (
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="{}" rel="stylesheet" media="print" onload="this.media=\'all\'">'.format(url)
        )

    return re.sub(
        r'<link href="(https://fonts\.googleapis\.com/[^"]+)" rel="stylesheet">',
        replace_link,
        html
    )


# ── Main ─────────────────────────────────────────────────────────────────────

def process_file(filepath):
    vol_slug = os.path.basename(filepath).replace('.html', '').replace('-', '_')

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    if INJECTION_MARKER in html:
        print('  SKIP (already injected): {}'.format(os.path.basename(filepath)))
        return False

    # 1. Async font loading
    html = make_font_async(html)

    # 2. Inject CSS before the first </style>
    if '</style>' in html:
        html = html.replace('</style>', INJECT_CSS + '\n</style>', 1)
    else:
        print('  WARN: no </style> found in {}'.format(os.path.basename(filepath)))

    # 3. TTS buttons on .e/.eng and .t/.thai-script lines
    html = inject_tts(html)

    # 4. Bookmark button on every .card
    html = inject_bookmarks(html, vol_slug)

    # 5. Notes pill + JS before </body>
    if '</body>' in html:
        html = html.replace('</body>', INJECT_BEFORE_BODY + '\n</body>', 1)
    else:
        print('  WARN: no </body> found in {}'.format(os.path.basename(filepath)))

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print('  OK: {}'.format(os.path.basename(filepath)))
    return True


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print('KruExchange Feature Injector v1')
    print('Working dir: {}'.format(script_dir))
    print()

    injected = 0
    skipped  = 0
    missing  = 0

    for fname in TARGET_FILES:
        fpath = os.path.join(script_dir, fname)
        if not os.path.exists(fpath):
            print('  MISSING: {}'.format(fname))
            missing += 1
            continue
        try:
            changed = process_file(fpath)
            if changed:
                injected += 1
            else:
                skipped += 1
        except Exception as exc:
            print('  ERROR in {}: {}'.format(fname, exc))

    print()
    print('Done — injected: {}  skipped: {}  missing: {}'.format(injected, skipped, missing))


if __name__ == '__main__':
    main()
