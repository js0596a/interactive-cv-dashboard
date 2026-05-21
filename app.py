from __future__ import annotations

from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go

from cv_data import AWARDS, EDUCATION, EXPERIENCE, PROFILE, PROJECTS, SKILLS

ACCENT_COLORS = ["#0ea5a4", "#ff7a59", "#ffd166", "#3aa8ff", "#6b9ac4", "#f29e4c"]


def flatten_skills(category: str, min_level: int) -> list[dict]:
    rows = []
    for cat_name, items in SKILLS.items():
        if category != "All" and cat_name != category:
            continue
        for skill, level in items.items():
            if level >= min_level:
                rows.append({"category": cat_name, "skill": skill, "level": level})
    rows.sort(key=lambda row: row["level"], reverse=True)
    return rows


def filter_projects(tech_filter: list[str], query: str) -> list[dict]:
    tech_filter = tech_filter or []
    query = (query or "").strip().lower()
    filtered = []

    for project in PROJECTS:
        stack = {tech.lower() for tech in project["tech"]}
        if tech_filter and not stack.intersection({t.lower() for t in tech_filter}):
            continue
        if query:
            searchable = " ".join(
                [project["name"], project["description"], project["impact"], " ".join(project["tech"])]
            ).lower()
            if query not in searchable:
                continue
        filtered.append(project)

    return filtered


def filter_experience(tech_filter: list[str]) -> list[dict]:
    tech_filter = tech_filter or []
    if not tech_filter:
        return EXPERIENCE

    filtered = []
    lowered = {tech.lower() for tech in tech_filter}
    for role in EXPERIENCE:
        if lowered.intersection({tech.lower() for tech in role["tech"]}):
            filtered.append(role)
    return filtered


def card(title: str, value: str, subtitle: str) -> html.Div:
    return html.Div(
        className="kpi-card",
        children=[
            html.Div(title, className="kpi-title"),
            html.Div(value, className="kpi-value"),
            html.Div(subtitle, className="kpi-subtitle"),
        ],
    )


def empty_figure(title: str, message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=14, color="#35495e"),
    )
    fig.update_layout(
        title=title,
        margin=dict(l=24, r=24, t=60, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        font=dict(family="'Space Grotesk', sans-serif", color="#16212f"),
    )
    return fig


def style_figure(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, x=0.01, xanchor="left"),
        margin=dict(l=24, r=24, t=60, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'Space Grotesk', sans-serif", color="#16212f"),
    )
    fig.update_xaxes(gridcolor="rgba(22,33,47,0.12)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(22,33,47,0.12)", zeroline=False)
    return fig


def make_timeline_figure(roles: list[dict]) -> go.Figure:
    if not roles:
        return empty_figure("Career Timeline", "No experience matches this filter.")

    fig = go.Figure()
    for idx, role in enumerate(sorted(roles, key=lambda r: r["start_year"])):
        start_year = role["start_year"]
        end_year = role["end_year"]
        duration = end_year - start_year + 1
        label = f"{role['role']} | {role['company']}"
        fig.add_trace(
            go.Bar(
                x=[duration],
                y=[label],
                base=[start_year],
                orientation="h",
                marker=dict(color=ACCENT_COLORS[idx % len(ACCENT_COLORS)]),
                customdata=[[start_year, end_year, role["location"]]],
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Years: %{customdata[0]}-%{customdata[1]}<br>"
                    "Location: %{customdata[2]}"
                    "<extra></extra>"
                ),
            )
        )

    min_year = min(item["start_year"] for item in roles) - 1
    max_year = max(item["end_year"] for item in roles) + 1

    fig.update_layout(showlegend=False, bargap=0.5)
    fig.update_xaxes(dtick=1, range=[min_year, max_year], title="Year")
    return style_figure(fig, "Career Timeline")


def make_radar_figure(skill_rows: list[dict]) -> go.Figure:
    if not skill_rows:
        return empty_figure("Skill Radar", "No skills match this filter.")

    labels = [row["skill"] for row in skill_rows[:10]]
    values = [row["level"] for row in skill_rows[:10]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values + values[:1],
                theta=labels + labels[:1],
                fill="toself",
                line=dict(color="#0ea5a4", width=2),
                fillcolor="rgba(14,165,164,0.28)",
                marker=dict(size=5, color="#ff7a59"),
                name="Skill Level",
            )
        ]
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10], dtick=2, gridcolor="rgba(22,33,47,0.16)")),
        showlegend=False,
    )
    return style_figure(fig, "Skill Radar (Top 10)")


def make_skill_bubble_figure(skill_rows: list[dict]) -> go.Figure:
    if not skill_rows:
        return empty_figure("Skill Matrix", "Adjust filters to reveal your strongest tools.")

    fig = go.Figure(
        data=[
            go.Scatter(
                x=[row["category"] for row in skill_rows],
                y=[row["skill"] for row in skill_rows],
                mode="markers",
                marker=dict(
                    size=[row["level"] * 4 + 6 for row in skill_rows],
                    color=[row["level"] for row in skill_rows],
                    colorscale=[
                        [0.0, "#8ecae6"],
                        [0.35, "#3aa8ff"],
                        [0.7, "#0ea5a4"],
                        [1.0, "#ff7a59"],
                    ],
                    line=dict(width=1, color="rgba(22,33,47,0.16)"),
                    showscale=True,
                    colorbar=dict(title="Level"),
                ),
                text=[f"{row['skill']} ({row['level']}/10)" for row in skill_rows],
                hovertemplate="<b>%{y}</b><br>Category: %{x}<br>%{text}<extra></extra>",
            )
        ]
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return style_figure(fig, "Skill Matrix")


def make_project_score_figure(projects: list[dict]) -> go.Figure:
    if not projects:
        return empty_figure("Project Impact", "No projects match this filter.")

    ordered = sorted(projects, key=lambda p: p["score"], reverse=True)
    fig = go.Figure(
        data=[
            go.Bar(
                x=[project["score"] for project in ordered],
                y=[project["name"] for project in ordered],
                orientation="h",
                marker=dict(
                    color=[project["score"] for project in ordered],
                    colorscale=[
                        [0.0, "#90e0ef"],
                        [0.5, "#3aa8ff"],
                        [1.0, "#ff7a59"],
                    ],
                    line=dict(width=1, color="rgba(22,33,47,0.16)"),
                ),
                hovertemplate="<b>%{y}</b><br>Impact Score: %{x}<extra></extra>",
            )
        ]
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(range=[0, 10], dtick=1)
    return style_figure(fig, "Project Impact Score")


def make_project_cards(projects: list[dict]) -> list[html.Div]:
    if not projects:
        return [html.Div("No projects match your filters.", className="empty-state")]

    cards = []
    for project in projects:
        card_class = "project-card featured" if project.get("badge") else "project-card"
        card_children = []
        if project.get("badge"):
            card_children.append(html.Div(project["badge"], className="feature-badge"))

        card_children.extend(
            [
                html.Div(project["name"], className="card-title"),
                html.Div(project["description"], className="card-description"),
                html.Div(project["impact"], className="card-impact"),
                html.Div(
                    [html.Span(tag, className="tag") for tag in project["tech"]],
                    className="tag-row",
                ),
                html.A("View Project", href=project["link"], target="_blank", className="card-link"),
            ]
        )

        cards.append(
            html.Div(
                className=card_class,
                children=card_children,
            )
        )
    return cards


def make_experience_cards(roles: list[dict]) -> list[html.Div]:
    if not roles:
        return [html.Div("No experience roles match this tech filter.", className="empty-state")]

    cards = []
    for role in sorted(roles, key=lambda r: r["start_year"], reverse=True):
        cards.append(
            html.Div(
                className="experience-card",
                children=[
                    html.Div(f"{role['role']} @ {role['company']}", className="card-title"),
                    html.Div(f"{role['start_year']} - {role['end_year']} | {role['location']}", className="card-meta"),
                    html.Ul([html.Li(item) for item in role["highlights"]], className="bullet-list"),
                    html.Div([html.Span(tag, className="tag") for tag in role["tech"]], className="tag-row"),
                ],
            )
        )
    return cards


def make_education_cards() -> list[html.Div]:
    cards = []
    for item in EDUCATION:
        cards.append(
            html.Div(
                className="education-card",
                children=[
                    html.Div(item["degree"], className="card-title"),
                    html.Div(item["school"], className="card-description"),
                    html.Div(str(item["year"]), className="card-meta"),
                ],
            )
        )
    return cards


def make_award_cards() -> list[html.Div]:
    if not AWARDS:
        return [html.Div("No scholarships or awards added yet.", className="empty-state")]

    cards = []
    for award in sorted(AWARDS, key=lambda item: item.get("year", 0), reverse=True):
        amount = award.get("amount")
        amount_text = f"${amount:,}" if amount else "Recognition"
        summary = f"{award['type']} | {amount_text}"
        cards.append(
            html.Div(
                className="award-card",
                children=[
                    html.Div(award["title"], className="card-title"),
                    html.Div(f"{award['year']} | {award['issuer']}", className="card-meta"),
                    html.Div(summary, className="card-impact"),
                    html.Ul([html.Li(item) for item in award["details"]], className="bullet-list"),
                ],
            )
        )
    return cards


def make_skill_chips(skill_rows: list[dict]) -> list[html.Span]:
    if not skill_rows:
        return [html.Span("No skills selected", className="tag")]
    return [html.Span(f"{row['skill']} ({row['level']})", className="tag") for row in skill_rows]


def panel_visibility(selected_view: str) -> tuple[dict, dict, dict, dict]:
    hidden = {"display": "none"}
    visible = {"display": "block"}

    if selected_view == "overview":
        return visible, hidden, hidden, hidden
    if selected_view == "experience":
        return hidden, visible, hidden, hidden
    if selected_view == "projects":
        return hidden, hidden, visible, hidden
    return hidden, hidden, hidden, visible


all_tech = sorted({tech for project in PROJECTS for tech in project["tech"]} | {tech for role in EXPERIENCE for tech in role["tech"]})
all_categories = ["All"] + sorted(SKILLS.keys())

app = Dash(__name__)
app.title = "Interactive CV Dashboard"

app.layout = html.Div(
    id="app-shell",
    children=[
        html.Div(className="bg-grid"),
        html.Div(className="orb orb-1"),
        html.Div(className="orb orb-2"),
        html.Div(className="orb orb-3"),
        html.Div(
            className="page",
            children=[
                html.Header(
                    className="hero",
                    children=[
                        html.Div("Interactive CV", className="eyebrow"),
                        html.H1(PROFILE["name"], className="name"),
                        html.Div(PROFILE["headline"], className="headline"),
                        html.P(PROFILE["summary"], className="summary"),
                        html.Div(
                            className="contact-row",
                            children=[
                                html.Span(PROFILE["location"]),
                                html.Span(PROFILE["email"]),
                                html.Span(PROFILE["phone"]),
                            ],
                        ),
                        html.Div(
                            className="link-row",
                            children=[
                                html.A(label, href=url, target="_blank", className="pill-link")
                                for label, url in PROFILE["links"].items()
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="dashboard-grid",
                    children=[
                        html.Aside(
                            className="control-panel",
                            children=[
                                html.H3("Control Deck"),
                                html.Label("View"),
                                dcc.RadioItems(
                                    id="view-mode",
                                    options=[
                                        {"label": "Overview", "value": "overview"},
                                        {"label": "Experience", "value": "experience"},
                                        {"label": "Projects", "value": "projects"},
                                        {"label": "Skills", "value": "skills"},
                                    ],
                                    value="overview",
                                    className="view-pills",
                                    labelClassName="view-pill",
                                ),
                                html.Label("Skill Category"),
                                dcc.Dropdown(
                                    id="skill-category",
                                    options=[{"label": item, "value": item} for item in all_categories],
                                    value="All",
                                    clearable=False,
                                ),
                                html.Label("Minimum Skill Level"),
                                dcc.Slider(
                                    id="skill-min",
                                    min=1,
                                    max=10,
                                    value=6,
                                    step=1,
                                    marks={1: "1", 4: "4", 7: "7", 10: "10"},
                                ),
                                html.Label("Filter by Technology"),
                                dcc.Dropdown(
                                    id="tech-filter",
                                    options=[{"label": item, "value": item} for item in all_tech],
                                    multi=True,
                                    placeholder="Select one or more",
                                ),
                                html.Label("Search Projects"),
                                dcc.Input(
                                    id="project-search",
                                    type="text",
                                    placeholder="e.g. NLP, dashboard, API",
                                    debounce=True,
                                ),
                            ],
                        ),
                        html.Main(
                            className="main-panel",
                            children=[
                                html.Div(id="view-badge", className="view-badge"),
                                html.Div(id="kpi-row", className="kpi-row"),
                                html.Div(
                                    id="overview-panel",
                                    className="panel",
                                    children=[
                                        dcc.Graph(id="timeline-graph", config={"displayModeBar": False}),
                                        html.Div(
                                            className="split-grid",
                                            children=[
                                                dcc.Graph(id="project-score", config={"displayModeBar": False}),
                                                dcc.Graph(id="skill-radar", config={"displayModeBar": False}),
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="experience-panel",
                                    className="panel",
                                    children=[
                                        html.H3("Experience Story"),
                                        html.Div(id="experience-grid", className="card-grid"),
                                        html.H3("Education"),
                                        html.Div(id="education-grid", className="education-grid"),
                                        html.H3("Scholarships & Awards"),
                                        html.Div(id="awards-grid", className="card-grid"),
                                    ],
                                ),
                                html.Div(
                                    id="projects-panel",
                                    className="panel",
                                    children=[
                                        html.H3("Selected Projects"),
                                        html.Div(id="project-grid", className="card-grid"),
                                    ],
                                ),
                                html.Div(
                                    id="skills-panel",
                                    className="panel",
                                    children=[
                                        dcc.Graph(id="skill-bubbles", config={"displayModeBar": False}),
                                        html.H3("Skill Tags"),
                                        html.Div(id="skill-chips", className="tag-row"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("view-badge", "children"),
    Output("kpi-row", "children"),
    Output("timeline-graph", "figure"),
    Output("skill-radar", "figure"),
    Output("skill-bubbles", "figure"),
    Output("project-score", "figure"),
    Output("project-grid", "children"),
    Output("experience-grid", "children"),
    Output("education-grid", "children"),
    Output("awards-grid", "children"),
    Output("skill-chips", "children"),
    Output("overview-panel", "style"),
    Output("experience-panel", "style"),
    Output("projects-panel", "style"),
    Output("skills-panel", "style"),
    Input("skill-category", "value"),
    Input("skill-min", "value"),
    Input("tech-filter", "value"),
    Input("project-search", "value"),
    Input("view-mode", "value"),
)
def refresh_dashboard(category: str, min_level: int, tech_filter: list[str], search: str, view_mode: str):
    skill_rows = flatten_skills(category, min_level)
    projects = filter_projects(tech_filter, search)
    roles = filter_experience(tech_filter)
    award_funding = sum((item.get("amount") or 0) for item in AWARDS)

    min_start = min(item["start_year"] for item in EXPERIENCE)
    max_end = max(item["end_year"] for item in EXPERIENCE)
    total_years = max_end - min_start + 1

    kpis = [
        card("Career Span", f"{total_years} yrs", f"{min_start}-{max_end}"),
        card("Visible Projects", str(len(projects)), "Based on filters"),
        card("Visible Skills", str(len(skill_rows)), "Above minimum level"),
        card("Roles", str(len(roles)), "Matching tech filter"),
        card("Awards", str(len(AWARDS)), f"${award_funding:,} scholarship funding"),
    ]

    view_title = {
        "overview": "Overview Mode",
        "experience": "Experience Mode",
        "projects": "Projects Mode",
        "skills": "Skills Mode",
    }.get(view_mode, "Overview Mode")

    overview_style, experience_style, projects_style, skills_style = panel_visibility(view_mode)

    return (
        view_title,
        kpis,
        make_timeline_figure(roles),
        make_radar_figure(skill_rows),
        make_skill_bubble_figure(skill_rows),
        make_project_score_figure(projects),
        make_project_cards(projects),
        make_experience_cards(roles),
        make_education_cards(),
        make_award_cards(),
        make_skill_chips(skill_rows[:24]),
        overview_style,
        experience_style,
        projects_style,
        skills_style,
    )


if __name__ == "__main__":
    app.run(debug=True)
