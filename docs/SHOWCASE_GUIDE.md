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
| `demo/quality-overdraft-check` | `Adjust transfer balance validation` | Quality specialist should identify the weakened insufficient-funds guard; the database constraint prevents a negative balance but the API raises an unhandled database error instead of returning 409. |
| `demo/tests-daily-limit-no-tests` | `Add a daily outgoing transfer limit` | Test specialist should identify missing coverage for the newly added limit and its boundary cases. |
| `demo/docs-statement-endpoint` | `Add account statement endpoint` | Documentation specialist should identify that the public endpoint is absent from the API reference. |
| `demo/clean-activity-summary` | `Add account activity summary` | Demonstrate a feature with implementation, tests, and documentation changed together. |

All four agents still run on every PR. These branches are designed to make one specialist's responsibility especially visible; they do not disable the other agents. The actual findings depend on the model, prompt, retrieved context, diff size, and reviewer configuration.

## Push the branches to GitHub

Create an empty GitHub repository first. Do not initialize it with a README, license, or `.gitignore`; this project already has those files.

**Option A — use the full repository ZIP (easiest):** this archive includes the `.git` directory and all six local branches. Extract it, open a terminal inside the extracted `PocketBank_Demo_Repository` folder, and run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
git push origin --all
```

Replace the URL with your repository URL. The second command pushes the five `demo/*` branches as well as any other local branches.

**Option B — use the Git bundle:** clone the bundle, change its `origin` URL to your new GitHub repository, create local branches from the bundle's remote-tracking refs, and push them:

```bash
git clone /path/to/PocketBank_Demo_Git_Bundle.bundle pocketbank-demo
cd pocketbank-demo
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

git branch demo/security-hardcoded-secret origin/demo/security-hardcoded-secret
git branch demo/quality-overdraft-check origin/demo/quality-overdraft-check
git branch demo/tests-daily-limit-no-tests origin/demo/tests-daily-limit-no-tests
git branch demo/docs-statement-endpoint origin/demo/docs-statement-endpoint
git branch demo/clean-activity-summary origin/demo/clean-activity-summary

git push -u origin main
git push origin --all
```

Replace `/path/to/` and the GitHub URL with your actual paths. The **source-only ZIP** contains the clean `main` source code but no Git history or prebuilt demo branches; use Option A or B when you want the showcase PR branches.

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
3. Open the quality PR. Explain why the service must reject insufficient funds before the database update; the database constraint masks the defect but causes a 500-style error instead of a controlled 409 response.
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
