# Ambassador — BGA • BIST Parent Loyalty Programme

One-page website for the Ambassador loyalty programme: exclusive offers from
partner businesses across Tbilisi for BGA and BIST parents.

## Structure

- `index.html` — the site (a single self-contained page)
- `support.js` — page runtime (renders the page content and interactions)
- `image-slot.js` — image slot component used by the page

## Deployment

The site is served by GitHub Pages directly from this branch (Settings →
Pages → Deploy from a branch). Every push redeploys it automatically; the
`.nojekyll` file makes Pages publish the files as-is without a Jekyll build.

To view locally, serve the folder with any static file server, e.g.:

```sh
python3 -m http.server
```

then open <http://localhost:8000>.
