# Interactive CV Dashboard

This is my resume as a web app.

I built it because a PDF can only show so much. With this version, people can click through my experience, projects, skills, and awards in a way that feels more real.

## Quick Look

![Overview](docs/screenshots/01-overview.png)
![Experience and Awards](docs/screenshots/02-experience-awards.png)
![Projects - FoodBridge](docs/screenshots/03-projects-foodbridge.png)
![Skills](docs/screenshots/04-skills.png)

## Why I Made It

- I wanted a portfolio piece that also works as my CV.
- I wanted recruiters to see both technical depth and product thinking.
- I wanted to highlight real projects, especially FoodBridge from GeorgeHacks.

## What The App Shows

- Overview: quick stats + profile summary
- Experience: timeline-style cards
- Projects: searchable project list with links
- Skills: grouped technical skills
- Awards: scholarships and academic recognition

## Tech Stack

- Python
- Dash + Plotly
- CSS
- Pytest

## Run It (Copy/Paste)

```bash
git clone https://github.com/js0596a/interactive-cv-dashboard.git
cd interactive-cv-dashboard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:8050`

If `8050` is busy:

```bash
python -c "from app import app; app.run(debug=True, port=8051)"
```

## Make It Yours

If you want to use this for your own CV:

1. Edit `cv_data.py` with your profile, experience, projects, skills, and awards.
2. Keep the same field names so the dashboard still renders correctly.
3. Run the app again.

## Links

- LinkedIn: [linkedin.com/in/edu-sal](https://linkedin.com/in/edu-sal)
- GitHub: [github.com/js0596a](https://github.com/js0596a)
- Devpost (FoodBridge / GeorgeHacks): [food-bridge-isqzu0](https://devpost.com/software/food-bridge-isqzu0)
- Recurtido MLP Dashboard: [recurtido-mlp-dashboard](https://github.com/js0596a/recurtido-mlp-dashboard)

## Note

This repo is public-safe and does not include private company datasets.
