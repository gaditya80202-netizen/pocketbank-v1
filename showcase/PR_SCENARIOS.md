# PR scenario index

The actual scenarios live on Git branches so they can be pushed and opened as real pull requests. This file is a quick index.

- `demo/security-hardcoded-secret`: intentionally unsafe admin lookup for security-review demonstration.
- `demo/quality-overdraft-check`: intentionally weakened balance guard for quality-review demonstration.
- `demo/tests-daily-limit-no-tests`: daily outgoing-transfer limit implemented without matching tests; documentation is updated to isolate the test-coverage gap.
- `demo/docs-statement-endpoint`: new statement endpoint without an API reference update.
- `demo/clean-activity-summary`: an activity summary feature with implementation, tests, and API documentation.

See `docs/SHOWCASE_GUIDE.md` for the end-to-end workflow. Do not deploy the intentionally defective branches.
