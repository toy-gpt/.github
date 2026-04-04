"""
checks.py — toy-gpt org health scanner

WHY: Scan all repos in the toy-gpt org and report on workflow status,
     file presence, and migration state (mkdocs -> zensical).

USAGE:
    uv run --env-file .env python src/toy-gpt-github/checks.py
    uv run --env-file .env python -m toy-gpt-github.checks

REQUIRES:
    export GITHUB_TOKEN=<your-pat>   # needs repo + actions read scope
    pip install httpx rich           # or add to pyproject.toml dev deps
"""

import os
import sys
from dataclasses import dataclass, field

import httpx
from rich.console import Console
from rich.table import Table

# ============================================================
# Config
# ============================================================

ORG = "toy-gpt"
BASE = "https://api.github.com"

# Workflow filenames to check (as they appear in .github/workflows/)
WORKFLOWS_TO_CHECK = ["ci-shared.yml", "deploy-docs-shared.yml", "links.yml"]

# Files whose presence indicates repo health / migration state
FILES_TO_CHECK = {
    "zensical.toml": "zensical",
    "SE_MANIFEST.toml": "manifest",
    ".github/dependabot.yml": "dependabot",
    "py.typed": "py.typed",
}

# Thin caller pattern — workflow files should contain this string if migrated
CALLER_PATTERN = "uses: toy-gpt/.github/.github/workflows/"

# Repos that ARE the org workflows — skip thin-caller check
SKIP_THIN_CALLER = {".github"}

# Repos that don't need SE_MANIFEST.toml
SKIP_MANIFEST = {".github", "toy-gpt-chat"}

# ============================================================
# Data
# ============================================================


@dataclass
class WorkflowStatus:
    name: str
    status: str  # "pass", "fail", "missing", "unknown"
    is_thin_caller: bool = False


@dataclass
class RepoReport:
    name: str
    archived: bool = False
    workflows: list[WorkflowStatus] = field(default_factory=list)
    files: dict[str, bool] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)


# ============================================================
# GitHub API helpers
# ============================================================


def make_client(token: str) -> httpx.Client:
    return httpx.Client(
        base_url=BASE,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=15,
    )


def get_repos(client: httpx.Client, org: str) -> list[dict]:
    repos = []
    page = 1
    while True:
        r = client.get(f"/orgs/{org}/repos", params={"per_page": 100, "page": page})
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos


def get_latest_run(client: httpx.Client, org: str, repo: str, workflow: str) -> str:
    """Returns 'pass', 'fail', 'missing', or 'unknown'."""
    r = client.get(
        f"/repos/{org}/{repo}/actions/workflows/{workflow}/runs",
        params={"per_page": 1, "branch": "main"},
    )
    if r.status_code == 404:
        return "missing"
    if r.status_code != 200:
        return "unknown"
    runs = r.json().get("workflow_runs", [])
    if not runs:
        return "missing"
    conclusion = runs[0].get("conclusion")
    if conclusion == "success":
        return "pass"
    if conclusion in ("failure", "timed_out", "cancelled"):
        return "fail"
    return "unknown"


def file_exists(client: httpx.Client, org: str, repo: str, path: str) -> bool:
    r = client.get(f"/repos/{org}/{repo}/contents/{path}")
    return r.status_code == 200


def is_thin_caller(client: httpx.Client, org: str, repo: str, workflow: str) -> bool:
    """Check if a workflow file contains the org caller pattern."""
    r = client.get(f"/repos/{org}/{repo}/contents/.github/workflows/{workflow}")
    if r.status_code != 200:
        return False
    import base64

    content = base64.b64decode(r.json().get("content", "")).decode(
        "utf-8", errors="replace"
    )
    return CALLER_PATTERN in content


# ============================================================
# Per-repo analysis
# ============================================================


def analyse_repo(client: httpx.Client, repo: dict) -> RepoReport:
    name = repo["name"]
    report = RepoReport(name=name, archived=repo.get("archived", False))

    if report.archived:
        return report

    # Workflow statuses
    for wf in WORKFLOWS_TO_CHECK:
        status = get_latest_run(client, ORG, name, wf)
        thin = False
        if status != "missing":
            thin = is_thin_caller(client, ORG, name, wf)
        report.workflows.append(
            WorkflowStatus(name=wf, status=status, is_thin_caller=thin)
        )

    # File presence
    for path, label in FILES_TO_CHECK.items():
        report.files[label] = file_exists(client, ORG, name, path)

    # Derive issues
    actions_url = f"https://github.com/{ORG}/{name}/actions"
    for wf in report.workflows:
        if wf.status == "fail":
            report.issues.append(f"workflow failing: {wf.name}\n  → {actions_url}")
        if (
            name not in SKIP_THIN_CALLER
            and wf.status != "missing"
            and not wf.is_thin_caller
        ):
            report.issues.append(f"not a thin caller: {wf.name}")

    if report.files.get("mkdocs") and not report.files.get("zensical"):
        report.issues.append("not migrated to zensical")

    if name not in SKIP_MANIFEST and not report.files.get("manifest"):
        report.issues.append("SE_MANIFEST.toml missing")

    if not report.files.get("dependabot"):
        report.issues.append("dependabot.yml missing")

    return report


# ============================================================
# Output
# ============================================================

STATUS_SYMBOL = {
    "pass": "[green]✓[/green]",
    "fail": "[red]✗[/red]",
    "missing": "[dim]—[/dim]",
    "unknown": "[yellow]?[/yellow]",
}


def render(reports: list[RepoReport]) -> None:
    console = Console()

    table = Table(title="toy-gpt org health", show_lines=True)
    table.add_column("Repo", style="bold")
    table.add_column("ci", justify="center")
    table.add_column("deploy", justify="center")
    table.add_column("links", justify="center")
    table.add_column("thin?", justify="center")
    table.add_column("zen", justify="center")
    table.add_column("mani", justify="center")
    table.add_column("dbot", justify="center")
    table.add_column("Issues")

    for r in reports:
        if r.archived:
            table.add_row(f"[dim]{r.name} (archived)[/dim]", *["—"] * 8)
            continue

        wf_map = {w.name: w for w in r.workflows}

        def ws(name: str, wf_map=wf_map) -> str:
            w = wf_map.get(name)
            return STATUS_SYMBOL.get(w.status, "?") if w else "—"

        def thin_all(r=r) -> str:
            non_missing = [w for w in r.workflows if w.status != "missing"]
            if not non_missing:
                return "—"
            return (
                "[green]✓[/green]"
                if all(w.is_thin_caller for w in non_missing)
                else "[red]✗[/red]"
            )

        def f(label: str, r=r) -> str:
            return "[green]✓[/green]" if r.files.get(label) else "[red]✗[/red]"

        issues = "\n".join(r.issues) if r.issues else "[green]ok[/green]"

        table.add_row(
            r.name,
            ws("ci-shared.yml"),
            ws("deploy-docs-shared.yml"),
            ws("links.yml"),
            thin_all(),
            f("zensical"),
            f("manifest"),
            f("dependabot"),
            issues,
        )

    console.print(table)

    total = sum(1 for r in reports if not r.archived)
    clean = sum(1 for r in reports if not r.archived and not r.issues)
    console.print(f"\n[bold]{clean}/{total}[/bold] repos clean")


# ============================================================
# Main
# ============================================================


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN not set.", file=sys.stderr)
        sys.exit(1)

    with make_client(token) as client:
        print(f"Fetching repos for {ORG}...")
        repos = get_repos(client, ORG)
        repos.sort(key=lambda r: r["name"])
        print(f"Found {len(repos)} repos. Scanning...\n")

        reports = []
        for repo in repos:
            print(f"  {repo['name']}")
            reports.append(analyse_repo(client, repo))

    render(reports)


if __name__ == "__main__":
    main()
