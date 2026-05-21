from __future__ import annotations

from numbers import Number

from cv_data import AWARDS, EDUCATION, EXPERIENCE, PROFILE, PROJECTS, SKILLS


def test_profile_has_required_keys() -> None:
    required = {"name", "headline", "location", "email", "phone", "summary", "links"}
    assert required.issubset(PROFILE.keys())


def test_links_look_like_urls() -> None:
    for label, url in PROFILE["links"].items():
        assert label
        assert isinstance(url, str)
        assert url.startswith(("http://", "https://"))


def test_experience_rows_are_well_formed() -> None:
    assert EXPERIENCE
    for row in EXPERIENCE:
        assert row["start_year"] <= row["end_year"]
        assert isinstance(row["highlights"], list) and row["highlights"]
        assert isinstance(row["tech"], list) and row["tech"]


def test_projects_scores_and_links() -> None:
    assert PROJECTS
    for row in PROJECTS:
        assert 0 <= float(row["score"]) <= 10
        assert row["link"].startswith(("http://", "https://"))
        assert isinstance(row["tech"], list) and row["tech"]


def test_skills_range() -> None:
    assert SKILLS
    for category, skills in SKILLS.items():
        assert category
        assert skills
        for level in skills.values():
            assert isinstance(level, Number)
            assert 0 <= float(level) <= 10


def test_education_and_awards() -> None:
    assert EDUCATION
    for item in EDUCATION:
        assert isinstance(item["year"], int)

    for award in AWARDS:
        assert isinstance(award["year"], int)
        assert isinstance(award["details"], list) and award["details"]
