import copy
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from engineering.release_gate import BASE_GATES, inspect, main, parse_instant


def sample():
    m = {
        "project_id": "example-merchant", "name": "Example Merchant",
        "owner": "Cod3Black Engineering", "customer_problem": "Manual order tracking",
        "revenue_metric": "Paid orders completed",
        "runbook_url": "https://example.invalid/runbook",
        "data_classification": "confidential",
        "critical_workflows": ["order to fulfillment"],
        "required_gates": list(BASE_GATES) + ["payment"]
    }
    e = {
        "project_id": m["project_id"], "environment": "staging",
        "release_sha": "a" * 40, "run_id": "ci-123", "fixture": False,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "gates": {k: {"status": "PASS", "artifact": "ci://run-123/" + k}
                  for k in m["required_gates"]}
    }
    return m, e


class ReleaseGateTests(unittest.TestCase):
    def test_all_necessary_evidence_is_preflight_only(self):
        m, e = sample()
        result = inspect(m, e)
        self.assertEqual(result["preflight"], "PASS")
        self.assertFalse(result["certified"])
        self.assertEqual(result["authority"], "NON_AUTHORITATIVE_PREFLIGHT")

    def test_missing_gate_is_blocking(self):
        m, e = sample()
        del e["gates"]["payment"]
        self.assertIn("gate payment: evidence missing", inspect(m, e)["blockers"])

    def test_failed_gate_blocks(self):
        m, e = sample()
        e["gates"]["security"]["status"] = "FAIL"
        self.assertEqual(inspect(m, e)["preflight"], "BLOCKED")

    def test_duplicate_gates_block(self):
        m, e = sample()
        m["required_gates"].append("build")
        self.assertEqual(inspect(m, e)["preflight"], "BLOCKED")

    def test_missing_baseline_blocks(self):
        m, e = sample()
        m["required_gates"].remove("rollback")
        self.assertIn("manifest is missing required gate rollback",
                      inspect(m, e)["blockers"])

    def test_fixture_blocks(self):
        m, e = sample()
        e["fixture"] = True
        self.assertEqual(inspect(m, e)["preflight"], "BLOCKED")

    def test_missing_fixture_flag_blocks(self):
        m, e = sample()
        del e["fixture"]
        self.assertEqual(inspect(m, e)["preflight"], "BLOCKED")

    def test_stale_evidence_blocks(self):
        m, e = sample()
        e["executed_at"] = (datetime.now(timezone.utc) -
                            timedelta(days=2)).isoformat()
        self.assertIn("evidence is stale", inspect(m, e)["blockers"])

    def test_future_evidence_blocks(self):
        m, e = sample()
        e["executed_at"] = (datetime.now(timezone.utc) +
                            timedelta(hours=1)).isoformat()
        self.assertIn("evidence is timestamped in the future",
                      inspect(m, e)["blockers"])

    def test_missing_timezone_blocks(self):
        m, e = sample()
        e["executed_at"] = "2026-10-24T10:00:00"
        self.assertEqual(inspect(m, e)["preflight"], "BLOCKED")

    def test_mismatched_project_blocks(self):
        m, e = sample()
        e["project_id"] = "other"
        self.assertEqual(inspect(m, e)["preflight"], "BLOCKED")

    def test_non_sha_blocks(self):
        m, e = sample()
        e["release_sha"] = "main"
        self.assertEqual(inspect(m, e)["preflight"], "BLOCKED")

    def test_artifact_reference_required(self):
        m, e = sample()
        e["gates"]["e2e"]["artifact"] = ""
        self.assertIn("gate e2e: artifact reference missing",
                      inspect(m, e)["blockers"])

    def test_non_object_manifest_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "m.json").write_text("[]")
            (p / "e.json").write_text("{}")
            self.assertEqual(main(["--manifest", str(p/"m.json"),
                                   "--evidence", str(p/"e.json")]), 2)

    def test_bad_json_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "m.json").write_text("{INVALID")
            (p / "e.json").write_text("{}")
            self.assertEqual(main(["--manifest", str(p/"m.json"),
                                   "--evidence", str(p/"e.json")]), 2)

    def test_output_file_is_written_and_non_authoritative(self):
        m, e = sample()
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p/"m.json").write_text(json.dumps(m))
            (p/"e.json").write_text(json.dumps(e))
            out = p/"out"/"attestation.json"
            rc = main(["--manifest", str(p/"m.json"), "--evidence",
                       str(p/"e.json"), "--output", str(out)])
            self.assertEqual(rc, 0)
            self.assertTrue(out.exists())
            self.assertFalse(json.loads(out.read_text())["certified"])

    def test_digest_changes_with_evidence(self):
        m, e = sample()
        first = inspect(m, e)["evidence_sha256"]
        changed = copy.deepcopy(e)
        changed["run_id"] = "ci-124"
        self.assertNotEqual(first, inspect(m, changed)["evidence_sha256"])

    def test_timestamps_parsed_with_zone_only(self):
        self.assertIsNone(parse_instant("not-time"))
        self.assertIsNone(parse_instant("2026-10-24T11:00:00"))
        self.assertIsNotNone(parse_instant("2026-10-24T11:00:00Z"))


if __name__ == "__main__":
    unittest.main()
