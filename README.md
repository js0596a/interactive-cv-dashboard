# Interactive CV Dashboard

![Preview](docs/cv-dashboard-preview.svg)

Interactive, recruiter-friendly CV built with Python Dash and Plotly, based on my real resume and project work.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-4.x-0A192F?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Plotly](https://img.shields.io/badge/Plotly-6.x-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)

## Why this repo

Most resumes are static PDFs. This one is interactive and lets employers explore impact, technical stack, and project depth through live filters and visuals.

## Featured highlight

- George Hacks x UN Reboot the Earth Hackathon winner (UN & FAO track)
- Project: [FoodBridge Devpost](https://devpost.com/software/food-bridge-isqzu0)

## What employers can inspect

- Career timeline and role details
- Project impact cards and links
- Skill depth by category and proficiency
- Analytics-first workflow using Python + BI tools

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

Open `http://127.0.0.1:8050`.

If port `8050` is busy:

```bash
python3 -c "from app import app; app.run(debug=True, port=8051)"
```

## Customize content

All resume data is in `cv_data.py`.

Main dashboard app is `app.py`.

Styles and UI animations are in `assets/styles.css`.

## Repo structure

```text
.
├── app.py
├── cv_data.py
├── requirements.txt
├── assets/
│   └── styles.css
├── docs/
│   └── cv-dashboard-preview.svg
└── .github/
    └── workflows/
        └── ci.yml
```

## Profile upgrades

To make your full GitHub profile look employer-ready too:

- Use `PROFILE_README_TEMPLATE.md`
- Follow `GITHUB_POLISH_CHECKLIST.md`

## Links

- LinkedIn: [linkedin.com/in/edu-sal](https://linkedin.com/in/edu-sal)
- GitHub: [github.com/js0596a](https://github.com/js0596a)
- Devpost: [FoodBridge](https://devpost.com/software/food-bridge-isqzu0)
