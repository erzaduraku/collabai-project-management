#!/usr/bin/env python3
"""
CollabAI Project Management - GitHub Issues Import Script
=========================================================
Imports tasks from tasks.csv into GitHub Issues with:
  - Labels (backend, frontend, auth, db, api, etc.)
  - Milestones (Sprint 1, Sprint 2, Sprint 3)
  - Assignees (mapped from first names to GitHub usernames)
  - Story points in issue body
  - Dependencies listed in issue body

Usage (GitHub Actions provides TOKEN and REPO automatically):
    python3 import_issues.py

Environment variables:
    GITHUB_TOKEN  - Personal access token with repo + issues write scope
    GITHUB_REPO   - Owner/repo slug, e.g. "erzaduraku/collabai-project-management"

Assignee mapping (edit ASSIGNEE_MAP to match real GitHub usernames):
    Erza     -> erzaduraku
    Edonita  -> set ASSIGNEE_EDONITA env var or edit map below
    Leona    -> set ASSIGNEE_LEONA   env var or edit map below
    Engji    -> set ASSIGNEE_ENGJI   env var or edit map below
    Fatlinda -> set ASSIGNEE_FATLINDA env var or edit map below
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "erzaduraku/collabai-project-management")
API_BASE = "https://api.github.com"
TASKS_CSV = Path(__file__).parent.parent.parent / "tasks.csv"

# Map first names from CSV to GitHub usernames.
# Override any entry with an environment variable (e.g. ASSIGNEE_EDONITA=myuser).
ASSIGNEE_MAP: dict[str, str] = {
    "Erza": os.environ.get("ASSIGNEE_ERZA", "erzaduraku"),
    "Edonita": os.environ.get("ASSIGNEE_EDONITA", ""),
    "Leona": os.environ.get("ASSIGNEE_LEONA", ""),
    "Engji": os.environ.get("ASSIGNEE_ENGJI", ""),
    "Fatlinda": os.environ.get("ASSIGNEE_FATLINDA", ""),
}

# Label definitions: name -> (color hex without #, description)
LABEL_DEFINITIONS: dict[str, tuple[str, str]] = {
    "backend":    ("0075ca", "Backend / Django / DRF work"),
    "frontend":   ("e4e669", "Frontend / React work"),
    "auth":       ("d93f0b", "Authentication & Authorization"),
    "db":         ("1d76db", "Database models & migrations"),
    "api":        ("0052cc", "REST API endpoints"),
    "testing":    ("bfd4f2", "Tests (unit, integration, e2e)"),
    "ci":         ("c5def5", "CI/CD pipeline"),
    "docs":       ("fef2c0", "Documentation"),
    "ai":         ("b60205", "AI / OpenAI integration"),
    "pm":         ("006b75", "Project management"),
    "github":     ("006b75", "GitHub configuration"),
    "drf":        ("0075ca", "Django REST Framework"),
    "oop":        ("0075ca", "Object-Oriented Programming"),
    "middleware": ("0075ca", "Middleware"),
    "react":      ("e4e669", "React / Frontend framework"),
    "tenant":     ("1d76db", "Multi-tenancy"),
    "redis":      ("e11d48", "Redis / Caching"),
    "tasks":      ("e4e669", "Task management features"),
    "roles":      ("d93f0b", "Role-based access control"),
    "e2e":        ("bfd4f2", "End-to-end testing"),
    "search":     ("0052cc", "Search & filtering"),
    "celery":     ("b60205", "Celery async tasks"),
    "async":      ("b60205", "Async background jobs"),
    "swagger":    ("fef2c0", "Swagger / OpenAPI docs"),
    "final":      ("006b75", "Final integration & delivery"),
    "priority:high":   ("b60205", "High priority"),
    "priority:medium": ("e4e669", "Medium priority"),
    "priority:low":    ("0e8a16", "Low priority"),
}

# Milestones: title -> due_on (ISO 8601 date, midnight UTC)
MILESTONE_DEFINITIONS: list[dict] = [
    {
        "title": "Sprint 1",
        "description": "Foundation: Setup, Auth, Core Models, Basic Frontend",
        "due_on": "2026-05-09T00:00:00Z",
    },
    {
        "title": "Sprint 2",
        "description": "Features: CRUD APIs, Dashboard, Task Board, CI, Cache",
        "due_on": "2026-05-14T00:00:00Z",
    },
    {
        "title": "Sprint 3",
        "description": "Polish: AI, Search, Docs, Final Integration",
        "due_on": "2026-05-20T00:00:00Z",
    },
]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _headers() -> dict[str, str]:
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _request(method: str, path: str, data: dict | None = None) -> dict | list:
    url = f"{API_BASE}{path}"
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=_headers(), method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        msg = exc.read().decode()
        print(f"  ✗ HTTP {exc.code} {method} {path}: {msg}", file=sys.stderr)
        raise


def _get(path: str) -> dict | list:
    return _request("GET", path)


def _post(path: str, data: dict) -> dict:
    return _request("POST", path, data)  # type: ignore[return-value]


def _patch(path: str, data: dict) -> dict:
    return _request("PATCH", path, data)  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------

def ensure_labels() -> dict[str, int]:
    """Create missing labels; return {name: id} map."""
    repo_path = f"/repos/{GITHUB_REPO}/labels"
    existing: dict[str, int] = {}

    # Fetch existing labels (paginate up to 5 pages)
    page = 1
    while True:
        page_labels = _get(f"{repo_path}?per_page=100&page={page}")
        assert isinstance(page_labels, list)
        for lbl in page_labels:
            existing[lbl["name"]] = lbl["id"]
        if len(page_labels) < 100:
            break
        page += 1

    print(f"  Found {len(existing)} existing labels")

    for name, (color, description) in LABEL_DEFINITIONS.items():
        if name in existing:
            continue
        try:
            lbl = _post(repo_path, {"name": name, "color": color, "description": description})
            existing[name] = lbl["id"]
            print(f"  ✓ Created label: {name}")
        except urllib.error.HTTPError:
            # Label may have been created concurrently or there's a conflict; skip
            pass
        time.sleep(0.2)  # Respect rate limits

    return existing


def ensure_milestones() -> dict[str, int]:
    """Create missing milestones; return {title: number} map."""
    repo_path = f"/repos/{GITHUB_REPO}/milestones"
    existing_milestones = _get(f"{repo_path}?state=all&per_page=100")
    assert isinstance(existing_milestones, list)
    existing: dict[str, int] = {m["title"]: m["number"] for m in existing_milestones}

    print(f"  Found {len(existing)} existing milestones")

    for ms in MILESTONE_DEFINITIONS:
        if ms["title"] in existing:
            print(f"  ✓ Milestone exists: {ms['title']}")
            continue
        created = _post(repo_path, ms)
        existing[ms["title"]] = created["number"]
        print(f"  ✓ Created milestone: {ms['title']}")
        time.sleep(0.2)

    return existing


def get_existing_issue_titles() -> set[str]:
    """Return set of existing open+closed issue titles to avoid duplicates."""
    titles: set[str] = set()
    page = 1
    while True:
        issues = _get(f"/repos/{GITHUB_REPO}/issues?state=all&per_page=100&page={page}")
        assert isinstance(issues, list)
        for issue in issues:
            if "pull_request" not in issue:
                titles.add(issue["title"])
        if len(issues) < 100:
            break
        page += 1
    return titles


def resolve_assignees(assignees_str: str) -> list[str]:
    """Convert comma-separated first names to GitHub usernames."""
    result: list[str] = []
    for name in assignees_str.split(","):
        name = name.strip()
        username = ASSIGNEE_MAP.get(name, "")
        if username:
            result.append(username)
    return result


def create_issue(
    row: dict,
    milestone_map: dict[str, int],
    existing_titles: set[str],
) -> bool:
    """Create a single GitHub issue from a CSV row. Returns True if created."""
    title = row["Title"].strip()

    if title in existing_titles:
        print(f"  ↩ Skipping (already exists): {title}")
        return False

    # Build label list from CSV + priority
    label_names: list[str] = []
    for lbl in row.get("Labels", "").split(","):
        lbl = lbl.strip()
        if lbl and lbl in LABEL_DEFINITIONS:
            label_names.append(lbl)

    priority = row.get("Priority", "").strip().lower()
    if priority in ("high", "medium", "low"):
        label_names.append(f"priority:{priority}")

    # Milestone
    sprint = row.get("Sprint", "").strip()
    milestone_number = milestone_map.get(sprint)

    # Assignees
    assignees = resolve_assignees(row.get("Assignees", ""))

    # Body – append metadata footer
    body = row.get("Body", "").strip()
    metadata_lines: list[str] = []
    if row.get("Start Date"):
        metadata_lines.append(f"**Start Date:** {row['Start Date']}")
    if row.get("Due Date"):
        metadata_lines.append(f"**Due Date:** {row['Due Date']}")
    if row.get("Sprint"):
        metadata_lines.append(f"**Sprint:** {row['Sprint']}")
    if row.get("Status"):
        metadata_lines.append(f"**Status:** {row['Status']}")
    if row.get("Story Points"):
        metadata_lines.append(f"**Story Points:** {row['Story Points']}")
    if row.get("Dependencies"):
        metadata_lines.append(f"**Dependencies:** {row['Dependencies']}")

    if metadata_lines:
        body += "\n\n---\n" + "\n".join(metadata_lines)

    payload: dict = {
        "title": title,
        "body": body,
        "labels": label_names,
    }
    if milestone_number:
        payload["milestone"] = milestone_number
    if assignees:
        payload["assignees"] = assignees

    try:
        issue = _post(f"/repos/{GITHUB_REPO}/issues", payload)
        existing_titles.add(title)
        print(f"  ✓ Created issue #{issue['number']}: {title}")
        return True
    except urllib.error.HTTPError:
        print(f"  ✗ Failed to create issue: {title}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _resolve_csv_path() -> Path:
    """Return the path to tasks.csv, trying multiple locations."""
    if TASKS_CSV.exists():
        return TASKS_CSV
    alt = Path(__file__).parent / "tasks.csv"
    if alt.exists():
        return alt
    raise FileNotFoundError(f"tasks.csv not found (tried {TASKS_CSV} and {alt})")


def main() -> None:
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable is not set", file=sys.stderr)
        sys.exit(1)

    try:
        csv_path = _resolve_csv_path()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print(f"CollabAI GitHub Issues Importer")
    print(f"Repository: {GITHUB_REPO}")
    print("=" * 60)

    print("\n[1/4] Ensuring labels exist…")
    ensure_labels()

    print("\n[2/4] Ensuring milestones exist…")
    milestone_map = ensure_milestones()

    print("\n[3/4] Fetching existing issues…")
    existing_titles = get_existing_issue_titles()
    print(f"  Found {len(existing_titles)} existing issues")

    print("\n[4/4] Creating issues from tasks.csv…")
    created = 0
    skipped = 0
    failed = 0

    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if not row.get("Title", "").strip():
                continue
            try:
                if create_issue(row, milestone_map, existing_titles):
                    created += 1
                else:
                    skipped += 1
            except Exception as exc:
                print(f"  ✗ Error processing row '{row.get('Title', '?')}': {exc}", file=sys.stderr)
                failed += 1
            time.sleep(0.5)  # Stay well within GitHub rate limits (5000 req/h)

    print("\n" + "=" * 60)
    print(f"Done!  Created: {created}  Skipped: {skipped}  Failed: {failed}")
    print("=" * 60)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
