"""ClientForge AI: Autonomous B2B Revenue & Audit Agent Suite.

Runs the end-to-end pipeline:
1. Collector Agent (Crawl & Inspect)
2. Analyst Agent (Score & Diagnose Revenue Leaks)
3. Outreach Strategist Agent (Generate Value-First Pitches)
4. Deliverable Builder Agent (Build Executive HTML & Markdown Reports)
"""
import argparse
import sys
from pathlib import Path

from config import REPORTS_DIR, GEMINI_API_KEY
from crawler import SiteInspector
from analyst import AuditAnalystAgent
from pitcher import OutreachStrategistAgent
from reporter import DeliverableBuilderAgent


def run_pipeline(url: str, sender_name: str = "Growth Consultant", use_ai: bool = True, output_dir: Path = REPORTS_DIR):
    """Executes the full agentic auditing and deliverable generation pipeline."""
    print("=" * 70)
    print("🚀 CLIENTFORGE AI: B2B AUDIT & REVENUE AGENT PIPELINE")
    print("=" * 70)
    print(f"[*] Target URL: {url}")
    print(f"[*] Sender Name: {sender_name}")
    print(f"[*] AI Engine: {'Gemini API Enabled' if use_ai and GEMINI_API_KEY else 'Heuristic Diagnostic Engine'}")
    print("-" * 70)

    # Step 1: Collector Agent
    print("\n[Step 1/4] 🕷️ Collector Agent crawling and inspecting target website...")
    inspector = SiteInspector(url)
    crawl_data = inspector.inspect()

    if not crawl_data.get("success"):
        print(f"\n❌ Failed to crawl {url}: {crawl_data.get('error')}")
        return None

    print(f"  ✓ Success! Responded in {crawl_data['load_time_ms']} ms (Status: {crawl_data['status_code']})")
    print(f"  ✓ Extracted: {crawl_data['h1_count']} H1s, {crawl_data['image_count']} images, {len(crawl_data['detected_tech'])} tech signals")
    if crawl_data.get("emails"):
        print(f"  ✓ Direct Contact Discovered: {', '.join(crawl_data['emails'])}")
    if crawl_data.get("phone_numbers"):
        print(f"  ✓ Phone Number Discovered: {', '.join(crawl_data['phone_numbers'])}")

    # Step 2: Analyst Agent
    print("\n[Step 2/4] 🧠 Analyst Agent calculating scorecards & diagnosing revenue leaks...")
    analyst = AuditAnalystAgent(use_ai=use_ai)
    audit_result = analyst.analyze(crawl_data)

    scores = audit_result["scores"]
    print(f"  ✓ Overall Score: {scores['overall']}/100 (Grade: {scores['letter_grade']})")
    print(f"    - SEO: {scores['seo']}/100")
    print(f"    - Conversion Architecture: {scores['conversion']}/100")
    print(f"    - Mobile & Performance: {scores['performance']}/100")
    print(f"    - AI Readiness: {scores['ai_readiness']}/100")

    leaks = audit_result["insights"].get("revenue_leaks", [])
    print(f"\n  🚨 Identified {len(leaks)} Major Revenue Leaks:")
    for idx, leak in enumerate(leaks, 1):
        print(f"    {idx}. [{leak.get('severity', 'High')}] {leak.get('title')}")

    # Step 3: Outreach Strategist Agent
    print("\n[Step 3/4] ✍️ Outreach Strategist Agent generating value-first pitches...")
    pitcher = OutreachStrategistAgent()
    pitches = pitcher.generate_pitches(audit_result, sender_name=sender_name)
    print("  ✓ Created 3 High-Conversion Email Sequences + 1 LinkedIn Connection Pitch")

    # Step 4: Deliverable Builder Agent
    print("\n[Step 4/4] 📄 Deliverable Builder Agent generating presentation-ready reports...")
    builder = DeliverableBuilderAgent(output_dir)
    files = builder.save_deliverables(audit_result, pitches)

    print("\n" + "=" * 70)
    print("✅ PIPELINE EXECUTION COMPLETE!")
    print("=" * 70)
    print(f"📁 Deliverables Directory: {files['client_dir']}")
    print(f"  • Executive HTML Report : {files['html_report']}")
    print(f"  • Markdown Audit Report : {files['markdown_report']}")
    print(f"  • Cold Outreach Pitches : {files['pitches_file']}")
    print("=" * 70)

    return files


def main():
    parser = argparse.ArgumentParser(description="ClientForge AI - Autonomous Revenue Agent Suite")
    parser.add_argument("--url", type=str, help="Target website URL to audit (e.g. https://example.com)")
    parser.add_argument("--sender", type=str, default="Your Name", help="Your name for personalized pitch generation")
    parser.add_argument("--no-ai", action="store_true", help="Force heuristic offline analysis without calling Gemini")
    parser.add_argument("--output", type=str, default=str(REPORTS_DIR), help="Output directory for reports")

    args = parser.parse_args()

    url = args.url
    if not url:
        print("\n=== ClientForge AI: Revenue & B2B Audit Agent ===")
        url = input("Enter target company URL (e.g., example.com): ").strip()
        if not url:
            print("❌ Error: URL cannot be empty.")
            sys.exit(1)

    sender = args.sender
    if sender == "Your Name":
        entered = input("Enter your name for email signatures [Default: Your Name]: ").strip()
        if entered:
            sender = entered

    run_pipeline(url=url, sender_name=sender, use_ai=not args.no_ai, output_dir=Path(args.output))


if __name__ == "__main__":
    main()
