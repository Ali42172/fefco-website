# Moving fefco.ae from WordPress to the new site

The new site is plain static HTML in `dist/` (56 pages, English + Arabic). It runs on any static host.
Recommended: **Cloudflare Pages** or **Vercel** (free tier, global CDN, free SSL). Netlify also works (`_redirects` is included).

## 0. Chosen setup: GitHub Pages
The repo includes `.github/workflows/deploy.yml`. On every push it builds the site, copies all photos listed in `media.txt` from the WordPress media library into `assets/media/`, shrinks them, and publishes to GitHub Pages. Preview URL: `https://<github-user>.github.io/<repo>/`.

DNS records for the boss (at the DNS panel for fefco.ae — do NOT change nameservers, do NOT touch MX/TXT email records):

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | <github-user>.github.io |

Remove only the old A record(s) for @ and the old www record. Then add `static/CNAME` containing `fefco.ae`, push, and tick 'Enforce HTTPS' in the repo's Pages settings.

## 1. Copy the images off WordPress (manual alternative)
Pages currently load photos from `https://fefco.ae/wp-content/uploads/...`. Those URLs disappear when DNS moves.
1. Download the WordPress media library (WP admin → Tools → Export → Media, or FTP `wp-content/uploads/`).
2. Put the folders (`2023/`, `2024/`, `2025/`, `2026/`) into `static/assets/media/`.
3. In `data_common.py` set `MEDIA_BASE = "/assets/media/"`, then run `python3 build.py`.
4. Optional: convert to WebP at 1600 px max for speed.

## 2. Deploy
- Vercel: new project → upload `dist/` (or connect a GitHub repo containing it). `vercel.json` sets redirects and caching.
- Cloudflare Pages: Create project → Direct upload → `dist/`. `_redirects` is read automatically.

## 3. Point the domain (only after checking the preview URL)
1. Add `fefco.ae` and `www.fefco.ae` as custom domains in the host.
2. At the DNS provider for fefco.ae, change the A / CNAME records to the values the host shows.
3. **Keep the MX records unchanged** so email (info@fefco.ae, solar@fefco.ae) keeps working.
4. Keep the old WordPress hosting running for 30 days as a backup (e.g. at old.fefco.ae).

## 4. After go-live
- Search Console: add the property, submit `https://fefco.ae/sitemap.xml`.
- Check a few old URLs redirect (e.g. `/solar-pv-systems/` → `/solar-panel-installation-dubai/`).
- See SEO-PLAN.md for the follow-up list.

## Editing content
All text lives in `data_*.py` (English and Arabic side by side). Edit, run `python3 build.py`, redeploy `dist/`.
