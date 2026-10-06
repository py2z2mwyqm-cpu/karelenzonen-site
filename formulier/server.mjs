// Contactformulier van karelenzonen.nl. De site zelf staat statisch op GitHub Pages; dit is het
// enige stukje dat op een server moet draaien. Verstuurt via Resend vanaf karelenzonen.nl (zelfde
// koppeling als Mensje) naar info@karelenzonen.nl en stuurt de bezoeker terug naar de pagina.
import http from 'node:http';

const PORT = process.env.PORT || 8080;
const SITE = 'https://karelenzonen.nl';
const TOEGESTAAN = ['karelenzonen.nl', 'www.karelenzonen.nl'];
const MAIL_FROM = process.env.MAIL_FROM || 'KAREL & Zonen website <website@karelenzonen.nl>';
const MAIL_TO = process.env.MAIL_TO || 'info@karelenzonen.nl';
const RESEND_API_KEY = process.env.RESEND_API_KEY;

const VELDEN = {
  naam: 'form-field-a73465',
  email: 'form-field-f91ea8',
  telefoon: 'form-field-mrskrv',
  vraag: 'form-field-ffdfba',
};

function terugPad(req) {
  try {
    const ref = new URL(req.headers.referer || '');
    if (TOEGESTAAN.includes(ref.hostname)) return ref.pathname || '/';
  } catch {}
  return '/';
}

function terug(res, req, status) {
  res.writeHead(303, { Location: `${SITE}${terugPad(req)}?verzonden=${status}#contact` });
  res.end();
}

function leesBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (c) => {
      data += c;
      if (data.length > 20000) { reject(new Error('te groot')); req.destroy(); }
    });
    req.on('end', () => resolve(new URLSearchParams(data)));
    req.on('error', reject);
  });
}

const enkeleRegel = (v) => (v || '').replace(/[\r\n]+/g, ' ').trim();

http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  if (req.method === 'GET' && url.pathname === '/gezond') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    return res.end(RESEND_API_KEY ? 'ok' : 'geen RESEND_API_KEY');
  }
  if (req.method !== 'POST' || url.pathname !== '/contact') {
    res.writeHead(302, { Location: SITE });
    return res.end();
  }
  let form;
  try { form = await leesBody(req); } catch { return terug(res, req, '0'); }

  if (form.get('website')) return terug(res, req, '1'); // spamval, onzichtbaar voor mensen

  const naam = enkeleRegel(form.get(VELDEN.naam));
  const email = enkeleRegel(form.get(VELDEN.email));
  const telefoon = enkeleRegel(form.get(VELDEN.telefoon));
  const vraag = (form.get(VELDEN.vraag) || '').trim();
  const geldigeMail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  if (!naam || !vraag || !geldigeMail || naam.length > 200 || vraag.length > 5000 || !RESEND_API_KEY) {
    return terug(res, req, '0');
  }

  const tekst = [
    'Nieuw bericht via het contactformulier op karelenzonen.nl',
    '',
    `Naam: ${naam}`,
    `E-mail: ${email}`,
    `Telefoon: ${telefoon || '(niet ingevuld)'}`,
    `Pagina: ${SITE}${terugPad(req)}`,
    '',
    'Vraag of opmerking:',
    vraag,
  ].join('\n');

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: MAIL_FROM,
        to: [MAIL_TO],
        reply_to: email,
        subject: `Contactformulier karelenzonen.nl: ${naam}`,
        text: tekst,
      }),
    });
    if (!r.ok) console.error('Resend weigerde', r.status, await r.text());
    return terug(res, req, r.ok ? '1' : '0');
  } catch (e) {
    console.error('Versturen mislukt', e);
    return terug(res, req, '0');
  }
}).listen(PORT, () => console.log(`contactformulier luistert op ${PORT}`));
