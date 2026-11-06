# HASEEN — Hybrid PSO–GA Feature Selection

نظام هجين لاختيار السمات (**PSO–GA**) مبني على رسالة الماجستير
«Hybrid PSO–GA Feature Selection» — جامعة دامغان، حسين ناصر حسين.

A hybrid **Particle Swarm Optimization + Genetic Algorithm** feature-selection
system. Ships a desktop GUI (Windows), a web demo, the MATLAB reference
implementation, and both thesis datasets.

---

## المحتويات | Contents

| المسار | الوصف |
|---|---|
| `desktop/` | تطبيق سطح المكتب (PySide6) — عربي/إنجليزي، يعمل على ويندوز |
| `desktop/build/` | سكربتات البناء: PyInstaller spec، Inno Setup، QA، الأدلة |
| `app/` | نسخة ويب (Flask) لنفس المحرّك |
| `extracted_zip/hussiandamghan/` | كود MATLAB الأصلي + الصور + مجموعات البيانات |
| `release/` | صفحة التحميل وملفات البصمات (الملفات التنفيذية في GitHub Releases) |

---

## مجموعات البيانات | Datasets

| الملف | الحجم | المهمة |
|---|---|---|
| `spambase.xlsx` | 4601 × 58 | كشف البريد المزعج (spam) |
| `Data_phishing.xlsx` | 11055 × 31 | كشف مواقع التصيّد (phishing) |

---

## التشغيل السريع | Quick start

### تطبيق سطح المكتب

```bash
cd desktop
pip install -r requirements.txt
python run_app.py            # تشغيل الواجهة
python run_app.py --selftest # فحص ذاتي سريع
python verify_app.py         # فحص شامل (71 اختبار)
```

### نسخة الويب

```bash
cd app
pip install -r requirements.txt
python app.py                # ثم افتح http://localhost:5000
```

---

## بناء نسخة ويندوز | Building the Windows release

راجع `desktop/build/BUILD_WINDOWS_LINUX.md` للوصف الكامل.
الملخص: يُبنى الملف التنفيذي بـ **PyInstaller** من
`desktop/build/thesis_app.spec`، ثم يُغلّف بمثبّت **Inno Setup** من
`desktop/build/installer.iss`. يمكن البناء على لينكس عبر **Wine**.

الملفات الناتجة (منشورة في تبويب Releases):

| الملف | الحجم |
|---|---|
| `HybridPSOGA-Setup-1.0.0.exe` | 86.7 م.ب — مثبّت ويندوز |
| `HybridPSOGA-Windows-Portable.zip` | 129.3 م.ب — نسخة محمولة |

### البصمات | Checksums

```
62df5a3bb60714c3057a799c5e78cd7835337b44b98c9030824dda3899cf1d99  HybridPSOGA-Setup-1.0.0.exe
5fb27bed489e89062c6555a92c5de9b92221433a6ab9ff304cf964c8257c8f10  HybridPSOGA-Windows-Portable.zip
```

---

## المتطلبات | Requirements

- Python 3.10+
- `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`, `openpyxl`
- `PySide6` (لسطح المكتب) أو `Flask` (للويب)

---

## ملاحظات | Notes

- الملفات التنفيذية غير موقّعة رقميًا؛ قد يظهر تحذير SmartScreen على ويندوز.
- الملفات الأكبر من 100 م.ب مستثناة من Git وتُنشر كأصول في Releases.
