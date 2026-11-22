# -*- coding: utf-8 -*-
"""Static site generator for fefco.ae (English at /, Arabic at /ar/)."""
import json, os, shutil, html, datetime
from data_common import *
from data_solar import SOLAR
from data_water import WATER
from data_mep import MEP
from data_products import PRODUCT_GROUPS

OUT = os.path.join(os.path.dirname(__file__), "dist")
BASE_PATH = os.environ.get("BASE_PATH", "").rstrip("/")
import data_common
if os.environ.get("MEDIA_BASE"): data_common.MEDIA_BASE = os.environ["MEDIA_BASE"]
MEDIA_USED = set()
GEN = {"villa": "2026/11/image.png", "carport": "2026/11/image-1.png", "cleaning": "2026/11/image-2.png", "audit": "2026/11/image-3.png", "water": "2026/11/image-4.png", "ac": "2026/11/image-5.png"}
BIG_PNG = set(GEN.values())
TODAY = datetime.date.today().isoformat()
SERVICES = SOLAR + WATER + MEP
BY_SLUG = {s["slug"]: s for s in SERVICES}
LEADER_NAME = {"en": "Mustafa Asgar Ali", "ar": "مصطفى أصغر علي"}
E = html.escape

def img(p):
    if p.startswith("http") or p.startswith("/"): return p
    MEDIA_USED.add(p)
    # large PNGs (ChatGPT renders) are converted to JPEG by the deploy workflow
    if p in BIG_PNG and not data_common.MEDIA_BASE.startswith("http"): p = p[:-4] + ".jpg"
    return data_common.MEDIA_BASE + p
def url(lang, path=""):
    path = path.strip("/")
    base = "/ar/" if lang == "ar" else "/"
    return base + (path + "/" if path else "")
def absu(lang, path=""): return DOMAIN + url(lang, path)

# ---------- icons ----------
I = {
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.4-1.5-.9-.8-1.5-1.8-1.6-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.7 17.8L0 24l6.3-1.7A11.8 11.8 0 0 0 24 12c0-3.2-1.2-6.1-3.6-8.4z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 "arr": '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10" stroke-width="1.6"/><path d="m8 12 3 3 5-6"/></svg>',
 "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.7s7 7.3 7 12.3a7 7 0 0 1-14 0c0-5 7-12.3 7-12.3z"/></svg>',
 "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0 5 5L22 14l-8 8-2.3-2.3a4 4 0 0 0-5-5L2 10l8-8z" transform="scale(.9) translate(1.3 1.3)"/></svg>',
 "chip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>',
 "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8V6.5c0-.8.2-1.3 1.4-1.3H17V2.2C16.7 2.1 15.7 2 14.6 2 12.2 2 10.6 3.4 10.6 6v2H8v3.3h2.6V22H14V11.3h2.7l.4-3.3z"/></svg>',
 "th": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M17 11.5c-.5-3-2.5-4.5-5-4.5-3 0-5 2.2-5 5.2 0 3.6 2.4 5.8 5.3 5.8 2.6 0 4.6-1.5 4.6-3.8 0-2.4-2.4-3.2-4.5-3.2-1.8 0-3 .8-3 2s1 1.8 2.3 1.8c2.3 0 3.3-2 3.3-4.8"/><path d="M12 21.5c5.2 0 9-3.5 9-9.5s-3.8-9.5-9-9.5S3 6 3 12s3.8 9.5 9 9.5z"/></svg>',
 "x_": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.8 3h3.1l-6.8 7.7 8 10.3h-6.2l-4.9-6.3L5.4 21H2.3l7.2-8.3L1.8 3h6.4l4.4 5.8zm-1.1 16.2h1.7L7.4 4.7H5.6z"/></svg>',
 "tt": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-1.8-2.5V9.7a5.7 5.7 0 1 0 4.9 5.6V9a7.4 7.4 0 0 0 4.3 1.4V7.3a4.3 4.3 0 0 1-3.2-1.5z"/></svg>',
 "yt": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.7 15V9l5.8 3z"/></svg>',
}
I["x"] = I["x"]
SOC_ICON = {"ig": I["ig"], "fb": I["fb"], "th": I["th"], "wa": I["wa"], "x": I["x_"], "tt": I["tt"], "yt": I["yt"]}
CAT_ICON = {"solar": I["sun"], "water": I["drop"], "mep": I["wrench"], "smart": I["chip"]}
BEN_ICONS = [I["bolt"], I["shield"], I["sun"], I["check"], I["wrench"], I["chip"]]

def wa_link(text=""):
    return "https://wa.me/%s%s" % (COMPANY["whatsapp"], ("?text=" + __import__("urllib.parse").parse.quote(text)) if text else "")

# ---------- layout ----------
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Heebo:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap">'

def org_schema():
    return {
      "@context": "https://schema.org",
      "@graph": [
        {"@type": ["Organization", "LocalBusiness", "HomeAndConstructionBusiness"], "@id": DOMAIN + "/#org",
         "name": COMPANY["brand"], "legalName": COMPANY["legal"], "alternateName": ["FEFCO", "فيفكو", "FEFCO Electromechanical Services", "fefco.ae"],
         "url": DOMAIN + "/", "logo": DOMAIN + "/assets/fefco-solutions-logo.png", "image": img("2023/09/solar12-scaled.jpg"),
         "description": "FEFCO Solutions (FEFCO Electromechanical Services LLC) is a Dubai-based solar energy, water and electromechanical (MEP) contractor: rooftop solar PV, solar water heaters and repair, battery storage, EV chargers, water filtration, GRP tanks, plumbing, AMC maintenance and energy audits across the UAE.",
         "telephone": COMPANY["phone_main"], "email": COMPANY["email"],
         "address": {"@type": "PostalAddress", "streetAddress": "Deira Tower, 2307 Baniyas Road, Al Rigga", "addressLocality": "Deira, Dubai", "addressRegion": "Dubai", "addressCountry": "AE"},
         "geo": {"@type": "GeoCoordinates", "latitude": COMPANY["geo"][0], "longitude": COMPANY["geo"][1]}, "hasMap": COMPANY["maps"],
         "founder": {"@type": "Person", "name": "Mustafa Asgar Ali", "alternateName": "Mustafa Fefco", "jobTitle": "Founder"},
         "areaServed": [{"@type": "Country", "name": "United Arab Emirates"}, "Dubai", "Sharjah", "Abu Dhabi", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"],
         "sameAs": [s[1] for s in SOCIAL if s[2] != "wa"],
         "subOrganization": {"@type": "Organization", "name": "FEFCO AI Solutions", "url": AI_SITE, "sameAs": [s[1] for s in SOCIAL_AI]},
         "brand": [{"@type": "Brand", "name": b} for b in ["Lamborghini Calorclima", "Ariston", "Go Green", "SuitX", "EIRA"]],
         "knowsAbout": ["Solar PV installation", "Shams Dubai net metering", "Solar water heaters", "Solar water heater repair", "Battery energy storage", "EV charger installation", "Water filtration", "GRP water tanks", "Plumbing", "MEP maintenance", "Annual maintenance contracts", "Energy audits"],
         "contactPoint": [{"@type": "ContactPoint", "telephone": COMPANY["phone_main"], "contactType": "sales", "availableLanguage": ["English", "Arabic", "Hindi", "Urdu"], "areaServed": "AE"},
                          {"@type": "ContactPoint", "telephone": COMPANY["phone_main"], "contactType": "emergency", "hoursAvailable": "Mo-Su 00:00-23:59"}]},
        {"@type": "WebSite", "@id": DOMAIN + "/#web", "url": DOMAIN + "/", "name": "FEFCO Solutions", "inLanguage": ["en", "ar"], "publisher": {"@id": DOMAIN + "/#org"}}
      ]}

def head(lang, title, desc, path, image=None, extra_ld=None):
    alt = "ar" if lang == "en" else "en"
    ld = [org_schema()] + (extra_ld or [])
    return f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang=='ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{absu(lang, path)}">
<link rel="alternate" hreflang="en" href="{absu('en', path)}">
<link rel="alternate" hreflang="ar" href="{absu('ar', path)}">
<link rel="alternate" hreflang="x-default" href="{absu('en', path)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:site_name" content="FEFCO Solutions">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{absu(lang, path)}"><meta property="og:image" content="{E(img(image or '2023/09/solar12-scaled.jpg'))}">
<meta property="og:locale" content="{'ar_AE' if lang=='ar' else 'en_AE'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2A429E">
<link rel="icon" href="/assets/favicon.png">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
{''.join('<script type="application/ld+json">'+json.dumps(x, ensure_ascii=False)+'</script>' for x in ld)}
</head>
<body>
<a class="skip" href="#main">{UI[lang]['skip']}</a>
'''

def mega(lang):
    cols = ""
    for c in ["solar", "water", "mep", "smart"]:
        links = "".join(f'<a href="{url(lang, s["slug"])}">{E(s[lang]["nav"])}</a>' for s in SERVICES if s["cat"] == c)
        cols += f'<div><h4>{CATEGORIES[c][lang]}</h4>{links}</div>'
    u = UI[lang]
    return cols + f'<div class="all"><span class="muted">{u["emergency"]}: <a href="tel:{COMPANY["phone_main"]}" dir="ltr">{COMPANY["phone_main_disp"]}</a></span><a href="{url(lang, "services")}">{u["all_services"]}</a></div>'

def header(lang, path, current=""):
    u = UI[lang]; alt = "ar" if lang == "en" else "en"
    nav = f'''<div class="dd"><button type="button" aria-expanded="false" aria-haspopup="true">{u['services']} {I['chev']}</button><div class="mega">{mega(lang)}</div></div>
<a href="{url(lang,'products')}"{' aria-current="page"' if current=='products' else ''}>{u['products']}</a>
<a href="{url(lang,'projects')}"{' aria-current="page"' if current=='projects' else ''}>{u['projects']}</a>
<a href="{url(lang,'about')}"{' aria-current="page"' if current=='about' else ''}>{u['about']}</a>
<a href="{url(lang,'contact')}"{' aria-current="page"' if current=='contact' else ''}>{u['contact']}</a>'''
    drawer_cats = "".join(f'<details><summary>{CATEGORIES[c][lang]} {I["chev"]}</summary>' + "".join(f'<a href="{url(lang, s["slug"])}">{E(s[lang]["nav"])}</a>' for s in SERVICES if s["cat"] == c) + '</details>' for c in ["solar", "water", "mep", "smart"])
    top_l = ('<span class="dot"></span> Official dealer of <b>Lamborghini Calorclima</b> in the UAE · <a href="%s" rel="noopener">FEFCO AI Solutions</a>' % AI_SITE) if lang == "en" else ('<span class="dot"></span> الوكيل المعتمد لـ <b>لامبورغيني كالوركليما</b> في الإمارات · <a href="%s" rel="noopener">فيفكو للذكاء الاصطناعي</a>' % AI_SITE)
    return f'''<div class="topbar"><div class="wrap"><div class="tb-l">{top_l}</div>
<div class="tb-r"><a class="hide-m" href="tel:{COMPANY['phone_main']}">{I['phone']}<span dir="ltr">{COMPANY['phone_main_disp']}</span></a><a class="hide-m" href="{wa_link()}" rel="noopener">{I['wa']}{u['whatsapp']}</a><a class="hide-m" href="mailto:{COMPANY['email']}">{COMPANY['email']}</a><a class="lang" href="{url(alt, path)}" hreflang="{alt}" lang="{alt}">{u['lang_switch']}</a></div></div></div>
<header class="site"><div class="wrap">
<a class="logo" href="{url(lang)}" aria-label="FEFCO Solutions"><img src="/assets/fefco-solutions-logo.png" alt="FEFCO Solutions logo" width="417" height="208"></a>
<nav class="main" aria-label="Main">{nav}</nav>
<div class="h-cta"><a class="btn btn-wa btn-sm" href="{wa_link()}" rel="noopener">{I['wa']}WhatsApp</a><a class="btn btn-primary btn-sm" href="#quote">{u['survey'] if lang=='ar' else 'Free site survey'} {I['arr']}</a></div>
<button class="burger" type="button" data-open-drawer aria-label="{u['menu']}">{I['menu']}</button>
</div></header>
<div class="drawer" role="dialog" aria-modal="true" aria-label="{u['menu']}"><div class="panel">
<div class="top"><img src="/assets/fefco-solutions-logo.png" alt="FEFCO Solutions"><button class="burger" style="display:inline-flex" type="button" data-close-drawer aria-label="{u['close']}">{I['x']}</button></div>
{drawer_cats}
<a class="plain" href="{url(lang,'products')}">{u['products']}</a><a class="plain" href="{url(lang,'projects')}">{u['projects']}</a><a class="plain" href="{url(lang,'about')}">{u['about']}</a><a class="plain" href="{url(lang,'contact')}">{u['contact']}</a><a class="plain" href="{url(alt, path)}" lang="{alt}">{u['lang_switch']}</a>
<div class="btns"><a class="btn btn-primary" href="#quote" data-close-drawer>{u['quote']}</a><a class="btn btn-wa" href="{wa_link()}" rel="noopener">{I['wa']}{u['whatsapp']}</a><a class="btn btn-ghost" href="tel:{COMPANY['phone_main']}">{I['phone']}<span dir="ltr">{COMPANY['phone_main_disp']}</span></a></div>
</div></div>
<main id="main">'''

def lead_form(lang, preselect=""):
    u = UI[lang]
    opts = "".join(f'<option{" selected" if s["slug"]==preselect else ""}>{E(s[lang]["nav"])}</option>' for s in SERVICES)
    em = "".join(f"<option>{e}</option>" for e in u["emirates"])
    other = "أخرى" if lang == "ar" else "Other"
    return f'''<form class="lead-form" novalidate>
<div class="fgrid">
<div class="f"><label for="f-name">{u['form_name']}</label><input id="f-name" name="name" autocomplete="name" required></div>
<div class="f"><label for="f-phone">{u['form_phone']}</label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+971" dir="ltr" required></div>
<div class="f"><label for="f-service">{u['form_service']}</label><select id="f-service" name="service">{opts}<option>{other}</option></select></div>
<div class="f"><label for="f-emirate">{u['form_emirate']}</label><select id="f-emirate" name="emirate">{em}</select></div>
<div class="f full"><label for="f-email">{u['form_email']}</label><input id="f-email" name="email" type="email" autocomplete="email" dir="ltr"></div>
<div class="f full"><label for="f-msg">{u['form_msg']}</label><textarea id="f-msg" name="message"></textarea></div>
</div>
<p class="form-err" role="alert">{u['form_err']}</p>
<button class="btn btn-wa" type="submit">{I['wa']}{u['form_send']}</button>
<p class="form-note">{u['form_note']}</p>
</form>'''

def cta_band(lang, preselect=""):
    u = UI[lang]
    return f'''<section class="band mint" id="quote"><div class="wrap cta">
<div><span class="kicker">{u['survey']}</span><h2>{u['cta_title']}</h2><p class="lead">{u['cta_sub']}</p>
<div class="contact-lines">
<a href="tel:{COMPANY['phone_main']}"><span class="ic">{I['phone']}</span><span dir="ltr">{COMPANY['phone_main_disp']}</span></a>
<a href="{wa_link()}" rel="noopener"><span class="ic">{I['wa']}</span>{u['whatsapp']}</a>
<a href="mailto:{COMPANY['email']}"><span class="ic">{I['mail']}</span>{COMPANY['email']}</a>
<a href="{url(lang,'contact')}"><span class="ic">{I['pin']}</span>{COMPANY['address_'+lang]}</a>
</div></div>
{lead_form(lang, preselect)}
</div></section>'''

def footer(lang):
    u = UI[lang]
    def col(c): return "".join(f'<li><a href="{url(lang, s["slug"])}">{E(s[lang]["nav"])}</a></li>' for s in SERVICES if s["cat"] == c)
    soc = "".join(f'<a href="{s[1]}" rel="noopener" target="_blank">{s[0]}</a>' for s in SOCIAL)
    soc_ai = "".join(f'<a href="{s[1]}" rel="noopener" target="_blank">{s[0]}</a>' for s in SOCIAL_AI)
    yr = datetime.date.today().year
    return f'''</main>
<footer class="site"><div class="wrap">
<div class="cols">
<div><a class="f-logo" href="{url(lang)}"><img src="/assets/fefco-solutions-logo.png" alt="FEFCO Solutions" loading="lazy"></a>
<p>{u['footer_about']}</p>
<div class="f-lines"><a href="{wa_link()}" rel="noopener">{I['wa']}WhatsApp <span dir="ltr">{COMPANY['phone_main_disp']}</span></a><a href="tel:{COMPANY['phone_2']}">{I['phone']}<span dir="ltr">{COMPANY['phone_2_disp']}</span></a><a href="mailto:{COMPANY['email']}">{I['mail']}{COMPANY['email']}</a><a href="mailto:{COMPANY['email_solar']}">{I['mail']}{COMPANY['email_solar']}</a><span>{I['pin']}{COMPANY['address_'+lang]}</span></div>
<a class="division" href="{AI_SITE}" rel="noopener"><span class="dot"></span>{'Our AI division: FEFCO AI Solutions' if lang=='en' else 'قسم الذكاء الاصطناعي: فيفكو للذكاء الاصطناعي'}</a>
</div>
<div><h4>{CATEGORIES['solar'][lang]}</h4><ul>{col('solar')}</ul></div>
<div><h4>{CATEGORIES['water'][lang]}</h4><ul>{col('water')}</ul><h4 style="margin-top:26px">{CATEGORIES['smart'][lang]}</h4><ul>{col('smart')}</ul></div>
<div><h4>{CATEGORIES['mep'][lang]}</h4><ul>{col('mep')}</ul><h4 style="margin-top:26px">{u['footer_company']}</h4><ul><li><a href="{url(lang,'about')}">{u['about']}</a></li><li><a href="{url(lang,'projects')}">{u['projects']}</a></li><li><a href="{url(lang,'products')}">{u['products']}</a></li><li><a href="{url(lang,'contact')}">{u['contact']}</a></li><li><a href="{url(lang,'privacy')}">{u['privacy']}</a></li></ul></div>
</div>
<div class="f-follow"><span>{u['footer_follow']}</span>{soc}<span style="margin-inline-start:18px">{u['footer_ai']}</span>{soc_ai}</div>
<div class="f-bottom"><span>© {yr} {COMPANY['brand']} · {COMPANY['legal']}. {u['rights']}</span><span>{'Serving Dubai, Sharjah, Abu Dhabi, Ajman, Ras Al Khaimah, Fujairah and Umm Al Quwain' if lang=='en' else 'نخدم دبي والشارقة وأبوظبي وعجمان ورأس الخيمة والفجيرة وأم القيوين'}</span></div>
</div></footer>
<a class="fab" href="{wa_link()}" rel="noopener">{I['wa']}{'Chat on WhatsApp' if lang=='en' else 'تحدث عبر واتساب'}</a>
<nav class="mbar" aria-label="Quick contact"><a class="c" href="tel:{COMPANY['phone_main']}">{I['phone']}{u['call']}</a><a class="w" href="{wa_link()}" rel="noopener">{I['wa']}WhatsApp</a><a class="q" href="#quote">{'Free quote' if lang=='en' else 'عرض سعر مجاني'}</a></nav>
<script src="/assets/site.js" defer></script>
</body></html>'''

def write(lang, path, html_):
    d = os.path.join(OUT, "ar" if lang == "ar" else "", path.strip("/"))
    os.makedirs(d, exist_ok=True)
    if BASE_PATH:
        html_ = html_.replace('href="/', 'href="' + BASE_PATH + '/').replace('src="/', 'src="' + BASE_PATH + '/')
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_)

def svc_card(lang, s):
    return f'''<a class="svc-card" href="{url(lang, s['slug'])}"><div class="ph"><img src="{img(s['img'])}" alt="{E(s[lang]['nav'])}" loading="lazy"></div>
<div class="bd"><span class="cat">{CATEGORIES[s['cat']][lang]}</span><h3>{E(s[lang]['nav'])}</h3><p>{E(s[lang]['lead'][:150].rsplit(' ',1)[0])}…</p><span class="more">{UI[lang]['view_service']} {I['arr']}</span></div></a>'''

def faq_block(lang, faqs):
    items = "".join(f'<details><summary>{E(q)} {I["plus"]}</summary><p>{E(a)}</p></details>' for q, a in faqs)
    return f'<div class="faq">{items}</div>'

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumbs_ld(lang, items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + u} for i, (n, u) in enumerate(items)]}

# ---------- pages ----------
HOME = {
 "en": {"t": "FEFCO Solutions | Solar Panels, Solar Water Heaters, EV Chargers & MEP Maintenance in Dubai, UAE",
        "d": "FEFCO Solutions is a Dubai solar, water and electromechanical company: rooftop solar PV (DEWA Shams Dubai), solar water heater supply and repair, battery storage, EV chargers, water filtration, plumbing and AMC across the UAE.",
        "kicker": "Solar, water and MEP contractor in Dubai",
        "h1": "Solar power, hot water and maintenance, handled by one team.",
        "lead": "FEFCO designs, installs and maintains rooftop solar, solar water heaters, battery storage, EV chargers, water systems and plumbing for homes and businesses across the UAE.",
        "trust": ["DEWA Shams Dubai process handled", "700+ clients served", "24-hour emergency line"],
        "photo_cap": "Rooftop solar and EV charging for Dubai villas",
        "calc_t": "Estimate your solar savings", "calc_s": "Move the slider to your average monthly DEWA bill.",
        "bill": "Monthly electricity bill", "types": [("villa", "Villa"), ("business", "Business"), ("factory", "Industrial")],
        "r1": "System size", "r2": "Estimated cost", "r3": "Estimated yearly savings", "r4": "Payback",
        "calc_note": "Indicative only, based on typical Dubai yield and tariffs. Your survey gives exact figures.",
        "calc_btn": "Get my exact quote on WhatsApp",
        "brands": "Brands we supply, install and service",
        "explore_k": "What we do", "explore_h": "Everything your property needs to run on sunshine and stay running",
        "explore_p": "Pick an area to see the services inside it. Each one is delivered by FEFCO's own engineers and technicians.",
        "featured_k": "Most requested", "featured_h": "Popular services in Dubai",
        "proj_k": "Our work", "proj_h": "Real installations across the UAE", "proj_p": "Villas, factories, hotels and farms: a selection from FEFCO's project archive.",
        "proj_btn": "See more projects",
        "lead_k": "Founder", "lead_h": "Led by a founder who shows up on site",
        "lead_p": "Mustafa Asgar Ali founded FEFCO and still runs it hands-on. He is regularly on client sites and at industry events such as WETEX Dubai, demonstrating new technology to customers in person.",
        "lead_pts": ["Demonstrates new technology to clients in person, from SuitX exoskeletons to solar-cleaning solutions", "Leads partnerships with Lamborghini Calorclima and Inspire Clean Energy (EIRA)", "Oversees FEFCO AI Solutions, the group's AI and digital division"],
        "lead_tag": "Founder, FEFCO Solutions", "lead_tag2": "Trialling SuitX exoskeletons before launch in the UAE",
        "seg_k": "Who we work with", "seg_h": "From one villa to a whole portfolio",
        "segs": [("Homeowners", "Solar, hot water, EV charging and plumbing for villas and townhouses."), ("Businesses", "Offices, shops, restaurants and hotels that want lower running costs."), ("Industry", "Factories, warehouses and farms with big roofs and big loads."), ("Facility managers", "One accountable contractor for many systems and many sites.")],
        "faq_k": "Questions", "faq_h": "What customers ask us most",
        "social_k": "Follow FEFCO", "social_h": "See our latest projects on social media",
        "social_p": "Site videos, installations and tips for UAE homeowners and businesses. Follow us on Instagram, Facebook and Threads.",
        },
 "ar": {"t": "فيفكو سوليوشنز | الألواح الشمسية وسخانات المياه الشمسية وشواحن السيارات والصيانة في دبي والإمارات",
        "d": "فيفكو سوليوشنز شركة للطاقة الشمسية والمياه والأعمال الكهروميكانيكية في دبي: الطاقة الشمسية على الأسطح (شمس دبي)، وتوريد سخانات المياه الشمسية وإصلاحها، وتخزين الطاقة، وشواحن السيارات الكهربائية، وفلترة المياه، والسباكة، وعقود الصيانة في جميع أنحاء الإمارات.",
        "kicker": "مقاول طاقة شمسية ومياه وأعمال كهروميكانيكية في دبي",
        "h1": "الطاقة الشمسية والمياه الساخنة والصيانة، يتولاها فريق واحد.",
        "lead": "تصمم فيفكو وتركّب وتصون أنظمة الطاقة الشمسية على الأسطح وسخانات المياه الشمسية وتخزين الطاقة وشواحن السيارات الكهربائية وأنظمة المياه والسباكة للمنازل والشركات في جميع أنحاء الإمارات.",
        "trust": ["نتولى إجراءات شمس دبي", "أكثر من 700 عميل", "خط طوارئ على مدار 24 ساعة"],
        "photo_cap": "طاقة شمسية وشحن سيارات كهربائية لفلل دبي",
        "calc_t": "احسب توفيرك من الطاقة الشمسية", "calc_s": "حرّك المؤشر إلى متوسط فاتورة ديوا الشهرية.",
        "bill": "فاتورة الكهرباء الشهرية", "types": [("villa", "فيلا"), ("business", "تجاري"), ("factory", "صناعي")],
        "r1": "حجم النظام", "r2": "التكلفة التقديرية", "r3": "التوفير السنوي التقديري", "r4": "مدة الاسترداد",
        "calc_note": "أرقام إرشادية فقط مبنية على الإنتاج والتعرفة المعتادة في دبي. تعطيك المعاينة الأرقام الدقيقة.",
        "calc_btn": "احصل على عرضي الدقيق عبر واتساب",
        "brands": "علامات تجارية نورّدها ونركّبها ونصونها",
        "explore_k": "ماذا نقدم", "explore_h": "كل ما يحتاجه عقارك ليعمل بطاقة الشمس ويستمر في العمل",
        "explore_p": "اختر مجالاً لترى الخدمات التي يضمها. ينفذ كل خدمة مهندسو فيفكو وفنيوها.",
        "featured_k": "الأكثر طلباً", "featured_h": "خدمات شائعة في دبي",
        "proj_k": "أعمالنا", "proj_h": "تركيبات حقيقية في جميع أنحاء الإمارات", "proj_p": "فلل ومصانع وفنادق ومزارع: مختارات من أرشيف مشاريع فيفكو.",
        "proj_btn": "شاهد المزيد من المشاريع",
        "lead_k": "المؤسس", "lead_h": "بقيادة مؤسس حاضر في الموقع",
        "lead_p": "أسس مصطفى أصغر علي فيفكو وما زال يديرها بأسلوب عملي مباشر. يحضر باستمرار إلى مواقع العملاء والفعاليات المتخصصة مثل ويتكس دبي، ويعرض التقنيات الجديدة على العملاء بنفسه.",
        "lead_pts": ["يعرض التقنيات الجديدة على العملاء بنفسه، من هياكل SuitX إلى حلول تنظيف الألواح الشمسية", "يقود الشراكات مع لامبورغيني كالوركليما وإنسباير كلين إنرجي (EIRA)", "يشرف على فيفكو للذكاء الاصطناعي، القسم الرقمي للمجموعة"],
        "lead_tag": "المؤسس، فيفكو سوليوشنز", "lead_tag2": "تجربة هياكل SuitX قبل إطلاقها في الإمارات",
        "seg_k": "مع من نعمل", "seg_h": "من فيلا واحدة إلى محفظة عقارية كاملة",
        "segs": [("أصحاب المنازل", "الطاقة الشمسية والمياه الساخنة وشحن السيارات والسباكة للفلل والتاون هاوس."), ("الشركات", "المكاتب والمحلات والمطاعم والفنادق الراغبة في خفض تكاليف التشغيل."), ("الصناعة", "المصانع والمستودعات والمزارع ذات الأسطح الكبيرة والأحمال العالية."), ("مديرو المرافق", "مقاول واحد مسؤول عن أنظمة ومواقع متعددة.")],
        "faq_k": "أسئلة", "faq_h": "أكثر ما يسألنا عنه العملاء",
        "social_k": "تابع فيفكو", "social_h": "شاهد أحدث مشاريعنا على وسائل التواصل",
        "social_p": "فيديوهات من المواقع وتركيبات ونصائح لأصحاب المنازل والشركات في الإمارات. تابعنا على إنستغرام وفيسبوك وثريدز.",
        },
}
HOME_FAQ = {
 "en": [("What does FEFCO Solutions do?", "FEFCO Solutions (FEFCO Electromechanical Services LLC) is a Dubai-based contractor that installs and maintains rooftop solar PV, solar water heaters, battery storage, EV chargers, water filtration, GRP tanks, plumbing and electromechanical systems, and offers annual maintenance contracts across the UAE."),
        ("Is FEFCO approved for DEWA Shams Dubai solar projects?", "FEFCO's solar team handles the full Shams Dubai process for customers: design, DEWA submission, inspection and net-meter connection."),
        ("Which areas do you cover?", "Dubai, Sharjah, Abu Dhabi, Ajman, Ras Al Khaimah, Fujairah, Umm Al Quwain and Al Ain."),
        ("Do you repair solar water heaters from other brands?", "Yes. We repair and maintain all brands, including Ariston, Helien, Solahart, Chromagen and Lamborghini Calorclima."),
        ("How do I get a quote?", "Send a WhatsApp message to +971 50 786 7872, call us, or fill in the form. We arrange a free site survey and send a fixed written quote.")],
 "ar": [("ماذا تقدم فيفكو سوليوشنز؟", "فيفكو سوليوشنز (فيفكو للخدمات الكهروميكانيكية ذ.م.م) مقاول مقره دبي يركّب ويصون أنظمة الطاقة الشمسية على الأسطح وسخانات المياه الشمسية وتخزين الطاقة وشواحن السيارات الكهربائية وفلترة المياه وخزانات الفايبرجلاس والسباكة والأنظمة الكهروميكانيكية، ويقدم عقود صيانة سنوية في جميع أنحاء الإمارات."),
        ("هل تتولى فيفكو مشاريع شمس دبي؟", "يتولى فريق الطاقة الشمسية في فيفكو إجراءات شمس دبي كاملة للعملاء: التصميم والتقديم لديوا والفحص وتوصيل العداد الصافي."),
        ("ما المناطق التي تغطونها؟", "دبي والشارقة وأبوظبي وعجمان ورأس الخيمة والفجيرة وأم القيوين والعين."),
        ("هل تصلحون سخانات شمسية من علامات أخرى؟", "نعم. نصلح ونصون جميع العلامات، ومنها أريستون وهيلين وسولاهارت وكروماجين ولامبورغيني كالوركليما."),
        ("كيف أحصل على عرض سعر؟", "أرسل رسالة واتساب إلى ‎+971 50 786 7872‎ أو اتصل بنا أو املأ النموذج. نرتب معاينة مجانية للموقع ونرسل عرض سعر مكتوباً وثابتاً.")],
}
PROJECTS = [
 ("2023/09/solar12-scaled.jpg", "w2 h2", ("Commercial rooftop solar PV", "طاقة شمسية على سطح تجاري")),
 ("2024/05/installation2-1.jpeg", "w2", ("Solar water heaters, Dubai", "سخانات مياه شمسية، دبي")),
 ("2023/09/solarparking.jpeg", "", ("Solar carport", "مظلة سيارات شمسية")),
 ("2023/09/IMG_20191223_181707-scaled.jpg", "", ("Solar street lighting", "إنارة شوارع شمسية")),
 ("2023/09/Mothers-Villa_3.jpg", "w2", ("Villa rooftop design", "تصميم نظام شمسي لفيلا")),
 ("2023/09/PHOTO-2023-09-16-22-41-51.jpg", "", ("Robotic panel cleaning", "تنظيف آلي للألواح")),
 ("2023/09/grp3.jpg", "", ("GRP water tank", "خزان مياه فايبرجلاس")),
 ("2023/09/daylight.jpg", "", ("Tubular daylighting", "إضاءة طبيعية أنبوبية")),
 ("2023/09/IMG_20200409_111132.jpg", "", ("Rooftop solar, Dubai", "طاقة شمسية على سطح، دبي")),
 ("2023/09/filter.jpg", "", ("Water filtration plant", "محطة فلترة مياه")),
 ("2024/05/aristoninstallation.jpeg", "", ("Ariston solar water heater", "سخان أريستون الشمسي")),
]
PROJECTS_MORE = [
 ("2023/09/solar11-scaled.jpg", ("Rooftop solar array", "مصفوفة شمسية على سطح")), ("2023/09/IMG_20201226_161249-1-scaled.jpg", ("Industrial roof solar", "طاقة شمسية لسطح صناعي")),
 ("2023/09/IMG_20210120_124457-scaled.jpg", ("Solar PV installation", "تركيب ألواح شمسية")), ("2023/09/IMG_20200919_112316.jpg", ("Commercial building solar", "طاقة شمسية لمبنى تجاري")),
 ("2023/09/solar76.jpeg", ("Solar site", "موقع طاقة شمسية")), ("2023/09/solar5.jpeg", ("Panel installation", "تركيب الألواح")),
 ("2024/05/installation1.jpg", ("Solar water heater project", "مشروع سخانات شمسية")), ("2023/09/water1.jpeg", ("Solar hot water", "مياه ساخنة بالطاقة الشمسية")),
 ("2023/09/waterheater2.jpeg", ("Helien solar water heaters", "سخانات هيلين الشمسية")), ("2023/09/watersolar2.jpeg", ("Villa solar water heater", "سخان شمسي لفيلا")),
 ("2023/09/grp2.jpeg", ("GRP tank assembly", "تجميع خزان فايبرجلاس")), ("2023/09/dayl1.jpg", ("Daylighting system", "نظام إضاءة طبيعية")),
 ("2023/09/stree.jpg", ("Solar street lights", "أعمدة إنارة شمسية")), ("2023/09/solarparking2.jpeg", ("Solar parking shade", "مظلة مواقف شمسية")),
 ("2023/09/ro.jpg", ("RO water treatment", "معالجة مياه بالتناضح العكسي")), ("2023/09/IMG-20190212-WA0039.jpg", ("Electrical works", "أعمال كهربائية")),
 ("2023/09/PHOTO-2023-09-16-22-28-34.jpg", ("SuitX demonstration", "عرض SuitX التجريبي")), ("2023/09/20210621_171528.jpg", ("FEFCO office", "مكتب فيفكو")),
]
FEATURED = ["solar-panel-installation-dubai", "solar-water-heater-dubai", "solar-water-heater-repair-maintenance-dubai", "ev-charger-installation-dubai", "solar-panel-cleaning-maintenance-dubai", "amc-annual-maintenance-contract-dubai"]
LEADER_IMG = "2023/09/PHOTO-2023-09-16-22-28-32-2.jpg"

def page_home(lang):
    h = HOME[lang]; u = UI[lang]
    types = "".join(f'<button type="button" data-t="{k}" aria-pressed="{"true" if i==0 else "false"}">{v}</button>' for i, (k, v) in enumerate(h["types"]))
    chips = "".join(f'<span class="chip"><i></i>{b}</span>' for b in BRANDS) * 2
    tabs = ""; panels = ""
    cat_img = {"solar": "2023/09/IMG_20200409_111132.jpg", "water": "2024/05/installation1.jpg", "mep": "2024/05/repair1.jpeg", "smart": "2023/09/PHOTO-2023-09-16-22-28-34.jpg"}
    cat_desc = {"en": {"solar": "Generate, store and use your own clean power, with the paperwork handled.", "water": "Hot, clean and cool water for every tap, from heaters to tanks and filters.", "mep": "Electrical, plumbing and mechanical works, plus contracts that keep it all running.", "smart": "Monitoring, security and wearable tech for sites and industry."},
                "ar": {"solar": "أنتج طاقتك النظيفة وخزّنها واستخدمها، مع إنجاز المعاملات نيابة عنك.", "water": "مياه ساخنة ونظيفة وباردة لكل صنبور، من السخانات إلى الخزانات والفلاتر.", "mep": "أعمال كهربائية وسباكة وميكانيكية، مع عقود تحافظ على عمل كل شيء.", "smart": "المراقبة والأمن والتقنيات القابلة للارتداء للمواقع والصناعة."}}
    for i, c in enumerate(["solar", "water", "mep", "smart"]):
        items = [s for s in SERVICES if s["cat"] == c]
        tabs += f'<button class="tab" role="tab" id="t-{c}" aria-controls="p-{c}" aria-selected="{"true" if i==0 else "false"}"><span class="ic">{CAT_ICON[c]}</span>{CATEGORIES[c][lang]}<small>{len(items)}</small></button>'
        links = "".join(f'<a href="{url(lang, s["slug"])}"><b>{E(s[lang]["nav"])}</b><span>{E(s[lang]["ben"][0][1])}</span></a>' for s in items)
        panels += f'<div class="tabpanel" role="tabpanel" id="p-{c}" aria-labelledby="t-{c}"{"" if i==0 else " hidden"}><div><h3>{CATEGORIES[c][lang]}</h3><p class="muted">{cat_desc[lang][c]}</p><div class="svc-list">{links}</div></div><figure><img src="{img(cat_img[c])}" alt="{CATEGORIES[c][lang]}" loading="lazy"></figure></div>'
    featured = "".join(svc_card(lang, BY_SLUG[s]) for s in FEATURED)
    steps = "".join(f'<div class="step"><span class="n">{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PROCESS["install"][lang]))
    facts = "".join(f'<div class="fact"><b>{n}</b><span>{t}</span></div>' for n, t in FACTS[lang])
    gal = "".join(f'<figure class="{c}"><img src="{img(p)}" alt="{cap[0 if lang=="en" else 1]}" loading="lazy"><figcaption>{cap[0 if lang=="en" else 1]}</figcaption></figure>' for p, c, cap in PROJECTS)
    pts = "".join(f'<li>{I["check"]}<span>{p}</span></li>' for p in h["lead_pts"])
    segs = "".join(f'<div class="card"><div class="ic">{BEN_ICONS[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(h["segs"]))
    soc_tiles = "".join(f'<a href="{SOCIAL[0][1]}" rel="noopener" target="_blank" aria-label="Instagram"><img src="{img(p)}" alt="" loading="lazy"></a>' for p in ["2024/05/installation2-1.jpeg", "2023/09/solarparking.jpeg", "2023/09/PHOTO-2023-09-16-22-41-51-2.jpg", "2023/09/IMG_20191223_181707-scaled.jpg", "2024/05/repair1.jpeg", "2023/09/solar11-scaled.jpg"])
    soc_links = "".join(f'<a class="soc" href="{s[1]}" rel="noopener" target="_blank">{SOC_ICON[s[2]]}{s[0]}</a>' for s in SOCIAL)
    name = LEADER_NAME[lang] if LEADER_NAME else h["lead_tag"]
    body = f'''<section class="hero"><div class="wrap">
<div><span class="kicker">{h['kicker']}</span><h1>{h['h1']}</h1><p class="lead">{h['lead']}</p>
<div class="ctas"><a class="btn btn-primary" href="#quote">{u['survey']} {I['arr']}</a><a class="btn btn-wa" href="{wa_link()}" rel="noopener">{I['wa']}{u['whatsapp']}</a></div>
<div class="trust">{''.join(f'<span>{I["check"]}{t}</span>' for t in h['trust'])}</div></div>
<div class="hero-visual"><figure class="hero-photo"><img src="{img(GEN['villa'])}" alt="{h['photo_cap']}" fetchpriority="high" width="1672" height="941"><figcaption>{h['photo_cap']}</figcaption></figure>
<div class="calc" aria-labelledby="calc-t"><h2 id="calc-t">{h['calc_t']}</h2><p class="sub">{h['calc_s']}</p>
<div class="seg" role="group" aria-label="Property type">{types}</div>
<label for="bill">{h['bill']} <output id="billOut" for="bill"></output></label>
<input id="bill" type="range" min="500" max="40000" step="250" value="2000">
<div class="res"><div class="big"><small>{h['r3']}</small><b id="rSave"></b></div><div><small>{h['r1']}</small><b id="rSize"></b></div><div><small>{h['r4']}</small><b id="rPay"></b></div><div style="grid-column:1/-1"><small>{h['r2']}</small><b id="rCost"></b></div></div>
<a class="btn btn-wa" href="{wa_link()}" rel="noopener">{I['wa']}{h['calc_btn']}</a>
<p class="note">{h['calc_note']}</p></div></div>
</div></section>
<div class="chips-band"><p>{h['brands']}</p><div class="marquee" aria-hidden="false">{chips}</div></div>
<section class="band"><div class="wrap"><div class="sec-head"><span class="kicker">{h['explore_k']}</span><h2>{h['explore_h']}</h2><p>{h['explore_p']}</p></div>
<div class="explorer"><div class="tabs" role="tablist" aria-orientation="vertical">{tabs}</div><div>{panels}</div></div></div></section>
<section class="band sky"><div class="wrap"><div class="sec-head"><span class="kicker">{h['featured_k']}</span><h2>{h['featured_h']}</h2></div><div class="grid g3">{featured}</div>
<p style="margin-top:30px"><a class="btn btn-ghost" href="{url(lang,'services')}">{u['all_services']} {I['arr']}</a></p></div></section>
<section class="band tight"><div class="wrap facts">{facts}</div></section>
<section class="band mint"><div class="wrap"><div class="sec-head"><span class="kicker">{u['process']}</span><h2>{'From first call to handover in four steps' if lang=='en' else 'من أول اتصال حتى التسليم في أربع خطوات'}</h2></div><div class="steps">{steps}</div></div></section>
<section class="band"><div class="wrap"><div class="sec-head"><span class="kicker">{h['proj_k']}</span><h2>{h['proj_h']}</h2><p>{h['proj_p']}</p></div><div class="gallery">{gal}</div>
<p style="margin-top:28px"><a class="btn btn-ghost" href="{url(lang,'projects')}">{h['proj_btn']} {I['arr']}</a></p></div></section>
<section class="band sky"><div class="wrap leader"><figure><img src="{img(LEADER_IMG)}" alt="{E(name)}" loading="lazy"><div class="tag"><b>{E(name)}</b><span>{h['lead_tag']}</span></div></figure>
<div><span class="kicker">{h['lead_k']}</span><h2>{h['lead_h']}</h2><p class="lead">{h['lead_p']}</p><ul class="pts">{pts}</ul><a class="btn btn-primary" href="{url(lang,'about')}">{u['about']} {I['arr']}</a></div></div></section>
<section class="band"><div class="wrap"><div class="sec-head"><span class="kicker">{h['seg_k']}</span><h2>{h['seg_h']}</h2></div><div class="grid g4">{segs}</div></div></section>
<section class="band sky"><div class="wrap"><div class="sec-head"><span class="kicker">{h['faq_k']}</span><h2>{h['faq_h']}</h2></div>{faq_block(lang, HOME_FAQ[lang])}</div></section>
<section class="band"><div class="wrap"><div class="split" style="align-items:center"><div><span class="kicker">{h['social_k']}</span><h2>{h['social_h']}</h2><p class="lead">{h['social_p']}</p><div class="soc-links">{soc_links}</div></div><div class="social-grid" style="grid-template-columns:repeat(3,1fr)">{soc_tiles}</div></div></div></section>
{cta_band(lang)}'''
    out = head(lang, h["t"], h["d"], "", GEN["villa"], [faq_ld(HOME_FAQ[lang])]) + header(lang, "") + body + footer(lang)
    write(lang, "", out)

def page_service(lang, s):
    c = s[lang]; u = UI[lang]; path = s["slug"]
    ben = "".join(f'<div class="card"><div class="ic">{BEN_ICONS[i%6]}</div><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(c["ben"]))
    inc = "".join(f'<li>{I["check"]}<span>{E(x)}</span></li>' for x in c["inc"])
    who = "".join(f'<span class="pill">{E(x)}</span>' for x in c["who"])
    steps = "".join(f'<div class="step"><span class="n">{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PROCESS[s["proc"]][lang]))
    thumbs = "".join(f'<img src="{img(g)}" alt="{E(c["nav"])}" loading="lazy">' for g in s.get("gallery", [])[:3])
    related = [x for x in SERVICES if x["cat"] == s["cat"] and x["slug"] != s["slug"]][:3]
    if len(related) < 3: related += [BY_SLUG[f] for f in FEATURED if f != s["slug"] and BY_SLUG[f] not in related][:3 - len(related)]
    rel = "".join(svc_card(lang, x) for x in related)
    glance = ("<b>At a glance:</b> " if lang == "en" else "<b>باختصار:</b> ") + E(c["lead"]) + (" Areas served: Dubai, Sharjah, Abu Dhabi and all emirates. Contact: " if lang == "en" else " نخدم دبي والشارقة وأبوظبي وجميع الإمارات. للتواصل: ") + f'<a href="tel:{COMPANY["phone_main"]}" dir="ltr">{COMPANY["phone_main_disp"]}</a>.'
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": c["h1"], "serviceType": c["nav"], "description": c["d"], "url": absu(lang, path),
              "provider": {"@id": DOMAIN + "/#org"}, "areaServed": {"@type": "Country", "name": "United Arab Emirates"}, "image": img(s["img"]),
              "availableChannel": {"@type": "ServiceChannel", "servicePhone": COMPANY["phone_main"], "serviceUrl": absu(lang, path)}, "inLanguage": lang, "dateModified": TODAY}
    bc = crumbs_ld(lang, [(u["breadcrumb_home"], url(lang)), (u["services"], url(lang, "services")), (c["nav"], url(lang, path))])
    body = f'''<section class="svc-hero"><div class="wrap"><div>
<nav class="crumbs" aria-label="Breadcrumb"><a href="{url(lang)}">{u['breadcrumb_home']}</a><span>/</span><a href="{url(lang,'services')}">{u['services']}</a><span>/</span><span aria-current="page">{E(c['nav'])}</span></nav>
<span class="kicker">{CATEGORIES[s['cat']][lang]}</span><h1>{E(c['h1'])}</h1><p class="lead">{E(c['lead'])}</p>
<div class="ctas" style="display:flex;flex-wrap:wrap;gap:12px;margin-top:26px"><a class="btn btn-primary" href="#quote">{u['quote']} {I['arr']}</a><a class="btn btn-wa" href="{wa_link(('Hello FEFCO, I need: ' if lang=='en' else 'مرحباً فيفكو، أحتاج: ') + c['nav'])}" rel="noopener">{I['wa']}{u['whatsapp']}</a></div>
<p class="glance">{glance}</p></div>
<figure><img src="{img(s['img'])}" alt="{E(c['h1'])}" fetchpriority="high"></figure></div></section>
<section class="band"><div class="wrap split"><div class="prose"><span class="kicker">{u['why']}</span><h2>{E(c['nav'])}{' in the UAE' if lang=='en' else ' في الإمارات'}</h2><p>{E(c['body'])}</p><div class="thumbs">{thumbs}</div></div>
<div><span class="kicker">{u['included']}</span><h2>{'What you get' if lang=='en' else 'ما الذي تحصل عليه'}</h2><ul class="checks">{inc}</ul>
<h3 style="margin-top:34px">{u['who']}</h3><div class="pills">{who}</div></div></div></section>
<section class="band sky"><div class="wrap"><div class="sec-head"><span class="kicker">{u['why']}</span><h2>{'Why customers choose FEFCO' if lang=='en' else 'لماذا يختار العملاء فيفكو'}</h2></div><div class="grid g3">{ben}</div></div></section>
<section class="band mint"><div class="wrap"><div class="sec-head"><span class="kicker">{u['process']}</span><h2>{'How it works' if lang=='en' else 'كيف نعمل'}</h2></div><div class="steps">{steps}</div></div></section>
<section class="band"><div class="wrap"><div class="sec-head"><span class="kicker">{u['faq']}</span><h2>{E(c['nav'])}: {'your questions answered' if lang=='en' else 'إجابات أسئلتك'}</h2></div>{faq_block(lang, c['faq'])}</div></section>
<section class="band sky"><div class="wrap"><div class="sec-head"><span class="kicker">{u['related']}</span><h2>{'You may also need' if lang=='en' else 'قد تحتاج أيضاً'}</h2></div><div class="grid g3">{rel}</div></div></section>
{cta_band(lang, s['slug'])}'''
    out = head(lang, c["t"], c["d"], path, s["img"], [svc_ld, faq_ld(c["faq"]), bc]) + header(lang, path) + body + footer(lang)
    write(lang, path, out)

def simple_page(lang, path, title, desc, kicker, h1, lead, inner, current="", image=None, ld=None):
    u = UI[lang]
    bc = crumbs_ld(lang, [(u["breadcrumb_home"], url(lang)), (h1, url(lang, path))])
    body = f'''<section class="page-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{url(lang)}">{u['breadcrumb_home']}</a><span>/</span><span aria-current="page">{E(h1)}</span></nav>
<span class="kicker">{kicker}</span><h1>{E(h1)}</h1><p class="lead">{lead}</p></div></section>{inner}{cta_band(lang)}'''
    write(lang, path, head(lang, title, desc, path, image, [bc] + (ld or [])) + header(lang, path, current) + body + footer(lang))

def page_services(lang):
    u = UI[lang]; inner = ""
    for c in ["solar", "water", "mep", "smart"]:
        cards = "".join(svc_card(lang, s) for s in SERVICES if s["cat"] == c)
        inner += f'<section class="band{" sky" if c in ("water","smart") else ""}"><div class="wrap"><div class="sec-head"><span class="kicker">{u["services"]}</span><h2>{CATEGORIES[c][lang]}</h2></div><div class="grid g3">{cards}</div></div></section>'
    if lang == "en":
        simple_page(lang, "services", "All Services | Solar, Water, MEP & Maintenance in Dubai | FEFCO Solutions", "Every FEFCO service: solar PV, solar water heaters and repair, battery storage, EV chargers, carports, lighting, water filtration, GRP tanks, chillers, plumbing, MEP, AMC, energy audits, IoT monitoring and SuitX.", "FEFCO Solutions", "All services", "Solar, water, electromechanical and smart-technology services for homes, businesses and industry across the UAE.", inner)
    else:
        simple_page(lang, "services", "جميع الخدمات | الطاقة الشمسية والمياه والأعمال الكهروميكانيكية والصيانة في دبي | فيفكو", "جميع خدمات فيفكو: الطاقة الشمسية وسخانات المياه وإصلاحها وتخزين الطاقة وشواحن السيارات والمظلات والإنارة وفلترة المياه والخزانات والمبردات والسباكة والأعمال الكهروميكانيكية وعقود الصيانة وتدقيق الطاقة والمراقبة وSuitX.", "فيفكو سوليوشنز", "جميع الخدمات", "خدمات الطاقة الشمسية والمياه والأعمال الكهروميكانيكية والتقنيات الذكية للمنازل والشركات والصناعة في جميع أنحاء الإمارات.", inner)

def page_products(lang):
    rows = ""
    for g in PRODUCT_GROUPS:
        t, d = g[lang]
        items = "".join(f"<li>{E(x)}</li>" for x in g["items"])
        ask = wa_link(("Hello FEFCO, please send datasheet and price for: " if lang == "en" else "مرحباً فيفكو، أرجو إرسال النشرة الفنية والسعر لـ: ") + t)
        rows += f'<div class="prod" id="{g["id"]}"><img src="{img(g["img"])}" alt="{E(t)}" loading="lazy"><div><h3>{E(t)}</h3><p class="muted" style="margin:0">{E(d)}</p><ul>{items}</ul><a class="btn btn-wa btn-sm" style="margin-top:14px" href="{ask}" rel="noopener">{I["wa"]}{"Request datasheet & price" if lang=="en" else "اطلب النشرة الفنية والسعر"}</a></div></div>'
    inner = f'<section class="band"><div class="wrap grid">{rows}</div></section>'
    if lang == "en":
        simple_page(lang, "products", "Solar Products UAE | LiFePO4 Batteries, Inverters, Storage, Solar Lights & Water Heaters | FEFCO", "Buy solar products in the UAE from FEFCO: Go Green energy storage systems, LiFePO4 batteries, hybrid inverters, solar pump inverters, panels, solar street and flood lights, and Lamborghini Calorclima water heaters.", "Products", "Solar and water products", "Equipment we supply and support from Dubai, for installers, contractors and end users across the UAE.", inner, "products")
    else:
        simple_page(lang, "products", "منتجات الطاقة الشمسية في الإمارات | بطاريات ومحولات وتخزين وإنارة شمسية وسخانات | فيفكو", "اشترِ منتجات الطاقة الشمسية في الإمارات من فيفكو: أنظمة تخزين جو جرين وبطاريات LiFePO4 ومحولات هجينة ومحولات مضخات وألواح وإنارة شمسية وسخانات لامبورغيني كالوركليما.", "المنتجات", "منتجات الطاقة الشمسية والمياه", "معدات نورّدها وندعمها من دبي للمركّبين والمقاولين والمستخدمين النهائيين في جميع أنحاء الإمارات.", inner, "products")

def page_projects(lang):
    k = 0 if lang == "en" else 1
    figs = "".join(f'<figure class="{c}"><img src="{img(p)}" alt="{cap[k]}" loading="lazy"><figcaption>{cap[k]}</figcaption></figure>' for p, c, cap in PROJECTS)
    figs += "".join(f'<figure><img src="{img(p)}" alt="{cap[k]}" loading="lazy"><figcaption>{cap[k]}</figcaption></figure>' for p, cap in PROJECTS_MORE)
    inner = f'<section class="band"><div class="wrap"><div class="gallery">{figs}</div></div></section>'
    if lang == "en":
        simple_page(lang, "projects", "Projects | Solar PV, Solar Water Heater & MEP Installations in the UAE | FEFCO Solutions", "Photos of FEFCO projects across the UAE: rooftop solar PV, solar water heaters, solar carports, street lighting, GRP tanks, water filtration, daylighting and more.", "Our work", "Projects across the UAE", "A selection of installations by FEFCO teams in Dubai, Sharjah, Abu Dhabi and the Northern Emirates.", inner, "projects")
    else:
        simple_page(lang, "projects", "المشاريع | تركيبات الطاقة الشمسية والسخانات والأعمال الكهروميكانيكية في الإمارات | فيفكو", "صور مشاريع فيفكو في الإمارات: الطاقة الشمسية على الأسطح وسخانات المياه الشمسية والمظلات الشمسية والإنارة وخزانات الفايبرجلاس وفلترة المياه والإضاءة الطبيعية وغيرها.", "أعمالنا", "مشاريع في جميع أنحاء الإمارات", "مجموعة من التركيبات التي نفذتها فرق فيفكو في دبي والشارقة وأبوظبي والإمارات الشمالية.", inner, "projects")

def page_about(lang):
    h = HOME[lang]; u = UI[lang]
    name = LEADER_NAME[lang] if LEADER_NAME else h["lead_tag"]
    if lang == "en":
        story = ("FEFCO Solutions is the trading name of FEFCO Electromechanical Services LLC, a Dubai-based company working in solar energy, water systems and electromechanical services. "
                 "We started with solar water heaters and grew with our customers into rooftop solar PV, battery storage, EV charging, water filtration, GRP tanks, plumbing and full maintenance contracts. "
                 "Today we serve more than 700 clients, from single villas to factories, hotels and farms, and we are an official dealer of Lamborghini Calorclima water heaters in the UAE and the MENA distributor of the EIRA solar asset-management platform.")
        vals = [("Do it properly", "Correct sizing, quality equipment and neat installation, even where nobody will see it."), ("Say it clearly", "Written quotes, fixed prices and honest advice, including when not to buy."), ("Stay for the long run", "We maintain what we install and answer the phone years later.")]
        title, desc, h1, lead = "About FEFCO Solutions | Solar, Water & Electromechanical Company in Dubai", "About FEFCO Solutions (FEFCO Electromechanical Services LLC): a Dubai company for solar PV, solar water heaters, water systems, MEP and maintenance across the UAE, with an AI division, FEFCO AI Solutions.", "About FEFCO Solutions", "A Dubai energy, water and electromechanical company built on doing the work properly and staying for the long run."
        ai = f'<p>FEFCO also runs <a href="{AI_SITE}">FEFCO AI Solutions</a>, our AI automation and digital marketing division, which builds AI agents, websites and campaigns for UAE businesses.</p>'
    else:
        story = ("فيفكو سوليوشنز هو الاسم التجاري لشركة فيفكو للخدمات الكهروميكانيكية ذ.م.م، وهي شركة مقرها دبي تعمل في الطاقة الشمسية وأنظمة المياه والخدمات الكهروميكانيكية. "
                 "بدأنا بسخانات المياه الشمسية ونمونا مع عملائنا لنقدم الطاقة الشمسية على الأسطح وتخزين الطاقة وشحن السيارات الكهربائية وفلترة المياه وخزانات الفايبرجلاس والسباكة وعقود الصيانة الشاملة. "
                 "نخدم اليوم أكثر من 700 عميل، من الفلل إلى المصانع والفنادق والمزارع، ونحن وكيل معتمد لسخانات لامبورغيني كالوركليما في الإمارات وموزع منصة EIRA لإدارة الأصول الشمسية في الشرق الأوسط وشمال أفريقيا.")
        vals = [("نعمل بإتقان", "حجم صحيح ومعدات جيدة وتركيب مرتب، حتى حيث لا يراه أحد."), ("نتحدث بوضوح", "عروض مكتوبة وأسعار ثابتة ونصيحة صادقة، حتى عندما لا ننصح بالشراء."), ("نبقى على المدى الطويل", "نصون ما نركّبه ونرد على الهاتف بعد سنوات.")]
        title, desc, h1, lead = "من نحن | فيفكو سوليوشنز للطاقة الشمسية والمياه والأعمال الكهروميكانيكية في دبي", "تعرف على فيفكو سوليوشنز (فيفكو للخدمات الكهروميكانيكية ذ.م.م): شركة في دبي للطاقة الشمسية وسخانات المياه الشمسية وأنظمة المياه والأعمال الكهروميكانيكية والصيانة في الإمارات، ولها قسم للذكاء الاصطناعي.", "من نحن", "شركة طاقة ومياه وأعمال كهروميكانيكية في دبي، قائمة على إتقان العمل والبقاء مع العملاء على المدى الطويل."
        ai = f'<p>كما تدير فيفكو <a href="{AI_SITE}">فيفكو للذكاء الاصطناعي</a>، قسم الأتمتة بالذكاء الاصطناعي والتسويق الرقمي، الذي يبني وكلاء الذكاء الاصطناعي والمواقع والحملات للشركات في الإمارات.</p>'
    vcards = "".join(f'<div class="card"><div class="ic">{BEN_ICONS[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(vals))
    facts = "".join(f'<div class="fact"><b>{n}</b><span>{t}</span></div>' for n, t in FACTS[lang])
    pts = "".join(f'<li>{I["check"]}<span>{p}</span></li>' for p in h["lead_pts"])
    inner = f'''<section class="band"><div class="wrap split" style="align-items:center"><div class="prose"><span class="kicker">{'Our story' if lang=='en' else 'قصتنا'}</span><h2>{'Solar, water and MEP under one roof' if lang=='en' else 'الطاقة الشمسية والمياه والأعمال الكهروميكانيكية تحت سقف واحد'}</h2><p>{story}</p>{ai}</div>
<div class="gallery" style="grid-template-columns:1fr 1fr;grid-auto-rows:200px"><figure class="w2"><img src="{img('2023/09/20210621_171528.jpg')}" alt="FEFCO office" loading="lazy"></figure><figure><img src="{img('2024/05/repair1.jpeg')}" alt="" loading="lazy"></figure><figure><img src="{img('2023/09/solar11-scaled.jpg')}" alt="" loading="lazy"></figure></div></div></section>
<section class="band tight sky"><div class="wrap facts">{facts}</div></section>
<section class="band"><div class="wrap leader"><figure><img src="{img('2023/09/PHOTO-2023-09-16-22-28-34.jpg')}" alt="{E(name)}" loading="lazy"><div class="tag"><b>{E(name)}</b><span>{h['lead_tag']}</span></div></figure>
<div><span class="kicker">{h['lead_k']}</span><h2>{h['lead_h']}</h2><p class="lead">{h['lead_p']}</p><ul class="pts">{pts}</ul></div></div></section>
<section class="band mint"><div class="wrap"><div class="sec-head"><span class="kicker">{'How we work' if lang=='en' else 'قيمنا'}</span><h2>{'What we stand for' if lang=='en' else 'ما نؤمن به'}</h2></div><div class="grid g3">{vcards}</div></div></section>'''
    simple_page(lang, "about", title, desc, "FEFCO Solutions" if lang == "en" else "فيفكو سوليوشنز", h1, lead, inner, "about")

def page_contact(lang):
    u = UI[lang]
    map_q = "https://www.google.com/maps?q=%s,%s&z=16&output=embed" % COMPANY["geo"]
    soc = "".join(f'<a class="soc" href="{s[1]}" rel="noopener" target="_blank">{SOC_ICON[s[2]]}{s[0]}</a>' for s in SOCIAL)
    cards = f'''<div class="grid g4">
<a class="card" href="tel:{COMPANY['phone_main']}"><div class="ic">{I['phone']}</div><h3>{u['call']}</h3><p dir="ltr">{COMPANY['phone_main_disp']}<br>{COMPANY['phone_2_disp']}</p></a>
<a class="card" href="{wa_link()}" rel="noopener"><div class="ic">{I['wa']}</div><h3>WhatsApp</h3><p dir="ltr">{COMPANY['phone_main_disp']}</p></a>
<a class="card" href="mailto:{COMPANY['email']}"><div class="ic">{I['mail']}</div><h3>{'Email' if lang=='en' else 'البريد الإلكتروني'}</h3><p>{COMPANY['email']}<br>{COMPANY['email_solar']}</p></a>
<a class="card" href="{COMPANY['maps']}" rel="noopener" target="_blank"><div class="ic">{I['pin']}</div><h3>{'Office' if lang=='en' else 'المكتب'}</h3><p>{COMPANY['address_'+lang]}</p></a></div>
<div class="soc-links" style="margin-top:26px">{soc}</div>
<div style="margin-top:34px;border-radius:var(--r-lg);overflow:hidden;border:1px solid var(--line)"><iframe title="FEFCO location" src="{map_q}" width="100%" height="380" style="border:0;display:block" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'''
    inner = f'<section class="band"><div class="wrap">{cards}</div></section>'
    if lang == "en":
        simple_page(lang, "contact", "Contact FEFCO Solutions | Call, WhatsApp or Visit Us in Dubai", "Contact FEFCO Solutions in Dubai: call or WhatsApp +971 50 786 7872, email info@fefco.ae. Free site surveys for solar, water heaters, EV chargers, plumbing and AMC across the UAE.", "Contact", "Talk to FEFCO", "Call, WhatsApp or send the form. A 24-hour emergency line is available for breakdowns.", inner, "contact")
    else:
        simple_page(lang, "contact", "تواصل مع فيفكو سوليوشنز | اتصل أو راسلنا عبر واتساب أو زرنا في دبي", "تواصل مع فيفكو سوليوشنز في دبي: اتصل أو راسلنا عبر واتساب على ‎+971 50 786 7872‎ أو عبر البريد info@fefco.ae. معاينة مجانية للطاقة الشمسية والسخانات وشواحن السيارات والسباكة وعقود الصيانة.", "تواصل معنا", "تحدث مع فيفكو", "اتصل بنا أو راسلنا عبر واتساب أو أرسل النموذج. يتوفر خط طوارئ على مدار 24 ساعة للأعطال.", inner, "contact")

def page_privacy(lang):
    if lang == "en":
        txt = ["This website is operated by FEFCO Electromechanical Services LLC (FEFCO Solutions), Dubai, UAE.", "When you send an enquiry, the details you enter (name, phone, email, service and message) open in WhatsApp and are shared with our sales team only to answer your request.", "We may use privacy-friendly analytics and advertising tags (such as Google Analytics or Meta Pixel) to understand visits and measure enquiries. You can block these with your browser settings.", "We do not sell personal data. To ask for your data to be deleted, email info@fefco.ae."]
        simple_page(lang, "privacy", "Privacy Policy | FEFCO Solutions", "How FEFCO Solutions handles personal data sent through fefco.ae.", "Legal", "Privacy policy", "Last updated " + TODAY + ".", '<section class="band"><div class="wrap prose" style="max-width:780px">' + "".join(f"<p>{t}</p>" for t in txt) + "</div></section>")
    else:
        txt = ["يدير هذا الموقع شركة فيفكو للخدمات الكهروميكانيكية ذ.م.م (فيفكو سوليوشنز)، دبي، الإمارات العربية المتحدة.", "عند إرسال استفسار، تُفتح البيانات التي تدخلها (الاسم والهاتف والبريد والخدمة والرسالة) في واتساب وتُشارك مع فريق المبيعات فقط للرد على طلبك.", "قد نستخدم أدوات تحليل وإعلانات (مثل Google Analytics أو Meta Pixel) لفهم الزيارات وقياس الاستفسارات، ويمكنك حظرها من إعدادات المتصفح.", "لا نبيع البيانات الشخصية. لطلب حذف بياناتك راسلنا على info@fefco.ae."]
        simple_page(lang, "privacy", "سياسة الخصوصية | فيفكو سوليوشنز", "كيف تتعامل فيفكو سوليوشنز مع البيانات الشخصية المرسلة عبر fefco.ae.", "قانوني", "سياسة الخصوصية", "آخر تحديث " + TODAY + ".", '<section class="band"><div class="wrap prose" style="max-width:780px">' + "".join(f"<p>{t}</p>" for t in txt) + "</div></section>")

def page_404():
    body = f'<section class="page-hero"><div class="wrap"><span class="kicker">404</span><h1>This page has moved</h1><p class="lead">The page you opened isn\'t here any more. Try the services list or contact us.</p><p><a class="btn btn-primary" href="/services/">All services {I["arr"]}</a> <a class="btn btn-wa" href="{wa_link()}">{I["wa"]}WhatsApp us</a></p></div></section>'
    out = head("en", "Page not found | FEFCO Solutions", "Page not found.", "") + header("en", "") + body + footer("en")
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f: f.write(out.replace('<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex">'))

# ---------- SEO / AI files ----------
def seo_files():
    paths = ["", "services", "products", "projects", "about", "contact", "privacy"] + [s["slug"] for s in SERVICES]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p in paths:
        for lang in ("en", "ar"):
            pr = "1.0" if p == "" else ("0.9" if p in BY_SLUG else "0.6")
            xml.append(f'<url><loc>{absu(lang, p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority><xhtml:link rel="alternate" hreflang="en" href="{absu("en", p)}"/><xhtml:link rel="alternate" hreflang="ar" href="{absu("ar", p)}"/><xhtml:link rel="alternate" hreflang="x-default" href="{absu("en", p)}"/></url>')
    xml.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml))
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended", "xAI-Bot", "Grok", "meta-externalagent", "DuckAssistBot", "CCBot"]
    robots = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + "User-agent: *\nAllow: /\n\nSitemap: https://fefco.ae/sitemap.xml\n"
    open(os.path.join(OUT, "robots.txt"), "w").write(robots)
    # llms.txt (answer-engine friendly summary)
    L = ["# FEFCO Solutions", "", "> FEFCO Solutions (legal name FEFCO Electromechanical Services LLC) is a Dubai, UAE company that designs, installs and maintains solar energy, water and electromechanical (MEP) systems for homes, businesses and industry across all seven emirates. Official dealer of Lamborghini Calorclima water heaters in the UAE; authorised MENA distributor of the EIRA solar asset-management platform by Inspire Clean Energy. Its AI division is FEFCO AI Solutions (fefcoaisolutions.com).", "",
         "## Key facts", f"- Phone / WhatsApp: {COMPANY['phone_main_disp']} (24-hour emergency line); also {COMPANY['phone_2_disp']}", f"- Email: {COMPANY['email']}, {COMPANY['email_solar']}", f"- Office: {COMPANY['address_en']}", "- Areas served: Dubai, Sharjah, Abu Dhabi, Ajman, Ras Al Khaimah, Fujairah, Umm Al Quwain, Al Ain", "- 700+ clients served; free site surveys; handles DEWA Shams Dubai net-metering applications", "- Languages: English, Arabic (website in both)", "- Brands supplied/serviced: " + ", ".join(BRANDS), "- Social: " + ", ".join(s[1] for s in SOCIAL if s[2] != 'wa'), "",
         "## Services"]
    for s in SERVICES:
        L.append(f"- [{s['en']['nav']}]({absu('en', s['slug'])}): {s['en']['d']}")
    L += ["", "## Pages", f"- [Home]({DOMAIN}/)", f"- [All services]({DOMAIN}/services/)", f"- [Products]({DOMAIN}/products/)", f"- [Projects]({DOMAIN}/projects/)", f"- [About]({DOMAIN}/about/)", f"- [Contact]({DOMAIN}/contact/)", f"- [Arabic site]({DOMAIN}/ar/)", "", "## Optional", f"- [Full service details for AI assistants]({DOMAIN}/llms-full.txt)"]
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    F = ["# FEFCO Solutions — full service reference", "", L[2], ""]
    for s in SERVICES:
        c = s["en"]
        F += [f"## {c['h1']}", f"URL: {absu('en', s['slug'])}", "", c["lead"], "", c["body"], "", "Includes: " + "; ".join(c["inc"]) + ".", "For: " + "; ".join(c["who"]) + ".", ""]
        F += [f"Q: {q}\nA: {a}\n" for q, a in c["faq"]]
    open(os.path.join(OUT, "llms-full.txt"), "w", encoding="utf-8").write("\n".join(F))
    # redirects from old WordPress URLs
    red = []
    for s in SERVICES:
        for o in s.get("old", []): red.append((o, "/" + s["slug"] + "/"))
    prod_old = ["solar-energy-storage-systempps-4kwh", "solar-energy-storage-systempps-2kwh", "solar-energy-storage-systemes-1000", "solar-energy-storage-systemes-500", "solar-power-systemcpes-150", "70-kwhair-cooled-distributed", "ggsp-610-650w610-650w", "gg-spi-series-solar-pump-inverter", "25-6v-100ah-lifepo4-battery", "51-2v-314ah-lifepo4-battery", "12-8v-200ah-lifepo4-battery", "12-8v-100ah-lifepo4-battery", "12-8v-300ahlifepo4", "51-2v-628ah-lifepo4-battery", "51-2v-200ah-lifepo4-battery", "6-0-kwh-lifepo4-battery", "12-8v-120ah-lifepo4-battery", "25-6v-200ahlifepo4-battery", "25-6v-200ah-stackablelifepo4", "ggiv-3p-14kw", "ggiv-1p-series", "ggiv-6kw", "24v-5000w-hybrid-lnverter-single-phase", "ggiv-2kw", "dc-solar-cable"]
    for p in prod_old: red.append(("/" + p + "/", "/products/"))
    red += [("/contact-us/", "/contact/"), ("/portfolio/", "/projects/"), ("/home/", "/"), ("/login/", "https://fefco.ae/"), ("/wp-admin/*", "/"), ("/hello-world/", "/")]
    seen = set(); lines = []
    for a, b in red:
        if a in seen: continue
        seen.add(a); lines.append(f"{a} {b} 301")
        if a.endswith("/") and "*" not in a: lines.append(f"{a.rstrip('/')} {b} 301")
    open(os.path.join(OUT, "_redirects"), "w").write("\n".join(lines) + "\n")
    vercel = {"cleanUrls": False, "trailingSlash": True, "redirects": [{"source": a.rstrip("/") or "/", "destination": b, "permanent": True} for a, b in red if "*" not in a],
              "headers": [{"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}]}
    open(os.path.join(OUT, "vercel.json"), "w").write(json.dumps(vercel, indent=1))

def favicon():
    from PIL import Image
    src = os.path.join(OUT, "assets", "fefco-solutions-logo.png")
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    # the sun "o" is the right-most ~28% of the wordmark — use it as the favicon, unchanged
    sun = im.crop((int(w * .735), 0, w, int(h * .77)))
    s = max(sun.size); canvas = Image.new("RGBA", (s, s), (255, 255, 255, 0)); canvas.paste(sun, ((s - sun.size[0]) // 2, (s - sun.size[1]) // 2), sun)
    canvas.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "assets", "favicon.png"))

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(os.path.dirname(__file__), "static"), OUT)
    favicon()
    for lang in ("en", "ar"):
        page_home(lang); page_services(lang); page_products(lang); page_projects(lang); page_about(lang); page_contact(lang); page_privacy(lang)
        for s in SERVICES: page_service(lang, s)
    page_404(); seo_files()
    open(os.path.join(os.path.dirname(__file__), "media.txt"), "w").write("\n".join(sorted(MEDIA_USED)) + "\n")
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print("built", n, "files;", len(SERVICES), "services x 2 languages")

if __name__ == "__main__":
    build()
