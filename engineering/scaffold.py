#!/usr/bin/env python3
"""Generate a Cod3Black engineering project skeleton. Does not deploy."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    from engineering.release_gate import BASE_GATES, validate_manifest
except ModuleNotFoundError:
    from release_gate import BASE_GATES, validate_manifest


QUALITY_WORKFLOW = """name: New Project Baseline
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Check manifest and project tooling
        run: |
          python -m compileall -q tools
          python -c "import json,sys; from tools.release_gate import validate_manifest; faults=validate_manifest(json.load(open('project.json'))); print(faults); sys.exit(bool(faults))"
      # Add real build, security, unit, E2E and integration jobs before live release.
"""


def make_project(destination: Path, *, project_id: str, name: str,
                 owner: str, problem: str, revenue_metric: str,
                 classification: str = "internal") -> list[str]:
    manifest = {
        "project_id": project_id, "name": name, "owner": owner,
        "customer_problem": problem, "revenue_metric": revenue_metric,
        "data_classification": classification,
        "critical_workflows": ["REPLACE: document first customer journey"],
        "runbook_url": "docs/runbook.md",
        "required_gates": list(BASE_GATES)
    }
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    if destination.exists():
        raise FileExistsError("refusing to overwrite an existing directory")
    destination.mkdir(parents=True, mode=0o700)
    try:
        (destination / "docs").mkdir()
        (destination / "tools").mkdir()
        (destination / ".github" / "workflows").mkdir(parents=True)
        (destination / "project.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (destination / "README.md").write_text(
            "# " + name + "\n\n"
            "Status: SCAFFOLD ONLY. No app, customer data, paid service, or "
            "production system has been delivered.\n\n"
            "Customer problem: " + problem + "\n\n"
            "Business metric: " + revenue_metric + "\n\n"
            "See docs for runbook, architecture, security, and business case.\n",
            encoding="utf-8")
        docs = {
            "runbook.md": "# Runbook\n\nOwner: " + owner +
                "\n\nDescribe alerts, dependencies, rollback, restoration and escalation.\n",
            "architecture.md": "# Architecture\n\nDefine trust boundaries, data owner, "
                "API, database, dependency graph, delivery and disaster recovery.\n",
            "security.md": "# Security\n\nRecord identity roles, threat model, "
                "least privilege, logging, secrets, tests and incident response.\n",
            "business-case.md": "# Business case\n\nProblem: " + problem +
                "\n\nSuccess metric: " + revenue_metric +
                "\n\nRecord target buyer, pricing, distribution, pilot evidence and cost.\n"
        }
        for name, contents in docs.items():
            (destination / "docs" / name).write_text(contents, encoding="utf-8")
        (destination / "tools" / "release_gate.py").write_bytes(
            Path(__file__).with_name("release_gate.py").read_bytes())
        (destination / ".github" / "workflows" / "quality.yml").write_text(
            QUALITY_WORKFLOW, encoding="utf-8")
        (destination / ".gitignore").write_text(
            ".env\n.env.*\n!.env.example\n__pycache__/\n*.pyc\n"
            ".venv/\nnode_modules/\ncoverage/\n", encoding="utf-8")
    except Exception:
        shutil.rmtree(destination)
        raise
    return sorted(str(p.relative_to(destination)) for p in destination.rglob("*")
                  if p.is_file())


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--customer-problem", required=True)
    parser.add_argument("--revenue-metric", required=True)
    parser.add_argument("--data-classification", default="internal",
                        choices=["public", "internal", "confidential", "restricted"])
    args = parser.parse_args(argv)
    try:
        created = make_project(
            args.output, project_id=args.project_id, name=args.name,
            owner=args.owner, problem=args.customer_problem,
            revenue_metric=args.revenue_metric,
            classification=args.data_classification)
    except (FileExistsError, OSError, ValueError) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        return 2
    print(json.dumps({"project": args.project_id,
                      "status": "SCAFFOLD_ONLY", "files": created}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
