from __future__ import annotations

from pathlib import Path
from numbers import Number
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cv_data import AWARDS, EDUCATION, EXPERIENCE, PROFILE, PROJECTS, SKILLS


REQUIRED_PROFILE_KEYS = {"name", "headline", "location", "email", "phone", "summary", "links"}
REQUIRED_EXPERIENCE_KEYS = {"role", "company", "location", "start_year", "end_year", "highlights", "tech"}
REQUIRED_PROJECT_KEYS = {"name", "description", "impact", "tech", "link", "score"}
REQUIRED_EDUCATION_KEYS = {"degree", "school", "year"}
REQUIRED_AWARD_KEYS = {"title", "issuer", "year", "type", "details"}


def _is_http_url(value: str) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def validate() -> list[str]:
    errors: list[str] = []

    missing_profile = REQUIRED_PROFILE_KEYS - set(PROFILE.keys())
    if missing_profile:
        errors.append(f"PROFILE missing keys: {sorted(missing_profile)}")

    if not isinstance(PROFILE.get("links"), dict) or not PROFILE.get("links"):
        errors.append("PROFILE.links must be a non-empty dict")
    else:
        for label, url in PROFILE["links"].items():
            if not label or not isinstance(label, str):
                errors.append("PROFILE.links has a non-string or empty label")
            if not _is_http_url(url):
                errors.append(f"PROFILE.links['{label}'] is not a valid URL")

    if not isinstance(EXPERIENCE, list) or not EXPERIENCE:
        errors.append("EXPERIENCE must be a non-empty list")
    else:
        for idx, row in enumerate(EXPERIENCE):
            missing = REQUIRED_EXPERIENCE_KEYS - set(row.keys())
            if missing:
                errors.append(f"EXPERIENCE[{idx}] missing keys: {sorted(missing)}")
                continue
            if not isinstance(row["start_year"], int) or not isinstance(row["end_year"], int):
                errors.append(f"EXPERIENCE[{idx}] start_year/end_year must be int")
            elif row["start_year"] > row["end_year"]:
                errors.append(f"EXPERIENCE[{idx}] start_year > end_year")
            if not isinstance(row["highlights"], list) or not row["highlights"]:
                errors.append(f"EXPERIENCE[{idx}] highlights must be a non-empty list")
            if not isinstance(row["tech"], list) or not row["tech"]:
                errors.append(f"EXPERIENCE[{idx}] tech must be a non-empty list")

    if not isinstance(PROJECTS, list) or not PROJECTS:
        errors.append("PROJECTS must be a non-empty list")
    else:
        for idx, row in enumerate(PROJECTS):
            missing = REQUIRED_PROJECT_KEYS - set(row.keys())
            if missing:
                errors.append(f"PROJECTS[{idx}] missing keys: {sorted(missing)}")
                continue
            if not _is_http_url(row["link"]):
                errors.append(f"PROJECTS[{idx}].link is not a valid URL")
            if not isinstance(row["score"], Number):
                errors.append(f"PROJECTS[{idx}].score must be numeric")
            elif not (0 <= float(row["score"]) <= 10):
                errors.append(f"PROJECTS[{idx}].score must be between 0 and 10")
            if not isinstance(row["tech"], list) or not row["tech"]:
                errors.append(f"PROJECTS[{idx}].tech must be a non-empty list")

    if not isinstance(SKILLS, dict) or not SKILLS:
        errors.append("SKILLS must be a non-empty dict")
    else:
        for category, items in SKILLS.items():
            if not isinstance(items, dict) or not items:
                errors.append(f"SKILLS['{category}'] must be a non-empty dict")
                continue
            for skill, level in items.items():
                if not isinstance(level, Number) or not (0 <= float(level) <= 10):
                    errors.append(f"SKILLS['{category}']['{skill}'] must be numeric between 0 and 10")

    if not isinstance(EDUCATION, list) or not EDUCATION:
        errors.append("EDUCATION must be a non-empty list")
    else:
        for idx, row in enumerate(EDUCATION):
            missing = REQUIRED_EDUCATION_KEYS - set(row.keys())
            if missing:
                errors.append(f"EDUCATION[{idx}] missing keys: {sorted(missing)}")
                continue
            if not isinstance(row["year"], int):
                errors.append(f"EDUCATION[{idx}].year must be int")

    if not isinstance(AWARDS, list):
        errors.append("AWARDS must be a list")
    else:
        for idx, row in enumerate(AWARDS):
            missing = REQUIRED_AWARD_KEYS - set(row.keys())
            if missing:
                errors.append(f"AWARDS[{idx}] missing keys: {sorted(missing)}")
                continue
            if not isinstance(row["year"], int):
                errors.append(f"AWARDS[{idx}].year must be int")
            if "amount" in row and row["amount"] is not None and not isinstance(row["amount"], Number):
                errors.append(f"AWARDS[{idx}].amount must be numeric or null")
            if not isinstance(row["details"], list) or not row["details"]:
                errors.append(f"AWARDS[{idx}].details must be a non-empty list")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("CV data validation failed:\n")
        for err in errors:
            print(f"- {err}")
        return 1

    print("CV data validation passed")
    print(f"Experience entries: {len(EXPERIENCE)}")
    print(f"Project entries: {len(PROJECTS)}")
    print(f"Skill categories: {len(SKILLS)}")
    print(f"Awards entries: {len(AWARDS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
