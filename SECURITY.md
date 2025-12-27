# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | Yes                |

## Reporting a Vulnerability

Cod3BlackAgency takes security seriously. If you discover a security vulnerability in any of our repositories, please report it responsibly.

### How to Report

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Email security concerns to: [security@cod3blackagency.com]
3. Include:
   - Repository name
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 7 days
- **Resolution Target**: Within 30 days (severity dependent)

### Scope

This policy applies to all Cod3BlackAgency repositories:
- sd-studio-web
- family-powerhouse
- Ownly
- solovibe
- cba-ai-platform
- freelance-dashboard

### Recognition

We appreciate responsible disclosure and will acknowledge security researchers who report valid vulnerabilities (with permission).

## Security Practices

All Cod3BlackAgency projects implement:

- Dependency scanning via Dependabot
- Code scanning via GitHub CodeQL
- Environment variable management (no secrets in code)
- HTTPS-only deployments
- Input validation and sanitization
- Authentication best practices (where applicable)

## Dependencies

We regularly update dependencies to patch known vulnerabilities. Critical security updates are prioritized and deployed within 72 hours of disclosure.
