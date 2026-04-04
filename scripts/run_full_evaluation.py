#!/usr/bin/env python3
"""Master orchestration script: Run complete RAG evaluation pipeline."""

import argparse
import json
import logging
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EvaluationOrchestrator:
    """Orchestrate complete RAG evaluation pipeline."""
    
    def __init__(
        self,
        suite: str = "full",
        input_file: Optional[str] = None,
        skip_archive: bool = False,
    ) -> None:
        """Initialize orchestrator."""
        self.base_path = Path(__file__).parent.parent
        self.scripts_path = self.base_path / "scripts"
        self.results_path = self.base_path / "artifacts" / "latest"
        self.results_archive_path = self.base_path / "artifacts" / "archive"
        self.test_cases_archive_path = self.base_path / "data" / "archived"
        self.results_path.mkdir(parents=True, exist_ok=True)
        self.results_archive_path.mkdir(parents=True, exist_ok=True)
        self.test_cases_archive_path.mkdir(parents=True, exist_ok=True)

        self.suite = suite.lower()
        self.skip_archive = skip_archive
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.custom_input = Path(input_file).resolve() if input_file else None
        self.active_input_path = self._resolve_input_file()
        self.kb_output_path = self._resolve_kb_output_path(self.active_input_path)
        
        self.execution_log = {
            "start_time": datetime.now().isoformat(),
            "suite": self.suite,
            "active_input": str(self.active_input_path),
            "kb_output": str(self.kb_output_path),
            "phases": {},
            "status": "running",
        }

    def _load_cases(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load test cases from list or dict format."""
        with open(file_path, 'r', encoding='utf-8') as file_handle:
            data = json.load(file_handle)

        if isinstance(data, dict):
            return data.get("test_cases", [])
        return data if isinstance(data, list) else []

    def _save_cases(self, file_path: Path, cases: List[Dict[str, Any]]) -> None:
        """Save test cases in list format for evaluators."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file_handle:
            json.dump(cases, file_handle, indent=2, ensure_ascii=False)

    def _resolve_input_file(self) -> Path:
        """Resolve the active input file based on suite or custom input."""
        if self.custom_input:
            return self.custom_input

        suite_map = {
            "full": self.base_path / "data" / "processed" / "test_cases_formatted.json",
            "smoke": self.base_path / "data" / "processed" / "test_cases_smoke.json",
            "regression": self.base_path / "data" / "processed" / "test_cases_regression.json",
        }
        return suite_map.get(self.suite, suite_map["full"])

    def _resolve_kb_output_path(self, input_path: Path) -> Path:
        """Resolve KB-enriched output path for the selected suite."""
        if input_path.name == "test_cases_formatted.json":
            return self.base_path / "data" / "processed" / "test_cases_with_kb.json"
        return input_path.with_name(f"{input_path.stem}_with_kb.json")

    def create_subset_files(self) -> bool:
        """Create smoke and regression subset files from the formatted dataset."""
        source_path = self.base_path / "data" / "processed" / "test_cases_formatted.json"
        if not source_path.exists():
            logger.warning(f"Subset source not found: {source_path}")
            return False

        try:
            cases = self._load_cases(source_path)
            if not cases:
                logger.warning("No formatted cases available to build subsets")
                return False

            priority_rank = {"high": 0, "medium": 1, "low": 2}
            difficulty_rank = {"easy": 0, "medium": 1, "hard": 2}

            def sort_key(case: Dict[str, Any]) -> Tuple[int, int, int]:
                metadata = case.get("metadata", {})
                priority = str(metadata.get("priority", case.get("priority", "low"))).lower()
                difficulty = str(metadata.get("difficulty", case.get("difficulty", "medium"))).lower()
                case_id = int(metadata.get("id", case.get("id", 999999)))
                return (
                    priority_rank.get(priority, 3),
                    difficulty_rank.get(difficulty, 3),
                    case_id,
                )

            ranked_cases = sorted(cases, key=sort_key)
            smoke_cases = ranked_cases[:min(10, len(ranked_cases))]
            regression_cases = ranked_cases[:min(30, len(ranked_cases))]

            smoke_path = self.base_path / "data" / "processed" / "test_cases_smoke.json"
            regression_path = self.base_path / "data" / "processed" / "test_cases_regression.json"
            self._save_cases(smoke_path, smoke_cases)
            self._save_cases(regression_path, regression_cases)

            self.execution_log["subset_counts"] = {
                "smoke": len(smoke_cases),
                "regression": len(regression_cases),
                "full": len(cases),
            }
            logger.info(
                "Created subset files: smoke=%s cases, regression=%s cases, full=%s cases",
                len(smoke_cases),
                len(regression_cases),
                len(cases),
            )
            return True

        except Exception as err:
            logger.error(f"Failed to create subset files: {err}")
            return False
    
    def print_banner(self, title: str) -> None:
        """Print formatted banner."""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    
    def archive_previous_outputs(self) -> None:
        """Archive current results and input snapshots with a timestamp."""
        if self.skip_archive:
            logger.info("Skipping archive step (--skip-archive)")
            return

        result_files = [
            self.results_path / "ragas_evaluation.json",
            self.results_path / "ragas_evaluation.xlsx",
            self.results_path / "foundry_official_evaluation.json",
            self.results_path / "foundry_official_evaluation.xlsx",
            self.results_path / "combined_evaluation.json",
            self.results_path / "combined_evaluation.xlsx",
            self.results_path / "execution_log.json",
        ]
        existing_results = [file_path for file_path in result_files if file_path.exists()]
        snapshot_files = [file_path for file_path in [self.active_input_path, self.kb_output_path] if file_path.exists()]

        if not existing_results and not snapshot_files:
            logger.info("No previous results found to archive")
            return

        results_archive_dir = self.results_archive_path / self.timestamp
        cases_archive_dir = self.test_cases_archive_path / self.timestamp
        results_archive_dir.mkdir(parents=True, exist_ok=True)
        cases_archive_dir.mkdir(parents=True, exist_ok=True)

        archived_results = []
        for file_path in existing_results:
            shutil.copy2(file_path, results_archive_dir / file_path.name)
            archived_results.append(file_path.name)

        archived_cases = []
        for file_path in snapshot_files:
            shutil.copy2(file_path, cases_archive_dir / file_path.name)
            archived_cases.append(file_path.name)

        self.execution_log["archive"] = {
            "timestamp": self.timestamp,
            "results_archive": str(results_archive_dir),
            "test_cases_archive": str(cases_archive_dir),
            "archived_results": archived_results,
            "archived_test_cases": archived_cases,
        }
        logger.info(
            "Archived %s result files and %s test snapshots with timestamp %s",
            len(archived_results),
            len(archived_cases),
            self.timestamp,
        )

    def run_phase(
        self,
        phase_num: int,
        phase_name: str,
        script_path: str,
        env_overrides: Optional[Dict[str, str]] = None,
    ) -> Tuple[bool, str]:
        """Run a pipeline phase."""
        self.print_banner(f"Phase {phase_num}: {phase_name}")
        
        logger.info(f"Executing: {script_path}")
        phase_env = dict(**env_overrides) if env_overrides else {}
        env = {**dict(), **phase_env}
        env = {**__import__("os").environ, **env}
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=600,
                env=env,
            )
            
            if result.returncode == 0:
                logger.info(f"✓ Phase {phase_num} completed successfully")
                self.execution_log["phases"][phase_name] = {
                    "status": "success",
                    "return_code": result.returncode,
                    "stdout_tail": result.stdout[-1000:],
                }
                return True, result.stdout

            logger.error(f"✗ Phase {phase_num} failed with code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            self.execution_log["phases"][phase_name] = {
                "status": "failed",
                "return_code": result.returncode,
                "error": result.stderr,
            }
            return False, result.stderr
        
        except subprocess.TimeoutExpired:
            logger.error(f"✗ Phase {phase_num} timed out")
            self.execution_log["phases"][phase_name] = {
                "status": "timeout",
                "error": "Execution timeout",
            }
            return False, "Timeout"
        
        except Exception as err:
            logger.error(f"✗ Phase {phase_num} error: {err}")
            self.execution_log["phases"][phase_name] = {
                "status": "error",
                "error": str(err),
            }
            return False, str(err)
    
    def verify_results(self) -> bool:
        """Verify all results files exist."""
        required_files = [
            self.kb_output_path,
            self.results_path / "ragas_evaluation.json",
            self.results_path / "combined_evaluation.json",
        ]
        
        logger.info("\nVerifying results...")
        all_exist = True
        
        for file_path in required_files:
            if file_path.exists():
                size = file_path.stat().st_size
                logger.info(f"✓ {file_path.name} ({size} bytes)")
            else:
                logger.warning(f"✗ {file_path.name} not found")
                all_exist = False
        
        excel_file = self.results_path / "combined_evaluation.xlsx"
        if excel_file.exists():
            logger.info(f"✓ combined_evaluation.xlsx ({excel_file.stat().st_size} bytes)")
        else:
            logger.info("ℹ Excel report not generated (optional)")
        
        return all_exist
    
    def generate_execution_report(self) -> None:
        """Generate execution summary report."""
        self.execution_log["end_time"] = datetime.now().isoformat()
        
        failed_phases = [
            phase for phase in self.execution_log["phases"].values()
            if phase.get("status") != "success"
        ]
        self.execution_log["status"] = "failed" if failed_phases else "success"
        
        log_file = self.results_path / "execution_log.json"
        with open(log_file, 'w', encoding='utf-8') as file_handle:
            json.dump(self.execution_log, file_handle, indent=2)
        
        logger.info(f"✓ Execution log saved: {log_file}")
    
    def print_summary(self) -> None:
        """Print final summary report."""
        self.print_banner("FINAL SUMMARY")
        
        print(f"\nExecution Status: {self.execution_log['status'].upper()}")
        print(f"Suite: {self.suite.upper()}")
        print(f"Active Input: {self.active_input_path.name}")
        print(f"Start Time: {self.execution_log['start_time']}")
        print(f"End Time: {self.execution_log['end_time']}")
        
        print("\nPhase Results:")
        for phase_name, phase_result in self.execution_log["phases"].items():
            status = phase_result.get("status", "unknown").upper()
            symbol = "✓" if status == "SUCCESS" else "✗"
            print(f"  {symbol} {phase_name}: {status}")

        if "archive" in self.execution_log:
            print("\nArchive:")
            print(f"  📦 Results Archive: {self.execution_log['archive']['results_archive']}")
            print(f"  📦 Test Case Archive: {self.execution_log['archive']['test_cases_archive']}")
        
        print("\nOutput Files:")
        print(f"  📊 Results Directory: {self.results_path}")
        print(f"  📄 KB-Enriched Test Cases: {self.kb_output_path.name}")
        print(f"  📄 RAGAS Evaluation: ragas_evaluation.json")
        print(f"  📄 Foundry Evaluation: foundry_official_evaluation.json")
        print(f"  📄 Combined Report: combined_evaluation.json")
        print(f"  📄 Combined Report: combined_evaluation.xlsx")
        print(f"  📄 Execution Log: execution_log.json")
        
        print("\nRun Modes:")
        print("  • Full suite: python scripts/run_full_evaluation.py --suite full")
        print("  • Smoke suite: python scripts/run_full_evaluation.py --suite smoke")
        print("  • Regression suite: python scripts/run_full_evaluation.py --suite regression")
        
        print("\n" + "=" * 80)
    
    def run(self) -> int:
        """Run complete evaluation pipeline."""
        try:
            self.print_banner(f"RAG Evaluation Pipeline - {self.suite.upper()} Suite")
            self.create_subset_files()

            self.active_input_path = self._resolve_input_file()
            self.kb_output_path = self._resolve_kb_output_path(self.active_input_path)
            self.execution_log["active_input"] = str(self.active_input_path)
            self.execution_log["kb_output"] = str(self.kb_output_path)

            if not self.active_input_path.exists():
                logger.error(f"Test cases not found: {self.active_input_path}")
                return 1

            active_case_count = len(self._load_cases(self.active_input_path))
            self.execution_log["active_case_count"] = active_case_count
            logger.info(
                "Using suite '%s' with %s test cases from %s",
                self.suite,
                active_case_count,
                self.active_input_path.name,
            )

            self.archive_previous_outputs()

            phase1_env = {
                "TEST_CASES_PATH": str(self.active_input_path),
                "OUTPUT_TEST_CASES_PATH": str(self.kb_output_path),
            }
            success, _ = self.run_phase(
                1,
                "Load KB & Populate Context",
                str(self.scripts_path / "load_pdf_knowledge_base.py"),
                env_overrides=phase1_env,
            )
            if not success:
                logger.warning("Phase 1 failed - continuing with original test cases")

            evaluation_input = self.kb_output_path if self.kb_output_path.exists() else self.active_input_path
            evaluation_env = {"TEST_CASES_PATH": str(evaluation_input)}
            self.execution_log["evaluation_input"] = str(evaluation_input)
            
            success, _ = self.run_phase(
                2,
                "RAGAS KB Quality Evaluation",
                str(self.scripts_path / "foundry_evaluate_ragas.py"),
                env_overrides=evaluation_env,
            )
            if not success:
                logger.error("Phase 2 failed - cannot continue")
                self.execute_failed("RAGAS evaluation failed")
                return 1
            
            success, _ = self.run_phase(
                3,
                "Foundry Official Evaluation",
                str(self.scripts_path / "foundry_evaluate_official.py"),
                env_overrides=evaluation_env,
            )
            if not success:
                logger.warning("Phase 3 failed - continuing without Foundry evaluation")
            
            success, _ = self.run_phase(
                4,
                "Generate Combined Report",
                str(self.scripts_path / "generate_combined_report.py"),
            )
            if not success:
                logger.warning("Phase 4 failed - report generation skipped")
            
            self.print_banner("Verification")
            if not self.verify_results():
                logger.warning("Some result files not found")
            
            self.generate_execution_report()
            self.print_summary()
            
            return 0 if self.execution_log["status"] == "success" else 1
        
        except KeyboardInterrupt:
            logger.error("\nExecution interrupted by user")
            self.execution_log["status"] = "interrupted"
            self.generate_execution_report()
            return 1
        
        except Exception as err:
            logger.error(f"Fatal error: {err}")
            import traceback
            traceback.print_exc()
            self.execution_log["status"] = "error"
            self.generate_execution_report()
            return 1
    
    def execute_failed(self, reason: str) -> None:
        """Handle execution failure."""
        logger.error(f"\n✗ Pipeline execution failed: {reason}")
        self.generate_execution_report()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the RAG evaluation pipeline")
    parser.add_argument(
        "--suite",
        choices=["full", "smoke", "regression"],
        default="full",
        help="Choose which suite to run (default: full)",
    )
    parser.add_argument(
        "--input",
        help="Optional custom input JSON file. Overrides --suite when provided.",
    )
    parser.add_argument(
        "--skip-archive",
        action="store_true",
        help="Skip automatic archiving of previous results before the run.",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    orchestrator = EvaluationOrchestrator(
        suite=args.suite,
        input_file=args.input,
        skip_archive=args.skip_archive,
    )
    return orchestrator.run()


if __name__ == "__main__":
    sys.exit(main())
