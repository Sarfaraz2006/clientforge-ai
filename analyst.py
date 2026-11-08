"""Analyst Agent: Evaluates site findings, calculates scores, and identifies high-value revenue opportunities."""
import json
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    WEIGHT_SEO,
    WEIGHT_CONVERSION,
    WEIGHT_PERFORMANCE,
    WEIGHT_AI_READINESS,
)

# Optional Gemini import
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


class AuditAnalystAgent:
    """Analyzes site signals to produce scorecards, revenue leak diagnoses, and upsell roadmaps."""

    def __init__(self, use_ai: bool = True):
        self.use_ai = use_ai and bool(GEMINI_API_KEY) and HAS_GENAI
        if self.use_ai:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        else:
            self.client = None

    def analyze(self, data: dict) -> dict:
        """Processes crawler data and generates a full audit analysis."""
        scores = self._calculate_scores(data)

        if self.use_ai:
            try:
                ai_insights = self._generate_ai_insights(data, scores)
            except Exception as e:
                ai_insights = self._heuristic_fallback(data, scores, fallback_reason=str(e))
        else:
            ai_insights = self._heuristic_fallback(data, scores)

        return {
            "domain": data.get("domain"),
            "url": data.get("url"),
            "scores": scores,
            "insights": ai_insights,
            "raw_data": data,
        }

    def _calculate_scores(self, data: dict) -> dict:
        """Calculates four 0-100 pillar scores and an overall composite score."""
        if not data.get("success"):
            return {
                "overall": 0,
                "seo": 0,
                "conversion": 0,
                "performance": 0,
                "ai_readiness": 0,
                "letter_grade": "F",
            }

        # 1. SEO Score (0-100)
        seo = 0
        if 20 <= data.get("title_length", 0) <= 65:
            seo += 25
        elif data.get("title_length", 0) > 0:
            seo += 15

        if 50 <= data.get("meta_description_length", 0) <= 165:
            seo += 25
        elif data.get("meta_description_length", 0) > 0:
            seo += 15

        if data.get("h1_count", 0) == 1:
            seo += 20
        elif data.get("h1_count", 0) > 1:
            seo += 10  # Multiple H1s is suboptimal

        if data.get("og_title") and data.get("og_description"):
            seo += 15
        elif data.get("og_title") or data.get("og_description"):
            seo += 8

        if data.get("canonical_url"):
            seo += 15

        # 2. Conversion & Lead Capture (0-100)
        conversion = 0
        if data.get("has_contact_form"):
            conversion += 30
        if data.get("has_tel_link"):
            conversion += 25
        if data.get("has_mailto_link"):
            conversion += 15
        if data.get("has_chat_widget"):
            conversion += 20
        if data.get("social_links"):
            conversion += 10

        # 3. Performance & Mobile UX (0-100)
        perf = 0
        if data.get("has_viewport"):
            perf += 35

        load_ms = data.get("load_time_ms", 1000)
        if load_ms < 600:
            perf += 35
        elif load_ms < 1500:
            perf += 25
        elif load_ms < 3000:
            perf += 15
        else:
            perf += 5

        total_imgs = data.get("image_count", 0)
        missing_alt = data.get("images_missing_alt", 0)
        if total_imgs == 0 or (missing_alt / max(total_imgs, 1)) < 0.2:
            perf += 30
        elif (missing_alt / max(total_imgs, 1)) < 0.5:
            perf += 15

        # 4. AI & Automation Readiness (0-100)
        ai_ready = 0
        if data.get("has_chat_widget"):
            ai_ready += 40
        else:
            ai_ready += 10  # Prime candidate for AI Chatbot implementation

        if any(tech in data.get("detected_tech", []) for tech in ["Next.js / React", "Shopify", "Webflow"]):
            ai_ready += 30
        else:
            ai_ready += 15

        if data.get("has_contact_form") and not data.get("has_chat_widget"):
            ai_ready += 30  # Has inbound intent, desperately needs automated triage

        # Overall composite
        overall = int(
            (seo * WEIGHT_SEO)
            + (conversion * WEIGHT_CONVERSION)
            + (perf * WEIGHT_PERFORMANCE)
            + (ai_ready * WEIGHT_AI_READINESS)
        )
        overall = max(10, min(98, overall))

        # Letter grade
        if overall >= 88:
            grade = "A"
        elif overall >= 75:
            grade = "B"
        elif overall >= 60:
            grade = "C"
        elif overall >= 45:
            grade = "D"
        else:
            grade = "F"

        return {
            "overall": overall,
            "seo": min(100, seo),
            "conversion": min(100, conversion),
            "performance": min(100, perf),
            "ai_readiness": min(100, ai_ready),
            "letter_grade": grade,
        }

    def _generate_ai_insights(self, data: dict, scores: dict) -> dict:
        """Invokes Gemini model for high-fidelity audit analysis."""
        prompt = f"""
You are an elite Digital Growth & AI Automation Consultant conducting an executive audit for the business at {data['url']}.

Website Data:
- Domain: {data['domain']}
- Title: {data['title']} (Length: {data['title_length']})
- Meta Description: {data['meta_description']} (Length: {data['meta_description_length']})
- H1 Headings: {data['h1_texts']} (Count: {data['h1_count']})
- Load Time: {data['load_time_ms']} ms
- Mobile Viewport Present: {data['has_viewport']}
- Images: {data['image_count']} total, {data['images_missing_alt']} missing alt text
- Contact Form: {data['has_contact_form']}
- Phone / Tel Link: {data['has_tel_link']} (Phones: {data['phone_numbers']})
- Email / Mailto Link: {data['has_mailto_link']} (Emails: {data['emails']})
- Live Chat / AI Bot: {data['has_chat_widget']} (Type: {data['chat_type']})
- Tech Stack: {data['detected_tech']}
- Content Sample: {data['text_sample']}

Scores Calculated:
- Overall: {scores['overall']}/100 (Grade: {scores['letter_grade']})
- SEO: {scores['seo']}/100
- Conversion & Lead Capture: {scores['conversion']}/100
- Performance & Mobile: {scores['performance']}/100
- AI Readiness: {scores['ai_readiness']}/100

Produce a JSON response with this exact structure:
{{
  "executive_summary": "A concise 2-sentence assessment highlighting the company's core strengths and primary digital bottleneck.",
  "revenue_leaks": [
    {{"title": "Short bottleneck title", "impact": "Why this loses them revenue or customers", "severity": "High/Critical/Medium"}},
    {{"title": "...", "impact": "...", "severity": "..."}},
    {{"title": "...", "impact": "...", "severity": "..."}}
  ],
  "quick_wins": [
    {{"action": "Specific fix they can do in 48 hours", "expected_outcome": "Immediate benefit"}},
    {{"action": "...", "expected_outcome": "..."}},
    {{"action": "...", "expected_outcome": "..."}}
  ],
  "ai_opportunity": {{
    "solution_name": "Name of the high-ROI AI Automation or Agent",
    "description": "How an AI agent (e.g. 24/7 lead qualifier, booking bot, or automated response pipeline) will generate direct ROI for them.",
    "estimated_revenue_increase": "Realistic percentage or value impact"
  }}
}}
Return ONLY valid JSON.
"""
        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return json.loads(response.text)

    def _heuristic_fallback(self, data: dict, scores: dict, fallback_reason: str = None) -> dict:
        """Deterministic intelligence engine when API key is not present."""
        leaks = []
        quick_wins = []

        # Check chat / instant response
        if not data.get("has_chat_widget"):
            leaks.append({
                "title": "Absence of 24/7 Instant Lead Capture / Live Chat",
                "impact": "Over 68% of modern B2B/B2C visitors leave a website without converting if their initial question is not answered within 5 minutes. High bounce rate during off-hours.",
                "severity": "Critical",
            })
            quick_wins.append({
                "action": "Deploy an AI-driven 24/7 conversational lead qualification assistant to capture visitor intent immediately.",
                "expected_outcome": "25% to 40% immediate uplift in captured inbound leads.",
            })
        else:
            leaks.append({
                "title": f"Static Chat Widget ({data.get('chat_type')}) Missing Autonomous AI Reasoning",
                "impact": "Rule-based chats frustrate prospects with rigid decision trees instead of understanding natural customer inquiries.",
                "severity": "Medium",
            })

        # Check forms & contact mechanisms
        if not data.get("has_contact_form") and not data.get("has_tel_link"):
            leaks.append({
                "title": "Friction in Customer Contact Architecture",
                "impact": "Visitors cannot easily initiate an inquiry or booking directly on the homepage, causing drop-offs to competitors.",
                "severity": "Critical",
            })
        elif not data.get("has_tel_link"):
            leaks.append({
                "title": "Lack of Direct Mobile Click-to-Call Functionality",
                "impact": "Mobile users cannot tap to dial instantly, creating friction for high-intent emergency or immediate buyers.",
                "severity": "High",
            })

        # Check SEO / Meta
        if data.get("meta_description_length", 0) < 50:
            leaks.append({
                "title": "Missing or Truncated Meta Search Snippets",
                "impact": "Google search result listings appear unoptimized or auto-generated, depressing organic Click-Through Rate (CTR).",
                "severity": "High",
            })
            quick_wins.append({
                "action": "Rewrite homepage meta title and description with high-converting target keywords and clear value proposition.",
                "expected_outcome": "15-30% improvement in organic search click-through rate.",
            })

        # Check Heading Structure
        if data.get("h1_count", 0) == 0:
            quick_wins.append({
                "action": "Add a prominent H1 headline clearly stating what you do, who you serve, and your primary benefit.",
                "expected_outcome": "Clarifies value proposition within the first 3 seconds of visitor landing.",
            })
        elif data.get("h1_count", 0) > 1:
            quick_wins.append({
                "action": "Consolidate multiple H1 tags into a single clean hierarchy (1x H1, followed by structured H2/H3s).",
                "expected_outcome": "Strengthens primary keyword signals for search engine crawlers.",
            })

        # Missing alt tags
        if data.get("images_missing_alt", 0) > 0:
            quick_wins.append({
                "action": f"Add descriptive keyword-rich alt tags to {data.get('images_missing_alt')} images lacking accessibility tags.",
                "expected_outcome": "Improves Google Image search indexation and screen-reader accessibility.",
            })

        # Ensure we have at least 3 of each
        while len(leaks) < 3:
            leaks.append({
                "title": "Suboptimal Post-Click Conversion Funnel",
                "impact": "Traffic landing on the website lacks secondary lead magnets or automated email nurturing sequences.",
                "severity": "Medium",
            })
        while len(quick_wins) < 3:
            quick_wins.append({
                "action": "Add an automated appointment booking calendar link (e.g. Cal.com/Calendly) above the fold.",
                "expected_outcome": "Removes back-and-forth friction in scheduling sales calls.",
            })

        ai_opp = {
            "solution_name": "Autonomous 24/7 AI Lead Qualifier & Appointment Booking Agent",
            "description": f"An intelligent custom-trained agent integrated into {data['domain']} that answers visitor questions, handles objection handling, qualifies customer budget, and books meetings directly into your calendar.",
            "estimated_revenue_increase": "+30% to +50% in qualified inbound meetings booked without increasing ad spend.",
        }

        exec_summary = (
            f"The digital presence for {data['domain']} establishes a foundational baseline with a composite score of "
            f"{scores['overall']}/100 (Grade {scores['letter_grade']}). However, significant revenue leakage exists due to "
            f"unaddressed conversion friction and missed 24/7 autonomous engagement opportunities."
        )

        return {
            "executive_summary": exec_summary,
            "revenue_leaks": leaks[:3],
            "quick_wins": quick_wins[:3],
            "ai_opportunity": ai_opp,
            "engine": "heuristic_offline" if not fallback_reason else f"fallback_{fallback_reason[:30]}",
        }
