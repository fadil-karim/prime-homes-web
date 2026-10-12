# CLAUDE.md

Standing policy for this repository. Read it before making any change here.

## What this repo is

The Prime Homes Estate Agents Ltd website as a Cloudflare Workers static-assets
site. Everything served lives in `public/` and there is no build step - the files
in that directory are the site. The repo is connected to Cloudflare Workers Builds,
so **every push to `main` deploys to production**.

```
public/            everything served
  index.html, sales.html, lettings.html, property/*.html, ...
  404.html
  assets/css|js|img
  _headers         security + caching headers
  _redirects       old URLs from the previous site
  robots.txt, sitemap.xml
tools/
  properties.json  property listings (edit here)
  privacy.html     privacy policy text
  render.py        regenerates the pages from the data and templates
  render_check.py  screenshots + link check
wrangler.jsonc     assets-only config, no Worker script
package.json       wrangler devDependency + dev/deploy scripts
```

## Editing the site

Pages are generated: edit `tools/properties.json` or the templates in
`tools/render.py` (or `tools/privacy.html`), then run `python3 tools/render.py`
and commit the regenerated files in `public/`. Do not hand-edit generated HTML.
The stylesheet and `site.js` are hand-written and edited directly. The property
card markup exists in both `render.py` and `site.js`; keep them in step.

## Local development

```bash
npm install
npm run dev          # wrangler dev
```

## Verification - before every push to main

1. `npx wrangler deploy --dry-run`
2. `python3 tools/render_check.py`, then inspect the screenshots in
   `.render-check/`: styles applied, layout intact, nothing collapsed.

Never leave pushed work unverified or half-finished. Work in small, complete
batches: implement, verify, commit, push.

## Git and release workflow

- Before committing: `git config user.name "Fid" && git config user.email "fid_kk@proton.me"`
- Develop on the working branch and push there first. Release verified work by
  fast-forwarding `main` onto it and pushing `main`.
- Every push to `main` is a release. Versions are an ascending `vMAJOR.MINOR`
  sequence starting at `v1.0`; every push bumps the minor regardless of size. A
  major bump is reserved for a ground-up overhaul.
- With every push to `main`, provide release-tag text in the reply, in exactly
  this shape. The owner creates the GitHub release manually - **never push tags**:

  ```
  Tag: v<next>  —  Title: <five to nine words, plain and evocative>
  Description: <one to three sentences of editorial prose describing what changed
  from the owner's point of view — outcomes, not implementation. No bullet lists,
  no jargon, no file names.>
  ```

- Append the release line to the ledger below as part of the same push.
- Commit messages: descriptive imperative first line (what the change does, not
  "update X"), then a short prose body; dash bullets are fine there. One commit
  per coherent piece of work; several may share a push, but each push gets
  exactly one version entry.
- Never include model names, AI attribution trailers, session links, or other
  tooling identifiers in commit messages, titles, or code.

## Prompt archive

`prompt text/` holds the records for the version currently in service - nothing
else. Shipping version N replaces the folder's contents wholesale, in the same
push that releases the version: remove the previous version's folder(s) and add
`prompt text/N/` containing `input.txt` (the prompt, byte for byte), `output.txt`
(the reply that shipped it, byte for byte), `ai model.txt` (three lines:
Anthropic / Claude / the model that did the work) and every input image and file
the owner provided, each under its own name. The files are owner-supplied
records: never edit, reformat, trim or regenerate them. The version number N is
the count of prompts that have shipped, independent of the release tag.

## The site itself

The design, copy and features were built for the owner in v1.0 from the previous
site at primegroupuk.com: the logo, contact details, accreditations, testimonials,
property data and privacy policy are the client's and stay as they are unless the
owner asks. Changes to the design are their own release, requested deliberately.

## Release ledger

| Version | Title | Description |
| --- | --- | --- |
| v1.0 | A new front door for Prime Homes | The website has been rebuilt from the ground up with a cleaner, faster design that works properly on phones. Everything people used before is still here: property search for sales and lettings, full listings with photos and maps, the instant valuation and contact forms, testimonials, the app download and the customer portal link, all under the same logo. |
