<?php
// Contactformulier van karelenzonen.nl (statische kopie op Hostnet, sinds de verhuizing van Cloud86).
// Stuurt het bericht naar info@karelenzonen.nl. Afzender is website@karel.pro, omdat de SPF van
// karel.pro de Hostnet-servers toelaat en die van karelenzonen.nl alleen Outlook.

const ONTVANGER = 'info@karelenzonen.nl';
const AFZENDER = 'website@karel.pro';

function terug(string $status): void {
    $pad = '/';
    if (!empty($_SERVER['HTTP_REFERER'])) {
        $ref = parse_url($_SERVER['HTTP_REFERER']);
        $host = $ref['host'] ?? '';
        if (in_array($host, ['karelenzonen.nl', 'www.karelenzonen.nl'], true) && !empty($ref['path'])) {
            $pad = $ref['path'];
        }
    }
    header('Location: ' . $pad . '?verzonden=' . $status . '#contact', true, 303);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    terug('0');
}

// Spamval: dit veld is onzichtbaar voor mensen.
if (!empty($_POST['website'])) {
    terug('1');
}

$schoon = fn(string $v): string => trim(str_replace(["\r", "\n"], ' ', $v));
$naam = $schoon($_POST['form-field-a73465'] ?? '');
$email = trim($_POST['form-field-f91ea8'] ?? '');
$telefoon = $schoon($_POST['form-field-mrskrv'] ?? '');
$vraag = trim($_POST['form-field-ffdfba'] ?? '');

if ($naam === '' || $vraag === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)
    || mb_strlen($naam) > 200 || mb_strlen($vraag) > 5000) {
    terug('0');
}

$onderwerp = '=?UTF-8?B?' . base64_encode('Contactformulier karelenzonen.nl: ' . $naam) . '?=';
$tekst = "Nieuw bericht via het contactformulier op karelenzonen.nl\n\n"
    . "Naam: $naam\nE-mail: $email\nTelefoon: " . ($telefoon !== '' ? $telefoon : '(niet ingevuld)') . "\n"
    . "Pagina: " . ($_SERVER['HTTP_REFERER'] ?? 'onbekend') . "\n\n"
    . "Vraag of opmerking:\n$vraag\n";
$kop = "From: KAREL & Zonen website <" . AFZENDER . ">\r\n"
    . "Reply-To: $email\r\n"
    . "MIME-Version: 1.0\r\n"
    . "Content-Type: text/plain; charset=UTF-8\r\n";

$gelukt = mail(ONTVANGER, $onderwerp, $tekst, $kop, '-f' . AFZENDER);
terug($gelukt ? '1' : '0');
