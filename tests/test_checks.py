"""tests/test_checks.py

REQ: Verify the toy-gpt org health scanner builds correct reports and tables.
WHY: People read these tables, so a broken row or column count must be caught.

OBS: No test calls GitHub. httpx.MockTransport answers every request from a
     dictionary of canned responses, so these tests run offline without a token.
"""

from pathlib import Path

import httpx
import pytest

from toy_gpt_github.checks import (
    NO_ZENSICAL_REPOS,
    ORG,
    WORKFLOWS_TO_CHECK,
    RepoReport,
    WorkflowStatus,
    analyse_repo,
    file_exists,
    get_latest_run,
    md_cell,
    render,
    render_markdown,
    write_markdown_report,
)

# Canned GitHub answers: (HTTP status code, JSON body).
RUN_SUCCESS = (200, {"workflow_runs": [{"conclusion": "success"}]})
RUN_FAILURE = (200, {"workflow_runs": [{"conclusion": "failure"}]})
RUN_IN_PROGRESS = (200, {"workflow_runs": [{"conclusion": None}]})
RUN_NONE = (200, {"workflow_runs": []})
FILE_FOUND = (200, {})


def make_client(responses: dict[str, tuple[int, dict]]) -> httpx.Client:
    """Return a real httpx client whose requests are answered from responses.

    Each key is a request path. Any path that is not listed answers 404.
    """

    def answer(request: httpx.Request) -> httpx.Response:
        status_code, body = responses.get(request.url.path, (404, {}))
        return httpx.Response(status_code, json=body)

    return httpx.Client(
        base_url="https://api.github.com",
        transport=httpx.MockTransport(answer),
    )


# === Configuration ===


def test_org_is_toy_gpt() -> None:
    """Test that the scanner looks at the toy-gpt organization."""
    assert ORG == "toy-gpt"


def test_workflows_to_check_are_the_pup_up_workflows() -> None:
    """Test that the scanner checks the three pup-up workflow files."""
    assert WORKFLOWS_TO_CHECK == [
        "ci-python-zensical.yml",
        "deploy-zensical.yml",
        "links.yml",
    ]


def test_chat_is_the_only_repo_without_zensical() -> None:
    """Test that only the chat app is exempt from the Zensical check."""
    assert NO_ZENSICAL_REPOS == {"toy-gpt-chat"}


# === Markdown cell formatting ===


def test_md_cell_replaces_newlines() -> None:
    """Test that a newline becomes an HTML line break."""
    assert md_cell("first\nsecond") == "first<br>second"


def test_md_cell_escapes_pipes() -> None:
    """Test that a pipe is escaped so it cannot split a table cell."""
    assert md_cell("a|b") == "a\\|b"


# === Latest workflow run ===


def test_latest_run_success_is_pass() -> None:
    """Test that a successful run is reported as pass."""
    client = make_client(
        {"/repos/toy-gpt/demo/actions/workflows/links.yml/runs": RUN_SUCCESS}
    )
    assert get_latest_run(client, ORG, "demo", "links.yml") == "pass"


def test_latest_run_failure_is_fail() -> None:
    """Test that a failed run is reported as fail."""
    client = make_client(
        {"/repos/toy-gpt/demo/actions/workflows/links.yml/runs": RUN_FAILURE}
    )
    assert get_latest_run(client, ORG, "demo", "links.yml") == "fail"


def test_latest_run_with_no_runs_is_missing() -> None:
    """Test that a workflow that has never run is reported as missing."""
    client = make_client(
        {"/repos/toy-gpt/demo/actions/workflows/links.yml/runs": RUN_NONE}
    )
    assert get_latest_run(client, ORG, "demo", "links.yml") == "missing"


def test_latest_run_for_unknown_workflow_is_missing() -> None:
    """Test that a workflow GitHub does not know (404) is reported as missing."""
    client = make_client({})
    assert get_latest_run(client, ORG, "demo", "links.yml") == "missing"


def test_latest_run_in_progress_is_unknown() -> None:
    """Test that a run with no conclusion yet is reported as unknown."""
    client = make_client(
        {"/repos/toy-gpt/demo/actions/workflows/links.yml/runs": RUN_IN_PROGRESS}
    )
    assert get_latest_run(client, ORG, "demo", "links.yml") == "unknown"


def test_latest_run_server_error_is_unknown() -> None:
    """Test that a GitHub server error is reported as unknown."""
    client = make_client(
        {"/repos/toy-gpt/demo/actions/workflows/links.yml/runs": (500, {})}
    )
    assert get_latest_run(client, ORG, "demo", "links.yml") == "unknown"


# === File presence ===


def test_file_exists_is_true_when_github_finds_it() -> None:
    """Test that a file GitHub returns (200) exists."""
    client = make_client({"/repos/toy-gpt/demo/contents/zensical.toml": FILE_FOUND})
    assert file_exists(client, ORG, "demo", "zensical.toml") is True


def test_file_exists_is_false_when_github_does_not() -> None:
    """Test that a file GitHub does not find (404) does not exist."""
    client = make_client({})
    assert file_exists(client, ORG, "demo", "zensical.toml") is False


# === One repository ===


def test_archived_repo_is_skipped() -> None:
    """Test that an archived repository is not scanned."""
    client = make_client({})
    report = analyse_repo(client, {"name": "old-repo", "archived": True})
    assert report.archived is True
    assert report.workflows == []
    assert report.issues == []


def test_healthy_repo_has_no_issues() -> None:
    """Test that a repo with passing workflows and all files has no issues."""
    client = make_client(
        {
            "/repos/toy-gpt/demo/actions/workflows/ci-python-zensical.yml/runs": RUN_SUCCESS,
            "/repos/toy-gpt/demo/actions/workflows/deploy-zensical.yml/runs": RUN_SUCCESS,
            "/repos/toy-gpt/demo/actions/workflows/links.yml/runs": RUN_SUCCESS,
            "/repos/toy-gpt/demo/contents/zensical.toml": FILE_FOUND,
            "/repos/toy-gpt/demo/contents/.github/dependabot.yml": FILE_FOUND,
            "/repos/toy-gpt/demo/contents/py.typed": FILE_FOUND,
        }
    )
    report = analyse_repo(client, {"name": "demo"})
    assert report.issues == []
    assert report.files == {"zensical": True, "dependabot": True, "py.typed": True}
    assert [w.status for w in report.workflows] == ["pass", "pass", "pass"]


def test_failing_workflow_is_reported_with_the_actions_link() -> None:
    """Test that a failing workflow adds one issue that links to the Actions tab."""
    client = make_client(
        {
            "/repos/toy-gpt/demo/actions/workflows/ci-python-zensical.yml/runs": RUN_FAILURE,
            "/repos/toy-gpt/demo/contents/.github/dependabot.yml": FILE_FOUND,
        }
    )
    report = analyse_repo(client, {"name": "demo"})
    assert report.issues == [
        "workflow failing: ci-python-zensical.yml\n"
        + "  -> https://github.com/toy-gpt/demo/actions"
    ]


def test_missing_dependabot_file_is_reported() -> None:
    """Test that a repo without dependabot.yml gets an issue."""
    client = make_client({})
    report = analyse_repo(client, {"name": "demo"})
    assert report.issues == ["dependabot.yml missing"]


# === Markdown report ===


def test_markdown_header_and_separator_rows() -> None:
    """Test the header and separator rows of the Markdown table."""
    lines = render_markdown([]).splitlines()
    assert lines[0] == "# toy-gpt org health"
    assert lines[2] == "| Repo | ci | deploy | links | zen | dbot | Issues |"
    assert lines[3] == "| --- | --- | --- | --- | --- | --- | --- |"


def test_markdown_row_for_a_clean_repo() -> None:
    """Test the row for a repo whose workflows pass and whose files exist."""
    report = RepoReport(
        name="train-500-embeddings",
        workflows=[
            WorkflowStatus(name="ci-python-zensical.yml", status="pass"),
            WorkflowStatus(name="deploy-zensical.yml", status="pass"),
            WorkflowStatus(name="links.yml", status="pass"),
        ],
        files={"zensical": True, "dependabot": True},
    )
    assert "| train-500-embeddings | yes | yes | yes | yes | yes | ok |" in (
        render_markdown([report])
    )


def test_markdown_row_for_a_repo_with_a_missing_file() -> None:
    """Test that a missing file shows NO and its issue text."""
    report = RepoReport(
        name="demo",
        files={"zensical": True, "dependabot": False},
        issues=["dependabot.yml missing"],
    )
    assert "| demo | - | - | - | yes | NO | dependabot.yml missing |" in (
        render_markdown([report])
    )


def test_markdown_row_for_chat_shows_a_dash_for_zensical() -> None:
    """Test that the chat app shows - in the zen column, not NO."""
    report = RepoReport(
        name="toy-gpt-chat",
        workflows=[WorkflowStatus(name="links.yml", status="pass")],
        files={"zensical": False, "dependabot": True},
    )
    assert "| toy-gpt-chat | - | - | yes | - | yes | ok |" in render_markdown([report])


def test_markdown_row_for_an_archived_repo() -> None:
    """Test that an archived repo gets a row with the same number of cells."""
    report = RepoReport(name="old-repo", archived=True)
    assert "| old-repo (archived) | - | - | - | - | - | - |" in (
        render_markdown([report])
    )


def test_markdown_clean_count_ignores_archived_repos() -> None:
    """Test that the clean count includes only repos that are not archived."""
    reports = [
        RepoReport(name="clean-repo"),
        RepoReport(name="broken-repo", issues=["dependabot.yml missing"]),
        RepoReport(name="old-repo", archived=True),
    ]
    assert "**1/2** repos clean" in render_markdown(reports)


def test_every_markdown_table_line_has_seven_cells() -> None:
    """Test that the header, separator, and every row have the same cell count.

    GitHub draws a table only when these counts match.
    """
    reports = [
        RepoReport(
            name="train-500-embeddings",
            files={"zensical": True, "dependabot": True},
        ),
        RepoReport(name="toy-gpt-chat", files={"dependabot": True}),
        RepoReport(name="old-repo", archived=True),
        RepoReport(
            name="broken",
            files={"zensical": False, "dependabot": False},
            issues=[
                "workflow failing: links.yml\n  -> https://github.com/toy-gpt/broken/actions",
                "dependabot.yml missing",
            ],
        ),
    ]
    text = render_markdown(reports)
    table_lines = [line for line in text.splitlines() if line.startswith("|")]

    assert len(table_lines) == 6  # header, separator, and four repos
    for line in table_lines:
        assert len(line.strip("|").split("|")) == 7


def test_write_markdown_report_writes_the_file(tmp_path: Path) -> None:
    """Test that the Markdown report is written to the requested file."""
    output_path = tmp_path / "org-health.md"
    report = RepoReport(name="demo", files={"zensical": True, "dependabot": True})

    write_markdown_report([report], str(output_path))

    text = output_path.read_text(encoding="utf-8")
    assert text.startswith("# toy-gpt org health")
    assert "| demo |" in text


# === Console report ===


def test_render_prints_the_table_and_the_clean_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that the console report shows the repo and the clean count."""
    report = RepoReport(name="demo", files={"zensical": True, "dependabot": True})

    render([report])

    output = capsys.readouterr().out
    assert "toy-gpt org health" in output
    assert "demo" in output
    assert "1/1" in output
    assert "repos clean" in output
