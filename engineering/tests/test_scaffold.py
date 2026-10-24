import json
import tempfile
import unittest
from pathlib import Path

from engineering.scaffold import main, make_project
from engineering.release_gate import validate_manifest


class ScaffoldTests(unittest.TestCase):
    def test_starter_has_documented_boundary_and_minimum_contract(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)/"merchant"
            files = make_project(dest, project_id="merchant-ops",
                name="Merchant Operations", owner="Test Operator",
                problem="Lost order follow-ups", revenue_metric="Completed orders")
            manifest = json.loads((dest/"project.json").read_text())
            self.assertEqual(validate_manifest(manifest), [])
            self.assertIn("tools/release_gate.py", files)
            self.assertIn(".github/workflows/quality.yml", files)
            self.assertIn("docs/security.md", files)
            self.assertIn("SCAFFOLD ONLY", (dest/"README.md").read_text())

    def test_duplicate_target_refused_without_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)/"merchant"
            dest.mkdir()
            original = dest/"data"
            original.write_text("PROTECT")
            with self.assertRaises(FileExistsError):
                make_project(dest, project_id="merchant-ops",
                    name="Merchant Ops", owner="Operator",
                    problem="Missing data", revenue_metric="Customer value")
            self.assertEqual(original.read_text(), "PROTECT")

    def test_invalid_project_refused_without_directory(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)/"merchant"
            with self.assertRaises(ValueError):
                make_project(dest, project_id="../../unsafe",
                    name="Merchant Ops", owner="Operator",
                    problem="Missing data", revenue_metric="Revenue")
            self.assertFalse(dest.exists())

    def test_cli_blocks_invalid_id(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(main(["--output", str(Path(d)/"demo"),
                    "--project-id", ".", "--name", "Demo", "--owner", "Operator",
                    "--customer-problem", "Manual intake",
                    "--revenue-metric", "Sales"]), 2)

    def test_cli_works_and_generates_all_expected_files(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/"demo"
            result=main(["--output", str(dest), "--project-id","demo-app",
                     "--name","Demo App", "--owner","Operator",
                     "--customer-problem","Slow intake",
                     "--revenue-metric","Time saved"])
            self.assertEqual(result,0)
            self.assertTrue((dest/"project.json").is_file())
            self.assertIn("build", json.loads((dest/"project.json").read_text())["required_gates"])


if __name__ == "__main__":
    unittest.main()
