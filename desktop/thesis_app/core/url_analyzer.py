"""URL -> Phishing Websites feature vector.

Computes the 30 attributes of the "Phishing Websites" dataset from a URL
string, following the indicators of Mohammad, Thabtah & McCluskey (2012).

Important: the copy of the dataset shipped with the thesis stores many
attributes with the opposite sign to the UCI ``.arff`` file, so all values here
are produced in *this dataset's* encoding (see ``feature_meta.PHISHING_CODING``
and the note in ANALYSIS_REPORT.md). Emitting the documented sign instead
would invert the classifier.

Attributes that in the original study required fetching the page cannot be
derived from a URL string; they take the dataset's majority (neutral) value so
they contribute no spurious evidence either way. Everything that *can* be
derived from the URL — plus a small table of well-known registrable domains for
the trust indicators — is computed for real.
"""
from __future__ import annotations

import re
from urllib.parse import urlparse

from .feature_meta import PHISHING_CODING, PHISHING_FEATURES, PHISHING_NEUTRAL

TRUSTED_DOMAINS = {
    "google.com", "youtube.com", "facebook.com", "wikipedia.org", "amazon.com",
    "twitter.com", "x.com", "instagram.com", "linkedin.com", "microsoft.com",
    "apple.com", "github.com", "stackoverflow.com", "reddit.com",
    "netflix.com", "yahoo.com", "bing.com", "paypal.com", "dropbox.com",
    "adobe.com", "mozilla.org", "cloudflare.com", "gitlab.com", "openai.com",
    "who.int", "un.org", "bbc.co.uk", "gov.uk", "gov.eg", "edu.eg",
    "office.com", "live.com", "whatsapp.com", "telegram.org",
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly",
    "adf.ly", "bit.do", "cutt.ly", "rb.gy", "shorturl.at", "tiny.cc",
    "rebrand.ly", "s.id", "lnkd.in", "trib.al", "shorte.st", "bc.vc",
}

SUSPICIOUS_TLDS = {
    "tk", "ml", "ga", "cf", "gq", "top", "xyz", "work", "click", "link",
    "country", "kim", "loan", "download", "racing", "win", "bid", "stream",
    "gdn", "mom", "pw", "icu", "rest", "cyou", "buzz", "monster", "quest",
    "zip", "mov", "cfd", "sbs", "lol",
}

SUSPICIOUS_WORDS = {
    "login", "signin", "verify", "verification", "account", "update",
    "secure", "security", "banking", "confirm", "password", "credential",
    "wallet", "recover", "unlock", "suspend", "alert", "billing", "invoice",
    "payment", "webscr", "authorize", "authenticate", "recovery", "limited",
    "urgent", "blocked", "expired", "refund", "gift", "bonus", "prize",
}

POPULAR_BRANDS = {
    "paypal", "apple", "microsoft", "google", "amazon", "netflix", "facebook",
    "instagram", "whatsapp", "outlook", "office365", "dropbox", "adobe",
    "linkedin", "twitter", "binance", "coinbase", "metamask", "steam",
    "dhl", "fedex", "usps", "hsbc", "chase", "wellsfargo", "citibank",
    "santander", "barclays", "sberbank", "alrajhi", "qnb", "instapay",
}

_TWO_PART_SUFFIX = {"co", "com", "org", "net", "gov", "edu", "ac"}


def _registrable(host: str) -> str:
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    if parts[-2] in _TWO_PART_SUFFIX and len(parts) >= 3:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def _host_of(url: str) -> str:
    if "://" not in url:
        url = "http://" + url
    return (urlparse(url).hostname or "").lower().strip(".")


def _sig(key: str, **params) -> dict:
    """A language-neutral risk signal; the UI turns it into text.

    Keeping the wording out of this module means the analysis is identical in
    every language and the same signal can be rendered anywhere.
    """
    return {"key": key, "params": params}


def analyze_url(url: str) -> dict:
    """Return {'features', 'signals', 'meta'} for ``url``."""
    raw = url.strip()
    host = _host_of(raw)
    registrable = _registrable(host) if host else ""
    labels = [p for p in host.split(".") if p]
    parsed = urlparse(raw if "://" in raw else "http://" + raw)
    path_query = (parsed.path or "") + ("?" + parsed.query if parsed.query
                                        else "")

    is_trusted = registrable in TRUSTED_DOMAINS
    is_shortener = registrable in SHORTENERS
    tld = labels[-1] if labels else ""
    ip_like = bool(re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}", host))
    https = raw.lower().startswith("https://")

    f, signals = {}, []
    C = PHISHING_CODING

    # 1. having_IP_Address
    f["having_IP_Address"] = (C["having_IP_Address"]["sus"] if ip_like
                              else C["having_IP_Address"]["safe"])
    if ip_like:
        signals.append(_sig("ip"))

    # 2. URL_Length
    n = len(raw)
    if n > 75:
        f["URL_Length"] = C["URL_Length"]["sus"]
        signals.append(_sig("long", n=n))
    elif n >= 54:
        f["URL_Length"] = C["URL_Length"]["mid"]
    else:
        f["URL_Length"] = C["URL_Length"]["safe"]

    # 3. Shortining_Service
    f["Shortining_Service"] = (C["Shortining_Service"]["sus"] if is_shortener
                               else C["Shortining_Service"]["safe"])
    if is_shortener:
        signals.append(_sig("shortener"))

    # 4. having_At_Symbol
    at = "@" in raw
    f["having_At_Symbol"] = (C["having_At_Symbol"]["sus"] if at
                             else C["having_At_Symbol"]["safe"])
    if at:
        signals.append(_sig("at"))

    # 5. double_slash_redirecting
    dslash = "//" in path_query
    f["double_slash_redirecting"] = (C["double_slash_redirecting"]["sus"]
                                     if dslash
                                     else C["double_slash_redirecting"]["safe"])
    if dslash:
        signals.append(_sig("dslash"))

    # 6. Prefix_Suffix
    hyphen = "-" in host
    f["Prefix_Suffix"] = (C["Prefix_Suffix"]["sus"] if hyphen
                          else C["Prefix_Suffix"]["safe"])
    if hyphen:
        signals.append(_sig("hyphen"))

    # 7. having_Sub_Domain — suspicious when there are many sub-domains
    dots = max(len(labels) - 1, 0)
    if dots >= 3:
        f["having_Sub_Domain"] = C["having_Sub_Domain"]["sus"]
        signals.append(_sig("subdomains", n=dots))
    elif dots == 1:
        f["having_Sub_Domain"] = C["having_Sub_Domain"]["safe"]
    else:
        f["having_Sub_Domain"] = C["having_Sub_Domain"]["mid"]

    # 8. SSLfinal_State
    if https and is_trusted:
        f["SSLfinal_State"] = C["SSLfinal_State"]["safe"]
    elif https:
        f["SSLfinal_State"] = C["SSLfinal_State"]["mid"]
    else:
        f["SSLfinal_State"] = C["SSLfinal_State"]["sus"]
        signals.append(_sig("nohttps"))

    # 9. Domain_registeration_length
    f["Domain_registeration_length"] = (
        C["Domain_registeration_length"]["safe"] if is_trusted
        else C["Domain_registeration_length"]["sus"])

    # 11. port
    std_port = parsed.port in (None, 80, 443)
    f["port"] = C["port"]["safe"] if std_port else C["port"]["sus"]
    if not std_port:
        signals.append(_sig("port", port=parsed.port))

    # 12. HTTPS_token
    tok = "https" in host
    f["HTTPS_token"] = (C["HTTPS_token"]["sus"] if tok
                        else C["HTTPS_token"]["safe"])
    if tok:
        signals.append(_sig("httpstoken"))

    # 17. Submitting_to_email
    mail = "mailto:" in raw.lower()
    f["Submitting_to_email"] = (C["Submitting_to_email"]["sus"] if mail
                                else C["Submitting_to_email"]["safe"])
    if mail:
        signals.append(_sig("mailto"))

    # 18. Abnormal_URL — the host must appear inside the URL text
    abn = not (host and host in raw)
    f["Abnormal_URL"] = (C["Abnormal_URL"]["sus"] if abn
                         else C["Abnormal_URL"]["safe"])
    if abn:
        signals.append(_sig("abnormal"))

    # 24. age_of_domain
    f["age_of_domain"] = (C["age_of_domain"]["safe"] if is_trusted
                          else C["age_of_domain"]["sus"])
    if not is_trusted:
        signals.append(_sig("age"))

    # 25. DNSRecord
    f["DNSRecord"] = C["DNSRecord"]["safe"] if host else C["DNSRecord"]["sus"]

    # 26-29. reputation indicators
    for name in ("web_traffic", "Page_Rank", "Google_Index",
                 "Links_pointing_to_page"):
        f[name] = C[name]["safe"] if is_trusted else C[name]["sus"]

    # --- URL-only signals that have no dedicated attribute ---------------- #
    if tld in SUSPICIOUS_TLDS:
        signals.append(_sig("tld", tld=tld))
    found = sorted({w for w in SUSPICIOUS_WORDS if w in raw.lower()})
    if found:
        signals.append(_sig("words", words=", ".join(found)))
    brand = next((b for b in POPULAR_BRANDS if b in host), None)
    if brand and not is_trusted:
        signals.append(_sig("brand", brand=brand))
    if not host:
        signals.append(_sig("nohost"))

    # 30. Statistical_report
    blacklisted = tld in SUSPICIOUS_TLDS or (brand is not None
                                             and not is_trusted)
    f["Statistical_report"] = (C["Statistical_report"]["sus"] if blacklisted
                               else C["Statistical_report"]["safe"])

    # page-dependent attributes: for a trusted domain assume the benign value,
    # otherwise take the dataset's neutral (majority) value.
    for name, val in PHISHING_NEUTRAL.items():
        f[name] = C[name]["safe"] if is_trusted else val

    for name, _, _ in PHISHING_FEATURES:
        f.setdefault(name, PHISHING_NEUTRAL.get(name, 1))

    return {
        "features": f,
        "signals": signals,
        "meta": {
            "host": host,
            "registrable": registrable,
            "tld": tld,
            "length": n,
            "is_trusted": is_trusted,
            "is_shortener": is_shortener,
            "dots": dots,
            "https": https,
        },
    }


def feature_vector(url: str):
    """30 values in dataset column order, plus the analysis dict."""
    res = analyze_url(url)
    order = [name for name, _, _ in PHISHING_FEATURES]
    return [res["features"][name] for name in order], res
