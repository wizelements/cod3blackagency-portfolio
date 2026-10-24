# Cloud adoption decisions

**Existing workloads first.** Do not replace working Vercel applications or duplicate a live production database merely to add Azure/AWS branding.

| Capability | Default | Migration trigger |
| --- | --- | --- |
| Web storefront | Vercel | Measured availability or deployment constraint |
| Shared APIs and queues | Existing managed services first | Long-running jobs, queue semantics, or isolation needs |
| Database | One verified authoritative store per business domain | Documented integrity or availability issue |
| Storage/backup | Encrypted, isolated and tested | Recovery-objective failure |
| Mobile notifications | Existing Firebase integration | Delivery reliability requirement |
| Business operations | Evaluate Microsoft 365 Business Premium | Actual identity/device/customer collaboration benefit |
| Enterprise pilot | Azure first **as a non-production exercise** | Azure tenant, budget cap, named workload owner |
| Alternative pilot | AWS only if workload/customer needs it | Named business requirement |
| OPEE orchestration | Authenticated, bounded worker interface | Independent authority and recovery certification |

## Before provisioning any billable cloud resource

Identify account owner, customer/problem, monthly hard budget or alert and human escalation, region/data residency, expected usage, identity model, logging, backups, teardown path, IAM least privilege, and payment responsibility. Pricing/credits must be checked at deployment time. No production secrets in CI logs or repositories.

## Security boundary

Infrastructure as Code should run via reviewed pull requests and short-lived workload identities; no cloud root keys on agents, phones, shared hosts or repository secrets. Production account creation, billing and privileged changes require separately authorized credentials and approval.

## Pilot success criteria

Build one minimal service; provision through reviewed IaC, run basic tests, verify logs, verify rollback/teardown, confirm actual charges, record evidence. Stop the pilot if it cannot show a useful capability or business case.
