#!/usr/bin/env python3
"""Cod3Black release evidence preflight. Never issues production authority."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_GATES = (
    "build", "unit", "integration", "security", "e2e",
    "rollback", "observability"
)
ENVIRONMENTS = {"staging", "production"}
CLASSIFICATIONS = {"public", "internal", "confidential", "restricted"}
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]{2,63}$")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def canonical_bytes(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def parse_instant(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else None


def validate_manifest(manifest: dict) -> list[str]:
    issues: list[str] = []
    project_id = manifest.get("project_id")
    if not isinstance(project_id, str) or not ID_PATTERN.fullmatch(project_id):
        issues.append("manifest.project_id must be a lowercase slug (3-64 characters)")
    for key in ("name", "owner", "customer_problem", "revenue_metric", "runbook_url"):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            issues.append(f"manifest.{key} must be nonempty")
    if manifest.get("data_classification") not in CLASSIFICATIONS:
        issues.append("manifest.data_classification is unsupported")
    workflows = manifest.get("critical_workflows")
    if not isinstance(workflows, list) or not workflows or any(
        not isinstance(item, str) or not item.strip() for item in workflows
    ):
        issues.append("manifest.critical_workflows must contain valid entries")
    gates = manifest.get("required_gates")
    if not isinstance(gates, list) or any(
        not isinstance(item, str) or not item.strip() for item in gates
    ):
        issues.append("manifest.required_gates must be a list of nonempty strings")
    else:
        if len(gates) != len(set(gates)):
            issues.append("manifest.required_gates contains duplicates")
        for key in BASE_GATES:
            if key not in gates:
                issues.append(f"manifest is missing required gate {key}")
    return issues


def inspect(manifest: dict, evidence: dict, *,
            now: datetime | None = None, max_age_hours: int = 24) -> dict:
    now = now or datetime.now(timezone.utc)
    issues = validate_manifest(manifest)
    if max_age_hours < 1:
        issues.append("max_age_hours must be positive")
    if evidence.get("project_id") != manifest.get("project_id"):
        issues.append("evidence.project_id does not match manifest")
    env = evidence.get("environment")
    if env not in ENVIRONMENTS:
        issues.append("evidence.environment must be staging or production")
    sha = evidence.get("release_sha")
    if not isinstance(sha, str) or not SHA_PATTERN.fullmatch(sha):
        issues.append("evidence.release_sha must be a full lowercase Git SHA")
    if not isinstance(evidence.get("run_id"), str) or not evidence["run_id"].strip():
        issues.append("evidence.run_id must be nonempty")
    at = parse_instant(evidence.get("executed_at"))
    if at is None:
        issues.append("evidence.executed_at must be ISO8601 with timezone")
    else:
        if at > now + timedelta(minutes=5):
            issues.append("evidence is timestamped in the future")
        if at < now - timedelta(hours=max_age_hours):
            issues.append("evidence is stale")
    if evidence.get("fixture") is not False:
        issues.append("fixture or undeclared source: live evidence must state fixture=false")
    gates = evidence.get("gates")
    if not isinstance(gates, dict):
        gates = {}
        issues.append("evidence.gates must be an object")
    for key in manifest.get("required_gates", []):
        if not isinstance(key, str):
            continue
        entry = gates.get(key)
        if not isinstance(entry, dict):
            issues.append(f"gate {key}: evidence missing")
            continue
        if entry.get("status") != "PASS":
            issues.append(f"gate {key}: not PASS")
        artifact = entry.get("artifact")
        if not isinstance(artifact, str) or not artifact.strip():
            issues.append(f"gate {key}: artifact reference missing")
        # An artifact *reference* is not proof that the artifact is genuine.
    return {
        "project_id": manifest.get("project_id"),
        "environment": env,
        "release_sha": sha,
        "preflight": "PASS" if not issues else "BLOCKED",
        "blockers": sorted(set(issues)),
        "evidence_sha256": hashlib.sha256(canonical_bytes(evidence)).hexdigest(),
        "checked_at": now.isoformat(),
        "authority": "NON_AUTHORITATIVE_PREFLIGHT",
        "certified": False,
        "note": "References are not independently authenticated. No production deployment or completion authorization is granted.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-age-hours", type=int, default=24)
    args = parser.parse_args(argv)
    try:
        manifest = read_json(args.manifest)
        evidence = read_json(args.evidence)
        result = inspect(manifest, evidence, max_age_hours=args.max_age_hours)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {
            "preflight": "BLOCKED", "blockers": [str(exc)],
            "authority": "NON_AUTHORITATIVE_PREFLIGHT", "certified": False
        }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if result["preflight"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
