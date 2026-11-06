"""Bilingual (Arabic / English) user-interface strings.

Every visible string in the application lives here, so switching language never
leaves a stray label behind. Arabic is the default language and the layout
mirrors to RTL; English mirrors back to LTR.
"""
from __future__ import annotations

from PySide6.QtCore import QObject, Qt, Signal

# --------------------------------------------------------------------------- #
#  Strings                                                                     #
# --------------------------------------------------------------------------- #
S: dict[str, dict[str, str]] = {
    # ---- application shell -------------------------------------------------
    "app.name": {
        "ar": "نظام اختيار السمات الهجين PSO–GA",
        "en": "Hybrid PSO-GA Feature Selection System",
    },
    "app.short": {"ar": "PSO–GA", "en": "PSO-GA"},
    "app.subtitle": {
        "ar": "كشف البريد المزيف والمواقع المزيفة",
        "en": "Detecting fake emails and fake websites",
    },
    "app.tagline": {
        "ar": "تطبيق عملي لرسالة الماجستير — جامعة دامغان",
        "en": "Working application for the master's thesis — Damghan University",
    },

    # ---- navigation --------------------------------------------------------
    "nav.grp.start": {"ar": "البداية", "en": "Start"},
    "nav.grp.try": {"ar": "جرّب بنفسك", "en": "Try it yourself"},
    "nav.grp.experiment": {"ar": "التجربة والنتائج", "en": "Experiment and results"},
    "nav.grp.thesis": {"ar": "الرسالة والمراجع", "en": "The thesis and reference"},
    "nav.home": {"ar": "الرئيسية", "en": "Home"},
    "nav.dataset": {"ar": "مجموعات البيانات", "en": "Datasets"},
    "nav.algorithm": {"ar": "الخوارزمية", "en": "Algorithm"},
    "nav.experiment": {"ar": "تشغيل التجربة", "en": "Run experiment"},
    "nav.results": {"ar": "النتائج", "en": "Results"},
    "nav.detect_email": {"ar": "فحص بريد", "en": "Check email"},
    "nav.detect_url": {"ar": "فحص رابط", "en": "Check URL"},
    "nav.manual": {"ar": "إدخال السمات", "en": "Enter features"},
    "nav.about": {"ar": "عن الرسالة", "en": "About the thesis"},

    # ---- common ------------------------------------------------------------
    "common.language": {"ar": "اللغة", "en": "Language"},
    "common.arabic": {"ar": "العربية", "en": "Arabic"},
    "common.english": {"ar": "الإنجليزية", "en": "English"},
    "common.dataset": {"ar": "مجموعة البيانات", "en": "Dataset"},
    "common.run": {"ar": "تشغيل", "en": "Run"},
    "common.stop": {"ar": "إيقاف", "en": "Stop"},
    "common.reset": {"ar": "إعادة تعيين", "en": "Reset"},
    "common.analyze": {"ar": "تحليل", "en": "Analyse"},
    "common.clear": {"ar": "مسح", "en": "Clear"},
    "common.copy": {"ar": "نسخ", "en": "Copy"},
    "common.export": {"ar": "تصدير", "en": "Export"},
    "common.close": {"ar": "إغلاق", "en": "Close"},
    "common.ready": {"ar": "جاهز", "en": "Ready"},
    "common.running": {"ar": "قيد التشغيل…", "en": "Running…"},
    "common.done": {"ar": "انتهى", "en": "Finished"},
    "common.stopped": {"ar": "أُوقف", "en": "Stopped"},
    "common.error": {"ar": "خطأ", "en": "Error"},
    "common.value": {"ar": "القيمة", "en": "Value"},
    "common.meaning": {"ar": "المعنى", "en": "Meaning"},
    "common.name": {"ar": "الاسم", "en": "Name"},
    "common.symbol": {"ar": "الرمز", "en": "Symbol"},
    "common.description": {"ar": "الوصف", "en": "Description"},
    "common.metric": {"ar": "المقياس", "en": "Metric"},
    "common.thesis_value": {"ar": "قيمة الرسالة", "en": "Thesis value"},
    "common.computed": {"ar": "المحسوب", "en": "Computed"},
    "common.result": {"ar": "النتيجة", "en": "Result"},
    "common.confidence": {"ar": "الثقة", "en": "Confidence"},
    "common.verdict": {"ar": "القرار", "en": "Verdict"},
    "common.fake": {"ar": "مزيف", "en": "Fake"},
    "common.real": {"ar": "حقيقي", "en": "Real"},
    "common.correct": {"ar": "صحيح", "en": "Correct"},
    "common.wrong": {"ar": "خطأ", "en": "Wrong"},
    "common.yes": {"ar": "نعم", "en": "Yes"},
    "common.no": {"ar": "لا", "en": "No"},
    "common.feature": {"ar": "السمة", "en": "Feature"},
    "common.importance": {"ar": "الأهمية", "en": "Importance"},
    "common.step": {"ar": "الخطوة", "en": "Step"},
    "common.try_example": {"ar": "مثال جاهز", "en": "Try an example"},
    "common.page": {"ar": "صفحة", "en": "Page"},
    "common.size": {"ar": "الحجم", "en": "Size"},
    "metric.accuracy": {"ar": "الدقة", "en": "Accuracy"},
    "metric.auc": {"ar": "المساحة تحت المنحنى (AUC)", "en": "AUC"},
    "metric.features": {"ar": "السمات المختارة", "en": "Selected features"},

    # ---- home --------------------------------------------------------------
    "home.welcome": {
        "ar": "مرحباً بك في التطبيق العملي للرسالة",
        "en": "Welcome to the working application of the thesis",
    },
    "home.intro": {
        "ar": "هذا التطبيق يعيد تنفيذ طريقة الرسالة كاملةً ويعمل محلياً دون "
              "إنترنت: يختار السمات الفعّالة بخوارزمية هجينة تجمع تحسين سرب "
              "الجسيمات (PSO) والخوارزمية الجينية (GA)، ثم يصنّف البيانات "
              "بالغابة العشوائية (Random Forest). ويمكنك من خلاله فحص بريد "
              "إلكتروني أو رابط موقع بنفسك وترى النتيجة فوراً.",
        "en": "This application re-implements the thesis method end to end and "
              "runs locally with no internet: it selects effective features "
              "with a hybrid of Particle Swarm Optimization (PSO) and a "
              "Genetic Algorithm (GA), then classifies with a Random Forest. "
              "You can also check an email or a website URL yourself and see "
              "the verdict immediately.",
    },
    "home.student_info": {"ar": "معلومات الطالب", "en": "Student information"},
    "home.thesis_info": {"ar": "معلومات الرسالة", "en": "Thesis information"},
    "home.quick": {"ar": "ابدأ من هنا", "en": "Start here"},
    "home.quick.detect": {
        "ar": "افحص بريداً إلكترونياً أو رابطاً بنفسك",
        "en": "Check an email or a URL yourself",
    },
    "home.quick.experiment": {
        "ar": "شغّل خوارزمية PSO–GA وشاهد النتائج",
        "en": "Run the PSO-GA algorithm and see the results",
    },
    "home.quick.results": {
        "ar": "قارن قيم الرسالة بالقيم المحسوبة",
        "en": "Compare the thesis values with the computed ones",
    },
    "home.summary": {"ar": "ملخص النتائج", "en": "Results summary"},
    "home.howitworks": {
        "ar": "كيف يعرف التطبيق أن المدخل مزيف؟",
        "en": "How does the application decide an input is fake?",
    },

    # ---- datasets ----------------------------------------------------------
    "data.title": {"ar": "مجموعات البيانات", "en": "Datasets"},
    "data.intro": {
        "ar": "تستخدم الرسالة مجموعتين معياريتين مشهورتين. كلتاهما مضمّنة "
              "داخل التطبيق، فلا حاجة إلى إنترنت.",
        "en": "The thesis uses two well-known benchmark datasets. Both are "
              "bundled inside the application, so no internet is needed.",
    },
    "data.samples": {"ar": "عدد العينات", "en": "Samples"},
    "data.features": {"ar": "عدد السمات", "en": "Features"},
    "data.classes": {"ar": "الفئات", "en": "Classes"},
    "data.source": {"ar": "المصدر", "en": "Source"},
    "data.selected": {"ar": "السمات المختارة", "en": "Selected features"},
    "data.distribution": {"ar": "توزيع الفئات", "en": "Class distribution"},
    "data.columns": {"ar": "أسماء السمات", "en": "Feature names"},
    "data.file": {"ar": "الملف", "en": "File"},
    "data.sample_preview": {"ar": "نموذج من البيانات", "en": "Data preview"},

    # ---- algorithm ---------------------------------------------------------
    "algo.title": {"ar": "الخوارزمية الهجينة PSO–GA", "en": "The hybrid PSO-GA algorithm"},
    "algo.intro": {
        "ar": "تجمع الطريقة بين قدرة PSO على البحث السريع وقدرة GA على حفظ "
              "تنوّع المجتمع وتجنّب الوقوع في الحلول المثلى المحلية.",
        "en": "The method combines the fast search of PSO with the ability of "
              "the GA to keep the population diverse and avoid local optima.",
    },
    "algo.stages": {"ar": "مراحل الخوارزمية", "en": "Algorithm stages"},
    "algo.equations": {"ar": "المعادلات", "en": "Equations"},
    "algo.flow": {"ar": "مخطط سير العملية", "en": "Process flow"},
    "algo.params": {"ar": "البارامترات (الجدول 4-4)", "en": "Parameters (Table 4-4)"},
    "algo.preprocessing": {
        "ar": "المعالجة المسبقة (الفصل الثالث)",
        "en": "Pre-processing (chapter 3)",
    },
    "algo.encoding": {"ar": "التمثيل الثنائي", "en": "Binary encoding"},
    "algo.encoding_note": {
        "ar": "كل حل كروموسوم ثنائي بطول عدد السمات. القيمة 1 = السمة "
              "مختارة، و0 = محذوفة. فضاء البحث = 2^n.",
        "en": "Each solution is a binary chromosome as long as the feature "
              "set. 1 = selected, 0 = dropped. Search space = 2^n.",
    },

    # ---- experiment --------------------------------------------------------
    "exp.title": {"ar": "تشغيل التجربة", "en": "Run the experiment"},
    "exp.intro": {
        "ar": "شغّل خط أنابيب الرسالة كاملاً: التطبيع، تقسيم البيانات، "
              "اختيار السمات بـ PSO–GA، ثم تدريب الغابة العشوائية وتقييمها. "
              "تُعرض كل المنحنيات والمصفوفات أثناء التشغيل.",
        "en": "Run the full thesis pipeline: normalization, train/test split, "
              "PSO-GA feature selection, then Random Forest training and "
              "evaluation. Every curve and matrix is shown as it is produced.",
    },
    "exp.npop": {"ar": "حجم المجتمع (nPop)", "en": "Population size (nPop)"},
    "exp.maxit": {"ar": "عدد التكرارات (MaxIt)", "en": "Iterations (MaxIt)"},
    "exp.desired": {"ar": "عدد السمات المطلوبة", "en": "Desired features"},
    "exp.test_size": {"ar": "نسبة الاختبار", "en": "Test split"},
    "exp.seed": {"ar": "البذرة العشوائية", "en": "Random seed"},
    "exp.start": {"ar": "▶  تشغيل التجربة", "en": "▶  Run experiment"},
    "exp.progress": {"ar": "التقدّم", "en": "Progress"},
    "exp.iteration": {"ar": "التكرار", "en": "Iteration"},
    "exp.best_cost": {"ar": "أفضل كلفة", "en": "Best cost"},
    "exp.convergence": {"ar": "منحنى التقارب (دالة الكلفة)", "en": "Convergence curve (cost function)"},
    "exp.roc": {"ar": "منحنى ROC", "en": "ROC curve"},
    "exp.cm": {"ar": "مصفوفة الالتباس", "en": "Confusion matrix"},
    "exp.metrics": {"ar": "المقاييس", "en": "Metrics"},
    "exp.selected_features": {"ar": "السمات المختارة", "en": "Selected features"},
    "exp.n_selected": {"ar": "عدد السمات المختارة", "en": "Number of selected features"},
    "exp.train_acc": {"ar": "دقة التدريب", "en": "Training accuracy"},
    "exp.test_acc": {"ar": "دقة الاختبار", "en": "Test accuracy"},
    "exp.n_train": {"ar": "عينات التدريب", "en": "Training samples"},
    "exp.n_test": {"ar": "عينات الاختبار", "en": "Test samples"},
    "exp.time_select": {"ar": "زمن اختيار السمات", "en": "Feature-selection time"},
    "exp.time_fit": {"ar": "زمن تدريب النموذج", "en": "Model training time"},
    "exp.time_all": {"ar": "زمن التدريب بكل السمات", "en": "Training time with all features"},
    "exp.speedup": {"ar": "نسبة التسريع", "en": "Speed-up factor"},
    "exp.hypotheses": {"ar": "اختبار فرضيات الرسالة على هذه التجربة",
                       "en": "Testing the thesis hypotheses on this run"},
    "exp.hypotheses_note": {
        "ar": "يقارن هذا الجدول نتائج مجموعة السمات المختارة بنتائج استخدام "
              "كل السمات على نفس التقسيم ونفس البذرة، فتتحقّق الفرضيات 1 و2 "
              "و3 من الرسالة على تجربتك أنت.",
        "en": "This table compares the selected subset against using every "
              "feature, on the same split and the same seed, so hypotheses 1, "
              "2 and 3 of the thesis are checked on your own run.",
    },
    "exp.hypotheses_empty": {
        "ar": "شغّل التجربة ليظهر هنا اختبار الفرضيات.",
        "en": "Run the experiment and the hypothesis check appears here.",
    },
    "exp.with_all": {"ar": "بكل السمات", "en": "All features"},
    "exp.with_subset": {"ar": "بالسمات المختارة", "en": "Selected subset"},
    "exp.difference": {"ar": "الفرق", "en": "Difference"},
    "exp.features_used": {"ar": "عدد السمات المستخدمة", "en": "Features used"},
    "exp.log": {"ar": "سجل التنفيذ", "en": "Run log"},
    "exp.busy": {
        "ar": "التجربة قيد التنفيذ، الرجاء الانتظار…",
        "en": "The experiment is running, please wait…",
    },

    # ---- results -----------------------------------------------------------
    "res.title": {"ar": "النتائج: الرسالة مقابل المحسوب", "en": "Results: thesis vs computed"},
    "res.intro": {
        "ar": "يعرض الجدول القيم المنشورة في الرسالة إلى جانب القيم التي "
              "يحسبها هذا التطبيق فعلياً. الاختلاف البسيط طبيعي لأن الخوارزمية "
              "عشوائية، ولكنه يتغيّر مع البذرة العشوائية.",
        "en": "The table shows the values published in the thesis next to the "
              "values this application actually computes. A small difference "
              "is expected because the algorithm is stochastic, and it changes "
              "with the random seed.",
    },
    "res.published": {"ar": "القيم المنشورة", "en": "Published values"},
    "res.compare": {"ar": "جدول المقارنة", "en": "Comparison table"},
    "res.conflicts": {"ar": "تنبيهات: تعارضات داخل الرسالة", "en": "Notes: contradictions inside the thesis"},
    "res.conflicts_intro": {
        "ar": "توجد في الرسالة مواضع يختلف فيها النص عن الجدول 4-4 أو عن "
              "شيفرة MATLAB. نعرضها كما هي، دون تعديل، لأن المطلوب إعادة "
              "إنتاج الرسالة طبق الأصل. والتطبيق يتبع الجدول 4-4 لأنه الأكثر "
              "تحديداً.",
        "en": "In several places the thesis text disagrees with Table 4-4 or "
              "with the MATLAB source. They are shown here unchanged, because "
              "the brief is to reproduce the thesis exactly. The application "
              "follows Table 4-4 as the most specific specification.",
    },
    "res.topic": {"ar": "الموضوع", "en": "Topic"},
    "res.text_says": {"ar": "ما يقوله نص الرسالة", "en": "What the text says"},
    "res.table_says": {"ar": "ما يقوله الجدول 4-4", "en": "What Table 4-4 says"},
    "res.code_says": {"ar": "ما تقوله الشيفرة", "en": "What the code says"},
    "res.page24": {"ar": "أرقام صفحة 24", "en": "Page-24 numbers"},
    "res.page24_note": {
        "ar": "صفحة 24 من الرسالة تذكر مجموعة أرقام مختلفة عن الملخص "
              "والاستنتاج لنفس مجموعة Spambase. المجموعتان معروضتان هنا.",
        "en": "Page 24 of the thesis gives a different set of numbers from the "
              "abstract and conclusion for the same Spambase dataset. Both "
              "sets are shown here.",
    },
    "res.conclusion": {"ar": "الخلاصة كما في الرسالة", "en": "Conclusion as in the thesis"},
    "res.convergence": {"ar": "تحليل منحنى التقارب كما وصفته الرسالة",
                        "en": "Convergence analysis as described in the thesis"},
    "res.start_cost": {"ar": "الكلفة في البداية", "en": "Cost at the start"},
    "res.final_cost": {"ar": "الكلفة النهائية", "en": "Cost at the end"},
    "res.stable_from": {"ar": "يستقر بعد التكرار", "en": "Stabilizes after iteration"},

    # ---- detect email ------------------------------------------------------
    "mail.title": {"ar": "فحص بريد إلكتروني", "en": "Check an email"},
    "mail.intro": {
        "ar": "الصق نص البريد (الموضوع والجسم) ثم اضغط تحليل. يحوّل التطبيق "
              "النص إلى سمات Spambase السبع والخمسين ثم يصنّفه: مزيف (Spam) "
              "أو حقيقي (Ham).",
        "en": "Paste the email text (subject and body) and press Analyse. The "
              "application converts the text into the 57 Spambase attributes "
              "and classifies it: fake (Spam) or real (Ham).",
    },
    "mail.placeholder": {
        "ar": "الصق نص البريد هنا…",
        "en": "Paste the email text here…",
    },
    "mail.example_spam": {"ar": "مثال بريد مزيف", "en": "Example fake email"},
    "mail.example_ham": {"ar": "مثال بريد حقيقي", "en": "Example real email"},
    "mail.features": {"ar": "السمات المستخرجة من النص", "en": "Features extracted from the text"},
    "mail.keywords": {"ar": "كلمات مفتاحية مكتشفة", "en": "Detected keywords"},
    "mail.top_features": {"ar": "أكثر السمات تأثيراً في القرار", "en": "Features that drove the decision"},
    "mail.empty": {"ar": "الرجاء إدخال نص البريد أولاً.", "en": "Please enter the email text first."},
    "mail.too_short": {
        "ar": "النص قصير جداً، أضف كلمات أكثر لنتيجة أدق.",
        "en": "The text is very short; add more words for a more reliable result.",
    },
    "mail.verdict_fake": {"ar": "بريد مزيف (Spam)", "en": "Fake email (Spam)"},
    "mail.verdict_real": {"ar": "بريد حقيقي (Ham)", "en": "Real email (Ham)"},

    # ---- detect URL --------------------------------------------------------
    "url.title": {"ar": "فحص رابط موقع", "en": "Check a website URL"},
    "url.intro": {
        "ar": "أدخل رابطاً كاملاً يبدأ بـ http:// أو https://. يحسب التطبيق "
              "سمات مجموعة «Phishing Websites» الثلاثين من الرابط نفسه ثم "
              "يصنّفه: مزيف (Phishing) أو حقيقي (Legitimate).",
        "en": "Enter a full URL starting with http:// or https://. The "
              "application derives the 30 Phishing-Websites attributes from the "
              "URL itself and classifies it: fake (Phishing) or real "
              "(Legitimate).",
    },
    "url.placeholder": {"ar": "https://example.com/login?id=1", "en": "https://example.com/login?id=1"},
    "url.example_fake": {"ar": "مثال موقع مزيف", "en": "Example fake site"},
    "url.example_real": {"ar": "مثال موقع حقيقي", "en": "Example real site"},
    "url.attributes": {"ar": "السمات الثلاثون المستخرجة من الرابط", "en": "The 30 attributes derived from the URL"},
    "url.signals": {"ar": "مؤشرات الخطر المكتشفة", "en": "Risk signals found"},
    "url.no_signals": {"ar": "لم تُكتشف مؤشرات خطر واضحة.", "en": "No clear risk signals found."},
    "url.domain": {"ar": "النطاق", "en": "Domain"},
    "url.registrable": {"ar": "النطاق المسجّل", "en": "Registrable domain"},
    "url.tld": {"ar": "الامتداد", "en": "TLD"},
    "url.https": {"ar": "يستخدم HTTPS", "en": "Uses HTTPS"},
    "url.length": {"ar": "طول الرابط", "en": "URL length"},
    "url.empty": {"ar": "الرجاء إدخال رابط أولاً.", "en": "Please enter a URL first."},
    "url.invalid": {
        "ar": "الرابط غير صالح. اكتب رابطاً كاملاً مثل https://example.com",
        "en": "That is not a valid URL. Enter a full URL such as https://example.com",
    },
    "url.verdict_fake": {"ar": "موقع مزيف (Phishing)", "en": "Fake website (Phishing)"},
    "url.verdict_real": {"ar": "موقع حقيقي (Legitimate)", "en": "Real website (Legitimate)"},

    # ---- manual ------------------------------------------------------------
    "man.title": {"ar": "إدخال السمات يدوياً", "en": "Enter features manually"},
    "man.intro": {
        "ar": "حدّد قيمة كل سمة بنفسك وشغّل المصنّف مباشرة على هذا المتجه. "
              "هذا هو نفس المدخل الذي تستخدمه الخوارزمية.",
        "en": "Set each attribute value yourself and run the classifier "
              "directly on that vector. This is exactly the input the "
              "algorithm uses.",
    },
    "man.howto": {
        "ar": "اختر مجموعة البيانات، ثم اضبط قيم السمات بالأسفل، واضغط "
              "«صنّف هذا المتجه». تظهر النتيجة في الأعلى مباشرة.",
        "en": "Pick a dataset, set the attribute values below, then press "
              "Classify this vector. The verdict appears directly above.",
    },
    "man.attributes": {"ar": "قيم السمات", "en": "Attribute values"},
    "man.attributes_hint": {
        "ar": "السمات مجمّعة حسب نوعها لتسهيل الإدخال.",
        "en": "Attributes are grouped by kind to make entry easier.",
    },
    "man.quickfill": {"ar": "تعبئة سريعة:", "en": "Quick fill:"},
    "man.grp.url": {"ar": "بنية الرابط", "en": "URL structure"},
    "man.grp.security": {"ar": "الشهادة والنطاق", "en": "Certificate and domain"},
    "man.grp.html": {"ar": "محتوى الصفحة وروابطها", "en": "Page content and links"},
    "man.grp.domain": {"ar": "سمعة الموقع", "en": "Site reputation"},
    "man.grp.word": {"ar": "تكرار الكلمات", "en": "Word frequencies"},
    "man.grp.char": {"ar": "تكرار المحارف", "en": "Character frequencies"},
    "man.grp.caps": {"ar": "الأحرف الكبيرة", "en": "Capital letters"},
    "man.load_sample": {"ar": "تحميل قيم سمة من البيانات", "en": "Load a feature vector from the data"},
    "man.classify": {"ar": "🔍  صنّف هذا المتجه", "en": "🔍  Classify this vector"},
    "man.all_suspicious": {"ar": "كل القيم مشبوهة", "en": "All values suspicious"},
    "man.all_safe": {"ar": "كل القيم سليمة", "en": "All values safe"},
    "man.reset": {"ar": "↺  إعادة تعيين", "en": "↺  Reset"},
    "man.random_sample": {"ar": "🎲  عيّنة عشوائية", "en": "🎲  Random sample"},
    "man.batch": {"ar": "📋  عشرة عيّنات", "en": "📋  Ten samples"},
    "man.sample_table": {"ar": "فحص عيّنات من بيانات الاختبار", "en": "Checking held-out samples"},
    "man.sample_note": {
        "ar": "يصنّف النموذج عيّنات مسحوبة من مجموعة الاختبار (لم تُستخدم في "
              "التدريب) ويقارن التوقّع بالتصنيف الحقيقي.",
        "en": "The model classifies samples drawn from the test set (never "
              "used for training) and compares the prediction with the true "
              "label.",
    },
    "man.actual": {"ar": "الحقيقي", "en": "Actual"},
    "man.predicted": {"ar": "التوقّع", "en": "Predicted"},

    # ---- about -------------------------------------------------------------
    "about.title": {"ar": "عن الرسالة والتطبيق", "en": "About the thesis and this application"},
    "about.cover": {"ar": "صفحة الغلاف", "en": "Cover page"},
    "about.abstract": {"ar": "الملخص", "en": "Abstract"},
    "about.objectives": {"ar": "أهداف البحث", "en": "Research objectives"},
    "about.problem": {"ar": "بيان المشكلة", "en": "Problem statement"},
    "about.importance": {"ar": "أهمية البحث", "en": "Importance of the research"},
    "about.questions": {"ar": "أسئلة البحث", "en": "Research questions"},
    "about.hypotheses": {"ar": "فرضيات البحث", "en": "Research hypotheses"},
    "about.preprocessing": {"ar": "المعالجة المسبقة", "en": "Pre-processing"},
    "about.classifier": {"ar": "المصنّف: الغابة العشوائية", "en": "Classifier: Random Forest"},
    "about.metrics": {"ar": "مقاييس التقييم", "en": "Evaluation metrics"},
    "about.scope": {"ar": "ما يستطيع التطبيق فعله وما لا يستطيع", "en": "What this application can and cannot do"},
    "about.tech": {"ar": "التقنيات المستخدمة", "en": "Technology used"},
    "about.tech_note": {
        "ar": "الرسالة والمجلد المضغوط يستخدمان لغة MATLAB للتنفيذ "
              "(الدوال TreeBagger و randperm و perfcurve و confusionchart). "
              "أعيد تنفيذ كل خطوة في هذا التطبيق بلغة Python مع مكتبة "
              "scikit-learn، بحيث تعطي نفس المخرجات: نفس دالة الكلفة، ونفس "
              "تحديثات PSO و GA، ونفس مقاييس التقييم والمنحنيات.",
        "en": "The archive that accompanies the thesis implements the method "
              "in MATLAB (functions TreeBagger, randperm, perfcurve, "
              "confusionchart). Every step has been re-implemented in Python "
              "with scikit-learn so it produces the same outputs: the same "
              "cost function, the same PSO and GA updates, and the same "
              "metrics and curves.",
    },
    "about.license": {
        "ar": "هذا التطبيق للاستخدام الأكاديمي في مناقشة الرسالة.",
        "en": "This application is for academic use in the thesis defense.",
    },

    # ---- charts ------------------------------------------------------------
    "chart.iteration": {"ar": "التكرار", "en": "Iteration"},
    "chart.cost": {"ar": "أفضل كلفة", "en": "Best cost"},
    "chart.fpr": {"ar": "نسبة الإيجابيات الخاطئة", "en": "False positive rate"},
    "chart.tpr": {"ar": "نسبة الإيجابيات الصحيحة", "en": "True positive rate"},
    "chart.auc": {"ar": "المساحة تحت المنحنى", "en": "AUC"},
    "chart.percent": {"ar": "النسبة %", "en": "Percent %"},
    "chart.actual": {"ar": "الحقيقي", "en": "Actual"},
    "chart.predicted": {"ar": "المتوقّع", "en": "Predicted"},
    "chart.no_data": {
        "ar": "شغّل التجربة أولاً لعرض المنحنى.",
        "en": "Run the experiment first to see this chart.",
    },

    # ---- MATLAB source page ------------------------------------------------
    "nav.matlab": {"ar": "شيفرة MATLAB", "en": "MATLAB source"},
    "matlab.intro": {
        "ar": "الملف المضغوط المرفق مع الرسالة يحتوي على الشيفرة الأصلية "
              "بلغة MATLAB. هذه هي الملفات الخمسة التي تنفّذ الخوارزمية، "
              "معروضة هنا كما هي حرفياً دون أي تعديل. التطبيق لا يشغّلها "
              "(يحتاج ذلك إلى MATLAB)، لكنه يعيد إنتاج نفس الخوارزمية بلغة "
              "Python بنفس المعاملات بالضبط.",
        "en": "The archive that accompanies the thesis holds the original "
              "MATLAB source. These are the five files that implement the "
              "algorithm, shown here verbatim and unmodified. The application "
              "does not run them (that would need MATLAB); instead it "
              "reproduces the same algorithm in Python with identical "
              "parameters.",
    },
    "matlab.run_order": {
        "ar": "ترتيب التنفيذ في MATLAB",
        "en": "Execution order in MATLAB",
    },
    "matlab.run_order_hint": {
        "ar": "شغّل main.m وهو يستدعي بقية الملفات تلقائياً.",
        "en": "Run main.m; it calls the other files automatically.",
    },
    "matlab.purpose": {"ar": "الوظيفة", "en": "Purpose"},
    "matlab.file": {"ar": "الملف", "en": "File"},
    "matlab.lines": {"ar": "الأسطر", "en": "Lines"},
    "matlab.p_main": {
        "ar": "البرنامج الرئيسي: تحميل البيانات، التطبيع، تقسيم 80/20، "
              "تشغيل الخوارزمية، تدريب النموذج النهائي وحساب الدقة.",
        "en": "Main script: load data, normalize, 80/20 split, run the "
              "algorithm, train the final model and report accuracy.",
    },
    "matlab.p_ga_pso": {
        "ar": "الخوارزمية الهجينة: تحديث سرعة PSO، الترميز السيني، الإصلاح، "
              "التزاوج والطفرة الجينيين، وتتبّع أفضل حل.",
        "en": "The hybrid algorithm: PSO velocity update, sigmoid "
              "binarization, repair, GA crossover and mutation, and tracking "
              "of the global best.",
    },
    "matlab.p_fitness": {
        "ar": "دالة التقييم: تدرّب غابة عشوائية بـ 50 شجرة وتعيد "
              "1 − الدقة + 0.01 × عقوبة عدد السمات.",
        "en": "Fitness: trains a 50-tree random forest and returns "
              "1 − accuracy + 0.01 × feature-count penalty.",
    },
    "matlab.p_repair": {
        "ar": "الإصلاح: يفرض أن يكون عدد السمات المختارة مساوياً للعدد "
              "المطلوب بالضبط.",
        "en": "Repair: forces the chromosome to hold exactly the desired "
              "number of selected features.",
    },
    "matlab.p_plot": {
        "ar": "الرسم: منحنى التقارب، مصفوفة الالتباس، منحنى ROC، وأعمدة "
              "مقاييس الأداء.",
        "en": "Plotting: convergence curve, confusion matrix, ROC curve and "
              "the performance-metrics bars.",
    },
    "matlab.source": {"ar": "الشيفرة الكاملة", "en": "Full source"},
    "matlab.verbatim": {
        "ar": "منسوخ حرفياً من الملف المضغوط، دون تغيير.",
        "en": "Copied verbatim from the archive, unmodified.",
    },
    "matlab.extra": {
        "ar": "ملفات أصلية إضافية من الملف المضغوط",
        "en": "Additional original files from the archive",
    },
    "matlab.extra_hint": {
        "ar": "ملفات .fig هي ملفات رسوم MATLAB الأصلية التي أنتجت صور "
              "النتائج، و main.asv نسخة احتياطية يكتبها محرّر MATLAB. "
              "التطبيق يضمّنها كما هي لأنه لا يستطيع فتحها خارج MATLAB، "
              "لكن حذفها كان سيجعل المجلد ناقصاً.",
        "en": "The .fig files are the original MATLAB figures that produced "
              "the result images, and main.asv is the editor backup MATLAB "
              "writes. The application bundles them unchanged because it "
              "cannot open them outside MATLAB, but dropping them would leave "
              "the folder incomplete.",
    },
    "matlab.extra_note": {
        "ar": "لا تُفتح داخل التطبيق — صيغة خاصة بـ MATLAB.",
        "en": "Not opened inside the application — a MATLAB-specific format.",
    },
    "matlab.missing": {
        "ar": "تحذير: بعض ملفات MATLAB الأصلية غير موجودة في هذه النسخة.",
        "en": "Warning: some original MATLAB files are missing from this build.",
    },
    "matlab.all_present": {
        "ar": "كل ملفات الملف المضغوط الأصلية موجودة ومضمّنة.",
        "en": "Every file from the original archive is present and bundled.",
    },

    # ---- thesis figures page ----------------------------------------------
    "nav.figures": {"ar": "أشكال الرسالة", "en": "Thesis figures"},
    "fig.intro": {
        "ar": "هذه صور النتائج التسع المصدَّرة من MATLAB في الملف المضغوط، "
              "معروضة كما هي. وهي تمثّل نتائج الرسالة المنشورة، بينما "
              "منحنيات صفحة «تشغيل التجربة» يرسمها التطبيق من حسابه الخاص. "
              "اعرض الصفحتين معاً للمقارنة.",
        "en": "These are the nine result images exported from MATLAB in the "
              "archive, shown unchanged. They represent the published results "
              "of the thesis, whereas the charts on the Run-experiment page "
              "are drawn by the application from its own computation. View "
              "both pages together to compare.",
    },
    "fig.spambase": {"ar": "نتائج Spambase", "en": "Spambase results"},
    "fig.phishing": {"ar": "نتائج Phishing", "en": "Phishing results"},
    "fig.spambase_hint": {
        "ar": "بريد إلكتروني — 57 سمة، 4601 عيّنة، 46 سمة مختارة.",
        "en": "Email — 57 features, 4601 samples, 46 selected.",
    },
    "fig.phishing_hint": {
        "ar": "مواقع — 30 سمة، 11055 عيّنة، 22 سمة مختارة.",
        "en": "Websites — 30 features, 11055 samples, 22 selected.",
    },
    "fig.curve_spam": {
        "ar": "الشكل 4-1: منحنى التقارب — Spambase",
        "en": "Figure 4-1: Convergence curve — Spambase",
    },
    "fig.cm_spam": {
        "ar": "الشكل 4-2: مصفوفة الالتباس — Spambase",
        "en": "Figure 4-2: Confusion matrix — Spambase",
    },
    "fig.roc_spam": {
        "ar": "الشكل 4-3: منحنى ROC — Spambase",
        "en": "Figure 4-3: ROC curve — Spambase",
    },
    "fig.per_spam": {
        "ar": "الشكل 4-4: تقييم أداء النموذج — Spambase",
        "en": "Figure 4-4: Performance evaluation — Spambase",
    },
    "fig.all_spam": {
        "ar": "لوحة النتائج المجمّعة — Spambase",
        "en": "Combined results panel — Spambase",
    },
    "fig.curve_phish": {
        "ar": "الشكل 4-5: منحنى التقارب — Phishing",
        "en": "Figure 4-5: Convergence curve — Phishing",
    },
    "fig.cm_phish": {
        "ar": "الشكل 4-6: مصفوفة الالتباس — Phishing",
        "en": "Figure 4-6: Confusion matrix — Phishing",
    },
    "fig.roc_phish": {
        "ar": "الشكل 4-7: منحنى ROC — Phishing",
        "en": "Figure 4-7: ROC curve — Phishing",
    },
    "fig.all_phish": {
        "ar": "الشكل 4-8: تقييم أداء النموذج — Phishing",
        "en": "Figure 4-8: Performance evaluation — Phishing",
    },
    "fig.source_note": {
        "ar": "المصدر: الملف المضغوط المرفق بالرسالة (hussiandamghan.zip). "
              "لم تُعدَّل الصور بأي شكل.",
        "en": "Source: the archive accompanying the thesis "
              "(hussiandamghan.zip). The images are unmodified.",
    },
    "fig.missing": {
        "ar": "تحذير: بعض صور الرسالة غير موجودة في هذه النسخة.",
        "en": "Warning: some thesis figures are missing from this build.",
    },
    "fig.open_hint": {
        "ar": "انقر على أي صورة لعرضها بحجمها الأصلي.",
        "en": "Click any image to view it at full size.",
    },
    "fig.published_values": {
        "ar": "القيم المنشورة المرتبطة بهذا الشكل",
        "en": "Published values for this figure",
    },

    # ---- home: hero banner ------------------------------------------------
    "home.hero.kicker": {
        "ar": "رسالة ماجستير · جامعة دامغان",
        "en": "Master's thesis · Damghan University",
    },
    "home.hero.by": {
        "ar": "إعداد الطالب",
        "en": "Prepared by",
    },
    "home.hero.affiliation": {
        "ar": "جامعة دامغان — قسم علوم الحاسوب · إشراف {sup}",
        "en": "Damghan University — Department of Computer Science · "
              "Supervised by {sup}",
    },
    "home.hero.chip_offline": {"ar": "يعمل دون إنترنت", "en": "Works offline"},
    "home.hero.chip_bilingual": {"ar": "عربي وإنجليزي", "en": "Arabic and English"},
    "home.hero.chip_accuracy": {
        "ar": "دقة {spam}% و {phish}%",
        "en": "Accuracy {spam}% and {phish}%",
    },

    # ---- home: action cards ----------------------------------------------
    "home.act.detect.title": {"ar": "افحص بريداً أو رابطاً", "en": "Check an email or a URL"},
    "home.act.detect.body": {
        "ar": "الصق نص رسالة أو اكتب رابط موقع، فيحوّله التطبيق إلى سمات "
              "ويحكم عليه فوراً.",
        "en": "Paste a message or type a website address; the application turns "
              "it into features and gives a verdict at once.",
    },
    "home.act.manual.title": {"ar": "أدخل السمات يدوياً", "en": "Enter features by hand"},
    "home.act.manual.body": {
        "ar": "حدّد قيمة كل سمة بنفسك وشغّل المصنّف على المتجه الذي بنيته.",
        "en": "Set each attribute value yourself and run the classifier on the "
              "vector you built.",
    },
    "home.act.experiment.title": {"ar": "شغّل التجربة كاملة", "en": "Run the full experiment"},
    "home.act.experiment.body": {
        "ar": "نفّذ خط أنابيب الرسالة كاملاً: تطبيع، اختيار سمات بـ PSO–GA، "
              "ثم غابة عشوائية وتقييم.",
        "en": "Execute the whole thesis pipeline: normalization, PSO-GA "
              "feature selection, then Random Forest training and evaluation.",
    },
    "home.act.open": {"ar": "افتح", "en": "Open"},
    "home.act.run": {"ar": "تشغيل", "en": "Run"},

    # ---- home: at a glance ------------------------------------------------
    "home.glance.title": {"ar": "نظرة سريعة على النتائج", "en": "Results at a glance"},
    "home.glance.hint": {
        "ar": "القيم المنشورة في الرسالة لكل مجموعة بيانات.",
        "en": "The values published in the thesis for each dataset.",
    },
    "home.glance.accuracy": {"ar": "الدقة", "en": "Accuracy"},
    "home.glance.selected": {"ar": "السمات المختارة", "en": "Selected features"},
    "home.glance.samples": {"ar": "عدد العينات", "en": "Samples"},
    "home.glance.details": {"ar": "كل الأرقام والتفاصيل", "en": "All numbers and detail"},

    # ---- home: how it works ----------------------------------------------
    "home.how.title": {
        "ar": "كيف يصل التطبيق إلى الحكم؟",
        "en": "How does the application reach a verdict?",
    },
    "home.how.sub": {
        "ar": "أربع خطوات فقط، من المدخل الخام إلى النتيجة.",
        "en": "Four steps, from the raw input to the result.",
    },
    "how.encode.title": {"ar": "تحويل المدخل إلى سمات", "en": "Turn the input into features"},
    "how.vote.title": {"ar": "تصويت الأشجار", "en": "The trees vote"},
    "how.confidence.title": {"ar": "حساب الثقة", "en": "Confidence is counted"},
    "how.select.title": {"ar": "اختيار السمات مسبقاً", "en": "Features were pre-selected"},
    "how.encode": {
        "ar": "البريد → 57 سمة، والرابط → 30 سمة",
        "en": "Email → 57 attributes, URL → 30 attributes",
    },
    "how.vote": {
        "ar": "100 شجرة قرار تصوّت على الفئة",
        "en": "100 decision trees each vote on the class",
    },
    "how.confidence": {
        "ar": "الثقة = نسبة الأشجار المتفقة",
        "en": "Confidence = the share of trees that agreed",
    },
    "how.select": {
        "ar": "PSO–GA أبقت 46 و22 سمة فقط",
        "en": "PSO-GA kept only 46 and 22 attributes",
    },

    # ---- collapsible section headers -------------------------------------
    "sec.expand_all": {"ar": "إظهار كل التفاصيل", "en": "Show every detail"},
    "sec.collapse_all": {"ar": "إخفاء كل التفاصيل", "en": "Hide every detail"},
}


class Translator(QObject):
    """Holds the active language and notifies the UI when it changes."""

    changed = Signal(str)

    def __init__(self, lang: str = "ar"):
        super().__init__()
        self._lang = lang

    # -- language ----------------------------------------------------------
    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, value: str):
        value = "en" if value == "en" else "ar"
        if value != self._lang:
            self._lang = value
            self.changed.emit(value)

    def toggle(self):
        self.lang = "en" if self._lang == "ar" else "ar"

    # -- lookup ------------------------------------------------------------
    def __call__(self, key: str) -> str:
        entry = S.get(key)
        if entry is None:
            return key
        return entry.get(self._lang, entry.get("en", key))

    def t(self, key: str) -> str:
        return self(key)

    @property
    def is_rtl(self) -> bool:
        return self._lang == "ar"

    @property
    def alignment(self):
        return Qt.AlignRight if self.is_rtl else Qt.AlignLeft

    @property
    def layout_direction(self):
        return Qt.RightToLeft if self.is_rtl else Qt.LeftToRight


#: single shared instance used by every page
TRANSLATOR = Translator("ar")


def t(key: str) -> str:
    """Shorthand for ``TRANSLATOR.t(key)``."""
    return TRANSLATOR.t(key)


#: Wording for the language-neutral risk signals emitted by
#: ``core.url_analyzer``. Each entry is a format string; ``{...}`` placeholders
#: are filled from the signal's parameters.
SIGNAL_TEXT = {
    "ip": {"ar": "الرابط يستخدم عنوان IP مباشرة بدل اسم نطاق",
           "en": "The URL uses a bare IP address instead of a domain name"},
    "long": {"ar": "الرابط طويل جداً ({n} محرفاً)",
             "en": "The URL is very long ({n} characters)"},
    "shortener": {"ar": "الرابط يستخدم خدمة اختصار روابط",
                  "en": "The URL uses a link-shortening service"},
    "at": {"ar": "الرابط يحتوي الرمز @ (قد يخفي النطاق الحقيقي)",
           "en": "The URL contains @, which can hide the real domain"},
    "dslash": {"ar": "يوجد // داخل مسار الرابط (إعادة توجيه محتملة)",
               "en": "The URL path contains //, a possible redirect"},
    "hyphen": {"ar": "اسم النطاق يحتوي شرطة -",
               "en": "The domain name contains a hyphen"},
    "subdomains": {"ar": "عدد كبير من النطاقات الفرعية ({n})",
                   "en": "Many sub-domains ({n})"},
    "nohttps": {"ar": "الرابط لا يستخدم HTTPS",
                "en": "The URL does not use HTTPS"},
    "port": {"ar": "الرابط يستخدم منفذاً غير قياسي ({port})",
             "en": "The URL uses a non-standard port ({port})"},
    "httpstoken": {"ar": "كلمة https مضمّنة في اسم النطاق",
                   "en": "The token https is embedded in the domain name"},
    "mailto": {"ar": "الرابط يستخدم mailto:",
               "en": "The URL uses mailto:"},
    "abnormal": {"ar": "الرابط غير طبيعي: اسم النطاق لا يطابق الرابط",
                 "en": "Abnormal URL: the host does not appear in the URL"},
    "age": {"ar": "عمر النطاق مجهول أو أقل من سنة",
            "en": "The domain age is unknown or under one year"},
    "tld": {"ar": "امتداد النطاق .{tld} شائع في حملات التصيّد",
            "en": "The .{tld} extension is common in phishing campaigns"},
    "words": {"ar": "كلمات حساسة في الرابط: {words}",
              "en": "Sensitive words in the URL: {words}"},
    "brand": {"ar": "اسم علامة تجارية ({brand}) على نطاق مختلف",
              "en": "Brand name ({brand}) on a different domain"},
    "nohost": {"ar": "لم يُستخرج اسم نطاق صالح من الرابط",
               "en": "No valid domain name could be extracted from the URL"},
}


def signal_text(sig) -> str:
    """Render one risk signal from ``core.url_analyzer`` in the active
    language."""
    if isinstance(sig, str):        # already-rendered text
        return sig
    entry = SIGNAL_TEXT.get(sig.get("key"))
    if entry is None:
        return sig.get("key", "")
    template = entry.get(TRANSLATOR.lang, entry.get("en", ""))
    try:
        return template.format(**sig.get("params", {}))
    except (KeyError, IndexError):
        return template


def sep() -> str:
    """Separator for joining data tokens (keywords, feature names)."""
    return "، " if TRANSLATOR.lang == "ar" else ", "


def pick(pair) -> str:
    """Pick the right member of an ``(english, arabic)`` tuple."""
    en, ar = pair[0], pair[1]
    return ar if TRANSLATOR.lang == "ar" else en
