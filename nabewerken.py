#!/usr/bin/env python3
"""Na spiegel.py: maakt verwijzingen naar wp-content/wp-includes relatief, zodat de kopie op elke host draait."""
import glob, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))
n = 0
for f in glob.glob('**/*', recursive=True):
    if not f.endswith(('.html', '.css', '.js')):
        continue
    s = open(f, encoding='utf-8', errors='surrogateescape').read(); o = s
    for host in ('https://karelenzonen.nl', 'https://www.karelenzonen.nl', '//karelenzonen.nl', '//www.karelenzonen.nl'):
        for d in ('wp-content', 'wp-includes'):
            s = s.replace(host + '/' + d + '/', '/' + d + '/')
            s = s.replace(host.replace('/', '\\/') + '\\/' + d + '\\/', '\\/' + d + '\\/')
    if s != o:
        open(f, 'w', encoding='utf-8', errors='surrogateescape').write(s); n += 1
print('aangepast', n)

# Contactformulier: versturen naar /contact.php in plaats van WordPress (admin-ajax bestaat niet meer).
import shutil
FORMSCRIPT = """<script id="kz-contactformulier">
(function () {
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f.classList || !f.classList.contains('brxe-form')) return;
    e.stopImmediatePropagation();
    f.setAttribute('action', '/contact.php');
    f.setAttribute('method', 'post');
  }, true);
  document.addEventListener('DOMContentLoaded', function () {
    var f = document.querySelector('form.brxe-form');
    if (!f) return;
    f.setAttribute('action', '/contact.php');
    var h = document.createElement('input');
    h.type = 'text'; h.name = 'website'; h.tabIndex = -1; h.autocomplete = 'off';
    h.setAttribute('aria-hidden', 'true');
    h.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;opacity:0';
    f.appendChild(h);
    var s = new URLSearchParams(location.search).get('verzonden');
    if (s === null) return;
    var p = document.createElement('p');
    p.setAttribute('role', 'status');
    p.textContent = s === '1'
      ? 'Bedankt, uw bericht is verstuurd. We nemen zo snel mogelijk contact met u op.'
      : 'Versturen is niet gelukt. Mail ons op info@karelenzonen.nl of bel ons, dan helpen we u direct.';
    p.style.cssText = 'margin:0 0 16px;padding:12px 16px;border-radius:8px;line-height:1.5;color:#1f2a24;background:' + (s === '1' ? '#e6f2ea' : '#fbe9e9');
    f.parentNode.insertBefore(p, f);
    setTimeout(function () { p.scrollIntoView({ block: 'center' }); }, 400);
  });
})();
</script>"""
m = 0
for f in glob.glob('**/*.html', recursive=True):
    s = open(f, encoding='utf-8', errors='surrogateescape').read()
    if 'brxe-form' in s and 'kz-contactformulier' not in s:
        s = s.replace('</body>', FORMSCRIPT + '\n</body>', 1)
        open(f, 'w', encoding='utf-8', errors='surrogateescape').write(s); m += 1
shutil.copy(os.path.join('..', 'extra', 'contact.php'), 'contact.php')
print('formulier omgezet op', m, 'pagina\'s')
