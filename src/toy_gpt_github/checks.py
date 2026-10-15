"""src/toy_gpt_github/checks.py - toy-gpt org health scanner.

WHY: Scan all repos in the toy-gpt org and report on workflow status
     and file presence.

USAGE:
    uv run --env-file .env python src/toy_gpt_github/checks.py
    uv run --env-file .env python -m toy_gpt_github.checks
    uv run --env-file .env python src/toy_gpt_github/checks.py --write-markdown org-health.md

REQUIRES:
    export GITHUB_TOKEN=<your-pat>   # needs repo + actions read scope
    pip install httpx rich           # or add to pyproject.toml dev deps
"""

from dataclasses import dataclass, field
import os
from pathlib import Path
import sys

import httpx
from rich.console import Console
from rich.table import Table

# ============================================================
# Config
# ============================================================

ORG = "toy-gpt"
BASE = "https://api.github.com"

# Workflow filenames to check (as they appear in .github/workflows/)
WORKFLOWS_TO_CHECK = ["ci-python-zensical.yml", "deploy-zensical.yml", "links.yml"]

# Files whose presence indicates repo health / migration state
FILES_TO_CHECK = {
    "zensical.toml": "zensical",
    ".github/dependabot.yml": "dependabot",
    "py.typed": "py.typed",
}

# Repositories without a Zensical docs site (zensical.toml does not apply).
NO_ZENSICAL_REPOS = {"toy-gpt-chat"}

# ============================================================
# Data
# ============================================================


@dataclass
class WorkflowStatus:
    """Represents the status of a single workflow in a repository."""

    name: str
    status: str  # "pass", "fail", "missing", "unknown"


@dataclass
class RepoReport:
    """Represents the health report of a single repository."""

    name: str
    archived: bool = False
    workflows: list[WorkflowStatus] = field(default_factory=list)
    files: dict[str, bool] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)


# ============================================================
# GitHub API helpers
# ============================================================


def make_client(token: str) -> httpx.Client:
    """Create an HTTPX client configured for the GitHub API."""
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
    """Retrieve all repositories for the given organization."""
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
    """Retrieve the latest run status for a given workflow in a repository.

    Returns 'pass', 'fail', 'missing', or 'unknown'.
    """
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
    """Check if a file exists in the repository."""
    r = client.get(f"/repos/{org}/{repo}/contents/{path}")
    return r.status_code == 200


# ============================================================
# Per-repo analysis
# ============================================================


def analyse_repo(client: httpx.Client, repo: dict) -> RepoReport:
    """Analyze a single repository and return its health report."""
    name = repo["name"]
    report = RepoReport(name=name, archived=repo.get("archived", False))

    if report.archived:
        return report

    # Workflow statuses
    for wf in WORKFLOWS_TO_CHECK:
        status = get_latest_run(client, ORG, name, wf)
        report.workflows.append(WorkflowStatus(name=wf, status=status))

    # File presence
    for path, label in FILES_TO_CHECK.items():
        report.files[label] = file_exists(client, ORG, name, path)

    # Derive issues
    actions_url = f"https://github.com/{ORG}/{name}/actions"
    for wf in report.workflows:
        if wf.status == "fail":
            report.issues.append(f"workflow failing: {wf.name}\n  -> {actions_url}")

    if not report.files.get("dependabot"):
        report.issues.append("dependabot.yml missing")

    return report


# ============================================================
# Output
# ============================================================

STATUS_SYMBOL = {
    "pass": "[green]yes[/green]",
    "fail": "[red]NO[/red]",
    "missing": "[dim]-[/dim]",
    "unknown": "[yellow]?[/yellow]",
}


def md_cell(text: str) -> str:
    """Return the given text formatted for a Markdown table cell."""
    text = text.replace("\n", "<br>")
    text = text.replace("|", "\\|")
    return text


def render(reports: list[RepoReport]) -> None:
    """Render the org health report as a table in the console."""
    console = Console()

    table = Table(title="toy-gpt org health", show_lines=True)
    table.add_column("Repo", style="bold")
    table.add_column("ci", justify="center")
    table.add_column("deploy", justify="center")
    table.add_column("links", justify="center")
    table.add_column("zen", justify="center")
    table.add_column("dbot", justify="center")
    table.add_column("Issues")

    for r in reports:
        if r.archived:
            table.add_row(f"[dim]{r.name} (archived)[/dim]", *["-"] * 6)
            continue

        wf_map = {w.name: w for w in r.workflows}

        def ws(name: str, wf_map=wf_map) -> str:
            w = wf_map.get(name)
            return STATUS_SYMBOL.get(w.status, "?") if w else "-"

        def f(label: str, r=r) -> str:
            return "[green]yes[/green]" if r.files.get(label) else "[red]NO[/red]"

        issues = "\n".join(r.issues) if r.issues else "[green]ok[/green]"

        table.add_row(
            r.name,
            ws("ci-python-zensical.yml"),
            ws("deploy-zensical.yml"),
            ws("links.yml"),
            "[dim]-[/dim]" if r.name in NO_ZENSICAL_REPOS else f("zensical"),
            f("dependabot"),
            issues,
        )

    console.print(table)

    total = sum(1 for r in reports if not r.archived)
    clean = sum(1 for r in reports if not r.archived and not r.issues)
    console.print(f"\n[bold]{clean}/{total}[/bold] repos clean")


def render_markdown(reports: list[RepoReport]) -> str:
    """Render the org health report as a Markdown string suitable for writing to a file."""
    headers = [
        "Repo",
        "ci",
        "deploy",
        "links",
        "zen",
        "dbot",
        "Issues",
    ]

    def sym(status: str) -> str:
        return {
            "pass": "yes",
            "fail": "NO",
            "missing": "-",
            "unknown": "?",
        }.get(status, "?")

    lines: list[str] = []
    lines.append("# toy-gpt org health")
    lines.append("")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for r in reports:
        if r.archived:
            lines.append(
                f"| {md_cell(r.name + ' (archived)')} | - | - | - | - | - | - |"
            )
            continue

        wf_map = {w.name: w for w in r.workflows}

        def ws(name: str, wf_map=wf_map) -> str:
            w = wf_map.get(name)
            return sym(w.status) if w else "-"

        def f(label: str, r=r) -> str:
            return "yes" if r.files.get(label) else "NO"

        issues = "; ".join(r.issues) if r.issues else "ok"

        row = [
            md_cell(r.name),
            md_cell(ws("ci-python-zensical.yml")),
            md_cell(ws("deploy-zensical.yml")),
            md_cell(ws("links.yml")),
            md_cell("-" if r.name in NO_ZENSICAL_REPOS else f("zensical")),
            md_cell(f("dependabot")),
            md_cell(issues),
        ]
        lines.append("| " + " | ".join(row) + " |")

    total = sum(1 for r in reports if not r.archived)
    clean = sum(1 for r in reports if not r.archived and not r.issues)

    lines.append("")
    lines.append(f"**{clean}/{total}** repos clean")
    lines.append("")

    return "\n".join(lines)


def write_markdown_report(reports: list[RepoReport], output_path: str) -> None:
    """Write the org health report as a Markdown file."""
    path = Path(output_path)
    path.write_text(render_markdown(reports), encoding="utf-8")


# ============================================================
# Main
# ============================================================


def main() -> None:
    """Main entry point for the script."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN not set.", file=sys.stderr)
        sys.exit(1)

    # Path to write the Markdown report to, if specified
    markdown_output_path = None
    if "--write-markdown" in sys.argv:
        idx = sys.argv.index("--write-markdown")
        if idx + 1 >= len(sys.argv):
            print("ERROR: --write-markdown requires a file path.", file=sys.stderr)
            sys.exit(1)
        markdown_output_path = sys.argv[idx + 1]

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

    if markdown_output_path:
        write_markdown_report(reports, markdown_output_path)
        print(f"\nWrote markdown report to {markdown_output_path}")


if __name__ == "__main__":
    main()
