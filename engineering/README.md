# Cod3Black Engineering Foundation

A reusable, dependency-free Python release-evidence preflight for client applications, with a standard project contract and CI checks. **Not an independent certification authority, cloud account, deployment, or payment-system proof.**

## Verified locally

```sh
python3 -m unittest discover -s engineering/tests -v
python3 engineering/release_gate.py --manifest engineering/examples/example-project.json --evidence engineering/examples/example-evidence.json
```

The example **must fail closed** (exit code 2): it is a fixture, not real evidence. The positive unit tests demonstrate the validation logic using synthetic evidence but DO NOT certify a live provider.

## Adoption instructions

1. Record a real project's problem, owner, revenue metric, sensitive-data classification, critical user journeys, and runbook in an independent manifest.
2. Identify its test and recovery gates, adding domain-specific gates like payment, inventory, load, data migration, regulated data and authorization.
3. Configure GitHub CI for reproducible build, test, security, typecheck, E2E and rollback exercises.
4. Supply run-linked evidence from the actual target revision and environment, with `fixture: false`. Do not fabricate passing gates.
5. Run `release_gate.py` with the manifest and collected evidence. Preflight passing means the *record* meets minimum structural and freshness requirements, not that it has been independently authenticated.
6. Independent engineering/production authority verifies each artifact and authorizes deployment through its separate protected process.
7. After release, verify real customer paths, record results, and retain rollback capability.

## Security properties

- **Fail closed** on missing, failed, duplicated, stale or future-dated required evidence.
- Base gates must cover build, unit, integration, security, end-to-end, rollback and observability.
- Produces a canonical SHA-256 fingerprint of supplied evidence.
- Never creates a certificate, signs anything, changes production systems, handles passwords, or deploys.
- Authenticity of artifact links, governance authority, and provider credentials MUST be checked separately.
- No secret values, operational account IDs or personally identifying information should be committed.

## Role of surrounding systems

GitHub is the change/review/CI control plane. Vercel remains a web deployment target. Azure or AWS can be added when measured workload requirements justify. Microsoft 365 is a business/identity option, not a requirement for this package. OPEE may propose and execute authorized actions, but may not sign its own protected production completion.

For cloud onboarding and commercial milestones, see [ROADMAP.md](ROADMAP.md) and [CLOUD_DECISIONS.md](CLOUD_DECISIONS.md).
