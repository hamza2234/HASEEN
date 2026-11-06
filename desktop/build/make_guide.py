"""Generates the step-by-step installation guide, in Arabic and English, as a
printable HTML file.

    python build/make_guide.py      ->  docs/dalil_altathbit.html
"""
from __future__ import annotations

import html
import os

OUT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "docs",
    "دليل_التثبيت.html"))

EN_STEPS = [
    ("Download the setup file",
     "You received one file: <b>HybridPSOGA-Setup-1.0.0.exe</b>. Copy it to the "
     "computer where the program should run. Nothing else is needed — no "
     "Python, no MATLAB, no internet connection."),
    ("Start the installer",
     "Double-click <b>HybridPSOGA-Setup-1.0.0.exe</b>. If Windows asks for "
     "permission, click <b>Yes</b>. The setup wizard opens."),
    ("Welcome page",
     "Read the short introduction and click <b>Next</b>."),
    ("Licence page",
     "Read the license (the program is for academic use in the thesis defense) "
     "and click <b>I accept the agreement</b>, then <b>Next</b>."),
    ("Choose the folder",
     "Keep the suggested folder, or choose another one. Click <b>Next</b>."),
    ("Choose the shortcuts",
     "Leave <b>Create a desktop shortcut</b> ticked. Click <b>Next</b>."),
    ("Ready to install",
     "Click <b>Install</b>. Installation takes under a minute."),
    ("Finish",
     "Leave <b>Launch the application</b> ticked and click <b>Finish</b>. The "
     "program opens."),
    ("Choose the language",
     "In the sidebar at the bottom, choose <b>العربية</b> or <b>English</b>. "
     "The whole interface switches, including the direction of the layout."),
    ("Use it",
     "Go to <b>Check email</b> and paste an email, or <b>Check URL</b> and type "
     "a website address. You get a verdict, the confidence, and the attributes "
     "behind the decision."),
]

AR_STEPS = [
    ("نزّل ملف التثبيت",
     "ستجد ملفاً واحداً باسم <b>HybridPSOGA-Setup-1.0.0.exe</b>. انسخه إلى "
     "الحاسوب الذي تريد تشغيل البرنامج عليه. لا تحتاج إلى أي شيء آخر: لا "
     "Python ولا MATLAB ولا اتصال بالإنترنت."),
    ("ابدأ التثبيت",
     "انقر نقراً مزدوجاً على <b>HybridPSOGA-Setup-1.0.0.exe</b>. إذا طلب "
     "ويندوز الإذن فاختر <b>نعم</b>. ستُفتح نافذة التثبيت."),
    ("صفحة الترحيب",
     "اقرأ المقدمة المختصرة ثم اضغط <b>Next</b>."),
    ("صفحة الترخيص",
     "اقرأ الترخيص (البرنامج للاستخدام الأكاديمي في مناقشة الرسالة) ثم اختر "
     "<b>I accept the agreement</b> ثم <b>Next</b>."),
    ("اختر المجلد",
     "اترك المجلد المقترح كما هو، أو اختر مجلداً آخر. ثم اضغط <b>Next</b>."),
    ("اختر الاختصارات",
     "اترك خيار <b>Create a desktop shortcut</b> محدَّداً. ثم اضغط <b>Next</b>."),
    ("جاهز للتثبيت",
     "اضغط <b>Install</b>. يستغرق التثبيت أقل من دقيقة."),
    ("إنهاء",
     "اترك خيار <b>Launch the application</b> محدَّداً ثم اضغط <b>Finish</b>. "
     "سيفتح البرنامج."),
    ("اختر اللغة",
     "في الشريط الجانبي في الأسفل اختر <b>العربية</b> أو <b>English</b>. "
     "ستتغيّر الواجهة كاملة، بما في ذلك اتجاه التخطيط."),
    ("ابدأ الاستخدام",
     "اذهب إلى <b>فحص بريد</b> والصق نص بريد، أو <b>فحص رابط</b> واكتب عنوان "
     "موقع. ستحصل على القرار ونسبة الثقة والسمات التي بنى عليها القرار."),
]

UNINSTALL_EN = (
    "Open <b>Settings → Apps → Installed apps</b>, find "
    "<b>Hybrid PSO-GA Feature Selection System</b> and click <b>Uninstall</b>. "
    "No internet connection is needed at any point, before or after "
    "installation."
)
UNINSTALL_AR = (
    "افتح <b>الإعدادات ← التطبيقات ← التطبيقات المثبَّتة</b>، وابحث عن "
    "<b>Hybrid PSO-GA Feature Selection System</b> ثم اضغط <b>إلغاء التثبيت</b>. "
    "لا حاجة إلى اتصال بالإنترنت في أي مرحلة، لا قبل التثبيت ولا بعده."
)

REQ_EN = [
    ("Operating system", "Windows 10 or 11 (64-bit)"),
    ("Disk space", "about 900 MB after installation"),
    ("Memory", "4 GB or more"),
    ("Internet", "not required at any time"),
    ("Other software", "none — Python and MATLAB are not needed"),
]
REQ_AR = [
    ("نظام التشغيل", "ويندوز 10 أو 11 (بنية 64 بت)"),
    ("مساحة القرص", "حوالي 900 ميغابايت بعد التثبيت"),
    ("الذاكرة", "4 غيغابايت أو أكثر"),
    ("الإنترنت", "غير مطلوب في أي مرحلة"),
    ("برامج أخرى", "لا شيء — لا حاجة إلى Python ولا إلى MATLAB"),
]

HEAD = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>دليل التثبيت — نظام اختيار السمات الهجين PSO-GA</title>
<style>
  @page { size: A4; margin: 18mm 16mm; }
  body { font-family: "Noto Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif;
         color:#1c2430; line-height:1.8; max-width: 840px; margin: 0 auto;
         padding: 24px; background:#fff; }
  h1 { font-size: 25px; margin: 0 0 4px; }
  h2 { font-size: 19px; margin: 36px 0 14px; padding-bottom:6px;
       border-bottom: 2px solid #2f6fed; color:#2359c8; }
  .sub { color:#6b7686; font-size: 13px; margin-bottom: 24px; }
  ol { padding-inline-start: 22px; }
  li { margin-bottom: 13px; }
  li b { color:#2359c8; }
  table { width:100%; border-collapse: collapse; margin: 12px 0; }
  th, td { border:1px solid #e2e6ec; padding: 8px 11px; text-align: start;
           font-size: 13px; }
  th { background:#f1f3f6; font-weight:700; }
  .box { background:#eaf1ff; border:1px solid #bcd2ff; border-radius:9px;
         padding: 13px 16px; margin: 16px 0; font-size: 13px; }
  .ltr { direction: ltr; text-align: left; }
  .foot { margin-top: 40px; padding-top: 14px; border-top:1px solid #e2e6ec;
          color:#6b7686; font-size: 12px; }
  @media print { body { padding: 0; } h2 { page-break-after: avoid; } }
</style>
</head>
<body>
"""


def _steps(items) -> str:
    out = ["<ol>"]
    for title, body in items:
        out.append(f"<li><b>{html.escape(title)}</b><br>{body}</li>")
    out.append("</ol>")
    return "\n".join(out)


def _table(rows) -> str:
    out = ["<table>"]
    for k, v in rows:
        out.append(f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>")
    out.append("</table>")
    return "\n".join(out)


def build_html() -> str:
    parts = [HEAD]

    # ---------- Arabic ----------
    parts.append("<h1>دليل التثبيت خطوة بخطوة</h1>")
    parts.append('<div class="sub">نظام اختيار السمات الهجين PSO-GA — '
                 "التطبيق العملي لرسالة الماجستير<br>"
                 "حسين ناصر حسين — جامعة دامغان — إشراف: د. عبد العلي بصيري"
                 "</div>")
    parts.append('<div class="box">التثبيت بالعربية: اضغط <b>Next</b> في كل '
                 "صفحة، ثم <b>Install</b>، ثم <b>Finish</b>. ثلاث نقرات فقط "
                 "تكفي.</div>")
    parts.append("<h2>متطلبات التشغيل</h2>")
    parts.append(_table(REQ_AR))
    parts.append("<h2>خطوات التثبيت</h2>")
    parts.append(_steps(AR_STEPS))
    parts.append("<h2>إلغاء التثبيت</h2>")
    parts.append(f"<p>{UNINSTALL_AR}</p>")

    # ---------- English ----------
    parts.append('<hr style="margin:44px 0 0; border:none; border-top:1px solid '
                 '#e2e6ec;">')
    parts.append('<div class="ltr">')
    parts.append("<h1>Installation guide, step by step</h1>")
    parts.append('<div class="sub">Hybrid PSO-GA Feature Selection System — '
                 "working application for the master's thesis<br>"
                 "Hussein Naser Hussein — Damghan University — "
                 "Supervisor: Dr. Abdolali Basiri</div>")
    parts.append('<div class="box">In English: click <b>Next</b> on every '
                 "page, then <b>Install</b>, then <b>Finish</b>. Three clicks "
                 "is all it takes.</div>")
    parts.append("<h2>Requirements</h2>")
    parts.append(_table(REQ_EN))
    parts.append("<h2>Installation steps</h2>")
    parts.append(_steps(EN_STEPS))
    parts.append("<h2>Uninstalling</h2>")
    parts.append(f"<p>{UNINSTALL_EN}</p>")
    parts.append("</div>")

    parts.append('<div class="foot">This application reproduces the '
                 "master's thesis of Hussein Naser Hussein and is intended for "
                 "academic use in the thesis defense.</div>")
    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    path = OUT
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build_html())
    print(f"written: {path}")


if __name__ == "__main__":
    main()
