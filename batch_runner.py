"""Batch Pipeline Runner: Processes a list of target websites in bulk."""
import argparse
from pathlib import Path
from config import REPORTS_DIR
from main import run_pipeline


def run_batch(file_path: Path, sender_name: str = "Growth Consultant", use_ai: bool = True):
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    lines = [line.strip() for line in file_path.read_text().splitlines() if line.strip() and not line.startswith("#")]
    print(f"\n📦 Loaded {len(lines)} targets from {file_path}")

    successful = 0
    failed = 0

    for idx, target in enumerate(lines, 1):
        print(f"\n[{idx}/{len(lines)}] Processing target: {target}")
        try:
            res = run_pipeline(url=target, sender_name=sender_name, use_ai=use_ai, output_dir=REPORTS_DIR)
            if res:
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error auditing {target}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"🎉 BATCH COMPLETE: {successful} Audits Generated, {failed} Failed.")
    print(f"📁 Check reports in: {REPORTS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ClientForge Batch Auditor")
    parser.add_argument("--file", type=str, default="sample_targets.txt", help="Path to text file containing target URLs")
    parser.add_argument("--sender", type=str, default="Your Name", help="Your name for outreach templates")
    parser.add_argument("--no-ai", action="store_true", help="Force offline heuristic mode")

    args = parser.parse_args()
    run_batch(Path(args.file), sender_name=args.sender, use_ai=not args.no_ai)
