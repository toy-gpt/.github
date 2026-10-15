# Toy GPT Organization (.github repo)

[![Version](https://img.shields.io/badge/version-v0.2.2-blue)](https://github.com/toy-gpt/.github/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/license/MIT)
[![CI](https://github.com/toy-gpt/.github/actions/workflows/ci-org.yml/badge.svg?branch=main)](https://github.com/toy-gpt/.github/actions/workflows/ci-org.yml)
[![Check Links](https://github.com/toy-gpt/.github/actions/workflows/links.yml/badge.svg)](https://github.com/toy-gpt/.github/actions/workflows/links.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://github.com/toy-gpt/.github/security)

> GitHub profile repo for the toy-gpt organization on GitHub.

## Organization Checks

You need a GitHub Personal Access Token (PAT)
with read access to the org.
And it must be set as an environment variable before running the script.

### Step 1. Create the token

Go to https://github.com/settings/tokens?type=beta (fine-grained tokens, recommended)

- Resource owner: toy-gpt (the org)
- Repository access: All repositories
- Permissions needed:
  - Actions = Read-only
  - Contents = Read-only
  - Metadata = Read-only (auto-selected)

### Step 2. Generate and Copy the token

Copy to .env (not committed to GitHub).
You only see it once.

## Developer

### Clone and Open in VS Code

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/username/.github

cd .github
code .
```

### Initialize and Update the Python Environment

With the project open in VS Code, open a VS Code terminal.
Paste each command and hit Enter or Return after to run it.

```shell
uvx pup-clean --delete
uv self update
uv python pin 3.14
uv python install
uv lock --upgrade
uv sync
uv audit
```

### Set Up and Run Git Hooks

Set up and run the git hooks to perform
basic checks automatically before
any changes get pushed to GitHub.

In the VS Code terminal,
paste each command and hit Enter or Return after to run it.

```shell
uv run prek install --force
uv run prek update --freeze --cooldown-days 7

git add -A
uv run prek run --all-files
# repeat if changes were made
uv run prek run --all-files
```

### Run Common Chores

Run linters, formatters, type checks, tests, and
build the documentation.

```shell
uv run ruff check . --fix
uv run ruff format .

uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

### Git add-commit-push to GitHub

After making useful changes, save your work to GitHub.

```shell
git add -A
git commit -m "update"
# rerun if changes were made
git add -A
git commit -m "update"

git push -u origin main
```

## toy-gpt org health

| Repo                             | ci  | deploy | links | thin? | zen | mani | dbot | Issues |
| -------------------------------- | --- | ------ | ----- | ----- | --- | ---- | ---- | ------ |
| .github                          | -   | -      | yes   | -     | yes | NO   | yes  | ok     |
| toy-gpt-chat                     | -   | -      | yes   | yes   | NO  | yes  | yes  | ok     |
| train-100-unigram                | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-100-unigram-animals        | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-200-bigram                 | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-200-bigram-animals         | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-201-bigram-llm-glossary    | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-300-context-2              | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-300-context-2-animals      | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-301-context-2-llm-glossary | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-302-context-2-repo-tour    | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-400-context-3              | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-400-context-3-animals      | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-401-context-3-llm-glossary | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-500-embeddings             | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-600-attention              | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |
| train-600-attention-3            | yes | yes    | yes   | yes   | yes | yes  | yes  | ok     |

**17/17 repos** clean

## Resources

- [Pro-Analytics-02](https://denisecase.github.io/pro-analytics-02/) - guide to professional Python

## Annotations

[ANNOTATIONS](.annotations/annotations.md)

<!--
WHY: Keep decision rationale close to code and configuration.
-->

## License

[MIT](./LICENSE)

<!--
WHY: Provide terms of reuse and limits of liability.
-->
