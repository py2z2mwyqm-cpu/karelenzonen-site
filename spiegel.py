#!/usr/bin/env python3
"""Maakt een statische kopie van karelenzonen.nl met dezelfde paden (voor verhuizing van Cloud86 naar Hostnet)."""
import re, os, sys, urllib.request, urllib.parse, html
BASIS = "https://karelenzonen.nl"
DOEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
UA = {"User-Agent": "Mozilla/5.0 (KAREL-spiegel)"}
gedaan, wachtrij, fouten = set(), [], []

def haal(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.headers.get("Content-Type", "")

def pad_voor(url, ctype=""):
    p = urllib.parse.urlparse(url).path or "/"
    p = urllib.parse.unquote(p)
    if p.endswith("/"):
        p += "index.html"
    elif "text/html" in ctype and not os.path.splitext(p)[1]:
        p += "/index.html"
    return os.path.join(DOEL, p.lstrip("/"))

def eigen(url):
    u = urllib.parse.urlparse(url)
    return u.netloc in ("karelenzonen.nl", "www.karelenzonen.nl", "")

def normaliseer(ref, van):
    ref = html.unescape(ref.strip())
    if ref.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
        return None
    absu = urllib.parse.urljoin(van, ref)
    absu = absu.split("#")[0]
    u = urllib.parse.urlparse(absu)
    if not eigen(absu) or u.scheme not in ("http", "https"):
        return None
    if u.path.startswith(("/wp-admin", "/wp-login", "/xmlrpc", "/wp-json", "/feed", "/comments/feed")) or "/feed" in u.path:
        return None
    if u.query and not os.path.splitext(u.path)[1]:
        return None  # ?p=123-shortlinks en zoekopdrachten: dat zijn duplicaten van echte pagina's
    return BASIS + u.path

def verwerk(url):
    if url in gedaan:
        return
    gedaan.add(url)
    try:
        ophaal = url
        if not os.path.splitext(urllib.parse.urlparse(url).path)[1]:
            ophaal = url + "?LSCWP_CTRL=before_optm"  # onbewerkte pagina, zonder LiteSpeed-optimalisatie
        data, ctype = haal(ophaal)
    except Exception as e:
        fouten.append(f"{url}: {e}"); return
    if "?" in url:  # query-varianten (bv. ?ver=) bewaren we onder het kale pad
        url = url.split("?")[0]
    doel = pad_voor(url, ctype)
    os.makedirs(os.path.dirname(doel), exist_ok=True)
    with open(doel, "wb") as f:
        f.write(data)
    if "text/html" in ctype:
        tekst = data.decode("utf-8", "replace")
        refs = re.findall(r'(?:href|src|data-src|data-bg|poster)=["\']([^"\']+)["\']', tekst)
        for ss in re.findall(r'(?:srcset|data-srcset)=["\']([^"\']+)["\']', tekst):
            refs += [d.strip().split(" ")[0] for d in ss.split(",") if d.strip()]
        refs += re.findall(r'url\(\s*["\']?([^"\')]+)', tekst)
        for r in refs:
            n = normaliseer(r, url)
            if n: wachtrij.append(n)
    elif "css" in ctype or url.endswith(".css"):
        tekst = data.decode("utf-8", "replace")
        for r in re.findall(r'url\(\s*["\']?([^"\')]+)', tekst) + re.findall(r'@import\s+["\']([^"\']+)', tekst):
            n = normaliseer(r, url)
            if n: wachtrij.append(n)

startpunten = sys.argv[1:]
wachtrij.extend(startpunten)
while wachtrij:
    verwerk(wachtrij.pop(0))
print(f"opgehaald: {len(gedaan)}, fouten: {len(fouten)}")
for f in fouten: print("FOUT", f)
