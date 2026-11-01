# Showcase guide for the AI Pull-Request Review Agent

This repository is structured to produce focused pull requests against the clean `main` branch. Each branch is independent: create one PR, review it, close or merge it as appropriate, and then move to the next scenario. For a repeatable presentation, close each demo PR without merging and create the next PR against `main`.

## Before the demo

1. Push this repository to a new GitHub repository.
2. Install/configure your GitHub App for this demo repository, including webhook delivery to your running local Smee/FastAPI setup.
3. Make sure Redis/ARQ, TimescaleDB, the API, and the worker for your AI review agent are running.
4. Confirm that a push to the demo repository's default branch triggers indexing.
5. Open the repository's `main` branch and verify the clean codebase before starting.

This banking demo app is separate from the AI review agent. Do not copy the review agent's `.env`, private key, database credentials, or tokens into this repository.

## Branches and what each should demonstrate

| Branch | Suggested PR title | Intended review signal |
|---|---|---|
| `demo/security-hardcoded-secret` | `Add admin account search` | Security specialist should identify the hardcoded credential and unsafe SQL query. |
| `demo/quality-overdraft-check` | `Adjust transfer balance validation` | Quality specialist should identify the weakened insufficient-funds guard. |
| `demo/tests-daily-limit-no-tests` | `Add a daily outgoing transfer limit` | Test specialist should identify missing coverage for the newly added limit and its boundary cases. |
| `demo/docs-statement-endpoint` | `Add account statement endpoint` | Documentation specialist should identify that the public endpoint is absent from the API reference. |
| `demo/clean-activity-summary` | `Add account activity summary` | Demonstrate a feature with implementation, tests, and documentation changed together. |

All four agents still run on every PR. These branches are designed to make one specialist's responsibility especially visible; they do not disable the other agents. The actual findings depend on the model, prompt, retrieved context, diff size, and reviewer configuration.

## Push the branches to GitHub

After extracting the source ZIP or cloning the Git bundle, create an empty GitHub repository. Then run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
git push origin --all
```

Replace the URL with your repository URL. The bundle contains all local branches; `git push origin --all` publishes them.

## Create the PRs

Create each PR with `main` as the base and the named `demo/*` branch as the compare branch. You can use GitHub's **Compare & pull request** prompt or create PRs from the Pull requests page. Do not merge the intentionally defective branches into `main`.

If you have GitHub CLI (`gh`) installed, an example is:

```bash
gh pr create --base main --head demo/security-hardcoded-secret --title "Add admin account search" --body "Demonstration PR for the AI security review specialist."
```

Repeat with the other branch names and titles in the table.

## Recommended live-demo sequence

1. Start with the clean `main` branch and explain the app's account and transfer flow.
2. Open the security PR. Show the changed lines, then the AI's finding and its rationale.
3. Open the quality PR. Explain why allowing an overdraft is a business-logic defect.
4. Open the daily-limit PR. Show that the implementation exists but the new policy has no tests for below-limit, exact-limit, and over-limit cases.
5. Open the statement endpoint PR. Show the code change and the stale API reference.
6. Open the clean feature PR. Show the implementation, tests, and documentation arriving together.
7. In the AI review dashboard, show specialist status, findings, token/cost telemetry, and review history.
8. Approve one review from the dashboard and show that the agent publishes a GitHub **COMMENT** review. It does not submit GitHub's APPROVE event, merge the PR, or edit source code.
9. For stale-SHA protection, open a separate PR, let the agent review it, push another commit, and then attempt to approve the old review. The live-head check should prevent publishing a stale review.

## Reset between demonstrations

The PR branches are immutable examples. If you close a PR without merging, you can create another PR from the same branch only after closing the previous one. To demonstrate again from a fresh repository, use the Git bundle to create a clean clone and push its branches to a new GitHub repository.

## What success looks like

Do not judge the demo solely by whether an agent emits a finding. Check that findings point to valid changed lines, are not duplicated, contain a concrete rationale, and are appropriate to the specialist. The clean PR is especially useful for checking false positives. The reviewer's validation and human approval flow are part of the demonstration, not optional decoration.
