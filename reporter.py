"""Deliverable Builder Agent: Renders clean Markdown and executive-styled HTML reports."""
from pathlib import Path
from datetime import datetime


class DeliverableBuilderAgent:
    """Builds presentation-ready client deliverables (Markdown and HTML)."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def save_deliverables(self, audit_result: dict, pitches: dict) -> dict:
        """Saves report.md, report.html, and pitches.json to the target client directory."""
        domain = audit_result.get("domain", "target_site").replace(":", "_").replace("/", "_")
        client_dir = self.output_dir / domain
        client_dir.mkdir(parents=True, exist_ok=True)

        md_path = client_dir / "executive_audit.md"
        html_path = client_dir / "executive_audit.html"
        pitches_path = client_dir / "outreach_pitches.md"

        # Generate content
        md_content = self._render_markdown(audit_result, pitches)
        html_content = self._render_html(audit_result)
        pitches_content = self._render_pitches_markdown(audit_result, pitches)

        # Write files
        md_path.write_text(md_content, encoding="utf-8")
        html_path.write_text(html_content, encoding="utf-8")
        pitches_path.write_text(pitches_content, encoding="utf-8")

        return {
            "client_dir": str(client_dir),
            "markdown_report": str(md_path),
            "html_report": str(html_path),
            "pitches_file": str(pitches_path),
        }

    def _render_markdown(self, result: dict, pitches: dict) -> str:
        domain = result.get("domain")
        scores = result.get("scores", {})
        insights = result.get("insights", {})
        raw = result.get("raw_data", {})
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        leaks = insights.get("revenue_leaks", [])
        quick_wins = insights.get("quick_wins", [])
        ai_opp = insights.get("ai_opportunity", {})

        leaks_md = "\n".join(
            f"- **[{leak.get('severity', 'High')}] {leak.get('title')}:** {leak.get('impact')}"
            for leak in leaks
        )
        wins_md = "\n".join(
            f"- **Action:** {w.get('action')}\n  - *Expected Outcome:* {w.get('expected_outcome')}"
            for w in quick_wins
        )

        return f"""# Executive Digital Health & AI Opportunity Audit
**Target Property:** `{domain}` ({result.get('url')})  
**Audit Date:** {now}  
**Overall Performance Score:** **{scores.get('overall', 0)}/100** (Grade: **{scores.get('letter_grade', 'N/A')}**)

---

## 1. Executive Scorecard
| Pillar | Score | Status |
| :--- | :--- | :--- |
| **Overall Health** | **{scores.get('overall', 0)} / 100** | Grade {scores.get('letter_grade', 'N/A')} |
| **SEO & Discoverability** | {scores.get('seo', 0)} / 100 | {'Optimal' if scores.get('seo', 0) >= 80 else 'Attention Required'} |
| **Conversion & Lead Capture** | {scores.get('conversion', 0)} / 100 | {'High Velocity' if scores.get('conversion', 0) >= 80 else 'Friction Detected'} |
| **Performance & Mobile UX** | {scores.get('performance', 0)} / 100 | {f"{raw.get('load_time_ms', 0)} ms response"} |
| **AI & Automation Readiness** | {scores.get('ai_readiness', 0)} / 100 | {'High Upsell Potential' if scores.get('ai_readiness', 0) < 70 else 'Modern'} |

---

## 2. Executive Assessment
{insights.get('executive_summary', 'Comprehensive assessment conducted on client property.')}

---

## 3. High-Impact Revenue Leaks (Identified Bottlenecks)
{leaks_md}

---

## 4. 48-Hour High-ROI Quick Wins
{wins_md}

---

## 5. Strategic AI Automation Opportunity
- **Recommended Solution:** `{ai_opp.get('solution_name')}`
- **Operational Scope:** {ai_opp.get('description')}
- **Projected Revenue Impact:** **{ai_opp.get('estimated_revenue_increase')}**

---

## 6. Technical Diagnostics
- **Page Title:** {raw.get('title', 'N/A')} ({raw.get('title_length', 0)} chars)
- **Meta Description:** {raw.get('meta_description', 'Missing')[:120]}... ({raw.get('meta_description_length', 0)} chars)
- **H1 Elements:** {len(raw.get('h1_texts', []))} found ({', '.join(raw.get('h1_texts', ['None'])[:2])})
- **Mobile Viewport Tag:** {'Configured (Mobile-Friendly)' if raw.get('has_viewport') else 'MISSING (Mobile Penalty)'}
- **Inbound Lead Forms:** {'Active' if raw.get('has_contact_form') else 'No forms detected'}
- **Direct Phone Dial (tel:):** {raw.get('phone_numbers') or 'None detected'}
- **Contact Emails:** {raw.get('emails') or 'None detected'}
- **Live Chat / Conversational Bot:** {raw.get('chat_type') if raw.get('has_chat_widget') else 'None (Immediate Upsell Candidate)'}
- **Detected Technology Stack:** {', '.join(raw.get('detected_tech', [])) or 'Custom / Unknown'}
"""

    def _render_pitches_markdown(self, result: dict, pitches: dict) -> str:
        domain = result.get("domain")
        p1 = pitches.get("value_first_pitch", {})
        p2 = pitches.get("quick_fix_pitch", {})
        p3 = pitches.get("ai_upsell_pitch", {})
        ln = pitches.get("linkedin_connection_note", "")

        return f"""# Personalized Outreach Sequences for `{domain}`

## Angle 1: Value-First Complimentary Audit (Highest Response Rate)
*Best for cold email to the owner or marketing director.*

**Subject:** `{p1.get('subject')}`  
**Recipient:** `{p1.get('recipient_preview')}`

```text
{p1.get('body')}
```

---

## Angle 2: The Specific Flaw & Quick Fix (Direct & Urgent)
*Best for short, punchy outreach.*

**Subject:** `{p2.get('subject')}`

```text
{p2.get('body')}
```

---

## Angle 3: The AI Automation / Chatbot Upgrade Pitch
*Best for selling AI agency services ($500 - $1,500 setup).*

**Subject:** `{p3.get('subject')}`

```text
{p3.get('body')}
```

---

## Angle 4: LinkedIn Connection Note (<300 Characters)
*Copy and paste directly into LinkedIn connection request note:*

```text
{ln}
```
"""

    def _render_html(self, result: dict) -> str:
        domain = result.get("domain")
        scores = result.get("scores", {})
        insights = result.get("insights", {})
        raw = result.get("raw_data", {})
        now = datetime.now().strftime("%B %d, %Y")

        overall = scores.get("overall", 70)
        grade = scores.get("letter_grade", "B")

        # Color based on score
        if overall >= 80:
            score_color = "#10B981"  # Emerald
        elif overall >= 60:
            score_color = "#F59E0B"  # Amber
        else:
            score_color = "#EF4444"  # Red

        leaks_html = "".join(
            f"""
            <div class="card leak-card">
                <div class="leak-header">
                    <span class="badge badge-{leak.get('severity', 'high').lower()}">{leak.get('severity', 'High')} Impact</span>
                    <h4>{leak.get('title')}</h4>
                </div>
                <p>{leak.get('impact')}</p>
            </div>
            """
            for leak in insights.get("revenue_leaks", [])
        )

        wins_html = "".join(
            f"""
            <div class="card win-card">
                <h4>🎯 {win.get('action')}</h4>
                <div class="win-meta"><strong>Expected ROI:</strong> {win.get('expected_outcome')}</div>
            </div>
            """
            for win in insights.get("quick_wins", [])
        )

        ai_opp = insights.get("ai_opportunity", {})

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Digital Audit: {domain}</title>
    <style>
        :root {{
            --bg: #0B0F19;
            --surface: #111827;
            --border: #1F2937;
            --text-main: #F3F4F6;
            --text-muted: #9CA3AF;
            --accent: #3B82F6;
            --emerald: #10B981;
            --amber: #F59E0B;
            --rose: #EF4444;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background-color: var(--bg); color: var(--text-main); line-height: 1.6; padding: 40px 20px; }}
        .container {{ max-width: 950px; margin: 0 auto; }}
        header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 24px; margin-bottom: 36px; }}
        .logo-badge {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(59, 130, 246, 0.1); color: var(--accent); padding: 6px 14px; border-radius: 9999px; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; }}
        .audit-title {{ font-size: 32px; font-weight: 800; margin-top: 12px; }}
        .audit-meta {{ color: var(--text-muted); font-size: 14px; margin-top: 4px; }}
        .score-hero {{ display: flex; align-items: center; justify-content: center; background: radial-gradient(circle at center, rgba(31, 41, 55, 0.8), rgba(17, 24, 39, 0.9)); border: 1px solid var(--border); border-radius: 16px; padding: 32px; margin-bottom: 36px; text-align: center; }}
        .score-circle {{ width: 130px; height: 130px; border-radius: 50%; border: 6px solid {score_color}; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-right: 36px; flex-shrink: 0; }}
        .score-num {{ font-size: 42px; font-weight: 900; line-height: 1; color: {score_color}; }}
        .score-denom {{ font-size: 13px; color: var(--text-muted); font-weight: 600; }}
        .score-info h2 {{ font-size: 24px; margin-bottom: 8px; }}
        .score-info p {{ color: var(--text-muted); max-width: 580px; font-size: 15px; }}
        .grid-4 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 36px; }}
        .metric-tile {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }}
        .metric-title {{ font-size: 13px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }}
        .metric-val {{ font-size: 28px; font-weight: 800; margin-top: 6px; }}
        .bar-bg {{ background: #1F2937; height: 6px; border-radius: 3px; margin-top: 12px; overflow: hidden; }}
        .bar-fill {{ height: 100%; border-radius: 3px; }}
        .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 24px; margin-bottom: 20px; }}
        .card h3 {{ font-size: 18px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
        .leak-card {{ border-left: 4px solid var(--rose); }}
        .leak-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }}
        .badge {{ font-size: 11px; padding: 3px 8px; border-radius: 6px; font-weight: 700; text-transform: uppercase; }}
        .badge-critical {{ background: rgba(239, 68, 68, 0.2); color: var(--rose); }}
        .badge-high {{ background: rgba(245, 158, 11, 0.2); color: var(--amber); }}
        .badge-medium {{ background: rgba(59, 130, 246, 0.2); color: var(--accent); }}
        .win-card {{ border-left: 4px solid var(--emerald); margin-bottom: 12px; padding: 18px 24px; }}
        .win-meta {{ font-size: 13px; color: var(--emerald); margin-top: 6px; }}
        .ai-card {{ background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(16, 185, 129, 0.08)); border: 1px solid rgba(59, 130, 246, 0.3); }}
        .ai-tag {{ color: var(--accent); font-weight: 700; font-size: 14px; margin-bottom: 6px; }}
        .tech-tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
        .tech-pill {{ background: #1F2937; color: #D1D5DB; font-size: 12px; padding: 4px 10px; border-radius: 6px; }}
        footer {{ text-align: center; color: var(--text-muted); font-size: 13px; border-top: 1px solid var(--border); padding-top: 24px; margin-top: 40px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <span class="logo-badge">⚡ ClientForge AI Diagnostics</span>
                <h1 class="audit-title">Digital Health & Revenue Audit</h1>
                <div class="audit-meta">Domain: <strong>{domain}</strong> | Audited on {now}</div>
            </div>
            <div>
                <span class="badge" style="background:#1F2937; color:#9CA3AF; padding:8px 16px; font-size:13px;">Verified Audit</span>
            </div>
        </header>

        <section class="score-hero">
            <div class="score-circle">
                <span class="score-num">{overall}</span>
                <span class="score-denom">/ 100</span>
            </div>
            <div class="score-info">
                <h2>Health Rating: Grade {grade}</h2>
                <p>{insights.get('executive_summary')}</p>
            </div>
        </section>

        <section class="grid-4">
            <div class="metric-tile">
                <div class="metric-title">Search & SEO</div>
                <div class="metric-val">{scores.get('seo', 0)}%</div>
                <div class="bar-bg"><div class="bar-fill" style="width: {scores.get('seo', 0)}%; background: var(--accent);"></div></div>
            </div>
            <div class="metric-tile">
                <div class="metric-title">Lead Conversion</div>
                <div class="metric-val">{scores.get('conversion', 0)}%</div>
                <div class="bar-bg"><div class="bar-fill" style="width: {scores.get('conversion', 0)}%; background: var(--emerald);"></div></div>
            </div>
            <div class="metric-tile">
                <div class="metric-title">Mobile & Speed</div>
                <div class="metric-val">{scores.get('performance', 0)}%</div>
                <div class="bar-bg"><div class="bar-fill" style="width: {scores.get('performance', 0)}%; background: var(--amber);"></div></div>
            </div>
            <div class="metric-tile">
                <div class="metric-title">AI Readiness</div>
                <div class="metric-val">{scores.get('ai_readiness', 0)}%</div>
                <div class="bar-bg"><div class="bar-fill" style="width: {scores.get('ai_readiness', 0)}%; background: #8B5CF6;"></div></div>
            </div>
        </section>

        <section>
            <h2 style="margin-bottom: 16px; font-size: 20px;">🚨 Revenue Leaks Detected</h2>
            {leaks_html}
        </section>

        <section style="margin-top: 32px;">
            <h2 style="margin-bottom: 16px; font-size: 20px;">⚡ 48-Hour High-ROI Quick Wins</h2>
            {wins_html}
        </section>

        <section style="margin-top: 32px;">
            <div class="card ai-card">
                <div class="ai-tag">✨ Recommended High-ROI AI Agent Solution</div>
                <h3 style="margin-bottom: 8px; font-size: 22px;">{ai_opp.get('solution_name')}</h3>
                <p style="color: #D1D5DB; margin-bottom: 16px;">{ai_opp.get('description')}</p>
                <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid var(--emerald); color: var(--emerald); padding: 12px 18px; border-radius: 8px; font-weight: 600; display: inline-block;">
                    Expected Impact: {ai_opp.get('estimated_revenue_increase')}
                </div>
            </div>
        </section>

        <section style="margin-top: 32px;">
            <div class="card">
                <h3>🛠️ Technical Environment Summary</h3>
                <div style="font-size: 14px; color: var(--text-muted); line-height: 2;">
                    <div>• <strong>Response Latency:</strong> {raw.get('load_time_ms', 0)} ms</div>
                    <div>• <strong>Mobile Viewport:</strong> {'Configured' if raw.get('has_viewport') else 'Missing'}</div>
                    <div>• <strong>Forms Present:</strong> {'Yes' if raw.get('has_contact_form') else 'No'}</div>
                    <div>• <strong>Live Chat / AI Bot:</strong> {raw.get('chat_type') if raw.get('has_chat_widget') else 'Not implemented'}</div>
                </div>
                <div class="tech-tags">
                    {''.join(f'<span class="tech-pill">{t}</span>' for t in raw.get('detected_tech', ['Custom Stack']))}
                </div>
            </div>
        </section>

        <footer>
            Generated automatically by ClientForge AI Revenue Agent Suite • Confidential Client Briefing
        </footer>
    </div>
</body>
</html>
"""
