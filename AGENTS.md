# AGENTS.md

## Project
Web demo that reproduces the master's thesis experiment
"Hybrid PSO–GA Feature Selection" (Damghan University, Hossein Naser Hussein).

Two datasets, both shipped inside `extracted_zip/hussiandamghan/`:
- `spambase.xlsx` — 4601 x 58 (57 features + label) → spam e-mail detection
- `Data_phishing.xlsx` — 11055 x 31 (30 features + label) → phishing website detection

## Layout
- `app/engine.py`   — self-contained Python port of the MATLAB sources
  (`main.m`, `GA_PSO_feature_selection.m`, `fitness_RF.m`,
  `repair_solution.m`, `plot_results.m`). Holds `THESIS` (published values),
  `PARAMS_TABLE` (Table 4-4), `load_dataset`, `ga_pso`, `run_experiment`,
  `predict_sample`, `sample_batch`.
- `app/app.py`      — Flask app. Pages: `/`, `/detect/<key>`, `/experiments`,
  `/results`, `/params`, `/methodology`. API: `POST /api/run`,
  `GET /api/job/<id>`, `POST /api/predict`, `POST /api/samples`,
  `POST /api/analyze_text`, `POST /api/analyze_url`,
  `POST /api/predict_manual`, `GET /api/features/<key>`.
- `app/feature_meta.py`  — column names + per-value legends for both datasets,
  plus `PHISHING_CODING` (which raw value means "suspicious" per attribute).
- `app/text_analyzer.py` — e-mail text -> the 57 Spambase features, using the
  exact UCI definitions (word_freq / char_freq / capital_run_length).
- `app/url_analyzer.py`  — URL string -> the 30 Phishing features.
- `app/verify.py`        — end-to-end check of every page, JS validity and all
  live-detection endpoints. Run `python3 verify.py` with the server up.
- `app/templates/`  — Jinja templates (Arabic RTL UI).
- `app/static/style.css` — styles.
- `ANALYSIS_REPORT.md`   — deep analysis of the thesis and its numbers.

## Run
```bash
cd app && ./run.sh          # or: python3 app.py
```
Listens on `0.0.0.0:12000`. Public URL:
`https://work-1-jdmbnbotvoejtwun.prod-runtime.all-hands.dev/`

Dependencies: `pip install -r app/requirements.txt`
(flask, scikit-learn, pandas, numpy, openpyxl).

## Important notes
- The MATLAB code ships `desired_features` as a hard constraint, so the
  algorithm always returns exactly that many features (47 for Spambase in the
  code, 46 in the thesis text; 22 for Phishing).
- Published thesis metrics are stored verbatim in `engine.THESIS` and shown on
  the `/results` page next to the values actually computed by the app.
- The pipeline is stochastic; metrics vary by seed. Re-running with the same
  seed reproduces the same numbers.
- All UI text is Arabic. Keep it that way unless asked otherwise.

## The Phishing dataset's inverted encoding (read before touching it)
The copy of `Data_phishing.xlsx` shipped with the thesis stores many attributes
with the **opposite sign** to the official UCI `.arff` file. For example UCI
says `having_IP_Address = -1` means "uses an IP", but in this dataset `1` is
the suspicious value (59% phishing rate vs 49%).

Emitting the documented sign instead of the dataset's own sign **inverts the
classifier**: real sites get flagged as phishing and vice versa. This bit us
once already. `feature_meta.PHISHING_CODING` holds the verified per-attribute
`sus` / `mid` / `safe` values, derived from the empirical phishing rate of each
value in the shipped file. Always produce feature values through that mapping.

## Live detection: what the site can and cannot see
- `text_analyzer.py` sees **only the e-mail body text** — not attachments,
  not SMTP headers, not sender reputation.
- `url_analyzer.py` sees **only the URL string**. Attributes that the original
  study derived by fetching the page (Favicon, Request_URL, URL_of_Anchor,
  Links_in_tags, SFH, Redirect, on_mouseover, RightClick, popUpWidnow, Iframe,
  Statistical_report) are neutral-filled, except that a domain in the
  `TRUSTED_DOMAINS` table takes the benign value. Trust indicators
  (age_of_domain, web_traffic, Page_Rank, Google_Index, DNSRecord, SSLfinal_State)
  come from that table too — an unknown domain is never given the benefit of
  the doubt.
- Never present the verdict as proof. The UI already says it is a strong
  indicator, not a final judgement, and the user should confirm the real domain.

## Verifying a change
```bash
cd app && python3 app.py &        # start the server
python3 verify.py                 # 25 checks: pages, JS, e-mail, URL, manual, samples
```
`verify.py` expects `ALL CHECKS PASSED` and exit code 0.

# ---------------------------------------------------------------------------
# Desktop application (desktop/)
# ---------------------------------------------------------------------------
An offline, bilingual (Arabic/English) PySide6 desktop application that
reproduces the thesis. It shares no code with `app/` — the engine and analysers
were ported into `desktop/thesis_app/core/` so the desktop build is
self-contained and freezable.

## Layout
```
desktop/
  run_app.py               launcher (python run_app.py [--selftest])
  verify_app.py            66-check self-test
  thesis_app/
    main.py                entry point; --selftest runs headless
    core/engine.py         PSO-GA + RandomForest (port of app/engine.py)
    core/thesis_data.py    every fact/number/equation from the PDF
    core/feature_meta.py   attribute names + AR/EN labels and legends
    core/text_analyzer.py  email text -> 57 Spambase attributes
    core/url_analyzer.py   URL -> 30 Phishing attributes
    ui/main_window.py      shell, sidebar (grouped), language switch
    ui/i18n.py             288 strings + 17 risk signals, one shared TRANSLATOR
    ui/theme.py            palette + global stylesheet + chart styling
    ui/widgets.py          cards, hero banner, collapsible section, tables, charts
    ui/pages/*.py          eleven pages
    assets/data/           spambase.xlsx, Data_phishing.xlsx
    assets/figures/        the nine thesis result images (verbatim)
    assets/*.m             the five original MATLAB sources (verbatim)
    assets/matlab/         the .fig figures + main.asv from the archive
  build/thesis_app.spec    PyInstaller
  build/installer.iss      Inno Setup (Next/Next/Install/Finish)
  build/make_qa.py         defence Q&A -> docs/*.html (+ chromium -> PDF)
  build/make_guide.py      install guide -> docs/*.html (+ PDF)
  build/make_screenshots.py  every page in both languages -> docs/screenshots/
```

## Rules that matter
- **i18n**: every visible string goes in `ui/i18n.py` with both an `ar` and an
  `en` value. `verify_app.py` fails if any key is missing a language.
  Create translatable widgets through the `BasePage` helpers — `label(key)`,
  `button(key)`, `card(title_key, hint_key)` — which register the widget and
  its key together. Passing `t("key")` straight into `QLabel`/`Card`/`QPushButton`
  silently produces a string that never retranslates; `verify_app.py` catches
  this with a "no Arabic text leaks into the English interface" check.
- **Two ways to retranslate**: pages whose text is *looked up* register widgets
  (the default). Pages whose text is *computed* — `pick(...)`, dataset fields,
  table rows — set `rebuildable = True` and the whole widget tree is rebuilt on
  a language change. Do not mix the two in one page, with one exception: the
  manual page registers its chrome strings *and* rebuilds the attribute editor
  grid, because the attribute names and value meanings come from
  `feature_meta` rather than the string table. Any page that does this must
  register every string-table widget it creates, or the leak check fails.
- **Language-neutral data**: text generated in `core/` must not be a translated
  string. `url_analyzer` emits `{"key": ..., "params": ...}` records and the UI
  renders them with `i18n.signal_text()`. Join data tokens with `i18n.sep()`,
  never a literal `"، "`, or English mode shows an Arabic comma.
- **Keep each page short on open**: long reference material — equations, the
  Table 4-4 parameters, the MATLAB source listings, the raw attribute lists,
  the per-attribute derivation tables, the contradiction table, the
  convergence analysis — goes inside a collapsible section via
  `BasePage.add_section(title_key)`, which registers the header for
  retranslation the same way `add_card` does. The home page carries the hero
  (thesis title and the student's name), the three action cards and the
  headline numbers; anything else belongs on the page that owns the topic.
  Aim for a page that opens at roughly one screen of prose plus its controls.
- **Widget teardown**: when clearing a layout, capture the widget before
  unparenting — `w = item.widget(); w.setParent(None); w.deleteLater()`.
  Calling `item.widget()` twice is unsafe because the widget loses its owner on
  `setParent(None)` and CPython may collect it between the two calls.
- **RTL**: the shell sets `Qt.RightToLeft` from `TRANSLATOR.is_rtl`. Keep
  URL/email/formula inputs at `Qt.LeftToRight` explicitly, or they mirror.
- **Asset paths**: `engine._data_path` checks `sys._MEIPASS/thesis_app/assets/
  data`, then the source tree, then `extracted_zip/`. Add new bundled files to
  both `thesis_app/assets/` and the `datas` list in `build/thesis_app.spec`.
- **The archive must stay complete**: everything in `hussiandamghan.zip` is
  bundled — the two spreadsheets, the five `.m` sources, the nine result
  `.jpg` figures, the four `.fig` files and `main.asv`. `engine.MATLAB_FILES`,
  `engine.MATLAB_EXTRA_FILES` and `engine.FIGURES` are the single source of
  truth; `verify_app.py` fails if any of them is missing. The MATLAB page shows
  the `.m` files verbatim and the figures page shows the `.jpg` images
  verbatim — never re-draw or "clean up" either. Each caption carries its
  thesis figure number (4-1 … 4-8) so a reader can line the app up with the
  PDF; `verify_app.py` fails if a number goes missing.
- **Every chapter of the thesis must stay represented.** `core/thesis_data.py`
  is the single source of truth and is keyed to the thesis structure:
  `PROBLEM_STATEMENT_*` and `IMPORTANCE_*` (chapter 1), `OBJECTIVES`,
  `QUESTIONS`, `HYPOTHESES` (chapter 1), `PREPROCESSING`, `EQUATIONS`,
  `ALGORITHM_STAGES` (chapter 3), `CLASSIFIER_FACTS`, `METRICS`,
  `PARAMS_TABLE`, `CONVERGENCE` (chapter 4), `CONFLICTS`, `CONCLUSION_*`,
  `SCOPE_LIMITS` (chapter 5). Each narrative block needs both `_EN` and `_AR`.
  `verify_app.py` checks that all 33 meaningful thesis numbers and all 82
  distinct thesis terms are still reachable from the source, so deleting or
  rephrasing one fails the build rather than silently dropping it. The term
  check reads AST string literals, not the raw file, so line wrapping in a
  multi-line literal does not produce a false failure.
- **Hypotheses must be testable in the app, not just quoted.** `run_experiment`
  evaluates the selected subset *and* the all-feature baseline on the same
  split and seed, and reports the accuracy delta, the feature reduction and the
  training-time speed-up. Hypotheses 1-3 of the thesis are then literally
  checked on the user's own run in the experiment page.
- **Never exclude `numpy.f2py`** in the spec — `scipy._external.array_api_compat`
  imports it at runtime and the frozen build dies with
  `ModuleNotFoundError: No module named 'numpy.f2py'`.
- **Frozen GUI plugin**: run under `QT_QPA_PLATFORM=offscreen` (or Xvfb) when
  testing headless; `--selftest` avoids Qt entirely so it runs with no display.
- **matplotlib**: `MPLCONFIGDIR` is forced to a temp path in `main.py`, because
  an installed application directory is often read-only.

## Verifying a change
```bash
cd desktop
python run_app.py --selftest          # core + bundled data, no display needed
xvfb-run -a python3 verify_app.py     # 71 checks incl. both languages + no leaks
./dist/HybridPSOGA/HybridPSOGA --selftest   # after a PyInstaller build
```
To catch translation regressions by hand, switch language on every page with a
verdict on screen: the stateful pages (email, URL, manual, experiment) keep
their result, so any string computed from the old language survives unless the
page refreshes it.
Regenerate the docs after changing any user-visible text:
```bash
python build/make_qa.py && python build/make_guide.py
chromium --headless --no-sandbox --print-to-pdf=... "file://...html"
```

## Build
```bash
pyinstaller build/thesis_app.spec --noconfirm   # ~65 s, 376 MB folder
iscc build/installer.iss                        # Windows only, needs Inno Setup 6
```
The 376 MB is PySide6 (100 MB) + scipy (75 MB) + numpy/pandas/sklearn/
matplotlib; that is normal for this stack and unavoidable without dropping
scikit-learn.

## Building the Windows release from Linux
PyInstaller cannot cross-compile, so Windows artefacts are produced by running
a Windows Python toolchain under Wine. `build/BUILD_WINDOWS_LINUX.md` holds the
full recipe; the two things that cost the most time to discover are the
dependency pins: numpy must be 1.26.4 (2.x ships an OpenBLAS that calls
`crealf`, which Wine's `ucrtbase` stubs and aborts on) and PySide6 must be
6.6.3.1 (6.7+ links `icuuc.dll`, which the wheel does not ship). Both the
frozen exe and the Inno Setup installer pass `--selftest` under Wine, and
`verify_app.py` reports 71 passed / 0 failed on the Windows stack.

Note that a Wine pass is not a substitute for a real Windows smoke test: the
frozen exe loads the genuine Windows UCRT, so it must be launched once on
Windows before release.
