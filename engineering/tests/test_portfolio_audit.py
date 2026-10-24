import json
import tempfile
import unittest
from pathlib import Path

from engineering.portfolio_audit import analyze, main


class PortfolioTests(unittest.TestCase):
    def setUp(self):
        self.inventory = {"snapshot_date":"2026-10-24","source":"test",
          "repositories":[
            {"name":"org/repo-a","archived":False,"visibility":"private",
             "size_kb":0,"business_owner":"UNVERIFIED"},
            {"name":"org/repo-b","archived":True,"visibility":"public",
             "size_kb":75000,"business_owner":"Team"},
            {"name":"org/repo-c","archived":False,"visibility":"public",
             "size_kb":51000,"business_owner":"Team"}]}

    def test_expected_aggregation(self):
        report=analyze(self.inventory)
        self.assertEqual(report["counts"]["seen"],3)
        self.assertEqual(report["counts"]["active"],2)
        self.assertEqual(report["counts"]["archived"],1)
        self.assertEqual(report["counts"]["private"],1)
        self.assertEqual(report["counts"]["active_empty"],1)
        self.assertEqual(report["counts"]["active_over_50mb"],1)
        self.assertEqual(report["counts"]["active_business_owner_unverified"],1)
        self.assertEqual(report["mutations"],"NONE")

    def test_dup_rejected(self):
        self.inventory["repositories"].append(dict(self.inventory["repositories"][0]))
        with self.assertRaises(ValueError):
            analyze(self.inventory)

    def test_negative_size_rejected(self):
        self.inventory["repositories"][0]["size_kb"]=-1
        with self.assertRaises(ValueError):
            analyze(self.inventory)

    def test_non_boolean_archive_rejected(self):
        self.inventory["repositories"][0]["archived"]=0
        with self.assertRaises(ValueError):
            analyze(self.inventory)

    def test_private_report_file_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d)
            (base/"in.json").write_text(json.dumps(self.inventory))
            output=base/"report.json"
            args=["--inventory",str(base/"in.json"),"--private-report",str(output)]
            self.assertEqual(main(args),0)
            self.assertEqual(main(args),2)
            report=json.loads(output.read_text())
            self.assertEqual(report["counts"]["seen"],3)
            self.assertEqual(output.stat().st_mode & 0o077, 0)

if __name__=="__main__":
    unittest.main()
