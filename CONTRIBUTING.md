# Contributing to Cod3BlackAgency Projects

Thank you for your interest in contributing. This document outlines the process for contributing to Cod3BlackAgency repositories.

## Code of Conduct

All contributors are expected to maintain professional, respectful communication. Harassment, discrimination, or disruptive behavior will not be tolerated.

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the appropriate issue template
3. Provide clear reproduction steps
4. Include environment details (OS, Node version, etc.)

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Ensure all tests pass: `npm test` or `pnpm test`
5. Ensure linting passes: `npm run lint` or `pnpm lint`
6. Commit with clear messages following conventional commits
7. Push to your fork and open a PR

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example: `feat(auth): add JWT token refresh endpoint`

## Development Setup

Each repository includes setup instructions in its README. Generally:

```bash
# Clone the repo
git clone https://github.com/wizelements/[repo-name].git
cd [repo-name]

# Install dependencies
npm install  # or pnpm install

# Copy environment variables
cp .env.example .env

# Run development server
npm run dev  # or pnpm dev
```

## Code Standards

- TypeScript strict mode where applicable
- ESLint configuration must pass
- Prettier formatting enforced
- Test coverage for new features
- Documentation for public APIs

## Review Process

1. All PRs require at least one approval
2. CI checks must pass
3. No merge conflicts
4. Squash commits on merge

## Questions

Open a discussion in the relevant repository or contact [contact@cod3blackagency.com].
