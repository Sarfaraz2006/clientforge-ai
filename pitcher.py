"""Outreach Strategist Agent: Crafts high-converting, value-first personalized pitch templates."""


class OutreachStrategistAgent:
    """Generates multi-angle outreach emails and LinkedIn messages grounded in audit findings."""

    def generate_pitches(self, audit_result: dict, sender_name: str = "Your Name") -> dict:
        """Produces 3 customized email angles and 1 LinkedIn connection note."""
        domain = audit_result.get("domain", "your company")
        scores = audit_result.get("scores", {})
        insights = audit_result.get("insights", {})
        raw = audit_result.get("raw_data", {})

        leaks = insights.get("revenue_leaks", [])
        top_leak = leaks[0]["title"] if leaks else "conversion friction points"
        top_leak_impact = leaks[0]["impact"] if leaks else "leads dropping off before reaching your team"

        ai_opp = insights.get("ai_opportunity", {})
        solution_name = ai_opp.get("solution_name", "Autonomous AI Assistant")

        emails_found = raw.get("emails", [])
        target_email = emails_found[0] if emails_found else f"contact@{domain}"

        # Angle 1: Value-First Complimentary Audit Gift
        email_value_first = {
            "subject": f"Quick question regarding {domain}'s conversion flow (+ free audit)",
            "recipient_preview": target_email,
            "body": f"""Hi {domain} Team,

I recently analyzed the digital footprint and user experience for {domain} while researching leaders in your space.

Overall, your site foundation looks solid (we rated your technical baseline at {scores.get('overall', 72)}/100). However, our audit bot flagged a couple of critical revenue leaks that are likely costing you qualified inquiries:

1. {top_leak}: {top_leak_impact}
2. Missing 24/7 autonomous engagement for high-intent visitors who browse outside standard business hours.

I went ahead and compiled a full 1-page Executive Audit Report breaking down all 4 key pillars (SEO, Conversion Architecture, Mobile UX, and AI Automation Readiness) with specific 48-hour quick wins.

I've attached the report here for your team completely free — no strings attached.

If you'd like a quick 10-minute walkthrough on how we typically fix these bottlenecks and implement a 24/7 lead capture agent, feel free to grab a time here: [Your Calendar Link]

Best regards,

{sender_name}
Digital Growth & Automation Consultant
[Your Phone / Portfolio]
""",
        }

        # Angle 2: The Specific Flaw & Quick Fix (Direct & Urgent)
        email_quick_fix = {
            "subject": f"Noticed a small friction point on {domain}",
            "recipient_preview": target_email,
            "body": f"""Hi there,

Was just browsing {domain} and noticed something that might be causing you to lose high-intent prospects:

Specifically: {top_leak}. 
Impact: {top_leak_impact}

We recently helped another brand resolve this exact issue, which resulted in a 32% increase in captured inquiries within the first 14 days.

We put together a complimentary teardown showing the exact code & structural adjustments needed to resolve it.

Would you be open to taking a look at the short report? Happy to email it right over if it helps.

Best,

{sender_name}
[Your Agency / Service Name]
""",
        }

        # Angle 3: The AI Automation / Chatbot Upgrade Pitch
        email_ai_upsell = {
            "subject": f"Idea for {domain}: Adding a 24/7 booking agent",
            "recipient_preview": target_email,
            "body": f"""Hi {domain} Leadership,

Did you know that over 65% of high-intent visitors research services in the evening or weekends when your team is offline?

Right now, {domain} relies primarily on standard static contact points. Visitors who want an immediate answer or want to book an appointment right away often bounce to whichever competitor answers first.

We specialize in deploying **{solution_name}**:
- An intelligent assistant trained on your exact business data
- Instantly answers customer inquiries 24/7
- Qualifies budget and schedules appointments directly into your calendar

Our clients typically see a 30% to 50% increase in booked appointments without spending an extra dollar on traffic.

We already generated an automated audit of your site showing where this agent would deliver the highest immediate ROI. 

Would you be open to a 3-minute video demo of how this would look on {domain}?

Cheers,

{sender_name}
AI Automation Specialist
""",
        }

        # Angle 4: LinkedIn Connection Note (<300 chars)
        linkedin_note = (
            f"Hi! Came across {domain} and noticed your team is doing great work. "
            f"Ran a quick audit on your conversion pipeline and found 2 quick wins to boost lead capture. "
            f"Would love to connect and share the report if helpful!"
        )

        return {
            "value_first_pitch": email_value_first,
            "quick_fix_pitch": email_quick_fix,
            "ai_upsell_pitch": email_ai_upsell,
            "linkedin_connection_note": linkedin_note,
        }
