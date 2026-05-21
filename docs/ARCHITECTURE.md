# CV Dashboard Architecture

## Overview

The project is configuration-driven: `cv_data.py` acts as a structured data source, while `app.py` renders a multi-view interactive dashboard with Plotly visualizations and card components.

## Runtime flow

1. `app.py` imports structured content from `cv_data.py`.
2. Helper functions filter/shape data for each panel (overview, experience, projects, skills).
3. A single callback updates KPIs, charts, cards, and panel visibility.
4. CSS in `assets/styles.css` controls visual identity, animation, and responsiveness.

## Data model

- `PROFILE`: headline, contact, external links
- `EXPERIENCE`: role timeline + achievements
- `PROJECTS`: impact cards with links and scores
- `SKILLS`: category-level proficiency maps
- `EDUCATION`: academic entries
- `AWARDS`: scholarships and distinctions

## Quality gates

- `scripts/validate_cv_data.py`: validates data contract and URL format
- `pytest` tests in `tests/`: sanity checks for data consistency
- GitHub Actions in `.github/workflows/ci.yml`: compile + validate + test on push/PR

## Automation assets

- `scripts/capture_demo.py`: generates `docs/cv-dashboard-demo.gif` from live app interactions
- `scripts/check_links.sh`: HTTP checks for links defined in `cv_data.py`
- `Makefile`: repeatable local commands for setup, check, test, and demo generation
