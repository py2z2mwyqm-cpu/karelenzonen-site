# karelenzonen.nl, statische kopie

Kopie van de WordPress-site (Bricks-thema) die bij Cloud86 draaide op een account van de oude bouwer,
waar KAREL & Zonen geen toegang toe heeft. Gemaakt op 5-10-2026 om de site naar de eigen
Hostnet-webhosting te verhuizen. De domeinnaam staat in het Hostnet-account van Yannick.

- `spiegel.py <urls>`: haalt de pagina's onbewerkt op (`?LSCWP_CTRL=before_optm`, zonder LiteSpeed-optimalisatie) met alle bestanden, in `public/`.
- `nabewerken.py`: maakt wp-content/wp-includes relatief en zet het contactformulier om naar `/contact.php`.
- `extra/contact.php`: stuurt het formulier naar info@karelenzonen.nl, afzender website@karel.pro (SPF van karel.pro staat Hostnet toe).
- Lokaal bekijken: preview "karelenzonen-kopie" (python http.server op 8765). PHP draait lokaal niet.
