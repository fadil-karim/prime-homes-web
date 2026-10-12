#!/usr/bin/env python3
"""Generate the pages in public/ from the templates in this file and tools/properties.json.

Nothing here runs on Cloudflare: the generated files are committed and served as they
are. Run it after editing properties.json or a template, look at the result, then commit.

    python3 tools/render.py
"""
import datetime
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
TOOLS = ROOT / "tools"

SITE = "https://primegroupuk.com"
COMPANY = "Prime Homes Estate Agents Ltd"
PHONE_DISPLAY = "020 8767 3838"
PHONE_TEL = "+442087673838"
EMAIL = "info@primehomesuk.com"
ADDRESS_LINES = ["16 Upper Tooting Road", "London", "SW17 7PG"]
PORTAL = "https://www.primegroupuk.com/login/"
APP_IOS = "https://apps.apple.com/us/app/prime-homes-estate-agents-ltd/id1632376416"
APP_ANDROID = "https://play.google.com/store/apps/details?id=prime.globalnoticeboard.com"
TODAY = datetime.date.today().isoformat()

PROPERTY_TYPES = [
    "Flat", "Bedsit", "Block of Flats", "Bungalow", "Bungalow - Semi Detached", "Commercial",
    "House - Detached", "House - Semi Detached", "House - Terraced", "House - Town", "Farm",
    "Garage", "Land", "Maisonette", "Office", "Restaurant", "Warehouse",
]
SALES_FEATURES = [
    "Kitchen-Diner", "Off-road Parking", "On-road Parking", "Garden", "Wheelchair Access",
    "Elevator in Building", "Pool", "Gym", "En-suite", "Secure Car parking", "Open Plan Lounge",
    "Video Door Entry", "Valet Parking", "Sun Deck Terrace", "Concierge services", "Fridge Freezer",
    "Microwave", "Full Double Glazing", "Washing Machine", "Oven/Hob", "Burglar Alarm",
    "Gas Central Heating Combi Boiler", "Balcony", "Double Bedrooms", "Large Gardens", "Fireplace",
]
LETTINGS_FEATURES = [
    "Kitchen-Diner", "Off-road Parking", "On-road Parking", "Garden", "Wheelchair Access",
    "Elevator in Building", "Pool", "Gym", "Dining Room", "Furnished", "Internet", "Wireless Internet",
    "TV", "Washer", "Dryer", "Dishwasher", "Pets Allowed", "Family/Child Friendly", "DSS Allowed",
    "Smoking Allowed", "24/7 Security", "Hot Tub", "Cleaner", "En-suite", "Secure Car parking",
    "Open Plan Lounge", "Video Door Entry", "Valet Parking", "Sun Deck Terrace", "Concierge services",
    "Fridge Freezer", "Microwave", "Full Double Glazing", "Washing Machine", "Oven/Hob", "Burglar Alarm",
    "Gas Central Heating Combi Boiler", "Balcony", "Double Bedrooms", "Large Gardens", "Fireplace",
]
TESTIMONIALS = [
    ("Graham Byers", "Resident",
     "My family live in one of there blocks close to St. George's hospital and is close to the local shops, and for commuting Tooting Broadway station is a five minute walk away, very clean blocks and friendly and helpful staff. A very good place to live."),
    ("Amanda Blandford", "Tenant",
     "This is a wonderful estate agents. They are so helpful and friendly and reliable. I have been a tenant for a number of years and could not be happier. I couldn’t praise them any higher. I would recommend them to everyone I could. Their properties are to a very high standard and clean-you couldn’t wish for a better home."),
    ("Omid Omary", "Customer",
     "Thank you to all Manegment and all staff of Prime Group the are all ways nice and kind and honest with customer and there services excellent. I wish them all the best, best regards Omary"),
]
ACCREDITATIONS = [
    ("aff-dps", "Deposit Protection Service"),
    ("aff-nrla", "National Residential Landlords Association"),
    ("aff-property_redress_scheme", "Property Redress Scheme"),
    ("aff-residential_landlord", "Residential Landlords Association"),
    ("aff-ukala", "UKALA, the UK Association of Letting Agents"),
    ("aff-ico", "Information Commissioner's Office"),
    ("aff-gnb", "gnb Property Software"),
]
NAV = [
    ("/sales", "For Sale"), ("/lettings", "To Rent"), ("/services", "Services"),
    ("/valuation", "Valuation"), ("/projects", "Projects"), ("/testimonials", "Testimonials"),
    ("/contact", "Contact"),
]


def e(value):
    return html.escape(str(value), quote=True)


def T(template, **values):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(values.get(m.group(1), "")), template)


def icon(name):
    return f'<svg class="icon" aria-hidden="true"><use href="/assets/img/icons.svg#{name}"></use></svg>'


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def mailto(subject, body=""):
    from urllib.parse import quote
    return f"mailto:{EMAIL}?subject={quote(subject)}" + (f"&body={quote(body)}" if body else "")


# ----------------------------------------------------------------------------- layout

HEADER = """<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/"><img src="/assets/img/logo.png" alt="" width="34" height="51"><span>Prime Homes<small>Estate Agents Ltd</small></span></a>
    <nav class="nav" id="nav" aria-label="Main">{{nav}}</nav>
    <div class="header-actions">
      <a class="btn btn-ghost btn-sm" href="{{portal}}" target="_blank" rel="noopener">Login</a>
      <a class="btn btn-primary btn-sm" href="/valuation">Free valuation</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><svg class="icon i-menu" aria-hidden="true"><use href="/assets/img/icons.svg#menu"></use></svg><svg class="icon i-close" aria-hidden="true"><use href="/assets/img/icons.svg#close"></use></svg></button>
    </div>
  </div>
</header>"""

ACCREDITATIONS_HTML = """<section class="accreditations" aria-label="Accreditations and memberships">
  <div class="container">
    <p>Registered and affiliated with</p>
    <div class="logo-row">{{logos}}</div>
  </div>
</section>"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="footer-brand" href="/"><img src="/assets/img/logo.png" alt="" width="32" height="48"><span>Prime Homes<small>Estate Agents Ltd</small></span></a>
        <p>A family-run real estate development and investment business, based in south west London since 2000, with an in-house estate agency and property management team.</p>
      </div>
      <div>
        <h4>Quick links</h4>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/sales">Sales</a></li>
          <li><a href="/lettings">Lettings</a></li>
          <li><a href="/mortgages">Mortgages</a></li>
          <li><a href="/projects">Upcoming projects</a></li>
          <li><a href="/contact">Contact us</a></li>
        </ul>
      </div>
      <div>
        <h4>Popular searches</h4>
        <ul>
          <li><a href="/valuation">Free instant valuation</a></li>
          <li><a href="/sales?q=Tooting">Property for sale in Tooting</a></li>
          <li><a href="/lettings?q=SW17">Property to rent in SW17</a></li>
          <li><a href="/lettings?cat=commercial">Commercial lettings</a></li>
          <li><a href="/privacy">Privacy policy</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact us</h4>
        <ul class="contact-list">
          <li>{{i_mail}}<a href="mailto:{{email}}">{{email}}</a></li>
          <li>{{i_phone}}<a href="tel:{{tel}}">{{phone}}</a></li>
          <li>{{i_pin}}<span>{{address}}</span></li>
          <li>{{i_clock}}<span>Monday to Friday, 10:30am to 6pm<br>Saturday and Sunday closed</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>&copy; <span data-year>{{year}}</span> {{company}}. All rights reserved.</div>
      <ul>
        <li><a href="/privacy">Privacy policy</a></li>
        <li><a href="{{portal}}" target="_blank" rel="noopener">Customer portal</a></li>
      </ul>
    </div>
  </div>
</footer>"""

LAYOUT = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<meta name="description" content="{{description}}">
<link rel="canonical" href="{{site}}{{path}}">
<meta property="og:site_name" content="{{company}}">
<meta property="og:title" content="{{title}}">
<meta property="og:description" content="{{description}}">
<meta property="og:type" content="website">
<meta property="og:url" content="{{site}}{{path}}">
<meta property="og:image" content="{{site}}{{og_image}}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#AE0033">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
{{extra_head}}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{{header}}
<main id="main">
{{body}}
</main>
{{accreditations}}
{{footer}}
<script src="/assets/js/properties.js"></script>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def layout(*, title, description, path, body, active=None, og_image="/assets/img/hero.jpg", extra_head=""):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for href, label in NAV
    )
    header = T(HEADER, nav=nav, portal=PORTAL)
    logos = "".join(
        f'<img src="/assets/img/{f}.png" alt="{e(alt)}" loading="lazy" height="44">' for f, alt in ACCREDITATIONS
    )
    footer = T(
        FOOTER, i_mail=icon("mail"), i_phone=icon("phone"), i_pin=icon("pin"), i_clock=icon("clock"),
        email=EMAIL, tel=PHONE_TEL, phone=PHONE_DISPLAY, address="<br>".join(ADDRESS_LINES),
        year=datetime.date.today().year, company=COMPANY, portal=PORTAL,
    )
    return T(
        LAYOUT, title=e(title), description=e(description), site=SITE, path=path, company=COMPANY,
        og_image=og_image, extra_head=extra_head, header=header, body=body,
        accreditations=T(ACCREDITATIONS_HTML, logos=logos), footer=footer,
    )


# ----------------------------------------------------------------------------- shared pieces

def badge(p):
    if p["status"] == "let":
        return '<span class="badge let">Let</span>'
    if p["status"] == "sold":
        return '<span class="badge sold">Sold</span>'
    return '<span class="badge sale">For sale</span>' if p["market"] == "sales" else '<span class="badge rent">To rent</span>'


def card(p):
    """Property card. Keep in step with card() in public/assets/js/site.js."""
    img = p.get("thumb") or p["images"][0]
    specs = []
    if p.get("beds"):
        specs.append(f'<span>{icon("bed")}{plural(p["beds"], "bed")}</span>')
    if p.get("baths"):
        specs.append(f'<span>{icon("bath")}{plural(p["baths"], "bath")}</span>')
    if p.get("receptions"):
        specs.append(f'<span>{icon("sofa")}{plural(p["receptions"], "reception")}</span>')
    if p.get("type"):
        specs.append(f'<span>{icon("tag")}{e(p["type"])}</span>')
    summary = f'<p class="prop-summary">{e(p["summary"])}</p>' if p.get("summary") else ""
    return (
        f'<a class="prop-card" href="/property/{e(p["slug"])}">'
        f'<div class="prop-media"><img src="/assets/img/{e(img)}.jpg" alt="{e(p["title"])}" loading="lazy" width="640" height="480">{badge(p)}'
        f'<span class="badge-count">{icon("camera")}{len(p["images"])}</span></div>'
        f'<div class="prop-body"><div class="prop-price">{e(p["priceLabel"])}</div>'
        f'<h3 class="prop-title">{e(p["title"])}</h3>'
        f'<div class="prop-area">{icon("pin")}{e(p["area"])}</div>'
        f'{summary}<div class="specs">{"".join(specs)}</div></div></a>'
    )


def page_head(title, lede, crumbs):
    trail = "".join(f"<span><a href=\"{href}\">{e(label)}</a></span>" if href else f"<span>{e(label)}</span>" for href, label in crumbs)
    return T(
        """<section class="page-head"><div class="container">
  <nav class="crumbs" aria-label="Breadcrumb">{{trail}}</nav>
  <h1>{{title}}</h1>
  <p class="lede">{{lede}}</p>
</div></section>""",
        trail=trail, title=e(title), lede=lede,
    )


def testimonial(name, role, quote):
    initials = "".join(part[0] for part in name.split()[:2]).upper()
    return T(
        """<figure class="card testimonial">
  <div class="quote-mark" aria-hidden="true">&ldquo;</div>
  <blockquote>{{quote}}</blockquote>
  <figcaption><span class="avatar" aria-hidden="true">{{initials}}</span><span>{{name}}<small>{{role}}</small></span></figcaption>
</figure>""",
        quote=e(quote), initials=initials, name=e(name), role=e(role),
    )


def field(label, control, hint=""):
    hint_html = f'<p class="hint">{hint}</p>' if hint else ""
    return f'<div class="field"><span class="label">{label}</span>{control}{hint_html}</div>'


def labelled(label, control_id, control, cls="field"):
    return f'<div class="{cls}"><label for="{control_id}">{label}</label>{control}</div>'


FORM_NOTE = """<p class="form-note" role="status">Thanks. Your email app should now open with everything filled in; just press send. If it does not open, email us at <a href="mailto:{{email}}">{{email}}</a> or call <a href="tel:{{tel}}">{{phone}}</a>.</p>"""


def form_note():
    return T(FORM_NOTE, email=EMAIL, tel=PHONE_TEL, phone=PHONE_DISPLAY)


# ----------------------------------------------------------------------------- pages

def page_home(props):
    cards = "".join(card(p) for p in props)
    tests = "".join(testimonial(*t) for t in TESTIMONIALS)
    body = T("""<section class="hero">
  <div class="hero-media"><img src="/assets/img/hero.jpg" alt="Victorian terraced houses on Dafforne Road in Tooting" width="1600" height="1065" fetchpriority="high"></div>
  <div class="container">
    <p class="eyebrow">Estate agents &middot; Tooting, SW17</p>
    <h1>Find your next home in south west London.</h1>
    <p>Sales, lettings and property management from a family-run property group, based in south west London since 2000.</p>
  </div>
</section>
<div class="container search-wrap">
  <form class="search-card" id="home-search" action="/sales" method="get" aria-label="Property search">
    <div class="field"><label for="s-category">I'm looking for</label><select class="select" id="s-category" name="category"><option value="residential-sales">Residential sales</option><option value="residential-lettings">Residential lettings</option><option value="commercial-sales">Commercial sales</option><option value="commercial-lettings">Commercial lettings</option></select></div>
    <div class="field"><label for="s-q">Location</label><input class="input" id="s-q" name="q" type="text" placeholder="e.g. Tooting, SW17, street name" autocomplete="off"></div>
    <div class="field"><label for="s-min">Min price</label><input class="input" id="s-min" name="min_price" type="text" inputmode="numeric" placeholder="&pound; Any"></div>
    <div class="field"><label for="s-beds">Min bedrooms</label><input class="input" id="s-beds" name="beds_min" type="number" min="0" max="20" placeholder="Any"></div>
    <button class="btn btn-primary" type="submit">{{i_search}} Search</button>
  </form>
  <div class="stats">
    <div class="stat"><strong>Since 2000</strong><span>Family-run and independent</span></div>
    <div class="stat"><strong>Sales &amp; lettings</strong><span>Residential and commercial</span></div>
    <div class="stat"><strong>In-house management</strong><span>Looking after our own portfolio</span></div>
    <div class="stat"><strong>Tooting, SW17</strong><span>16 Upper Tooting Road</span></div>
  </div>
</div>

<section class="section" id="about">
  <div class="container about-grid">
    <div>
      <p class="eyebrow">About us</p>
      <h2>A family-run property group, rooted in south west London.</h2>
      <p>Established in 2000, Prime Group is a family-run real estate development and investment business based primarily in south west London. We specialize in building and delivering high quality build to rent homes and semi commercial properties.</p>
      <p>Our team identifies underutilized sites and we take a collaborative approach with local councils and communities to create welcoming and sustainable places to live and work. Recently the group is also exploring real estate opportunities abroad with a view of market diversification.</p>
      <ul class="about-points">
        <li>{{i_check}}<span>Our in-house estate agency and property management team provide aftercare service to the group's property portfolio.</span></li>
        <li>{{i_check}}<span>Managing our own homes keeps a pulse on local market trends and gives valuable insight into arising opportunities and challenges.</span></li>
        <li>{{i_check}}<span>Registered with the ICO and affiliated with the DPS, NRLA, Property Redress Scheme, RLA and UKALA.</span></li>
      </ul>
      <a class="btn btn-outline" href="/contact">Talk to the team {{i_arrow}}</a>
    </div>
    <div class="about-media">
      <img src="/assets/img/dafforne-5.jpg" alt="Open-plan kitchen with bi-fold doors onto a garden" width="1200" height="797" loading="lazy">
      <div class="float"><strong>25+ years</strong><span>building, letting and managing homes in south west London</span></div>
    </div>
  </div>
</section>

<section class="section section-sand" id="services">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow">Our services</p>
      <h2>Everything under one roof.</h2>
      <p class="lede">From finding tenants to selling your home, the same local team looks after you from the first viewing to the day you move.</p>
    </div>
    <div class="grid grid-4">
      <div class="card service-card"><div class="icon-badge green">{{i_key}}</div><h3>For rent</h3><p>Find out how our award winning service can help you with your rental property.</p><a class="link" href="/lettings">Properties to rent {{i_arrow}}</a></div>
      <div class="card service-card"><div class="icon-badge">{{i_home}}</div><h3>For sale</h3><p>We are here to help get you moving.</p><a class="link" href="/sales">Properties for sale {{i_arrow}}</a></div>
      <div class="card service-card"><div class="icon-badge green">{{i_gavel}}</div><h3>Auctions</h3><p>A quick and secure way of selling your property.</p><a class="link" href="/contact">Ask about auctions {{i_arrow}}</a></div>
      <div class="card service-card"><div class="icon-badge">{{i_calc}}</div><h3>Instant valuation</h3><p>Instant sales and rental valuations for your property.</p><a class="link" href="/valuation">Get a valuation {{i_arrow}}</a></div>
    </div>
  </div>
</section>

<section class="section" id="featured">
  <div class="container">
    <div class="results-bar" style="align-items:flex-end;margin-bottom:2rem">
      <div class="section-head" style="margin:0"><p class="eyebrow">Featured properties</p><h2 style="margin:0">Our latest homes and spaces.</h2></div>
      <a class="btn btn-outline btn-sm" href="/sales">View all properties {{i_arrow}}</a>
    </div>
    <div class="grid grid-3">{{cards}}</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="cta-band">
      <div><h2>Looking for somewhere new?</h2><p>We have properties available now. Take a look, or tell us what you need and we will keep an eye out for you.</p></div>
      <div class="actions"><a class="btn btn-light" href="/sales">For sale</a><a class="btn btn-outline" href="/lettings">To rent</a><a class="btn btn-outline" href="/valuation">Value my property</a></div>
    </div>
  </div>
</section>

<section class="section section-paper" id="app">
  <div class="container app-grid">
    <div>
      <p class="eyebrow green">Prime Home app</p>
      <h2>Search, save and enquire on the go.</h2>
      <p class="lede">The Prime Home app puts our sales and lettings in your pocket, with viewings and enquiries a tap away. Free on iPhone and Android.</p>
      <div class="store-buttons">
        <a class="store-btn" href="{{app_ios}}" target="_blank" rel="noopener">{{i_apple}}<span><small>Download on the</small>App Store</span></a>
        <a class="store-btn" href="{{app_android}}" target="_blank" rel="noopener">{{i_play}}<span><small>Get it on</small>Google Play</span></a>
      </div>
    </div>
    <img src="/assets/img/app-mockup.png" alt="The Prime Home app on two phones, showing the home screen and a property listing" width="600" height="656" loading="lazy">
  </div>
</section>

<section class="section" id="testimonials">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow">Testimonials</p>
      <h2>What our clients say.</h2>
    </div>
    <div class="grid grid-3">{{tests}}</div>
    <p class="text-center mt-2"><a class="btn btn-ghost" href="/testimonials">Read more testimonials {{i_arrow}}</a></p>
  </div>
</section>""",
        i_search=icon("search"), i_check=icon("check"), i_arrow=icon("arrow-right"), i_key=icon("key"),
        i_home=icon("home"), i_gavel=icon("gavel"), i_calc=icon("calculator"), i_apple=icon("apple"),
        i_play=icon("play"), cards=cards, tests=tests, app_ios=APP_IOS, app_android=APP_ANDROID,
    )
    return layout(
        title="Prime Homes Estate Agents Ltd | Sales and lettings in Tooting, south west London",
        description="Family-run estate agents in Tooting, SW17. Search properties for sale and to rent, get a free instant valuation, or talk to our in-house lettings and property management team.",
        path="/", body=body,
    )


def page_listing(market, props):
    sales = market == "sales"
    label = "Properties for sale" if sales else "Properties to rent"
    lede = ("Homes and commercial premises for sale across Tooting and south west London. Narrow the list with the filters, then book a viewing online."
            if sales else
            "Flats, houses and commercial space to let across Tooting and south west London. Narrow the list with the filters, then book a viewing online.")
    available = [p for p in props if p["market"] == market and p["status"] == "available"]
    cards = "".join(card(p) for p in available)
    features = SALES_FEATURES if sales else LETTINGS_FEATURES
    checks = "".join(
        f'<label class="check"><input type="checkbox" name="feature" value="{e(f)}"> {e(f)}</label>' for f in features
    )
    types = "".join(f'<option value="{e(t)}">{e(t)}</option>' for t in PROPERTY_TYPES)
    body = page_head(label, lede, [("/", "Home"), (None, label)]) + T("""<section class="section" style="padding-top:clamp(32px,4vw,48px)">
<div class="container listing" data-listing="{{market}}">
  <div>
    <div class="results-bar">
      <h2 id="results-count" aria-live="polite">{{count}}</h2>
      <div style="display:flex;gap:.6rem;align-items:center;flex-wrap:wrap">
        <button class="btn btn-outline btn-sm filters-toggle" type="button" aria-expanded="false" aria-controls="filters">{{i_sliders}} Filters</button>
        <label class="sort">Sort <select class="select" id="sort"><option value="">Featured</option><option value="price_max">Price: highest first</option><option value="price_min">Price: lowest first</option></select></label>
      </div>
    </div>
    <div class="results grid grid-2" id="results">{{cards}}</div>
  </div>
  <form class="filters" id="filters" aria-label="Narrow your search">
    <h2>Narrow your search</h2>
    <div class="field"><label for="f-q">Location</label><input class="input" id="f-q" name="q" type="text" placeholder="e.g. street, area, postcode" autocomplete="off"></div>
    <div class="field"><label for="f-cat">Category</label><select class="select" id="f-cat" name="cat"><option value="">Residential and commercial</option><option value="residential">Residential</option><option value="commercial">Commercial</option></select></div>
    <div class="field"><span class="label">Price</span><div class="row"><input class="input" name="min_price" type="text" inputmode="numeric" placeholder="&pound; Min" aria-label="Minimum price"><input class="input" name="max_price" type="text" inputmode="numeric" placeholder="&pound; Max" aria-label="Maximum price"></div></div>
    <div class="field"><span class="label">Bedrooms</span><div class="row"><input class="input" name="beds_min" type="number" min="0" placeholder="Min" aria-label="Minimum bedrooms"><input class="input" name="beds_max" type="number" min="0" placeholder="Max" aria-label="Maximum bedrooms"></div></div>
    <div class="field"><span class="label">Bathrooms</span><div class="row"><input class="input" name="baths_min" type="number" min="0" placeholder="Min" aria-label="Minimum bathrooms"><input class="input" name="baths_max" type="number" min="0" placeholder="Max" aria-label="Maximum bathrooms"></div></div>
    <div class="field"><span class="label">Reception rooms</span><div class="row"><input class="input" name="rec_min" type="number" min="0" placeholder="Min" aria-label="Minimum reception rooms"><input class="input" name="rec_max" type="number" min="0" placeholder="Max" aria-label="Maximum reception rooms"></div></div>
    <div class="field"><label for="f-type">Property type</label><select class="select" id="f-type" name="type"><option value="">Any property type</option>{{types}}</select></div>
    <details><summary>Features</summary><div class="checks">{{checks}}</div></details>
    <div class="actions"><button class="btn btn-primary" type="submit">{{i_search}} Search</button><button class="btn btn-ghost btn-sm" type="button" data-reset>Clear filters</button></div>
  </form>
</div>
</section>""",
        market=market, count=plural(len(available), "property").replace("propertys", "properties"),
        i_sliders=icon("sliders"), i_search=icon("search"), cards=cards, types=types, checks=checks,
    )
    return layout(
        title=f"{label} in Tooting and south west London | Prime Homes Estate Agents Ltd",
        description=lede, path=f"/{market}", body=body, active=f"/{market}",
    )


def page_property(p):
    sales = p["market"] == "sales"
    market_label = "For sale" if sales else "To rent"
    n = len(p["images"])
    thumbs = "".join(
        f'<button type="button" class="{"is-active" if i == 0 else ""}" aria-label="Photo {i + 1} of {n}"><img src="/assets/img/{e(img)}.jpg" alt="" loading="lazy" width="224" height="168"></button>'
        for i, img in enumerate(p["images"])
    )
    specs = []
    if p.get("beds"):
        specs.append(f'<span>{icon("bed")}{plural(p["beds"], "bedroom")}</span>')
    if p.get("baths"):
        specs.append(f'<span>{icon("bath")}{plural(p["baths"], "bathroom")}</span>')
    if p.get("receptions"):
        specs.append(f'<span>{icon("sofa")}{plural(p["receptions"], "reception room")}</span>')
    specs.append(f'<span>{icon("tag")}{e(p["type"])}</span>')
    if p.get("tenure"):
        specs.append(f'<span>{icon("shield")}{e(p["tenure"])}</span>')

    rows = [("Reference number", p.get("reference")), ("Property type", p.get("type")),
            ("Tenure", p.get("tenure")), ("Length of lease", p.get("leaseLength")),
            ("Furnishing", p.get("furnishing")), ("Letting classification", p.get("lettingType")),
            ("Available from", p.get("availableFrom")), ("Deposit amount", p.get("deposit")),
            ("Garden", "Yes" if "Garden" in p.get("features", []) else None),
            ("En-suite", "Yes" if "En-suite" in p.get("features", []) else None)]
    info = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in rows if v)
    paras = "".join(f"<p>{e(d)}</p>" for d in p.get("description", []))
    features = ""
    if p.get("features"):
        items = "".join(f"<li>{icon('check')}{e(f)}</li>" for f in p["features"])
        features = f'<section><h2>Features</h2><ul class="feature-list">{items}</ul></section>'
    from urllib.parse import quote
    map_src = f"https://www.google.com/maps?q={quote(p['mapQuery'])}&output=embed"
    is_let = p["status"] == "let"
    status_note = ('<p class="status-note">This property has now been let. Ask us about similar homes and we will let you know as soon as something suitable comes up.</p>'
                   if is_let else
                   f'<p class="meta">{market_label} &middot; Ref {e(p["reference"])}</p>')
    modal_title = "Ask about similar homes" if is_let else "Request a viewing"
    subject = (f"Enquiry about homes similar to {p['title']} ({p['reference']})" if is_let
               else f"Viewing request: {p['title']} ({p['reference']})")
    email_href = mailto(f"Enquiry: {p['title']} ({p['reference']})", f"Hello,\n\nI am interested in {p['title']} ({p['priceLabel']}, ref {p['reference']}).\n\n")
    times = "".join(f'<option>{h:02d}:{m}</option>' for h in range(11, 18) for m in ("00", "30")) + "<option>18:00</option>"
    titles = "".join(f"<option>{t}</option>" for t in ["Mr", "Mrs", "Ms", "Miss", "Dr", "Sir", "Lord", "Other"])

    body = T("""<div class="container" style="padding-top:1.5rem">
  <nav class="crumbs" aria-label="Breadcrumb"><span><a href="/">Home</a></span><span><a href="/{{market}}">{{market_label}}</a></span><span>{{title}}</span></nav>
  <div class="gallery" data-gallery='{{gallery_json}}'>
    <div class="gallery-main"><img src="/assets/img/{{img0}}.jpg" alt="{{title}}" width="1200" height="800" fetchpriority="high">{{badge}}<span class="btn btn-sm btn-expand">{{i_max}} View all {{n}} photos</span></div>
    <div class="thumbs">{{thumbs}}</div>
  </div>
  <div class="prop-head">
    <div><h1>{{title}}</h1><div class="prop-area">{{i_pin}}{{area}}</div></div>
    <div class="price">{{price}}<small>Ref {{reference}}</small></div>
  </div>
  <div class="key-specs">{{specs}}</div>
  <div class="prop-layout">
    <div class="prop-main">
      <section><h2>Property description</h2>{{paras}}</section>
      <section><h2>Property information</h2><dl class="info-table">{{info}}</dl></section>
      {{features}}
      <section><h2>Location</h2><p class="meta" style="color:var(--muted)">{{area}}</p><div class="map"><iframe title="Map showing {{title}}" src="{{map_src}}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></section>
      <section><h2>Share this property</h2><div class="share"><a href="#" data-share="facebook">Facebook</a><a href="#" data-share="x">X</a><a href="#" data-share="linkedin">LinkedIn</a><a href="#" data-share="whatsapp">WhatsApp</a><a href="#" data-share="email">Email</a></div></section>
    </div>
    <aside class="agent-card">
      <div class="card">
        <div class="price">{{price}}</div>
        {{status_note}}
        <button class="btn btn-primary btn-block" type="button" data-open-modal>{{i_cal}} {{modal_title}}</button>
        <a class="btn btn-outline btn-block" href="tel:{{tel}}">{{i_phone}} Call {{phone}}</a>
        <a class="btn btn-ghost btn-block" href="{{email_href}}">{{i_mail}} Email about this property</a>
        <p class="meta">Already a customer? <a href="{{portal}}" target="_blank" rel="noopener">Log in to the customer portal</a> to submit an enquiry.</p>
      </div>
      <div class="card">
        <strong>Prime Homes Estate Agents Ltd</strong>
        <p class="meta">{{address}}<br>Monday to Friday, 10:30am to 6pm</p>
      </div>
    </aside>
  </div>
</div>

<div class="modal" id="viewing-modal" role="dialog" aria-modal="true" aria-labelledby="viewing-title">
  <div class="modal-box">
    <button class="modal-close" type="button" aria-label="Close">{{i_close}}</button>
    <h2 id="viewing-title">{{modal_title}}</h2>
    <p class="meta" style="color:var(--muted);margin-bottom:1.25rem">{{title}} &middot; {{price}}</p>
    <form data-mailto data-subject="{{subject}}" data-intro="{{intro}}" novalidate="false">
      <div class="form-grid">
        <div class="field"><label for="v-date">Preferred date</label><input class="input" id="v-date" name="date" type="date" data-label="Preferred date"></div>
        <div class="field"><label for="v-time">Preferred time</label><select class="select" id="v-time" name="time" data-label="Preferred time"><option value="">Any time</option>{{times}}</select></div>
        <div class="field full"><label class="check"><input type="checkbox" name="flexible" data-label="Flexible on date and time"> I'm flexible on date and time</label></div>
        <div class="field"><label for="v-title">Title</label><select class="select" id="v-title" name="title" data-label="Title">{{titles}}</select></div>
        <div class="field"><label for="v-first">First name</label><input class="input" id="v-first" name="first_name" type="text" required autocomplete="given-name" data-label="First name"></div>
        <div class="field"><label for="v-last">Last name</label><input class="input" id="v-last" name="last_name" type="text" required autocomplete="family-name" data-label="Last name"></div>
        <div class="field"><span class="label">Preferred contact</span><div class="radio-row"><label class="radio-pill"><input type="radio" name="contact" value="Phone" data-label="Preferred contact" checked><span>Phone</span></label><label class="radio-pill"><input type="radio" name="contact" value="Email" data-label="Preferred contact"><span>Email</span></label><label class="radio-pill"><input type="radio" name="contact" value="Either" data-label="Preferred contact"><span>Either</span></label></div></div>
        <div class="field"><label for="v-email">Email</label><input class="input" id="v-email" name="email" type="email" required autocomplete="email" data-label="Email"></div>
        <div class="field"><label for="v-phone">Contact number</label><input class="input" id="v-phone" name="phone" type="tel" required autocomplete="tel" data-label="Contact number"></div>
      </div>
      <p class="form-foot">Pressing submit opens your email app with the request filled in, ready to send to {{email}}. We never share your details.</p>
      <button class="btn btn-primary btn-block" type="submit">Submit request</button>
      {{form_note}}
    </form>
  </div>
</div>

<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo gallery">
  <button class="lb-close" type="button" aria-label="Close">{{i_close}}</button>
  <button class="lb-prev" type="button" aria-label="Previous photo">{{i_prev}}</button>
  <img src="/assets/img/{{img0}}.jpg" alt="{{title}}">
  <button class="lb-next" type="button" aria-label="Next photo">{{i_next}}</button>
  <div class="lb-count">1 / {{n}}</div>
</div>""",
        market=p["market"], market_label=market_label, title=e(p["title"]), gallery_json=json.dumps(p["images"]),
        img0=e(p["images"][0]), badge=badge(p), i_max=icon("maximize"), n=n, thumbs=thumbs, i_pin=icon("pin"),
        area=e(p["area"]), price=e(p["priceLabel"]), reference=e(p["reference"]), specs="".join(specs),
        paras=paras, info=info, features=features, map_src=e(map_src), status_note=status_note,
        i_cal=icon("calendar"), modal_title=modal_title, tel=PHONE_TEL, phone=PHONE_DISPLAY, i_phone=icon("phone"),
        email_href=e(email_href), i_mail=icon("mail"), portal=PORTAL, address=", ".join(ADDRESS_LINES),
        i_close=icon("close"), subject=e(subject), intro=e(f"Property: {p['title']} ({p['priceLabel']}, ref {p['reference']})"),
        times=times, titles=titles, email=EMAIL, form_note=form_note(), i_prev=icon("chevron-left"), i_next=icon("chevron-right"),
    )
    desc = (p.get("summary") or p["title"])[:155]
    return layout(
        title=f"{p['title']} | {p['priceLabel']} | Prime Homes Estate Agents Ltd",
        description=desc, path=f"/property/{p['slug']}", body=body, active=f"/{p['market']}",
        og_image=f"/assets/img/{p['images'][0]}.jpg",
    )


def page_services():
    body = page_head("Our services", "Sales, lettings, auctions and valuations from one local team.",
                     [("/", "Home"), (None, "Our services")]) + T("""<section class="section">
  <div class="container">
    <div class="split">
      <img src="/assets/img/svc-rent.jpg" alt="A bright living room with a sofa and armchair" width="900" height="1393" loading="lazy">
      <div>
        <p class="eyebrow green">For rent</p>
        <h2>Lettings and management, handled in house.</h2>
        <p>Find out how our award winning service can help you with your rental property. Because we manage the group's own portfolio, the same team that lets your property looks after it afterwards.</p>
        <p><a class="btn btn-green" href="/lettings">Properties to rent {{i_arrow}}</a> <a class="btn btn-ghost" href="/contact">Landlord enquiry</a></p>
      </div>
    </div>
    <div class="split reverse">
      <img src="/assets/img/svc-sale.jpg" alt="A hand holding a set of house keys" width="900" height="675" loading="lazy">
      <div>
        <p class="eyebrow">For sale</p>
        <h2>We are here to help get you moving.</h2>
        <p>Local knowledge, honest advice and a sales process that keeps you informed at every step, from the first valuation to completion.</p>
        <p><a class="btn btn-primary" href="/sales">Properties for sale {{i_arrow}}</a> <a class="btn btn-ghost" href="/valuation">Value my home</a></p>
      </div>
    </div>
    <div class="split">
      <img src="/assets/img/svc-val.jpg" alt="A model house, coins and number blocks on a wooden table" width="900" height="599" loading="lazy">
      <div>
        <p class="eyebrow green">Instant valuation</p>
        <h2>Find out what your property could be worth.</h2>
        <p>Instant sales and rental valuations. Tell us a little about your property and the team will come back with a valuation and a clear idea of your options.</p>
        <p><a class="btn btn-green" href="/valuation">Get a free valuation {{i_arrow}}</a></p>
      </div>
    </div>
  </div>
</section>
<section class="section section-sand">
  <div class="container">
    <div class="grid grid-2">
      <div class="card service-card"><div class="icon-badge">{{i_gavel}}</div><h3>Auctions</h3><p>A quick and secure way of selling your property. Ask us whether auction is the right route for you.</p><a class="link" href="/contact">Talk to us about auctions {{i_arrow}}</a></div>
      <div class="card service-card"><div class="icon-badge green">{{i_percent}}</div><h3>Mortgages</h3><p>Buying with a mortgage? Tell us where you are in the process and we will help you take the next step.</p><a class="link" href="/mortgages">Mortgage enquiries {{i_arrow}}</a></div>
    </div>
  </div>
</section>""", i_arrow=icon("arrow-right"), i_gavel=icon("gavel"), i_percent=icon("percent"))
    return layout(title="Our services | Prime Homes Estate Agents Ltd",
                  description="Sales, lettings, property management, auctions and instant valuations from Prime Homes, family-run estate agents in Tooting, SW17.",
                  path="/services", body=body, active="/services")


def page_valuation():
    titles = "".join(f"<option>{t}</option>" for t in ["Mr", "Mrs", "Ms", "Miss", "Dr", "Sir", "Lord", "Other"])
    types = [("Any property type", True), ("Flat", False), ("Detached house", False), ("Terraced house", False), ("Semi-detached house", False)]
    type_pills = "".join(
        f'<label class="radio-pill"><input type="radio" name="property_type" value="{e(t)}" data-label="Property type"{" checked" if c else ""}><span>{e(t)}</span></label>'
        for t, c in types
    )
    bed_pills = "".join(
        f'<label class="radio-pill"><input type="radio" name="bedrooms" value="{b}" data-label="Bedrooms"{" checked" if b == "2" else ""}><span>{b}</span></label>'
        for b in ["1", "2", "3", "4", "5+"]
    )
    body = page_head("Free instant valuation", "Instant sales and rental valuations for homes in Tooting and south west London.",
                     [("/", "Home"), (None, "Free instant valuation")]) + T("""<section class="section section-paper">
  <div class="container contact-grid">
    <div>
      <p class="eyebrow">How it works</p>
      <h2>Tell us about your property.</h2>
      <p class="lede">Whether you are thinking of selling or letting, a valuation from people who buy, build and manage homes here is the best place to start.</p>
      <ol class="steps">
        <li><div><strong>Share the basics</strong>Postcode, property type and number of bedrooms are all we need to begin.</div></li>
        <li><div><strong>We look at the local market</strong>Recent sales and rents nearby, plus what we know from managing our own homes in the area.</div></li>
        <li><div><strong>You get your valuation</strong>A sales or rental figure and an honest conversation about your options, with no obligation.</div></li>
      </ol>
      <p class="mt-2">Prefer to talk? Call <a href="tel:{{tel}}">{{phone}}</a>, Monday to Friday, 10:30am to 6pm.</p>
    </div>
    <div class="form-card">
      <h2 style="font-size:1.5rem">Instant valuation form</h2>
      <form data-mailto data-subject="Instant valuation request" data-intro="Valuation request from the website">
        <div class="form-grid">
          <div class="field"><label for="val-title">Title</label><select class="select" id="val-title" name="title" data-label="Title">{{titles}}</select></div>
          <div class="field"><label for="val-name">Name</label><input class="input" id="val-name" name="name" type="text" required autocomplete="name" data-label="Name"></div>
          <div class="field"><label for="val-email">Email</label><input class="input" id="val-email" name="email" type="email" required autocomplete="email" data-label="Email"></div>
          <div class="field"><label for="val-phone">Phone number</label><input class="input" id="val-phone" name="phone" type="tel" required autocomplete="tel" data-label="Phone number"></div>
          <div class="field"><label for="val-type">Valuation type</label><select class="select" id="val-type" name="valuation_type" required data-label="Valuation type"><option value="">Choose one</option><option>Sales</option><option>Lettings</option></select></div>
          <div class="field"><label for="val-postcode">Postcode</label><input class="input" id="val-postcode" name="postcode" type="text" required autocomplete="postal-code" placeholder="e.g. SW17 7PG" data-label="Postcode"></div>
          <div class="field full"><label for="val-address">Property address</label><input class="input" id="val-address" name="address" type="text" autocomplete="street-address" placeholder="House number and street" data-label="Property address"></div>
          <div class="field full"><span class="label">What type of property is it?</span><div class="radio-row">{{type_pills}}</div></div>
          <div class="field full"><span class="label">Number of bedrooms</span><div class="radio-row">{{bed_pills}}</div></div>
          <div class="field full"><label for="val-notes">Anything else we should know?</label><textarea class="textarea" id="val-notes" name="notes" rows="3" data-label="Notes"></textarea></div>
        </div>
        <p class="form-foot">Pressing submit opens your email app with the request filled in, ready to send to {{email}}. We never share your details.</p>
        <button class="btn btn-primary btn-block" type="submit">Request my valuation</button>
        {{form_note}}
      </form>
    </div>
  </div>
</section>""", tel=PHONE_TEL, phone=PHONE_DISPLAY, titles=titles, type_pills=type_pills, bed_pills=bed_pills, email=EMAIL, form_note=form_note())
    return layout(title="Free instant valuation | Prime Homes Estate Agents Ltd",
                  description="Get a free sales or rental valuation for your property in Tooting and south west London from Prime Homes Estate Agents.",
                  path="/valuation", body=body, active="/valuation")


def page_contact():
    from urllib.parse import quote
    map_src = "https://www.google.com/maps?q=" + quote("16 Upper Tooting Road, London SW17 7PG") + "&output=embed"
    body = page_head("Contact us", "If you have any questions or need any help, get in touch using the form or the details below.",
                     [("/", "Home"), (None, "Contact us")]) + T("""<section class="section">
  <div class="container contact-grid">
    <div>
      <div class="contact-cards">
        <div class="card"><div class="icon-badge">{{i_pin}}</div><div><h3>Our address</h3><p>{{address}}</p></div></div>
        <div class="card"><div class="icon-badge green">{{i_mail}}</div><div><h3>Our email</h3><p><a href="mailto:{{email}}">{{email}}</a></p></div></div>
        <div class="card"><div class="icon-badge">{{i_phone}}</div><div><h3>Our phone</h3><p><a href="tel:{{tel}}">{{phone}}</a></p></div></div>
        <div class="card"><div class="icon-badge green">{{i_clock}}</div><div><h3>Working hours</h3><dl class="hours"><div><dt>Monday to Friday</dt><dd>10:30am to 6:00pm</dd></div><div><dt>Saturday and Sunday</dt><dd>Closed</dd></div></dl></div></div>
      </div>
      <div class="map mt-2"><iframe title="Map showing the Prime Homes office at 16 Upper Tooting Road" src="{{map_src}}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
    </div>
    <div class="form-card">
      <h2 style="font-size:1.5rem">Enquiry form</h2>
      <form data-mailto data-subject="Enquiry from the website" data-intro="Enquiry from the website contact form">
        <div class="form-grid">
          <div class="field full"><label for="c-name">Name</label><input class="input" id="c-name" name="name" type="text" required autocomplete="name" data-label="Name"></div>
          <div class="field"><label for="c-email">Email</label><input class="input" id="c-email" name="email" type="email" required autocomplete="email" data-label="Email"></div>
          <div class="field"><label for="c-phone">Phone</label><input class="input" id="c-phone" name="phone" type="tel" required autocomplete="tel" data-label="Phone"></div>
          <div class="field full"><label for="c-message">Message</label><textarea class="textarea" id="c-message" name="message" required data-label="Message"></textarea></div>
        </div>
        <p class="form-foot">Pressing send opens your email app with your message filled in, ready to send to {{email}}. We never share your details.</p>
        <button class="btn btn-primary btn-block" type="submit">Send</button>
        {{form_note}}
      </form>
    </div>
  </div>
</section>""", i_pin=icon("pin"), i_mail=icon("mail"), i_phone=icon("phone"), i_clock=icon("clock"),
        address="<br>".join(ADDRESS_LINES), email=EMAIL, tel=PHONE_TEL, phone=PHONE_DISPLAY, map_src=e(map_src), form_note=form_note())
    return layout(title="Contact us | Prime Homes Estate Agents Ltd",
                  description="Contact Prime Homes Estate Agents at 16 Upper Tooting Road, London SW17 7PG. Call 020 8767 3838 or email info@primehomesuk.com.",
                  path="/contact", body=body, active="/contact")


def page_testimonials():
    tests = "".join(testimonial(*t) for t in TESTIMONIALS)
    body = page_head("Testimonials", "What tenants, residents and clients say about working with us.",
                     [("/", "Home"), (None, "Testimonials")]) + T("""<section class="section">
  <div class="container">
    <div class="grid grid-3">{{tests}}</div>
    <div class="cta-band mt-2" style="margin-top:3rem">
      <div><h2>Had a good experience with us?</h2><p>We would love to hear about it, and so would the next person looking for a home.</p></div>
      <div class="actions"><a class="btn btn-light" href="{{href}}">Share your experience</a></div>
    </div>
  </div>
</section>""", tests=tests, href=e(mailto("Testimonial for Prime Homes")))
    return layout(title="Testimonials | Prime Homes Estate Agents Ltd",
                  description="Read what tenants and clients say about Prime Homes Estate Agents in Tooting, south west London.",
                  path="/testimonials", body=body, active="/testimonials")


def page_projects():
    body = page_head("Upcoming projects", "Our next homes and developments in south west London.",
                     [("/", "Home"), (None, "Upcoming projects")]) + T("""<section class="section">
  <div class="container">
    <div class="split">
      <div>
        <p class="eyebrow green">Coming soon</p>
        <h2>Details of our next projects will appear here.</h2>
        <p class="lede">Prime Group builds and delivers high quality build to rent homes and semi commercial properties. Register your interest and we will let you know as soon as there is news to share.</p>
        <p class="mt-2"><a class="btn btn-primary" href="{{href}}">Register your interest</a> <a class="btn btn-ghost" href="/">Back to the home page</a></p>
      </div>
      <img src="/assets/img/dafforne-1.jpg" alt="Victorian terraced houses in Tooting" width="1200" height="798" loading="lazy">
    </div>
  </div>
</section>""", href=e(mailto("Upcoming projects: register my interest", "Hello,\n\nPlease let me know when details of your upcoming projects are available.\n\nName:\nPhone:\n")))
    return layout(title="Upcoming projects | Prime Homes Estate Agents Ltd",
                  description="Upcoming build to rent homes and developments from Prime Group in south west London. Register your interest.",
                  path="/projects", body=body, active="/projects")


def page_mortgages():
    body = page_head("Mortgages", "Help with the next step when you are buying with a mortgage.",
                     [("/", "Home"), (None, "Mortgages")]) + T("""<section class="section">
  <div class="container">
    <div class="split">
      <div class="prose">
        <h2>Buying with a mortgage?</h2>
        <p>Whether you are a first-time buyer, moving home or investing, knowing what you can borrow makes everything that follows simpler. Tell us where you are in the process and we will help you take the next step.</p>
        <p>Call <a href="tel:{{tel}}">{{phone}}</a>, Monday to Friday 10:30am to 6pm, or send us a note and we will come back to you.</p>
        <p class="mt-2"><a class="btn btn-primary" href="{{href}}">Make a mortgage enquiry</a> <a class="btn btn-ghost" href="/sales">Browse properties for sale</a></p>
      </div>
      <img src="/assets/img/svc-sale.jpg" alt="A hand holding a set of house keys" width="900" height="675" loading="lazy">
    </div>
  </div>
</section>""", tel=PHONE_TEL, phone=PHONE_DISPLAY, href=e(mailto("Mortgage enquiry", "Hello,\n\nI would like some help with a mortgage.\n\nName:\nPhone:\nWhere I am in the process:\n")))
    return layout(title="Mortgages | Prime Homes Estate Agents Ltd",
                  description="Mortgage enquiries for buyers in Tooting and south west London. Talk to Prime Homes Estate Agents about your next step.",
                  path="/mortgages", body=body)


def page_privacy():
    fragment = (TOOLS / "privacy.html").read_text(encoding="utf-8")
    body = page_head("Privacy policy", "How Prime Homes Estate Agents Ltd collects, uses and protects your personal data.",
                     [("/", "Home"), (None, "Privacy policy")]) + f'<section class="section"><div class="container"><div class="prose">{fragment}</div></div></section>'
    return layout(title="Privacy policy | Prime Homes Estate Agents Ltd",
                  description="The privacy policy for the Prime Homes Estate Agents Ltd website and services.",
                  path="/privacy", body=body)


def page_404():
    body = T("""<section class="error-page">
  <div class="container">
    <p class="eyebrow" style="justify-content:center">Page not found</p>
    <h1>404</h1>
    <h2>We could not find that page.</h2>
    <p class="lede" style="margin-inline:auto">The property may have been sold or let, or the link may be out of date. Try a search, or head back to the home page.</p>
    <div class="actions"><a class="btn btn-primary" href="/">Home page</a><a class="btn btn-outline" href="/sales">For sale</a><a class="btn btn-outline" href="/lettings">To rent</a></div>
  </div>
</section>""")
    return layout(title="Page not found | Prime Homes Estate Agents Ltd",
                  description="That page could not be found.", path="/404", body=body,
                  extra_head='<meta name="robots" content="noindex">\n')


# ----------------------------------------------------------------------------- build

def main():
    props = json.loads((TOOLS / "properties.json").read_text(encoding="utf-8"))
    pages = {
        "index.html": page_home(props),
        "sales.html": page_listing("sales", props),
        "lettings.html": page_listing("lettings", props),
        "services.html": page_services(),
        "valuation.html": page_valuation(),
        "contact.html": page_contact(),
        "testimonials.html": page_testimonials(),
        "projects.html": page_projects(),
        "mortgages.html": page_mortgages(),
        "privacy.html": page_privacy(),
        "404.html": page_404(),
    }
    for p in props:
        pages[f"property/{p['slug']}.html"] = page_property(p)
    for name, content in pages.items():
        target = PUBLIC / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"wrote public/{name} ({len(content.encode('utf-8'))} bytes)")

    data = "// Generated by tools/render.py from tools/properties.json. Edit the JSON, not this file.\n"
    data += "window.PRIME_PROPERTIES = " + json.dumps(props, ensure_ascii=False, indent=2) + ";\n"
    (PUBLIC / "assets/js/properties.js").write_text(data, encoding="utf-8")
    print("wrote public/assets/js/properties.js")

    urls = ["/", "/sales", "/lettings", "/services", "/valuation", "/contact", "/testimonials", "/projects", "/mortgages", "/privacy"]
    urls += [f"/property/{p['slug']}" for p in props]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls)
    sitemap += "</urlset>\n"
    (PUBLIC / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("wrote public/sitemap.xml")


if __name__ == "__main__":
    main()
