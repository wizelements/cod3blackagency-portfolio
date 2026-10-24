#!/usr/bin/env python3
"""Read-only repository portfolio census; no repository mutations."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def analyze(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("inventory must be a JSON object")
    repos = data.get("repositories")
    if not isinstance(repos, list):
        raise ValueError("repositories must be an array")
    seen = set()
    review = []
    archived = private = active_empty = oversized = unassigned = 0
    for item in repos:
        if not isinstance(item, dict):
            raise ValueError("invalid repository entry")
        name = item.get("name")
        if not isinstance(name, str) or "/" not in name or name in seen:
            raise ValueError("invalid or duplicate repository name")
        seen.add(name)
        is_archived = item.get("archived")
        size = item.get("size_kb")
        if not isinstance(is_archived, bool):
            raise ValueError("archived must be boolean")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise ValueError("size_kb must be a nonnegative integer")
        if item.get("visibility") not in ("public", "private", "internal"):
            raise ValueError("unsupported visibility")
        private += int(item["visibility"] == "private")
        archived += int(is_archived)
        if is_archived:
            continue
        why = []
        if item.get("business_owner") in (None, "", "UNVERIFIED"):
            unassigned += 1
            why.append("business owner unverified")
        if size == 0:
            active_empty += 1
            why.append("empty active repository; review usefulness")
        if size > 50000:
            oversized += 1
            why.append("large repository; review stored artifacts")
        if why:
            review.append({"repository": name, "reasons": why})
    return {
        "snapshot_date": data.get("snapshot_date"),
        "source": data.get("source"),
        "counts": {
            "seen": len(repos), "active": len(repos)-archived,
            "archived": archived, "private": private,
            "active_empty": active_empty,
            "active_over_50mb": oversized,
            "active_business_owner_unverified": unassigned
        },
        "manual_review": sorted(review, key=lambda i: i["repository"].lower()),
        "limits": ["Connected repository visibility can be incomplete",
                   "GitHub account owner is not necessarily business owner",
                   "Size is not evidence of defects",
                   "No live workflow, cost, vulnerability or deployment checks performed"],
        "mutations": "NONE"
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory", type=Path, required=True)
    ap.add_argument("--private-report", type=Path)
    args = ap.parse_args(argv)
    try:
        report = analyze(json.loads(args.inventory.read_text(encoding="utf-8")))
        if args.private_report:
            if args.private_report.exists():
                raise FileExistsError("refusing to overwrite an existing report")
            args.private_report.parent.mkdir(parents=True, exist_ok=True)
            fd = os.open(args.private_report, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
                f.write("\n")
        print(json.dumps({"counts": report["counts"],
                          "mutations": "NONE", "private_report_written": bool(args.private_report)}, indent=2))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print("BLOCKED: " + str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
