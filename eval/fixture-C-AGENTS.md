# Kiwi Freight Platform — contributor guide

## Build

`npm run build` produces the SDK bundle. Run `npm test` before opening a PR.

## Documentation

Docs live in `docs/`. Locale: en-NZ. Follow the Google developer documentation
style guide otherwise.

Use `courier`, not `shipper`. Use `consignment`, not `parcel`.

## Releases

Tag with `v<major>.<minor>.<patch>`. The changelog is generated from commit subjects.
