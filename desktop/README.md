# Hybrid PSO-GA Feature Selection System

A complete, offline desktop application that reproduces the master's thesis of
**Hussein Naser Hussein** (Damghan University, supervised by Dr. Abdolali
Basiri, May 2026):

> Development of a Hybrid Method Based on Particle Swarm Optimization and
> Genetic Algorithm for Selecting an Effective Feature Subset

The application implements everything in the two source documents — the 30-page
thesis and the MATLAB archive — and adds a working detector you can use to check
your own emails and website URLs.

---

## What is inside

| Page | What it shows |
|---|---|
| **Home** | Student and thesis details, a results summary, and a short explanation of how a verdict is reached |
| **Datasets** | The two benchmark datasets, their sizes, class balance, every attribute name and a preview of the real rows |
| **Algorithm** | The six stages of the hybrid method, all five equations (3-1 to 3-5), Table 4-4, and the pre-processing pipeline |
| **Run experiment** | Runs the full pipeline live with a progress bar, and draws the convergence curve, the ROC curve, the confusion matrix and the selected features |
| **Results** | Every value published in the thesis beside the value this application computes, plus the eight contradictions found inside the thesis |
| **Check email** | Paste any email text and get a verdict (fake / real) with confidence, the driving attributes and the full 57-attribute vector |
| **Check URL** | Type any website address and get a verdict with all 30 attributes and the risk signals found |
| **Enter features** | Set every attribute by hand and classify the vector, or inspect held-out samples |
| **About the thesis** | Cover page, abstract, objectives, questions, hypotheses, the classifier, the metrics and what the application cannot do |

The whole interface is available in **Arabic (default, right-to-left)** and
**English (left-to-right)**, switchable at any moment from the sidebar.

---

## Installation

### Option A — the installer (recommended, no Python needed)

1. Run `HybridPSOGA-Setup-1.0.0.exe`.
2. Click **Next**, read the licence, click **Next** again.
3. Keep the default folder, click **Next**.
4. Click **Install**.
5. Click **Finish** — the application starts.

A desktop shortcut and a Start-menu entry are created. Nothing is downloaded at
any point; the application never needs an internet connection.

To remove it: **Settings → Apps → Installed apps → Hybrid PSO-GA Feature
Selection System → Uninstall**.

### Option B — run from source

```bash
cd desktop
python -m pip install -r requirements.txt
python run_app.py
```

Requires Python 3.10 or newer.

### Option C — build the executable yourself

```bash
cd desktop
python -m pip install -r requirements.txt
pyinstaller build/thesis_app.spec --noconfirm
```

This writes `dist/HybridPSOGA/`. Run `dist/HybridPSOGA/HybridPSOGA.exe`.

To also build the installer, install
[Inno Setup 6](https://jrsoftware.org/isdl.php) and run:

```bash
iscc build/installer.iss
```

The setup file appears in `desktop/build/Output/`.

---

## How the detection works

Both detectors follow the thesis exactly. The classifier is a Random Forest of
100 trees; the verdict is the majority vote, and the confidence shown is the
share of trees that agreed.

**Email.** The text is converted into the 57 Spambase attributes using the
official UCI definitions: 48 word frequencies (`100 × occurrences ÷ total
words`), 6 character frequencies (`100 × occurrences ÷ total characters`), and
three statistics about runs of capital letters (average, longest, total). The
vector is normalized with the dataset's own min/max and passed to the forest.

**Website.** The 30 Phishing-Websites attributes are derived from the URL string
itself — IP-address host, URL length, `@` symbol, `//` in the path, hyphen in
the domain, sub-domain count, `https` token in the domain, non-standard port,
and whether the registrable domain appears in a built-in table of well-known
trusted domains. Attributes the original study obtained by fetching the page
(favicon, request URLs, anchors, form handler, redirects, mouse events, iframe,
statistical reports) cannot come from a string, so they take the dataset's
majority value — except for a domain in the trusted table, which takes the
benign value. Trust indicators (domain age, traffic, PageRank, Google index,
DNS record, SSL state) come from that same table, so an unknown domain is never
given the benefit of the doubt.

### What it does not do

It reads the email body text only — not attachments, not SMTP headers, not the
sender's reputation. It reads the URL string only — it does not fetch the page.
The output is a strong statistical indicator, not proof. Always confirm the real
domain or sender before acting.

---

## Published results

| | Spambase (email) | Phishing (website) |
|---|---|---|
| Samples | 4,601 | 11,055 |
| Attributes | 57 | 30 |
| Selected by PSO-GA | 46 | 22 |
| Accuracy | 96.79% | 98.20% |
| Precision | 96.40% | 97.98% |
| Recall | 97.89% | 98.80% |
| F1-score | 97.14% | 98.39% |
| AUC | 0.988 | 0.996 |

The algorithm is stochastic, so a re-run gives slightly different numbers; the
seed can be fixed in the Run-experiment page to make a result reproducible.

### Contradictions inside the thesis

The application records eight places where the thesis text disagrees with
Table 4-4 or with the MATLAB source — for example the mutation rate (text:
adaptive 0.20 → 0.02; table and code: constant 0.2), the inertia weight (text:
0.9 → 0.4; table and code: 0.7), the crossover type (text: two-point; table:
single point), the population size (text and table: 20; `main.m` passes 10),
and the Spambase metrics (abstract: 96.79%; page 24: 96.33%). They are shown
unchanged on the Results page, because the brief is to reproduce the thesis
exactly rather than to silently correct it. The application follows Table 4-4
as the most specific specification.

---

## Programming languages found in the source material

The thesis and the bundled archive use **MATLAB only**. The five `.m` files are
`main.m`, `GA_PSO_feature_selection.m`, `fitness_RF.m`, `repair_solution.m` and
`plot_results.m`, and they call MATLAB functions such as `TreeBagger`,
`randperm`, `perfcurve`, `confusionchart` and `readmatrix`. There is no Python,
Java or C++ anywhere in the submitted material.

This application is a faithful re-implementation in **Python** (with
scikit-learn, pandas, numpy and matplotlib, and PySide6 for the interface). It
was written so the work can be demonstrated on any computer without a MATLAB
licence. Every step matches the MATLAB source: the same cost function
(`fitness_RF.m`), the same PSO velocity update and sigmoid binarisation, the
same crossover and mutation, the same repair step, the same 20% hold-out split
and the same evaluation metrics and curves.

---

## Layout

```
desktop/
├── run_app.py                    launcher
├── requirements.txt
├── verify_app.py                 self-test (66 checks)
├── thesis_app/
│   ├── main.py                   application entry point
│   ├── core/
│   │   ├── engine.py             PSO-GA + Random Forest, the thesis pipeline
│   │   ├── thesis_data.py        every fact, number and equation from the PDF
│   │   ├── feature_meta.py       attribute names, labels and legends
│   │   ├── text_analyzer.py      email text -> 57 Spambase attributes
│   │   └── url_analyzer.py       URL -> 30 Phishing attributes
│   ├── ui/
│   │   ├── main_window.py        shell, sidebar, language switch
│   │   ├── theme.py              colours and stylesheet
│   │   ├── widgets.py            cards, tiles, tables, charts
│   │   ├── i18n.py               223 strings + 17 risk signals, ar/en
│   │   └── pages/                the eleven pages
│   └── assets/
│       ├── data/                 spambase.xlsx, Data_phishing.xlsx
│       ├── figures/              the nine thesis result figures
│       ├── matlab/               the .fig figures and main.asv backup
│       └── *.m                   the original MATLAB sources
├── build/
│   ├── thesis_app.spec           PyInstaller specification
│   ├── installer.iss             Inno Setup installer script
│   ├── make_qa.py                generates the defence Q&A document
│   ├── license.txt
│   └── README_APP.txt
└── docs/
    ├── screenshots/              every page in both languages
    └── اسئلة_واجوبة_المناقشة.html   Arabic Q&A for the defence
```

---

## Verification

```bash
cd desktop
python verify_app.py
```

66 checks: dataset sizes and feature counts, the published values, the
completeness of both language tables, ten known URLs classified correctly, spam
and ham emails classified correctly, every page built and rendered in both
languages, every file from the original archive present, the MATLAB page
showing the real sources, the figures page loading all nine images with their
thesis figure numbers, that all 33 meaningful thesis numbers and all thesis
terms survive in the source, that the US English spelling of the thesis is
kept, that every chapter is still represented, and a short end-to-end
experiment run.
