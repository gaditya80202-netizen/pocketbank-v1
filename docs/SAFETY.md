# Safety and scope

PocketBank is a deliberately limited educational application. It simulates balances in a local SQLite file and does not move real money.

Never use real names, account numbers, credentials, payment cards, or other sensitive data with this repository. Do not expose it to the public internet. Do not deploy it as a banking product.

The `main` branch is the clean demonstration baseline. The `demo/security-hardcoded-secret` and `demo/quality-overdraft-check` branches intentionally introduce defects to exercise a code-review agent. Those branches are unsafe by design and must not be deployed. Switch back to `main` after demonstrating them.

The security showcase branch intentionally introduces a static credential and SQL injection risk in an isolated, local-only route. Use only the fictional seed data. Do not send destructive SQL payloads or test against a real database.
