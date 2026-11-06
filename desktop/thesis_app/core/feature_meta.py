"""Feature metadata for the two thesis datasets.

Column order follows the official UCI definitions:

* Spambase  — 48 ``word_freq_*``, then 6 ``char_freq_*``, then the three
  ``capital_run_length_*`` attributes.
* Phishing Websites — 30 attributes, each encoded ``{-1, 0, 1}``.

``legend`` maps each raw value to the meaning UCI gives it; where UCI leaves
the encoding implicit the mapping is the one the dataset's own statistics
support (verified against the class distribution of each value).
"""

# --------------------------------------------------------------------------- #
#  Spambase                                                                    #
# --------------------------------------------------------------------------- #
SPAMBASE_WORDS = [
    "make", "address", "all", "3d", "our", "over", "remove", "internet",
    "order", "mail", "receive", "will", "people", "report", "addresses",
    "free", "business", "email", "you", "credit", "your", "font", "000",
    "money", "hp", "hpl", "george", "650", "lab", "labs", "telnet", "857",
    "data", "415", "85", "technology", "1999", "parts", "pm", "direct", "cs",
    "meeting", "original", "project", "re", "edu", "table", "conference",
]

SPAMBASE_CHARS = [";", "(", "[", "!", "$", "#"]


def _spambase_names():
    names = [f"word_freq_{w}" for w in SPAMBASE_WORDS]
    names += [f"char_freq_{c}" for c in SPAMBASE_CHARS]
    names += ["capital_run_length_average", "capital_run_length_longest",
              "capital_run_length_total"]
    return names


# --------------------------------------------------------------------------- #
#  Phishing Websites                                                           #
# --------------------------------------------------------------------------- #
# The copy of the Phishing Websites dataset shipped with the thesis stores
# several attributes with the opposite sign to the UCI .arff file, so the
# encoding below is the one *this dataset* actually uses. Every entry was
# verified against the class distribution of the value (see ANALYSIS_REPORT).
#
# (name, arabic label, {value: arabic meaning})
PHISHING_FEATURES = [
    ("having_IP_Address", "وجود عنوان IP في الرابط",
     {1: "الرابط يستخدم عنوان IP", -1: "الرابط يستخدم اسم نطاق"}),
    ("URL_Length", "طول الرابط",
     {1: "طويل (أكثر من 75 محرفاً)", 0: "متوسط (54-75 محرفاً)",
      -1: "قصير (أقل من 54 محرفاً)"}),
    ("Shortining_Service", "استخدام خدمة اختصار الروابط",
     {-1: "يستخدم خدمة اختصار", 1: "لا يستخدم خدمة اختصار"}),
    ("having_At_Symbol", "وجود الرمز @ في الرابط",
     {1: "يوجد رمز @", -1: "لا يوجد رمز @"}),
    ("double_slash_redirecting", "إعادة التوجيه بشرطتين مائلتين //",
     {-1: "توجد // داخل الرابط", 1: "لا توجد // داخل الرابط"}),
    ("Prefix_Suffix", "وجود شرطة في اسم النطاق",
     {1: "اسم النطاق يحتوي شرطة -", -1: "اسم النطاق بدون شرطة"}),
    ("having_Sub_Domain", "عدد النطاقات الفرعية",
     {1: "نطاقات فرعية كثيرة", 0: "عدد قليل من النطاقات الفرعية",
      -1: "عدد متوسط من النطاقات الفرعية"}),
    ("SSLfinal_State", "حالة شهادة SSL النهائية",
     {1: "شهادة مفقودة أو غير موثوقة", 0: "شهادة سليمة وموثوقة",
      -1: "شهادة مشكوك فيها"}),
    ("Domain_registeration_length", "مدة تسجيل النطاق",
     {-1: "مدة التسجيل قصيرة أو مجهولة", 1: "مسجّل لمدة سنة أو أكثر"}),
    ("Favicon", "أيقونة الموقع (Favicon)",
     {1: "الأيقونة من نفس النطاق", -1: "الأيقونة من نطاق خارجي"}),
    ("port", "المنفذ غير القياسي",
     {1: "منفذ غير قياسي أو غير معروف", -1: "منفذ قياسي"}),
    ("HTTPS_token", "الرمز https داخل اسم النطاق",
     {-1: "اسم النطاق يحتوي https", 1: "اسم النطاق لا يحتوي https"}),
    ("Request_URL", "نطاق الموارد المطلوبة",
     {1: "معظم الموارد من نطاق خارجي", -1: "معظم الموارد من نفس النطاق"}),
    ("URL_of_Anchor", "روابط الوسم <a>",
     {1: "معظم الروابط فارغة أو خارجية", 0: "نسبة معتدلة من الروابط الخارجية",
      -1: "الروابط تشير لنفس النطاق"}),
    ("Links_in_tags", "روابط داخل الوسوم <meta>/<script>/<link>",
     {1: "معظم الروابط خارجية", 0: "نسبة معتدلة خارجية",
      -1: "معظم الروابط لنفس النطاق"}),
    ("SFH", "هدف إرسال النموذج (Server Form Handler)",
     {1: "الهدف يشير لنطاق مختلف أو فارغ", 0: "الهدف يشير لنطاق آخر",
      -1: "الهدف سليم"}),
    ("Submitting_to_email", "الإرسال إلى بريد إلكتروني",
     {1: "يستخدم mail() أو mailto", -1: "لا يستخدم mail() أو mailto"}),
    ("Abnormal_URL", "رابط غير طبيعي (URL غير مطابق للنطاق)",
     {-1: "الرابط غير طبيعي", 1: "الرابط طبيعي ومطابق"}),
    ("Redirect", "عدد عمليات إعادة التوجيه",
     {0: "يوجد إعادة توجيه واحدة أو أكثر", 1: "لا توجد إعادة توجيه"}),
    ("on_mouseover", "تغيير شريط الحالة عند المرور بالمؤشر",
     {1: "يوجد تغيير", -1: "لا يوجد تغيير"}),
    ("RightClick", "تعطيل الزر الأيمن للفأرة",
     {1: "الزر الأيمن معطّل", -1: "الزر الأيمن يعمل"}),
    ("popUpWidnow", "النوافذ المنبثقة (popup)",
     {-1: "توجد نوافذ منبثقة", 1: "لا توجد نوافذ منبثقة"}),
    ("Iframe", "استخدام إطار iframe",
     {-1: "يوجد iframe", 1: "لا يوجد iframe"}),
    ("age_of_domain", "عمر النطاق",
     {1: "عمر النطاق قصير أو مجهول", -1: "عمر النطاق سنة أو أكثر"}),
    ("DNSRecord", "سجل DNS للنطاق",
     {1: "لا يوجد سجل DNS", -1: "يوجد سجل DNS"}),
    ("web_traffic", "حركة الزيارات للموقع",
     {1: "حركة زيارات ضعيفة", 0: "حركة زيارات متوسطة",
      -1: "الموقع ضمن أكثر المواقع زيارة"}),
    ("Page_Rank", "ترتيب الصفحة (PageRank)",
     {1: "ترتيب الصفحة منخفض", -1: "ترتيب الصفحة مرتفع"}),
    ("Google_Index", "فهرسة الموقع في محرك البحث",
     {1: "الموقع غير مفهرس", -1: "الموقع مفهرس في Google"}),
    ("Links_pointing_to_page", "عدد الروابط الواردة للموقع",
     {-1: "عدد قليل من الروابط الواردة", 0: "عدد متوسط",
      1: "عدد كبير من الروابط الواردة"}),
    ("Statistical_report", "تقارير إحصائية عن الموقع",
     {1: "الموقع مدرج في قوائم الحظر/التقارير", -1: "الموقع غير مدرج"}),
]

# value used when the URL *is* suspicious on that aspect, and the benign value.
# ``mid`` is the middle option for three-valued attributes.
PHISHING_CODING = {
    "having_IP_Address":           {"sus": 1, "safe": -1},
    "URL_Length":                  {"sus": 1, "mid": 0, "safe": -1},
    "Shortining_Service":          {"sus": -1, "safe": 1},
    "having_At_Symbol":            {"sus": 1, "safe": -1},
    "double_slash_redirecting":    {"sus": -1, "safe": 1},
    "Prefix_Suffix":               {"sus": 1, "safe": -1},
    "having_Sub_Domain":           {"sus": 1, "mid": -1, "safe": 0},
    "SSLfinal_State":              {"sus": 1, "mid": -1, "safe": 0},
    "Domain_registeration_length": {"sus": -1, "safe": 1},
    "Favicon":                     {"sus": -1, "safe": 1},
    "port":                        {"sus": 1, "safe": -1},
    "HTTPS_token":                 {"sus": -1, "safe": 1},
    "Request_URL":                 {"sus": 1, "safe": -1},
    "URL_of_Anchor":               {"sus": 1, "mid": 0, "safe": -1},
    "Links_in_tags":               {"sus": 1, "mid": 0, "safe": -1},
    "SFH":                         {"sus": 1, "mid": 0, "safe": -1},
    "Submitting_to_email":         {"sus": 1, "safe": -1},
    "Abnormal_URL":                {"sus": -1, "safe": 1},
    "Redirect":                    {"sus": 0, "safe": 1},
    "on_mouseover":                {"sus": 1, "safe": -1},
    "RightClick":                  {"sus": 1, "safe": -1},
    "popUpWidnow":                 {"sus": -1, "safe": 1},
    "Iframe":                      {"sus": -1, "safe": 1},
    "age_of_domain":               {"sus": 1, "safe": -1},
    "DNSRecord":                   {"sus": 1, "safe": -1},
    "web_traffic":                 {"sus": 1, "mid": 0, "safe": -1},
    "Page_Rank":                   {"sus": 1, "safe": -1},
    "Google_Index":                {"sus": 1, "safe": -1},
    "Links_pointing_to_page":      {"sus": -1, "mid": 0, "safe": 1},
    "Statistical_report":          {"sus": 1, "safe": -1},
}

# value used when the attribute cannot be derived from the URL alone; the
# dataset's own majority value, so it adds no spurious evidence either way.
PHISHING_NEUTRAL = {
    "Favicon": 1, "Request_URL": 1, "URL_of_Anchor": 0, "Links_in_tags": 0,
    "SFH": -1, "Redirect": 0, "on_mouseover": 1, "RightClick": 1,
    "popUpWidnow": 1, "Iframe": 1, "Statistical_report": 1,
}

# --------------------------------------------------------------------------- #
#  Spambase — high-signal indicator words (for the text analyzer)              #
# --------------------------------------------------------------------------- #
SPAM_WORDS = {
    "free", "money", "credit", "your", "you", "our", "remove", "business",
    "internet", "order", "mail", "receive", "will", "people", "report",
    "addresses", "email", "hp", "hpl", "george", "650", "lab", "labs",
    "telnet", "857", "data", "415", "85", "technology", "1999", "parts",
    "pm", "direct", "cs", "meeting", "original", "project", "re", "edu",
    "table", "conference", "make", "address", "all", "3d", "over",
}

HAM_WORDS = {
    "re", "edu", "george", "cs", "meeting", "project", "labs", "table",
    "conference", "original", "university", "thanks", "regards", "please",
    "hello", "hi", "attached", "let", "know", "tomorrow", "today",
}

FEATURE_NAMES = {
    "spambase": _spambase_names(),
    "phishing": [f[0] for f in PHISHING_FEATURES],
}

FEATURE_LABELS_AR = {
    "spambase": {n: n for n in _spambase_names()},
    "phishing": {f[0]: f[1] for f in PHISHING_FEATURES},
}


# --------------------------------------------------------------------------- #
#  English labels and legends                                                  #
# --------------------------------------------------------------------------- #
PHISHING_LABELS_EN = {
    "having_IP_Address": "IP address in the URL",
    "URL_Length": "URL length",
    "Shortining_Service": "URL shortening service",
    "having_At_Symbol": "@ symbol in the URL",
    "double_slash_redirecting": "Double slash // redirect",
    "Prefix_Suffix": "Hyphen in the domain name",
    "having_Sub_Domain": "Number of sub-domains",
    "SSLfinal_State": "Final SSL certificate state",
    "Domain_registeration_length": "Domain registration length",
    "Favicon": "Favicon source",
    "port": "Non-standard port",
    "HTTPS_token": "https token inside the domain",
    "Request_URL": "Domain of the requested resources",
    "URL_of_Anchor": "Links in <a> tags",
    "Links_in_tags": "Links in <meta>/<script>/<link> tags",
    "SFH": "Server form handler (SFH)",
    "Submitting_to_email": "Submits to an e-mail address",
    "Abnormal_URL": "Abnormal URL (does not match the domain)",
    "Redirect": "Number of redirects",
    "on_mouseover": "Status bar changes on mouseover",
    "RightClick": "Right-click disabled",
    "popUpWidnow": "Pop-up windows",
    "Iframe": "Uses an iframe",
    "age_of_domain": "Domain age",
    "DNSRecord": "DNS record",
    "web_traffic": "Website traffic",
    "Page_Rank": "PageRank",
    "Google_Index": "Indexed by a search engine",
    "Links_pointing_to_page": "Links pointing to the page",
    "Statistical_report": "Statistical reports about the site",
}

PHISHING_MEANINGS_EN = {
    "having_IP_Address": {1: "The URL uses an IP address",
                          -1: "The URL uses a domain name"},
    "URL_Length": {1: "Long (more than 75 characters)",
                   0: "Average (54-75 characters)",
                   -1: "Short (fewer than 54 characters)"},
    "Shortining_Service": {-1: "Uses a shortening service",
                           1: "Does not use a shortening service"},
    "having_At_Symbol": {1: "Contains an @ symbol",
                         -1: "No @ symbol"},
    "double_slash_redirecting": {-1: "Contains // inside the URL",
                                 1: "No // inside the URL"},
    "Prefix_Suffix": {1: "The domain name contains a hyphen",
                      -1: "The domain name has no hyphen"},
    "having_Sub_Domain": {1: "Many sub-domains",
                          0: "Few sub-domains",
                          -1: "An average number of sub-domains"},
    "SSLfinal_State": {1: "Certificate missing or untrusted",
                       0: "Certificate valid and trusted",
                       -1: "Certificate suspicious"},
    "Domain_registeration_length": {-1: "Registration short or unknown",
                                     1: "Registered for a year or more"},
    "Favicon": {1: "The favicon comes from the same domain",
                -1: "The favicon comes from an external domain"},
    "port": {1: "Non-standard or unknown port",
             -1: "Standard port"},
    "HTTPS_token": {-1: "The domain contains https",
                    1: "The domain does not contain https"},
    "Request_URL": {1: "Most resources come from an external domain",
                    -1: "Most resources come from the same domain"},
    "URL_of_Anchor": {1: "Most anchors are empty or external",
                      0: "A moderate share of external anchors",
                      -1: "Anchors point to the same domain"},
    "Links_in_tags": {1: "Most links are external",
                      0: "A moderate share is external",
                      -1: "Most links point to the same domain"},
    "SFH": {1: "The target points to a different domain or is empty",
            0: "The target points to another domain",
            -1: "The target is normal"},
    "Submitting_to_email": {1: "Uses mail() or mailto",
                            -1: "Does not use mail() or mailto"},
    "Abnormal_URL": {-1: "The URL is abnormal",
                     1: "The URL is normal and matches"},
    "Redirect": {0: "One or more redirects",
                 1: "No redirect"},
    "on_mouseover": {1: "The status bar changes",
                     -1: "No change"},
    "RightClick": {1: "Right-click is disabled",
                   -1: "Right-click works"},
    "popUpWidnow": {-1: "Pop-ups present",
                    1: "No pop-ups"},
    "Iframe": {-1: "An iframe is used",
               1: "No iframe"},
    "age_of_domain": {1: "Domain age short or unknown",
                      -1: "Domain age a year or more"},
    "DNSRecord": {1: "No DNS record",
                  -1: "A DNS record exists"},
    "web_traffic": {1: "Low traffic",
                    0: "Average traffic",
                    -1: "Among the most visited sites"},
    "Page_Rank": {1: "Low PageRank",
                  -1: "High PageRank"},
    "Google_Index": {1: "Not indexed",
                     -1: "Indexed by Google"},
    "Links_pointing_to_page": {-1: "Few inbound links",
                               0: "An average number",
                               1: "Many inbound links"},
    "Statistical_report": {1: "Listed in block lists or reports",
                           -1: "Not listed"},
}


def meaning(name: str, value: int, lang: str = "ar") -> str:
    """Human-readable meaning of one Phishing attribute value."""
    table = PHISHING_MEANINGS_EN if lang == "en" else None
    if table is not None:
        return table.get(name, {}).get(value, str(value))
    for n, _label, legend in PHISHING_FEATURES:
        if n == name:
            return legend.get(value, str(value))
    return str(value)


def label(name: str, lang: str = "ar") -> str:
    """Human-readable label of one Phishing attribute."""
    if lang == "en":
        return PHISHING_LABELS_EN.get(name, name)
    return FEATURE_LABELS_AR["phishing"].get(name, name)
