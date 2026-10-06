# Changelog

All notable changes to the `outpost` CLI are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/). Each
release's section below is pulled verbatim into its GitHub Release notes
by `.github/workflows/publish.yml` — keep an entry here _before_ pushing
the matching `vX.Y.Z` tag, or the release workflow will fail on purpose
rather than publish with empty notes.

## [Unreleased]

## [0.1.0] - 2026-10-05

### Added

- `outpost env create` / `list` / `status` / `destroy` / `extend` / `runbook` — core environment lifecycle commands.
- `outpost env pause` / `resume` — manage the grace-period/pause safety net (`RUNNING`/`EXPIRING` → `PAUSED` and back) directly from the CLI.
- `outpost audit list` — paginated, filterable audit log (`--env`, `--action`, `--actor-type`).
- `outpost teams list` — read-only team listing, mainly to support `--team` resolution by slug, name, or ID on `env create`/`list`.
- `outpost auth login` — logs in via GitHub and issues a CLI API key in a single step, using a loopback HTTP server on `127.0.0.1` (the same pattern `gh auth login` and VS Code use). No token to copy or paste.
- `outpost auth login --manual` — fallback for SSH/headless sessions where the browser completing login isn't on the same machine as the CLI.
- `outpost auth key generate` — re-issues an API key from an existing, still-fresh login token, for rotating a key without a full login.
- `--json` output on every list/status/audit command, for scripting.

### Fixed

- HTTP client now sets `follow_redirects=True` — FastAPI's collection routes (`/environments`, `/audit`, `/teams`) 307-redirect the no-trailing-slash form, which httpx does not follow by default; requests to them previously returned an empty, unparseable body.
- `--version` now reads from installed package metadata instead of a hardcoded string, so it can't drift out of sync with the version in `pyproject.toml`.

### Changed

- API errors now surface the server's own `{"detail": "..."}` message directly instead of a raw traceback, with a dedicated message for `401` pointing at `auth key generate`.
