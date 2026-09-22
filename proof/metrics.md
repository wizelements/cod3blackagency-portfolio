# Proof: Metrics and Validation

This file defines what counts as portfolio evidence.

## Evidence Policy

A metric is a **result** only when it was actually measured against a named build/deployment, with a date and reproducible method. Desired values must be labeled **targets**.

The portfolio must not convert:

- README claims into measured results;
- CI configuration into proof that a current run passed;
- a deployment URL into proof that the product works end-to-end;
- an upstream project's capabilities into Cod3Black-authored capability;
- historical measurements into current measurements.

## Currently Verified Infrastructure Facts

| System | Verified fact | Evidence source |
| --- | --- | --- |
| Cod3Black Agency / `c3bai` | Inspected production deployment reported **READY** | Connected Vercel account |
| Taste of Gratitude / `Gratog` | Inspected production deployment reported **READY** | Connected Vercel account |
| Taste of Gratitude / `Gratog` | `tasteofgratitude.shop` is a verified project domain | Connected Vercel account |
| GitHub portfolio | 121 owned repositories: 57 active, 64 archived after governance audit | Authenticated GitHub account |

These facts do **not** imply a Lighthouse score, uptime SLA, test coverage percentage, or business outcome unless those are separately measured.

## Required Format for Future Performance Evidence

Record:

- project;
- commit SHA;
- deployment ID/URL;
- environment;
- date/time;
- tool and version;
- exact command/config;
- result;
- threshold/target;
- pass/fail;
- evidence artifact or link.

Example:

```text
Project: example
Commit: abc123
Environment: production
Measurement: Lighthouse mobile
Tool/version: Lighthouse 13.x
Date: YYYY-MM-DD
Performance: 91
Accessibility: 98
Target: >= 90 / >= 95
Result: PASS
```

## Test and CI Evidence

Do not write `Pass` because a workflow file exists. Record the actual workflow run, local command output, or certification artifact.

Useful gates include, as appropriate:

```bash
npm run lint
npm run typecheck
npm test
npm run build
npm run test:e2e
git diff --check
```

Different repositories may use different stacks and therefore different verification commands.

## Security Evidence

Security claims require specific evidence such as:

- secret-scanning configuration/results;
- CodeQL or equivalent run;
- dependency-audit output;
- authorization tests;
- webhook-signature tests;
- threat model or security review;
- production configuration inspection.

There is no portfolio-wide claim that every repository has every security control.

## Business Evidence

The strongest proof is not technical vanity metrics. For commercial work, track outcomes such as:

- qualified leads captured;
- conversion rate;
- checkout completion;
- revenue processed;
- manual hours eliminated;
- response time reduced;
- operational errors prevented;
- repeat-customer or retention lift;
- verified time saved.

Where business metrics are unavailable, say so rather than substituting technical activity as economic proof.
