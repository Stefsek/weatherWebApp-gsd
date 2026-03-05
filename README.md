# ☁️ Weather App

Built with [opencode](https://opencode.ai) using the minimax-m2.5 model.

A clean, dark-themed weather app built with Streamlit. Search any city and instantly see real-time temperature, conditions, humidity, wind speed & direction, and an interactive map — all powered by the free [Open-Meteo](https://open-meteo.com) API (no API key required).

Built in a single day (~75 min of execution) using the [Get Shit Done](https://github.com/gsd-build/get-shit-done) workflow.

---

## Screenshots

**Empty state** — search bar and C/F toggle on load

![Empty state](examples/01-empty-state.png)

**Weather result** — Athens, showing temperature, condition, metrics grid, and interactive map

![Athens weather](examples/02-athens-weather.png)

**Another city** — New York in Celsius

![New York weather](examples/03-new-york-weather.png)

**Error handling** — graceful message when city is not found

![City not found](examples/04-error-not-found.png)

---

## Features

- **City search** — type any city name, results appear immediately
- **C / F toggle** — switch between Celsius and Fahrenheit; preference persists in session
- **Weather card** — city name, large temperature, and condition label (Clear, Overcast, Rain, Snow, Thunderstorm, etc.) mapped from WMO weather codes
- **Metrics grid** — 3-column card layout: Humidity | Wind speed | Wind direction (cardinal: N, NNE, NE, …)
- **Interactive map** — dark CartoDB dark_matter base map with a cyan `#00d4ff` circle marker pinned to the searched city
- **Error handling** — graceful messages for unknown cities, API errors, and network failures
- **Caching** — API responses cached 5 min (`@st.cache_data(ttl=300)`) to prevent redundant calls on Streamlit rerenders

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit 1.40+](https://streamlit.io) | Web framework — UI, session state, layout |
| [Open-Meteo](https://open-meteo.com) | Weather + geocoding API — free, no API key |
| [Folium](https://python-visualization.github.io/folium/) + [streamlit-folium](https://folium.streamlit.app) | Interactive map embedded in Streamlit |
| [UV](https://github.com/astral-sh/uv) | Package manager — faster than pip, lockfile included |
| Python 3.13.5 | Runtime |

---

## Project Structure

```
weatherApp/
├── main.py                          # Streamlit entry point — UI, session state, layout
├── pyproject.toml                   # Project metadata and dependencies (managed by uv)
├── uv.lock                          # Locked dependency tree
├── .python-version                  # Pins Python 3.13.5 for uv
├── .gitignore
├── IDEA.md                          # Original design spec (stack, colors, layout, API endpoints)
├── README.md
├── .streamlit/
│   └── config.toml                  # Dark theme config: colors, fastReruns off
├── .planning/                       # GSD planning context (see below)
├── examples/                        # Screenshots
│   ├── 01-empty-state.png
│   ├── 02-athens-weather.png
│   ├── 03-new-york-weather.png
│   └── 04-error-not-found.png
└── src/weather_app/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py
    │   └── weather_data.py          # WeatherData + GeocodingResult dataclasses with __post_init__ validation
    ├── services/
    │   ├── __init__.py
    │   ├── geocoding.py             # City name → lat/lon via Open-Meteo geocoding API
    │   └── weather.py               # lat/lon → WeatherData via Open-Meteo forecast API
    └── utils/
        ├── __init__.py
        ├── converters.py            # Celsius ↔ Fahrenheit conversion
        └── formatters.py            # WMO code → condition label, degrees → cardinal direction
```

---

## Running Locally

**Prerequisites:** Python 3.13+ and [uv](https://github.com/astral-sh/uv)

```bash
git clone <repo-url>
cd weatherApp

# Install dependencies from lockfile
uv sync

# Run the app
uv run streamlit run main.py
```

App opens at `http://localhost:8501`.

---

## How This Was Built — Get Shit Done (GSD)

The project started from [`IDEA.md`](IDEA.md) — a design spec written before any code, covering the intended tech stack, feature list, color palette, layout, key utility functions, and API endpoints. That document served as the input to GSD's kickoff, which used it as the starting context for research, requirement extraction, and roadmap generation.

This project was then planned and executed using **[Get Shit Done (GSD)](https://github.com/gsd-build/get-shit-done)** — a Claude Code workflow that brings structured engineering discipline to AI-assisted development. Instead of prompting Claude to "build a weather app" and hoping for the best, GSD breaks the work into researched, planned, and verified phases that build on each other.

### How GSD works

GSD is a set of [slash commands](https://github.com/gsd-build/get-shit-done) you install into Claude Code. The workflow has three main stages:

**1. Kickoff** — `/gsd:new-project`
Claude interviews you about what you want to build, researches the domain (APIs, libraries, pitfalls, competitive landscape), and produces a `PROJECT.md` with requirements and a phased `ROADMAP.md`. No code yet — just a solid plan.

**2. Plan & Execute phases** — `/gsd:plan-phase` → `/gsd:execute-phase`
Each phase gets its own `PLAN.md` before any code is written. A dedicated planner agent breaks the phase into atomic tasks, identifies file changes, and checks the plan against the phase goal. Then an executor agent runs it — making commits, handling deviations, and leaving a `SUMMARY.md` of what was done.

**3. Verify & ship** — `/gsd:verify-work` → `/gsd:complete-milestone`
A verifier agent checks the codebase against the original requirements (goal-backward, not just "did the tasks run?"). A retrospective is written. The milestone is archived. The next milestone starts clean.

All planning context lives in `.planning/` alongside your code so nothing is lost between sessions and any agent can resume with full context.

### This project's build log

**v1.0 shipped:** 2026-03-03 | 2 phases | 5 plans | 571 Python LOC | ~75 min total execution

#### Phase 1 — Core Weather Features

Goal: users can search any city and see weather data.

| Plan | What was built |
|------|---------------|
| 01-01: Foundation | `src/weather_app/` package structure, `WeatherData` + `GeocodingResult` dataclasses, converters, WMO code → label mapping in formatters |
| 01-02: UI Layer | Streamlit `main.py` — city search input, session state initialization, `handle_city_search()`, `display_weather()`, C/F segmented control, error display |

Requirements shipped: `CITY-01/02`, `TEMP-01/02/03`, `COND-01/02`, `METR-01/02/03`, `ERR-01/02`

#### Phase 2 — Visual Polish

Goal: beautiful, responsive dark-themed interface with interactive map.

| Plan | What was built |
|------|---------------|
| 02-01: Dark Theme & Layout | `.streamlit/config.toml` dark theme, CSS injection for gradient background (`#0a0a0f → #12121a`), gradient title (`#00d4ff → #7c3aed`) |
| 02-02: Metrics Grid Cards | Metric card CSS (gradient `#1a1a24 → #1e1e2a`, border `#2a2a3a`), label/value styling, C/F toggle custom border styling |
| 02-03: Interactive Map | Folium map with CartoDB dark_matter tiles, cyan `#00d4ff` circle marker, Leaflet attribution hidden via CSS injection into the iframe |

Requirements shipped: `MAP-01/02`, `DESN-01/02/03/04/05`

#### Key decisions made during the build

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Open-Meteo API | Free, no API key, global coverage | ✓ Zero setup friction |
| Dataclasses + `__post_init__` | Type safety without Pydantic overhead | ✓ Caught bugs early |
| `@st.cache_data(ttl=300)` | Prevent redundant calls on every Streamlit rerender | ✓ Seamless |
| CartoDB dark_matter tiles | Matches dark theme aesthetic | ✓ Cohesive look |
| CSS injection via `st.markdown` | `config.toml` doesn't support gradients or centering | ✓ Practical workaround |
| `folium.Element` for attribution CSS | Attribution lives in an iframe — Streamlit CSS can't reach it | ✓ Clean solution |
| Removed 400px max-width | Design spec said 400px but that was too narrow on desktop — C/F buttons were stacking | ✓ Fixed layout |

#### Retrospective highlights

- **What worked well:** modular `src/` structure made Phase 2 edits non-destructive; caching was effortless; Open-Meteo had zero friction
- **What needed a second pass:** the 400px max-width from the design spec looked bad at actual desktop viewport; Folium attribution required digging into iframe injection
- **Lessons:** design spec widths are for content cards, not Streamlit block containers — always test at real viewport width

---

## Planning Directory (`.planning/`)

GSD writes all planning context here. Every file serves a specific role:

```
.planning/
├── PROJECT.md              # Living source of truth: what the app is, requirements, key decisions
├── ROADMAP.md              # Phase-by-phase progress tracker with completion status
├── MILESTONES.md           # Milestone log: what shipped, LOC, timeline, accomplishments
├── STATE.md                # Machine-readable session state: current milestone, phase progress
├── RETROSPECTIVE.md        # What worked, what was inefficient, patterns established, key lessons
├── config.json             # GSD workflow settings (mode, model profile, which agents to run)
│
├── research/               # Pre-build domain research (generated by /gsd:new-project)
│   ├── SUMMARY.md          # Executive summary: recommended stack, features, pitfalls, confidence levels
│   ├── STACK.md            # Technology evaluation: Streamlit, Open-Meteo, UV, Folium
│   ├── FEATURES.md         # Feature analysis: must-have vs. should-have vs. defer
│   ├── ARCHITECTURE.md     # Layered architecture recommendation: services / models / utils / UI
│   └── PITFALLS.md         # Common failure modes: missing caching, session state errors, widget key collisions
│
└── milestones/
    ├── v1.0-REQUIREMENTS.md    # Full requirements list with traceability (19/19 shipped)
    ├── v1.0-ROADMAP.md         # Phase goals, success criteria, decisions, issues resolved
    └── v1.0-phases/
        ├── 01-core-weather/
        │   ├── 01-01-PLAN.md       # Atomic task list for foundation (models, utils, services)
        │   ├── 01-01-SUMMARY.md    # What was actually built, deviations, commit log
        │   ├── 01-02-PLAN.md       # Atomic task list for UI layer
        │   └── 01-02-SUMMARY.md    # What was actually built
        └── 02-visual-polish/
            ├── 02-CONTEXT.md       # Phase-level context carried across plans
            ├── 02-VERIFICATION.md  # Verifier agent output: goal-backward requirements check
            ├── 02-01-PLAN.md       # Dark theme & layout tasks
            ├── 02-01-SUMMARY.md
            ├── 02-02-PLAN.md       # Metrics grid card tasks
            ├── 02-02-SUMMARY.md
            ├── 02-03-PLAN.md       # Interactive map tasks
            └── 02-03-SUMMARY.md
```

---

## API Details

Both endpoints are [Open-Meteo](https://open-meteo.com) — completely free, no account or API key:

- **Geocoding:** `https://geocoding-api.open-meteo.com/v1/search` — city name → latitude, longitude, display name
- **Weather:** `https://api.open-meteo.com/v1/forecast` — lat/lon → current temperature, weather code, humidity, wind speed, wind direction

Responses are cached for 5 minutes to avoid redundant requests on Streamlit's rerun model.
