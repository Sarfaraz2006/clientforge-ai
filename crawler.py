"""Collector Agent: Deep Website and Technical Inspector."""
import time
import re
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT, USER_AGENT


class SiteInspector:
    """Crawls and extracts key technical, SEO, and conversion signals from a target website."""

    def __init__(self, url: str):
        self.raw_url = url
        self.url = self._normalize_url(url)
        self.domain = urlparse(self.url).netloc
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def _normalize_url(self, url: str) -> str:
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        return url

    def inspect(self) -> dict:
        """Executes full site inspection and returns structured findings."""
        start_time = time.time()
        result = {
            "url": self.url,
            "domain": self.domain,
            "success": False,
            "status_code": None,
            "load_time_ms": 0,
            "error": None,
            # SEO signals
            "title": "",
            "title_length": 0,
            "meta_description": "",
            "meta_description_length": 0,
            "has_viewport": False,
            "canonical_url": "",
            "og_title": "",
            "og_description": "",
            "og_image": "",
            # Content & structure
            "h1_count": 0,
            "h1_texts": [],
            "h2_count": 0,
            "h3_count": 0,
            "word_count": 0,
            "text_sample": "",
            # Media & performance
            "image_count": 0,
            "images_missing_alt": 0,
            "script_count": 0,
            "css_count": 0,
            # Conversion & Lead Capture
            "has_contact_form": False,
            "has_tel_link": False,
            "phone_numbers": [],
            "has_mailto_link": False,
            "emails": [],
            "has_chat_widget": False,
            "chat_type": None,
            # Social links
            "social_links": {},
            # Tech stack signals
            "detected_tech": [],
        }

        try:
            resp = self.session.get(self.url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            result["load_time_ms"] = int((time.time() - start_time) * 1000)
            result["status_code"] = resp.status_code
            result["final_url"] = resp.url

            if resp.status_code >= 400:
                result["error"] = f"HTTP Error {resp.status_code}"
                return result

            result["success"] = True
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")

            # 1. SEO analysis
            title_tag = soup.find("title")
            if title_tag and title_tag.string:
                result["title"] = title_tag.string.strip()
                result["title_length"] = len(result["title"])

            meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
            if meta_desc and meta_desc.get("content"):
                result["meta_description"] = meta_desc["content"].strip()
                result["meta_description_length"] = len(result["meta_description"])

            viewport = soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})
            result["has_viewport"] = bool(viewport and viewport.get("content"))

            canonical = soup.find("link", attrs={"rel": re.compile(r"^canonical$", re.I)})
            if canonical and canonical.get("href"):
                result["canonical_url"] = canonical["href"]

            # OpenGraph
            og_t = soup.find("meta", property="og:title")
            if og_t and og_t.get("content"):
                result["og_title"] = og_t["content"].strip()

            og_d = soup.find("meta", property="og:description")
            if og_d and og_d.get("content"):
                result["og_description"] = og_d["content"].strip()

            og_img = soup.find("meta", property="og:image")
            if og_img and og_img.get("content"):
                result["og_image"] = og_img["content"].strip()

            # 2. Heading hierarchy
            h1s = soup.find_all("h1")
            result["h1_count"] = len(h1s)
            result["h1_texts"] = [h.get_text(strip=True) for h in h1s[:5]]

            result["h2_count"] = len(soup.find_all("h2"))
            result["h3_count"] = len(soup.find_all("h3"))

            # 3. Content Analysis
            body_text = soup.get_text(separator=" ", strip=True)
            words = [w for w in body_text.split() if len(w) > 1]
            result["word_count"] = len(words)
            result["text_sample"] = " ".join(words[:150])

            # 4. Images & performance signals
            imgs = soup.find_all("img")
            result["image_count"] = len(imgs)
            result["images_missing_alt"] = sum(1 for img in imgs if not img.get("alt"))

            result["script_count"] = len(soup.find_all("script"))
            result["css_count"] = len(soup.find_all("link", rel="stylesheet"))

            # 5. Conversion & Lead Capture signals
            forms = soup.find_all("form")
            result["has_contact_form"] = len(forms) > 0

            # Phone & email discovery
            links = soup.find_all("a", href=True)
            phones = set()
            emails = set()
            for a in links:
                href = a["href"].strip()
                if href.startswith("tel:"):
                    phones.add(href.replace("tel:", "").strip())
                elif href.startswith("mailto:"):
                    clean_email = href.replace("mailto:", "").split("?")[0].strip()
                    emails.add(clean_email)

            # Regex search for emails in page if not in links
            if not emails:
                found_emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html)
                for e in set(found_emails[:3]):
                    if not any(ext in e.lower() for ext in [".png", ".jpg", ".webp", ".svg"]):
                        emails.add(e)

            result["has_tel_link"] = len(phones) > 0
            result["phone_numbers"] = list(phones)[:3]
            result["has_mailto_link"] = len(emails) > 0
            result["emails"] = list(emails)[:3]

            # Chat widget detection
            chat_indicators = {
                "Intercom": ["intercomSettings", "widget.intercom.io"],
                "Drift": ["driftt.com", "drift.load"],
                "Zendesk": ["zopim", "zendesk"],
                "Tidio": ["tidio.co", "tidioChatApi"],
                "HubSpot Chat": ["js.hs-scripts.com", "hubspot-messages"],
                "Crisp": ["client.crisp.chat"],
                "WhatsApp": ["api.whatsapp.com", "wa.me"],
                "LiveChat": ["livechatinc.com"],
            }
            raw_lower = html.lower()
            for chat_name, patterns in chat_indicators.items():
                if any(p.lower() in raw_lower for p in patterns):
                    result["has_chat_widget"] = True
                    result["chat_type"] = chat_name
                    break

            # 6. Social media presence
            social_domains = {
                "linkedin": "linkedin.com",
                "twitter": "twitter.com",
                "x": "x.com",
                "facebook": "facebook.com",
                "instagram": "instagram.com",
                "youtube": "youtube.com",
                "github": "github.com",
            }
            for a in links:
                href = a["href"].lower()
                for net, dom in social_domains.items():
                    if dom in href and net not in result["social_links"]:
                        result["social_links"][net] = a["href"]

            # 7. Technology stack detection
            tech_stack = []
            if "wp-content" in html or "wp-includes" in html:
                tech_stack.append("WordPress")
            if "cdn.shopify.com" in html or "Shopify.theme" in html:
                tech_stack.append("Shopify")
            if "webflow" in html:
                tech_stack.append("Webflow")
            if "__next" in html or "_next/static" in html:
                tech_stack.append("Next.js / React")
            if "googletagmanager.com" in html or "gtag(" in html:
                tech_stack.append("Google Analytics / Tag Manager")
            if "connect.facebook.net" in html:
                tech_stack.append("Meta Pixel")
            if "stripe.com" in html:
                tech_stack.append("Stripe")
            if "tailwind" in html:
                tech_stack.append("Tailwind CSS")

            result["detected_tech"] = tech_stack

        except requests.exceptions.RequestException as e:
            result["error"] = str(e)
            result["load_time_ms"] = int((time.time() - start_time) * 1000)

        return result
