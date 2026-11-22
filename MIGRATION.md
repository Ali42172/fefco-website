# Moving fefco.ae from WordPress to the new site

The new site is plain static HTML in `dist/` (56 pages, English + Arabic). It runs on any static host.
Recommended: **Cloudflare Pages** or **Vercel** (free tier, global CDN, free SSL). Netlify also works (`_redirects` is included).

## 1. Copy the images off WordPress (before anything else)
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
