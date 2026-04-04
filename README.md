# Toy GPT Organization (.github repo)

[![Version](https://img.shields.io/badge/version-v0.2.2-blue)](https://github.com/toy-gpt/.github/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
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

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/username/.github

cd .github
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
git add -A
uvx pre-commit run --all-files

uv run --env-file .env python src/toy-gpt-github/checks.py
uv run --env-file .env python src/toy-gpt-github/checks.py --format=markdown > org-health.md

uv run ruff format .
uv run ruff check . --fix
uv run zensical build

git add -A
git commit -m "update"
git push -u origin main
```

</details>

## toy-gpt org health

| Repo                             | ci  | deploy | links | thin? | zen | mani | dbot | Issues |
| -------------------------------- | --- | ------ | ----- | ----- | --- | ---- | ---- | ------ |
| .github                          | -   | -      | yes   | no    | yes | no   | yes  | ok     |
| toy-gpt-chat                     | -   | -      | yes   | yes   | no  | yes  | yes  | ok     |
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

**17/17 repos clean**

## Resources

- [Pro-Analytics-02](https://denisecase.github.io/pro-analytics-02/) - guide to professional Python

## Annotations

[ANNOTATIONS.md](./ANNOTATIONS.md)

<!--
WHY: Keep decision rationale close to code and configuration.
-->

## License

[MIT](./LICENSE)

<!--
WHY: Provide terms of reuse and limits of liability.
-->
