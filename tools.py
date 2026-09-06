import requests
import re
from datetime import datetime
from urllib.parse import urlparse
from ddgs import DDGS


# =========================================================
# WEATHER
# =========================================================

def get_weather(city):

    try:

        url = f"https://wttr.in/{city}?format=3"

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code == 200:

            return response.text.strip()

        return "Weather service unavailable."

    except Exception as e:

        return f"Weather error: {e}"


# =========================================================
# CURRENT DATE / TIME
# =========================================================

def get_current_time():

    try:

        now = datetime.now()

        return now.strftime(
            "%A, %d %B %Y • %I:%M:%S %p"
        )

    except Exception as e:

        return f"Time error: {e}"


# =========================================================
# CALCULATOR
# =========================================================

def calculate(expression):

    try:

        expression = expression.lower()

        expression = expression.replace(
            "x",
            "*"
        )

        expression = expression.replace(
            "×",
            "*"
        )

        expression = expression.replace(
            "÷",
            "/"
        )

        # Allow only basic mathematical characters
        if not re.match(
            r"^[0-9+\-*/().%\s]+$",
            expression
        ):

            return "Invalid mathematical expression."

        result = eval(
            expression,
            {
                "__builtins__": None
            },
            {}
        )

        return result

    except ZeroDivisionError:

        return "Cannot divide by zero."

    except Exception:

        return "Unable to calculate that expression."


# =========================================================
# WEB SEARCH
# =========================================================

def web_search(query):

    try:

        # Remove common commands
        clean_query = re.sub(

            r"search\s+(the\s+)?web\s*(for)?",
            "",
            query,
            flags=re.IGNORECASE

        ).strip()

        if not clean_query:

            clean_query = query

        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(

                clean_query,

                max_results=5

            )

            for item in search_results:

                title = item.get(
                    "title",
                    "Untitled"
                )

                body = item.get(
                    "body",
                    ""
                )

                href = item.get(
                    "href",
                    ""
                )

                results.append(

                    f"### {title}\n"
                    f"{body}\n"
                    f"🔗 {href}"

                )

        if not results:

            return "No web results found."

        return "\n\n".join(
            results
        )

    except Exception as e:

        return f"Web search error: {e}"


# =========================================================
# URL SECURITY ANALYSIS
# =========================================================

def cyber_url_scan(url):

    """
    Basic defensive URL analysis.

    This does NOT exploit the target.
    It only inspects the URL structure.
    """

    try:

        url = url.strip()

        if not url.startswith(
            ("http://", "https://")
        ):

            url = "https://" + url

        parsed = urlparse(url)

        hostname = parsed.hostname

        if not hostname:

            return "❌ Invalid URL."

        findings = []

        # -------------------------------------------------
        # HTTPS
        # -------------------------------------------------

        if parsed.scheme != "https":

            findings.append(
                "⚠️ URL is not using HTTPS."
            )

        else:

            findings.append(
                "✅ HTTPS is enabled."
            )

        # -------------------------------------------------
        # IP ADDRESS
        # -------------------------------------------------

        if re.match(
            r"^\d{1,3}(\.\d{1,3}){3}$",
            hostname
        ):

            findings.append(
                "⚠️ Host appears to use a direct IP address."
            )

        # -------------------------------------------------
        # SUSPICIOUS CHARACTERS
        # -------------------------------------------------

        suspicious_chars = [

            "@",
            "%40",
            "%2f",
            "%2F"

        ]

        for char in suspicious_chars:

            if char in url:

                findings.append(
                    f"⚠️ Suspicious URL character/pattern detected: `{char}`"
                )

        # -------------------------------------------------
        # SUBDOMAIN COUNT
        # -------------------------------------------------

        parts = hostname.split(".")

        if len(parts) >= 4:

            findings.append(
                "⚠️ URL contains multiple subdomains."
            )

        # -------------------------------------------------
        # LONG URL
        # -------------------------------------------------

        if len(url) > 150:

            findings.append(
                "⚠️ URL is unusually long."
            )

        else:

            findings.append(
                "✅ URL length looks normal."
            )

        # -------------------------------------------------
        # PUNYCODE
        # -------------------------------------------------

        if "xn--" in hostname.lower():

            findings.append(
                "⚠️ Punycode domain detected. "
                "Verify the domain carefully."
            )

        # -------------------------------------------------
        # FINAL REPORT
        # -------------------------------------------------

        report = [

            "🛡️ **NEXUS URL Security Analysis**",

            "",

            f"**URL:** `{url}`",

            f"**Host:** `{hostname}`",

            "",

            "### Findings"

        ]

        report.extend(

            f"- {finding}"

            for finding in findings

        )

        report.extend([

            "",

            "### Recommendation",

            "Do not enter credentials or sensitive "
            "information unless the domain is trusted "
            "and independently verified."

        ])

        return "\n".join(report)

    except Exception as e:

        return f"Cybersecurity analysis error: {e}"


# =========================================================
# HTTP SECURITY HEADERS
# =========================================================

def check_security_headers(url):

    try:

        if not url.startswith(
            ("http://", "https://")
        ):

            url = "https://" + url

        response = requests.get(

            url,

            timeout=10,

            allow_redirects=True,

            headers={

                "User-Agent":
                "NEXUS-AI-Security-Scanner/1.0"

            }

        )

        headers = response.headers

        security_headers = {

            "Strict-Transport-Security":
                "HSTS",

            "Content-Security-Policy":
                "CSP",

            "X-Content-Type-Options":
                "X-Content-Type-Options",

            "X-Frame-Options":
                "X-Frame-Options",

            "Referrer-Policy":
                "Referrer-Policy",

            "Permissions-Policy":
                "Permissions-Policy"

        }

        report = [

            "🛡️ **HTTP Security Header Analysis**",

            "",

            f"**URL:** `{response.url}`",

            f"**Status:** `{response.status_code}`",

            "",

            "### Security Headers"

        ]

        for header, label in security_headers.items():

            if header in headers:

                report.append(

                    f"✅ **{label}** — Present"

                )

            else:

                report.append(

                    f"⚠️ **{label}** — Missing"

                )

        return "\n".join(report)

    except Exception as e:

        return f"Security header check error: {e}"