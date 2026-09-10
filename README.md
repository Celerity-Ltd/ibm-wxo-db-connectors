# IBM Zurich Agentic AI

This repository contains the IBM Zurich agent and database connector examples, together with the Agentic AI Academy presentation.

## Presentation

The presentation is a self-contained static HTML deck:

- [Open the presentation](docs/index.html)

The presentation is organized as one standalone HTML page per slide. Shared presentation styles live in `docs/presentations/assets/deck.css`, while each slide owns its markup and navigation.

## Publish with GitHub Pages

The workflow in `.github/workflows/pages.yml` publishes the `docs` directory automatically whenever `main` is updated.

1. Push this repository to GitHub, keeping the default branch named `main`.
2. In **Settings > Pages**, set **Source** to **GitHub Actions**.
3. Push a change or run **Publish presentations to GitHub Pages** from the repository's **Actions** tab.
4. GitHub will show the public `github.io` URL in the workflow's deployment environment.

No build step or package installation is required for the presentation.

## Repository layout

- `agents/`: connector agents
- `connections/`: connection definitions
- `tools/`: database query tools
- `docs/index.html`: GitHub Pages entry point that opens slide 1
- `docs/presentations/`: standalone slide pages
- `docs/presentations/assets/`: shared presentation styles