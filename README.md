# Ambassador — BGA • BIST Parent Loyalty Programme

One-page website for the Ambassador loyalty programme: exclusive offers from
partner businesses across Tbilisi for BGA and BIST parents.

## Structure

- `index.html` — the site (a single self-contained page)
- `support.js` — page runtime (renders the page content and interactions)
- `image-slot.js` — image slot component used by the page

## Deployment

The site is a static page deployed to GitHub Pages automatically on every push
via the workflow in `.github/workflows/deploy-pages.yml`.

To view locally, serve the folder with any static file server, e.g.:

```sh
python3 -m http.server
```

then open <http://localhost:8000>.
