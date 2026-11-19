# Muscat Music & Art Academy website

Static, bilingual Arabic and English institutional website. Source is generated
with `python3 build.py` into `dist/`; the hosting manifest points to `dist`.

## Pages

- Home, about/founder, programmes, admissions, news, contact, and privacy
- Matching English pages under `dist/en/`
- Sitemap, robots file, and a custom 404 page

## Enquiries

The admissions form prepares a WhatsApp message in the visitor's browser. It
does not persist or transmit the form to the Site. The visitor decides whether
to send the message in WhatsApp. If the academy later wants an internal
registration system, it needs a protected server-backed form and an
administrative workflow.

## Editorial updates

Edit the Arabic and English content in `build.py`, then run `python3 build.py`.
Dates, credentials, and partnerships are linked to their original sources.
Programme availability, fees, timetable, and the exact address require the
academy to supply current approved details before they are listed.

The founder portrait is an unaltered, close crop of the academy-supplied photo
using CSS positioning, so her facial features remain identical to the original.
The original photo is at `dist/assets/founder-original.jpg`; it contains the
other person outside the visible crop. Other learning-space images are illustrative and
labelled as such. Replace them with academy-owned photography when available.
The emblem currently available from the user's files is a raster derivative;
replace it with the approved master logo before public launch if the master
differs.

## Home screen icon

`manifest.webmanifest`, 192/512 px app icons, an Apple touch icon, and a favicon
all use the current academy emblem. Visitors can add the site to their home
screen; this is a website shortcut, not a native App Store application.

## GitHub Pages

GitHub Pages is set to deploy the `main` branch from the repository root.
Run `python3 pages_prepare.py` after editing content: it regenerates `dist/`
for the private review Site and the root pages for the current temporary URL,
`https://byyassmin.com/Muscat-Music-Art-Academy/`. Commit both outputs.
When the academy domain is assigned, set `GH_PAGES_BASE` to its exact HTTPS
URL and update `BASE` in `build.py`, then rebuild and update the Pages domain
setting. `dist/` continues to be the static output for the private Site.

