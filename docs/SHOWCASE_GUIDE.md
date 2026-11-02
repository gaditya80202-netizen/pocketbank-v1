# PocketBank showcase runbook

This repository is a demonstration codebase for the AI Pull-Request Review Agent. It is a simulated banking API, not a real banking system. The demo branches include intentional defects; never deploy or merge those branches into `main`.

## 1. Demo prerequisites

Before opening pull requests, confirm that:

1. The PocketBank repository is pushed to GitHub and its default branch is `main`.
2. All five `demo/*` branches are pushed to the same GitHub repository.
3. The AI Review Agent's GitHub App is installed on `gaditya80202-netizen/pocketbank-review-demo` and has the repository permissions configured by the project.
4. The local AI Review Agent is running: Redis, FastAPI, ARQ worker, and Smee forwarding GitHub events to `http://127.0.0.1:8000/webhook/github`.
5. The worker can authenticate to GitHub as the GitHub App, retrieve the repository, and index the default branch. A successful webhook delivery alone is not proof that indexing succeeded; check the worker log and repository-index status.
6. The dashboard at `http://127.0.0.1:8000/dashboard` loads and accepts the configured HITL API token.

Keep the AI Review Agent's `.env`, GitHub App `.pem` private key, database credentials, and API tokens out of the PocketBank repository.

## 2. Branches and intended demonstrations

All four specialist agents run on every pull request. The branches below make a particular agent's responsibility easier to see; they do not select or disable individual agents. Actual findings depend on the model, prompt, retrieved context, diff, and reviewer configuration.

| Head branch | Suggested PR title | Intended review signal |
|---|---|---|
| `demo/security-hardcoded-secret` | Add admin account search endpoint | Security review of the deliberately hardcoded credential and unsafe SQL construction. |
| `demo/quality-overdraft-check` | Adjust transfer balance validation | Quality review of the weakened insufficient-funds guard: the database constraint prevents a negative balance, but the API can return an unhandled database error rather than a controlled 409 response. |
| `demo/tests-daily-limit-no-tests` | Add a daily outgoing transfer limit | Test review of the new daily limit and its missing boundary-case coverage. The branch also updates related descriptions so the test gap is the main signal. |
| `demo/docs-statement-endpoint` | Add account statement endpoint | Documentation review: the new public endpoint is not added to the API reference. |
| `demo/clean-activity-summary` | Add account activity summary | A low-noise comparison: implementation, tests, and API documentation are added together. |

## 3. Verify the local GitHub CLI and branches

Run these commands from the PocketBank repository folder:

```bash
cd ~/Documents/PocketBank_Demo_Repository

gh auth status
gh repo view gaditya80202-netizen/pocketbank-review-demo
git remote -v
git fetch origin --prune
git branch --list
git push origin --all
```

The active GitHub CLI account must have write access to `gaditya80202-netizen/pocketbank-review-demo`. The `origin` remote should point to that repository. The local branch list should include `main` and the five `demo/*` branches. `git push origin --all` ensures all local branches are published; it does not create pull requests.

## 4. Refresh showcase commit SHAs before every fresh demo run

**Run this section after pushing `main` and all five `demo/*` branches, but before creating the pull requests.** It is especially important when you delete and recreate the GitHub repository using the same owner/name, or when reusing a PocketBank copy that has already been reviewed by this AI Review Agent.

The AI Review Agent intentionally prevents duplicate work. Its review identity includes the GitHub App installation, repository name, PR number, and PR head commit SHA. The review history is stored in the external TimescaleDB database; deleting the GitHub repository does not delete those database records. If you recreate the same repository and reuse the same Git history, GitHub can reuse the same PR numbers and the branches can still point to the same commit SHAs. The reviewer may then return `already_processed` instead of running the agents again.

From the PocketBank repository root, run this **once before creating the five PRs**:

```bash
set -e

git fetch origin --prune

for branch in \
  demo/security-hardcoded-secret \
  demo/quality-overdraft-check \
  demo/tests-daily-limit-no-tests \
  demo/docs-statement-endpoint \
  demo/clean-activity-summary
do
  echo "Refreshing review SHA for $branch"
  git switch "$branch"
  git pull --ff-only origin "$branch"
  git commit --allow-empty -m "chore: refresh showcase SHA $(date -u +%Y%m%dT%H%M%SZ)"
  git push origin "$branch"
done

git switch main
```

**What the important command does:** `git commit --allow-empty` creates a real Git commit even though no source files changed. Git assigns that commit a new SHA. This changes the PR's head SHA while leaving the actual code diff—and therefore the planted security, quality, testing, or documentation scenario—unchanged. When the PR is opened, the AI Review Agent sees a new review identity and can run a fresh review instead of matching an old database record.

The loop applies that refresh to each of the five showcase branches, then returns your working copy to `main`. It does not delete old review history, reset the database, modify source code, or weaken the agent's duplicate-event protection. Do not delete database records or disable idempotency just to repeat a demonstration.

If you only need to rerun one existing PR, refresh only its branch using this pattern:

```bash
git switch demo/security-hardcoded-secret
git pull --ff-only origin demo/security-hardcoded-secret
git commit --allow-empty -m "chore: refresh security showcase SHA"
git push origin demo/security-hardcoded-secret
```

Replace the branch and commit message with the PR you are refreshing. If that PR is already open, the push creates a `synchronize` event; if the PR is not open yet, create it after the refresh so its initial `opened` event uses the new SHA.

If Git reports that your author identity is not configured, set it once for this repository before running the loop:

```bash
git config user.name "Your Name"
git config user.email "YOUR_GITHUB_EMAIL"
```

Use the email associated with your GitHub account (or its GitHub-provided noreply address). Do not put API keys or passwords in Git configuration.

## 5. Create the five pull requests with GitHub CLI

Use `gh pr create` for each PR. Every command explicitly sets `main` as the base and the corresponding `demo/*` branch as the head. The descriptions are intentionally neutral: they describe the change without revealing the findings the AI reviewer is meant to discover. Complete Section 4 first so each PR starts with a fresh head SHA.

**Important:** Create and review the PRs one at a time during the live demonstration. Each PR triggers all four agents and may incur model/embedding usage. Wait until the current review has completed and been inspected in the dashboard before creating the next one. Do not merge any of the demonstration PRs.

### PR 1 — Security scenario

```bash
gh pr create \
  --repo gaditya80202-netizen/pocketbank-review-demo \
  --base main \
  --head demo/security-hardcoded-secret \
  --title "Add admin account search endpoint" \
  --body "Adds an administrative endpoint for searching accounts by owner name, including the route and its access-check logic."
```

Expected demonstration focus: the security specialist should inspect the new admin endpoint and its data-access code. Do not point out the planted issues in the PR description.

### PR 2 — Code-quality scenario

```bash
gh pr create \
  --repo gaditya80202-netizen/pocketbank-review-demo \
  --base main \
  --head demo/quality-overdraft-check \
  --title "Adjust transfer balance validation" \
  --body "Updates the balance-validation behaviour in the transfer request flow."
```

Expected demonstration focus: insufficient-funds handling and the API's error behaviour.

### PR 3 — Test-coverage scenario

```bash
gh pr create \
  --repo gaditya80202-netizen/pocketbank-review-demo \
  --base main \
  --head demo/tests-daily-limit-no-tests \
  --title "Add a daily outgoing transfer limit" \
  --body "Introduces a daily outgoing-transfer limit and updates the related application descriptions."
```

Expected demonstration focus: whether the new limit has tests for below-limit, exact-limit, over-limit, and boundary conditions.

### PR 4 — Documentation scenario

```bash
gh pr create \
  --repo gaditya80202-netizen/pocketbank-review-demo \
  --base main \
  --head demo/docs-statement-endpoint \
  --title "Add account statement endpoint" \
  --body "Adds a read-only account statement endpoint and supporting tests."
```

Expected demonstration focus: the new public endpoint and whether the API reference explains it.

### PR 5 — Clean implementation scenario

```bash
gh pr create \
  --repo gaditya80202-netizen/pocketbank-review-demo \
  --base main \
  --head demo/clean-activity-summary \
  --title "Add account activity summary" \
  --body "Adds an account activity summary with service logic, a response model, tests, and API documentation."
```

Expected demonstration focus: a useful control case for judging false positives and review precision.

### Verify created PRs

```bash
gh pr list --repo gaditya80202-netizen/pocketbank-review-demo --state open
```

To open a particular PR in the browser, use its number from the list:

```bash
gh pr view PR_NUMBER --repo gaditya80202-netizen/pocketbank-review-demo --web
```

If a PR already exists for a branch, `gh pr create` will report that a pull request already exists. Use `gh pr view` or `gh pr list` to inspect it instead of creating a duplicate.

## 6. Recommended live-demo sequence

For each PR, use the same repeatable sequence:

1. Create the PR using the matching command above.
2. Confirm Smee shows the webhook delivery and FastAPI returns a successful response (normally HTTP 202).
3. Watch the ARQ worker. Confirm the review job starts and completes; investigate any GitHub, embedding, database, or LLM error rather than assuming the webhook response means the review succeeded.
4. Open the AI Review Agent dashboard and inspect the pending review, specialist statuses, findings, and token/cost telemetry.
5. Check that findings refer to relevant changed lines and include a concrete rationale. Treat the clean PR as a false-positive control.
6. Approve one review from the dashboard and verify that GitHub receives a **COMMENT** review. The dashboard's approval authorizes publication of the AI feedback; it is not GitHub's PR APPROVE event.
7. Do not merge the showcase PRs. Leave them open for a single session, or close them without merging after the demonstration.

## 7. Additional reliability demonstrations

### Stale-SHA protection

1. Open a fresh PR and let the AI reviewer finish reviewing its current head commit.
2. Push another commit to that PR branch before approving the old review.
3. Return to the dashboard and try to approve the review for the old commit.
4. The server should detect that the stored review SHA no longer matches GitHub's live PR head and prevent stale publication.

### Webhook duplicate/retry handling

Use GitHub's webhook delivery page to inspect deliveries. If deliberately redelivering an event, watch the webhook inbox and dispatcher logs to confirm how the application handles the repeated delivery. Do not assume every repeated event creates a new review; verify the persisted delivery/job state.

### Analytics and cost tracking

After several reviews have completed, open the dashboard analytics view. Explain that metrics depend on persisted review and agent-event data; unavailable usage or cost data should not be interpreted as zero.

## 8. Close and reset

To close a demonstration PR without merging it:

```bash
gh pr close PR_NUMBER --repo gaditya80202-netizen/pocketbank-review-demo
```

The scenario branches remain on GitHub and can be used to create another PR after the earlier PR is closed. Do not merge the intentionally defective security or quality branches into `main`.

For a completely fresh repeatable demo, create a new GitHub repository and push the clean repository history and all scenario branches there. Do not reset or force-push the public showcase repository during a presentation unless you explicitly intend to rewrite its history.

## 9. What success looks like

A strong demonstration is not simply an agent producing many findings. Check that findings are relevant, non-duplicated, tied to valid changed lines, and supported by a useful explanation. Check that the clean PR does not receive unjustified findings. Demonstrate that a human must approve publication, that publication is a GitHub **COMMENT** review, and that stale-SHA protection prevents publishing a review against an outdated PR commit.

PocketBank is a simulated demonstration application only. It has no real banking/payment integration and must not be used to handle real money, credentials, or customer data.
