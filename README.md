# ClientForge AI: Autonomous B2B Revenue & Audit Agent Suite

An autonomous multi-agent pipeline designed to discover, audit, score, and pitch B2B clients with zero friction.

## 🌟 What This Agent Does
1. **Collector Agent (`crawler.py`)**: Crawls target websites, measures response latency, analyzes SEO headers, checks mobile responsiveness, discovers direct contact emails/phone numbers, detects chat widgets, and maps technology stacks.
2. **Analyst Agent (`analyst.py`)**: Computes 4 key pillar scores (SEO, Conversion Architecture, Mobile/Speed UX, AI Readiness) and identifies 3 high-impact revenue leaks costing the company money. Supports both Gemini API and an offline diagnostic engine.
3. **Outreach Strategist Agent (`pitcher.py`)**: Generates 3 customized value-first cold email angles and a 300-character LinkedIn connection note grounded in the exact bottlenecks found.
4. **Deliverable Builder Agent (`reporter.py`)**: Produces an Executive HTML Audit Report (styled with modern dark theme cards, progress bars, and score badges) and a Markdown audit report suitable for client deliverables ($200+ perceived value).

---

## 🚀 Quick Start

### 1. Run a Single Website Audit
```bash
cd /root/.gemini/antigravity-cli/scratch/revenue_agent
python3 main.py --url https://example.com --sender "Your Name"
```

### 2. Run Batch Audits (Multiple Targets)
Create or edit `sample_targets.txt` with website URLs (one per line), then run:
```bash
python3 batch_runner.py --file sample_targets.txt --sender "Your Name"
```

All deliverables will be saved automatically in:
`reports/<domain>/`
- `executive_audit.html`: Open in any browser or print to PDF for client presentation.
- `executive_audit.md`: Markdown version for quick text sharing.
- `outreach_pitches.md`: Pre-written emails & LinkedIn messages ready to copy-paste.

---

## 🔑 Optional: Enable Deep Gemini AI Reasoning
By default, the agent runs in offline heuristic diagnostic mode. To enable deep LLM reasoning:
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

---

## 📖 Monetization Playbook
Read `MONETIZATION_PLAYBOOK.md` for the complete 7-day blueprint on how to find prospects, deliver audits, and close $150 to $1,500 deals using this tool.
