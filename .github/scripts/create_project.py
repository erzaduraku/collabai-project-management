#!/usr/bin/env python3
"""
CollabAI - GitHub Project Board Creator
========================================
Creates a GitHub Projects v2 board with columns:
  To Do | In Progress | Review | Done

Then adds all open/to-do issues to the board.

Usage:
    GITHUB_TOKEN=<token> GITHUB_REPO=owner/repo python3 create_project.py

Requires: token must have project write scope (classic PAT or fine-grained with projects permission)
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "erzaduraku/collabai-project-management")
GRAPHQL_URL = "https://api.github.com/graphql"

PROJECT_TITLE = "CollabAI Sprint Board"
PROJECT_COLUMNS = ["To Do", "In Progress", "Review", "Done"]


def _gql(query: str, variables: dict | None = None) -> dict:
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    body = json.dumps(payload).encode()
    headers = {
        "Authorization": f"bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    req = urllib.request.Request(GRAPHQL_URL, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if "errors" in result:
        raise RuntimeError(f"GraphQL errors: {result['errors']}")
    return result["data"]


def get_owner_id(owner: str) -> str:
    data = _gql("""
        query($login: String!) {
            repositoryOwner(login: $login) { id }
        }
    """, {"login": owner})
    return data["repositoryOwner"]["id"]


def create_project(owner_id: str, title: str) -> str:
    """Create a Projects v2 board; return projectId."""
    data = _gql("""
        mutation($ownerId: ID!, $title: String!) {
            createProjectV2(input: { ownerId: $ownerId, title: $title }) {
                projectV2 { id number }
            }
        }
    """, {"ownerId": owner_id, "title": title})
    project = data["createProjectV2"]["projectV2"]
    print(f"  ✓ Created project #{project['number']}: {title}  (id={project['id']})")
    return project["id"]


def get_status_field_id(project_id: str) -> tuple[str, dict[str, str]]:
    """Return (fieldId, {optionName: optionId}) for the Status field."""
    data = _gql("""
        query($projectId: ID!) {
            node(id: $projectId) {
                ... on ProjectV2 {
                    fields(first: 20) {
                        nodes {
                            ... on ProjectV2SingleSelectField {
                                id name
                                options { id name }
                            }
                        }
                    }
                }
            }
        }
    """, {"projectId": project_id})
    for field in data["node"]["fields"]["nodes"]:
        if field.get("name") == "Status":
            options = {opt["name"]: opt["id"] for opt in field.get("options", [])}
            return field["id"], options
    raise RuntimeError("Status field not found on project")


def add_column_option(project_id: str, field_id: str, name: str) -> str:
    """Add a single-select option; return its id."""
    data = _gql("""
        mutation($projectId: ID!, $fieldId: ID!, $name: String!) {
            updateProjectV2Field(input: {
                projectId: $projectId,
                fieldId: $fieldId,
                singleSelectOptions: [{ name: $name, color: GRAY, description: "" }]
            }) {
                projectV2Field {
                    ... on ProjectV2SingleSelectField {
                        options { id name }
                    }
                }
            }
        }
    """, {"projectId": project_id, "fieldId": field_id, "name": name})
    # Return the id of the newly created option
    for opt in data["updateProjectV2Field"]["projectV2Field"]["options"]:
        if opt["name"] == name:
            return opt["id"]
    raise RuntimeError(f"Could not find option '{name}' after creation")


def get_repo_issue_node_ids(owner: str, repo: str) -> list[tuple[int, str]]:
    """Return list of (issueNumber, nodeId) for all open issues."""
    issues: list[tuple[int, str]] = []
    cursor = None
    while True:
        vars_: dict = {"owner": owner, "repo": repo, "cursor": cursor}
        data = _gql("""
            query($owner: String!, $repo: String!, $cursor: String) {
                repository(owner: $owner, name: $repo) {
                    issues(first: 100, after: $cursor, states: OPEN) {
                        pageInfo { hasNextPage endCursor }
                        nodes { number id }
                    }
                }
            }
        """, vars_)
        page = data["repository"]["issues"]
        for node in page["nodes"]:
            issues.append((node["number"], node["id"]))
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return issues


def add_issue_to_project(project_id: str, issue_node_id: str) -> str:
    """Add an issue to the project; return item node id."""
    data = _gql("""
        mutation($projectId: ID!, $contentId: ID!) {
            addProjectV2ItemById(input: { projectId: $projectId, contentId: $contentId }) {
                item { id }
            }
        }
    """, {"projectId": project_id, "contentId": issue_node_id})
    return data["addProjectV2ItemById"]["item"]["id"]


def set_item_status(
    project_id: str, item_id: str, field_id: str, option_id: str
) -> None:
    _gql("""
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
            updateProjectV2ItemFieldValue(input: {
                projectId: $projectId,
                itemId: $itemId,
                fieldId: $fieldId,
                value: { singleSelectOptionId: $optionId }
            }) { projectV2Item { id } }
        }
    """, {
        "projectId": project_id,
        "itemId": item_id,
        "fieldId": field_id,
        "optionId": option_id,
    })


def main() -> None:
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN is not set", file=sys.stderr)
        sys.exit(1)

    owner, repo = GITHUB_REPO.split("/", 1)

    print("=" * 60)
    print("CollabAI GitHub Project Board Creator")
    print(f"Repository: {GITHUB_REPO}")
    print("=" * 60)

    print("\n[1/5] Resolving owner node ID…")
    owner_id = get_owner_id(owner)
    print(f"  Owner ID: {owner_id}")

    print(f"\n[2/5] Creating project '{PROJECT_TITLE}'…")
    project_id = create_project(owner_id, PROJECT_TITLE)

    print("\n[3/5] Configuring Status columns…")
    field_id, existing_options = get_status_field_id(project_id)
    print(f"  Existing options: {list(existing_options.keys())}")

    # Ensure all desired columns exist
    for col in PROJECT_COLUMNS:
        if col not in existing_options:
            opt_id = add_column_option(project_id, field_id, col)
            existing_options[col] = opt_id
            print(f"  ✓ Added column: {col}")
        else:
            print(f"  ✓ Column exists: {col}")

    todo_option_id = existing_options.get("To Do", "")

    print("\n[4/5] Fetching open issues…")
    issues = get_repo_issue_node_ids(owner, repo)
    print(f"  Found {len(issues)} open issues")

    print("\n[5/5] Adding issues to project board…")
    for number, node_id in issues:
        item_id = add_issue_to_project(project_id, node_id)
        if todo_option_id:
            set_item_status(project_id, item_id, field_id, todo_option_id)
        print(f"  ✓ Added issue #{number}")
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print(f"Done! Project board created: https://github.com/{GITHUB_REPO}/projects")
    print("=" * 60)


if __name__ == "__main__":
    main()
