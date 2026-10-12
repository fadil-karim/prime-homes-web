# Prime Homes Estate Agents Ltd — website

The website for Prime Homes Estate Agents Ltd (primegroupuk.com), rebuilt as a fast
static site. Everything served lives in `public/`; there is no build step and no
framework. Cloudflare Workers serves the directory directly.

## Structure

```
public/                    everything served
  index.html               home: hero, search, about, services, featured, app, testimonials
  sales.html               properties for sale, with filters and sorting
  lettings.html            properties to rent, with filters and sorting
  property/<slug>.html     one page per property: gallery, details, map, viewing request
  services.html  valuation.html  contact.html  testimonials.html
  projects.html  mortgages.html  privacy.html  404.html
  assets/css/site.css      the design
  assets/js/site.js        navigation, search and filters, gallery, forms, share links
  assets/js/properties.js  property data (generated, see below)
  assets/img/              logo, favicon source, property photos, accreditation logos
  _headers                 security and caching headers
  _redirects               the previous site's URLs, redirected to their new homes
  robots.txt  sitemap.xml  favicon.png
tools/
  properties.json          the property listings: the one place to edit them
  privacy.html             the privacy policy text
  render.py                writes the pages above from the data and templates
  render_check.py          screenshots every page and checks local links
wrangler.jsonc             assets-only Worker config
package.json               wrangler for local preview and the dry-run check
```

## Editing content

Property listings live in `tools/properties.json`. To add, change or remove one,
edit the JSON, drop the photos into `public/assets/img/` (JPEG, about 1200px wide,
plus a 640px `-sm` thumbnail), then regenerate the pages:

```bash
python3 tools/render.py
```

The script rewrites the home, listing and property pages, `properties.js` and the
sitemap. Page copy lives in the templates inside `tools/render.py`; the privacy
policy is `tools/privacy.html`. Commit the generated files: Cloudflare serves them
as they are.

Set `"status"` to `"available"`, `"let"` or `"sold"`. Let and sold properties stay
on the home page as recent activity but drop out of the search results, which is
how the previous site behaved.

## Features kept from the previous site

- Property search by category, location, price and bedrooms, from the home page
- Sales and lettings listings with the full set of filters: location, price,
  bedrooms, bathrooms, reception rooms, property type, features, and price sorting
- Property pages with photo gallery and lightbox, key facts, description, map,
  "request a viewing" form, share links and a link to the customer portal
- Free instant valuation form, contact form with opening hours and map
- Services, upcoming projects, testimonials and privacy policy pages
- Prime Home app links (App Store and Google Play), accreditation logos, the
  customer portal login, and the original logo

Forms open the visitor's email app with the enquiry filled in and addressed to
`info@primehomesuk.com`, so they work without a server. A Cloudflare Worker or a
form service can be wired in later if inbox delivery without the email step is
wanted.

The customer portal is still the one hosted with the previous site provider
(`https://www.primegroupuk.com/login/`); the login links point there.

## Local development

```bash
npm install
npm run dev          # wrangler dev, serves public/ at http://localhost:8787
```

Or simply `python3 -m http.server -d public` for a quick look (extensionless links
such as `/sales` only resolve under wrangler or Cloudflare).

## Verification before every push to main

1. `npx wrangler deploy --dry-run`
2. `python3 tools/render_check.py` and look at the screenshots in `.render-check/`

## Deployment

The repository is connected to Cloudflare Workers Builds: every push to `main`
deploys to production. Connect it (once) in the Cloudflare dashboard under
Workers & Pages → Create → Import a repository, pointing at this repo and `main`.
Then add the domain under the Worker's custom domains.

## External resources

Loaded by the visitor's browser from third parties:

- Google Fonts (Fraunces and Inter), with system fallbacks if unavailable
- Google Maps embeds on the contact page and property pages
- App Store and Google Play links for the Prime Home app
- The customer portal at primegroupuk.com (previous provider)

Everything else, including all images, is served from this repository.
