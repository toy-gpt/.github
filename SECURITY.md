# Security Policy

## Scope

This policy applies to repositories maintained by this organization
unless a repository provides its own security policy.

## Supported Versions

Security maintenance is prioritized based on the
operational classification of the repository:

- **Actively maintained software:** Security reports are evaluated against current releases.
  Fixes may be provided through subsequent releases.
- **Published packages:** Vulnerabilities affecting distributed packages
  receive priority assessment based on severity and potential impact.
- **Frozen research artifacts:** Historical experimental data, results, and
  pinned implementations are preserved for reproducibility.
  Security findings may be documented or addressed in subsequent versions
  without modifying the original evidence.
- **Archived repositories:** No ongoing security maintenance is guaranteed.

## Reporting a Vulnerability

### Primary Channel (GitHub Private Reporting)

Please report suspected vulnerabilities
using GitHub's **private vulnerability reporting**
feature in the affected repository.

1. Navigate to the repository's **Security** tab.
2. Select **Report a vulnerability** under the Advisories section.

### Alternate

If private reporting is unavailable,
open a public issue requesting a private reporting channel.
Do not include vulnerability details, credentials, exploits,
or other sensitive information in public issues.
Please include sufficient information
to reproduce and evaluate the issue,
including affected versions and potential impact.

## Response and Disclosure

Security reports are reviewed as part of normal repository maintenance.

We assess reported vulnerabilities and determine appropriate actions based on
severity, exploitability, affected users, and repository maintenance status.

Possible responses include patches, updated releases, security advisories,
documentation, or explicit acceptance of residual risk.

Response and remediation times depend on maintainer availability.

Please allow an opportunity for assessment and coordinated disclosure
before publicly releasing vulnerability details.

## Security Practices

Repositories may employ automated testing,
static analysis, dependency scanning,
Software Bills of Materials (SBOMs), workflow security checks,
vulnerability scanning, and release provenance controls
depending on their risk profile.

These measures reduce risk but
do not constitute a guarantee
that software is free of vulnerabilities.

The following strict rules apply to human contributors
and automated AI coding agents
operating within any organization repository:

### 1. Secrets & Credentials

- Never hardcode API keys, database passwords,
  JWT secrets, encryption keys, or tokens in source code.
- Use environment variables or
  designated secret management platforms.
- Do not write sensitive credentials, authorization headers,
  tokens, or personally-identifying information (PII)
  to console logs, standard output, or application telemetry.

### 2. Sensitive Files & Repository Operations

- Do not read, index, parse, or expose
  `.env` files, `*.pem` files, `*.key` files,
  or `/secrets/` directories.
- Do not execute potentially destructive shell commands
  (e.g., `rm -rf` on system roots, database drops,
  branch force-pushes, or bulk deletions)
  without explicit human confirmation.

### 3. Database Authorization

- Enforce least-privilege, deny-by-default authorization
  for access to nonpublic or user-/tenant-specific database records.
- Use database-enforced Row-Level Security (RLS)
  or equivalent row-access policies
  where supported and appropriate.
  Otherwise, enforce authorization **server-side** for every read and write.
- Never rely solely on client-side filtering
  or expose privileged database access to untrusted clients.
- Test that users cannot access or modify records
  belonging to other users or tenants without authorization.

### 4. Data Flow & Input

- Treat all incoming data from users, webhooks, or external APIs as untrusted.
- Validate, parse, and sanitize data strictly at system boundaries.
- Never instantiate service-role, administrative, or
  root-level database/API clients
  within client-facing components or frontend code.
