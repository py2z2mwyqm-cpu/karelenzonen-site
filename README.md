# karelenzonen.nl, statische kopie

Kopie van de WordPress-site (Bricks-thema) die bij Cloud86 draaide op een account van de oude bouwer,
waar KAREL & Zonen geen toegang toe heeft. Gemaakt op 5-10-2026. Sinds 6-10-2026 staat de site op GitHub Pages (map `docs/`, domein via `docs/CNAME`)
en draait alleen het contactformulier op Railway (dienst karelenzonen-formulier, project alluring-amazement). De domeinnaam staat in het Hostnet-account van Yannick.

- `spiegel.py <urls>`: haalt de pagina's onbewerkt op (`?LSCWP_CTRL=before_optm`, zonder LiteSpeed-optimalisatie) met alle bestanden, in `docs/`.
- `nabewerken.py`: maakt wp-content/wp-includes relatief en zet het contactformulier om naar de formulierdienst, en schrijft CNAME en .nojekyll.
- `formulier/`: kleine Node-dienst op Railway die het contactformulier via Resend (zelfde sleutel als Mensje) naar info@karelenzonen.nl stuurt. Uitrollen: `cd formulier && railway up --service karelenzonen-formulier --environment production`.
- Lokaal bekijken: preview "karelenzonen-kopie" (python http.server op 8765, map docs).
