# FEFCO Solutions — SEO & AI-search plan

Built 2026-11-22. English pages live at `/slug/`, Arabic at `/ar/slug/`; each pair is linked with hreflang.

## Keyword map (one primary keyword per landing page)

| Page | Primary keyword | Long-tail / questions | Arabic |
|---|---|---|---|
| /solar-panel-installation-dubai/ | solar panel installation dubai | solar company dubai; rooftop solar dubai; shams dubai solar installer; solar pv system for villa dubai; how much does solar cost in dubai | تركيب الواح شمسية دبي; شركة طاقة شمسية في دبي |
| /solar-water-heater-dubai/ | solar water heater dubai | solar water heater price in uae; solar heater for villa; thermosiphon solar water heater; ariston solar water heater dubai | سخان شمسي دبي; سعر سخان المياه الشمسي |
| /solar-water-heater-repair-maintenance-dubai/ | solar water heater repair dubai | solar water heater maintenance dubai; solar heater not heating; solar water heater repair near me; ariston solar heater repair | تصليح سخان شمسي دبي; صيانة سخان شمسي |
| /solar-panel-cleaning-maintenance-dubai/ | solar panel cleaning dubai | solar panel maintenance uae; solar amc dubai; robotic solar panel cleaning; how often clean solar panels dubai | تنظيف الالواح الشمسية دبي; صيانة الطاقة الشمسية |
| /solar-battery-storage-dubai/ | solar battery uae | lifepo4 battery dubai; hybrid inverter uae; solar backup power villa; off grid solar system uae | بطارية طاقة شمسية; بطارية ليثيوم دبي |
| /ev-charger-installation-dubai/ | ev charger installation dubai | home ev charger dubai; ev wallbox installation; commercial ev charging uae; dewa ev charger | تركيب شاحن سيارة كهربائية دبي |
| /solar-carport-parking-shades/ | solar carport uae | solar parking shade dubai; solar car parking; carport with ev charger | مظلات سيارات شمسية |
| /solar-street-flood-lights/ | solar street light uae | solar flood light dubai; all in one solar street light; solar lights for farm | انارة شوارع بالطاقة الشمسية; كشاف شمسي |
| /solar-air-conditioners-uae/ | solar air conditioner uae | hybrid solar ac; dc solar ac for cabin; solar ac price dubai | مكيف شمسي |
| /lamborghini-calorclima-water-heaters-uae/ | lamborghini water heater uae | lamborghini calorclima dubai; electric water heater dubai; italian water heater | سخان لامبورغيني; سخان كهربائي دبي |
| /water-filtration-treatment-dubai/ | water filter dubai | whole house water filter dubai; ro system dubai; water softener uae; water treatment company dubai | فلتر مياه دبي; جهاز تحلية مياه منزلي |
| /grp-water-tanks-uae/ | grp water tank uae | grp tank dubai price; sectional water tank; water tank cleaning dubai | خزان فايبر جلاس; تنظيف خزانات المياه دبي |
| /water-chillers-uae/ | water chiller uae | water tank chiller dubai; hot tap water summer uae | مبرد مياه الخزان |
| /plumbing-services-dubai/ | plumber dubai | plumbing services dubai; emergency plumber dubai; water leak repair dubai; water pump repair dubai | سباك دبي; خدمات سباكة |
| /amc-annual-maintenance-contract-dubai/ | amc dubai | annual maintenance contract dubai; mep maintenance company dubai; villa maintenance contract | عقد صيانة سنوي دبي |
| /electromechanical-mep-services-dubai/ | electromechanical company dubai | mep contractor dubai; electrical contractor dubai; mep services uae | شركة كهروميكانيك دبي |
| /energy-audit-dubai/ | energy audit dubai | reduce dewa bill; energy efficiency consultant uae | تدقيق الطاقة دبي |
| /daylighting-ventilation-air-curtains/ | tubular skylight uae | daylighting system dubai; roof ventilator uae; air curtain dubai | اضاءة طبيعية; ستارة هوائية |
| /solar-cctv-cameras-uae/ | solar cctv camera uae | 4g solar camera dubai; farm security camera; solar wifi camera | كاميرا مراقبة بالطاقة الشمسية |
| /iot-solar-monitoring-eira/ | solar asset management platform | solar monitoring software uae; eira inspire clean energy; solar o&m software mena | منصة ادارة الطاقة الشمسية |
| /suitx-exoskeletons-uae/ | suitx exoskeleton uae | industrial exoskeleton dubai; backx; shoulderx; legx | هيكل خارجي صناعي |

## What's already built in
- Unique title, meta description, H1 and canonical on all 56 pages (EN + AR)
- hreflang en / ar / x-default on every page and in sitemap.xml
- Schema.org JSON-LD: Organization + LocalBusiness (with sameAs socials and FEFCO AI Solutions as sub-organization), Service per landing page, FAQPage, BreadcrumbList
- Answer-first 'At a glance' summary on every service page and 4 FAQs per service (the format ChatGPT, Perplexity, Google AI Mode and Grok quote)
- /llms.txt and /llms-full.txt: plain-text company facts and every service for AI assistants
- robots.txt explicitly allows GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended, Applebot, xAI/Grok, Bingbot
- 301 redirects from every old WordPress URL (/solar-pv-systems/, product pages, /contact-us/, /portfolio/ …) in `_redirects` and `vercel.json`, so existing Google rankings carry over
- Fast static pages: no WordPress, no page builder; images lazy-loaded
- Conversion: sticky WhatsApp + quote in header, floating WhatsApp, mobile call/WhatsApp/quote bar, solar savings estimator, form that opens a pre-filled WhatsApp, dataLayer events (generate_lead, click_whatsapp, click_call) ready for GA4 / Google Ads / Meta

## To do after launch (owner actions)
1. Google Search Console + Bing Webmaster: verify fefco.ae, submit /sitemap.xml, request indexing of the 21 service pages.
2. Google Business Profile: match name, address and phone exactly to the website; add all services, photos and the website link; ask every happy customer for a review (reviews are the #1 local and AI-answer signal).
3. Same NAP on ReachUAE, Yellow Pages UAE, Dubizzle services, ServiceMarket, Bing Places and Apple Business Connect.
4. Create a LinkedIn company page and add it to the site footer and schema sameAs.
5. Publish 2 guides a month (e.g. 'Solar panel cost in Dubai 2026', 'Why is my solar water heater not hot?', 'Shams Dubai step by step') linking to the matching service page.
6. Add GA4 + Google Ads + Meta Pixel IDs (the site already pushes lead events to dataLayer).
7. Replace the leader name placeholder once confirmed, and add real customer reviews only with permission.
