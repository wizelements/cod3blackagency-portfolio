# Security Policy

## Scope

This repository documents Cod3Black Agency's portfolio and delivery practices. Security controls differ by product, maturity, architecture, and deployment, so this file does **not** claim that every repository has identical scanning, authentication, monitoring, or patching controls.

For an issue in a specific product, use that repository's security policy when one exists.

## Reporting a Vulnerability

Do not open a public issue containing exploit details, credentials, private data, or reproducible sensitive information.

Preferred reporting path:

1. Use the affected repository's private GitHub Security Advisory flow when enabled.
2. Otherwise email **contact@cod3blackagency.com** with `SECURITY` in the subject.
3. Include the affected repository/surface, impact, reproduction steps, and any suggested remediation.

Do not include real customer secrets or unnecessary personal data in a report.

## Handling Standard

Security reports should be triaged by severity and evidence. Remediation priority depends on exploitability, exposed data, affected users, and whether the issue reaches a production surface.

No fixed remediation deadline is promised here because severity and deployment context vary. Critical production exposure should receive priority over lower-risk development-only findings.

## Portfolio Security Principles

Current engineering expectations include:

- no committed production secrets;
- least-privilege credentials and server-side secret handling;
- input validation at trust boundaries;
- authentication/authorization where the product requires it;
- dependency and code scanning where configured;
- HTTPS for public production web deployments;
- webhook signature verification where applicable;
- explicit production versus prototype status;
- evidence-based security claims rather than blanket assertions.

The presence of this policy is not itself proof that every control above is implemented in every repository.
