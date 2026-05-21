# Advanced Percy + Appium-Python

This directory exercises the full applicable Percy SDK feature surface for `percy-appium-app` (Python). See the basic example at the repo root for the minimum integration.

## What this example covers

A pytest suite (`tests/test_advanced.py`) where each test exercises one row of the [App Percy / Appium Native matrix](../../../docs/advanced-example-feature-matrix.md): device_name override, orientation, fullscreen + status_bar/nav_bar heights, ignore regions via xpath / appium element / custom bbox, consider regions via xpath, sync mode, test_case + labels, build metadata via env.

Web-only options marked `N/A` in `matrix.yml` — native App Percy has no DOM.

## Run locally

```bash
cd advanced
make install
export AA_USERNAME="<browserstack username>"
export AA_ACCESS_KEY="<browserstack access key>"
export APP="bs://<your hashed app id>"
export PERCY_TOKEN="<your project token>"
make test
```

## CI note

The advanced CI job is `workflow_dispatch`-only — App Percy CI requires a real BrowserStack device session.

## Coverage matrix

States: `Covered` / `N/A — <reason>` / `Planned` / `Deprecated`. Source of truth is [`matrix.yml`](./matrix.yml).
