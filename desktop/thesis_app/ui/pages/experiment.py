"""Experiment page: runs the full thesis pipeline in a worker thread and shows
the convergence curve, ROC curve, confusion matrix, metrics and selected
features as they are produced."""
from __future__ import annotations

import numpy as np
from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout, QLabel,
                               QProgressBar, QSpinBox, QTextEdit,
                               QVBoxLayout, QWidget)

from ...core import engine, thesis_data
from .. import theme
from ..i18n import pick, sep, t
from ..widgets import (StatTile, chart_canvas, make_table, muted,
                       style_axes)
from .base import BasePage


class ExperimentWorker(QObject):
    """Runs ``engine.run_experiment`` off the UI thread."""

    finished = Signal(dict)
    failed = Signal(str)
    progress = Signal(int, int, float)

    def __init__(self, key, n_pop, max_it, desired, test_size, seed):
        super().__init__()
        self.args = (key, n_pop, max_it, desired, test_size, seed)

    def run(self):
        try:
            key, n_pop, max_it, desired, test_size, seed = self.args
            res = engine.run_experiment(
                key, n_pop=n_pop, max_it=max_it, desired=desired,
                test_size=test_size, seed=seed,
                progress=lambda i, n, c: self.progress.emit(i, n, c))
            self.finished.emit(res)
        except Exception as exc:                        # pragma: no cover
            self.failed.emit(f"{type(exc).__name__}: {exc}")


class ExperimentPage(BasePage):
    def build(self):
        self._result = None
        self._thread = None
        self._worker = None

        # ---- controls ----------------------------------------------------
        self.ctrl_card = self.add_card("exp.title", "exp.intro")
        self.ctrl_title = self.ctrl_card.title_label
        self.ctrl_hint = self.ctrl_card.hint_label

        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(14)

        self.dataset_combo = QComboBox()
        for key in ("spambase", "phishing"):
            self.dataset_combo.addItem(engine.THESIS[key]["dataset"], key)
        rl.addLayout(self._field(t("common.dataset"), self.dataset_combo))

        self.npop_spin = QSpinBox()
        self.npop_spin.setRange(2, 100)
        self.npop_spin.setValue(20)
        rl.addLayout(self._field(t("exp.npop"), self.npop_spin))

        self.maxit_spin = QSpinBox()
        self.maxit_spin.setRange(1, 200)
        self.maxit_spin.setValue(20)
        rl.addLayout(self._field(t("exp.maxit"), self.maxit_spin))

        self.desired_spin = QSpinBox()
        self.desired_spin.setRange(1, 60)
        self.desired_spin.setValue(engine.THESIS["spambase"]["n_selected"])
        rl.addLayout(self._field(t("exp.desired"), self.desired_spin))

        self.test_combo = QComboBox()
        self.test_combo.addItem("20%", 0.2)
        self.test_combo.addItem("30%", 0.3)
        rl.addLayout(self._field(t("exp.test_size"), self.test_combo))

        self.seed_spin = QSpinBox()
        self.seed_spin.setRange(0, 9999)
        self.seed_spin.setValue(0)
        rl.addLayout(self._field(t("exp.seed"), self.seed_spin))

        rl.addStretch(1)
        self.run_btn = self.button("exp.start")
        self.run_btn.setObjectName("Primary")
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.setMinimumWidth(180)
        self.run_btn.clicked.connect(self._start)
        rl.addWidget(self.run_btn, 0, Qt.AlignBottom)
        self.ctrl_card.add(row)
        self.dataset_combo.currentIndexChanged.connect(self._sync_desired)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.ctrl_card.add(self.progress)

        # ---- metric tiles -------------------------------------------------
        self.metrics_card = self.add_card("exp.metrics")
        self.metrics_title = self.metrics_card.title_label
        self.tiles = {
            "accuracy": StatTile(t("common.metric"), "—"),
            "precision": StatTile("Precision", "—"),
            "recall": StatTile("Recall", "—"),
            "f1": StatTile("F1", "—"),
            "auc": StatTile("AUC", "—"),
            "selected": StatTile(t("exp.n_selected"), "—"),
            "speedup": StatTile(t("exp.speedup"), "—"),
        }
        g = QGridLayout()
        g.setSpacing(12)
        for i, tile in enumerate(self.tiles.values()):
            g.addWidget(tile, i // 6, i % 6)
        self.metrics_card.add_layout(g)
        self.metric_labels = {
            "accuracy": ("Accuracy", "الدقة"),
            "precision": ("Precision", "الإحكام"),
            "recall": ("Recall", "الاستدعاء"),
            "f1": ("F1-score", "معيار F1"),
            "auc": ("AUC", "المساحة تحت المنحنى"),
            "selected": ("Selected features", "السمات المختارة"),
            "speedup": ("Speed-up", "نسبة التسريع"),
        }
        for name, tile in self.tiles.items():
            tile.set_label(pick(self.metric_labels[name]))

        # ---- charts -------------------------------------------------------
        charts = QWidget()
        cg = QGridLayout(charts)
        cg.setContentsMargins(0, 0, 0, 0)
        cg.setSpacing(16)

        conv_card = self.card("exp.convergence")
        self.conv_title = conv_card.title_label
        self.conv_canvas, self.conv_fig = chart_canvas(250)
        self.conv_ax = self.conv_fig.add_subplot(111)
        conv_card.add(self.conv_canvas)
        cg.addWidget(conv_card, 0, 0)

        roc_card = self.card("exp.roc")
        self.roc_title = roc_card.title_label
        self.roc_canvas, self.roc_fig = chart_canvas(250)
        self.roc_ax = self.roc_fig.add_subplot(111)
        roc_card.add(self.roc_canvas)
        cg.addWidget(roc_card, 0, 1)

        cm_card = self.card("exp.cm")
        self.cm_title = cm_card.title_label
        self.cm_canvas, self.cm_fig = chart_canvas(250)
        self.cm_ax = self.cm_fig.add_subplot(111)
        cm_card.add(self.cm_canvas)
        cg.addWidget(cm_card, 1, 0)

        self.feat_card = self.card("exp.selected_features")
        self.feat_title = self.feat_card.title_label
        self.feat_holder = QWidget()
        self.feat_lay = QVBoxLayout(self.feat_holder)
        self.feat_lay.setContentsMargins(0, 0, 0, 0)
        self.feat_card.add(self.feat_holder)
        cg.addWidget(self.feat_card, 1, 1)

        self.add(charts)

        # ---- log -----------------------------------------------------------
        self.log_card = self.add_card("exp.log")
        self.log_title = self.log_card.title_label
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(150)
        self.log.setStyleSheet("font-family:monospace; font-size:11px;")
        self.log.setLayoutDirection(Qt.LeftToRight)
        self.log_card.add(self.log)

        self._draw_empty()

        # ---- hypothesis check ----------------------------------------------
        self.hyp_card = self.add_card("exp.hypotheses", "exp.hypotheses_note")
        self.hyp_title = self.hyp_card.title_label
        self.hyp_hint = self.hyp_card.hint_label
        self.hyp_holder = QWidget()
        self.hyp_lay = QVBoxLayout(self.hyp_holder)
        self.hyp_lay.setContentsMargins(0, 0, 0, 0)
        self.hyp_lay.setSpacing(10)
        self.hyp_lay.addWidget(
            self.label("exp.hypotheses_empty", "Muted", wrap=True))
        self.hyp_card.add(self.hyp_holder)

        self.stretch()

    # ------------------------------------------------------------------ #
    def _field(self, label: str, widget) -> QVBoxLayout:
        lay = QVBoxLayout()
        lay.setSpacing(4)
        lab = QLabel(label)
        lab.setObjectName("Muted")
        lab.setWordWrap(True)
        lay.addWidget(lab)
        lay.addWidget(widget)
        self.keep(lab, "")          # placeholder; relabeled below
        lab._i18n_key = None
        return lay

    def _sync_desired(self):
        key = self.dataset_combo.currentData()
        self.desired_spin.setValue(engine.THESIS[key]["n_selected"])

    # ------------------------------------------------------------------ #
    def _start(self):
        if self._thread is not None:
            return
        key = self.dataset_combo.currentData()
        self.run_btn.setEnabled(False)
        self.progress.setValue(0)
        self.log.clear()
        self._log(t("exp.busy"))

        self._thread = QThread(self)
        self._worker = ExperimentWorker(
            key, self.npop_spin.value(), self.maxit_spin.value(),
            self.desired_spin.value(), self.test_combo.currentData(),
            self.seed_spin.value())
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)
        self._thread.start()

    def _on_progress(self, i: int, n: int, cost: float):
        self.progress.setValue(int(i / max(1, n) * 100))
        self.progress.setFormat(f"{t('exp.iteration')} {i}/{n} — "
                                f"{t('exp.best_cost')} {cost:.5f}")

    def _on_finished(self, res: dict):
        self._result = res
        self._stop_thread()
        self.progress.setValue(100)
        self.progress.setFormat(t("common.done"))
        self.run_btn.setEnabled(True)
        self._render(res)

    def _on_failed(self, message: str):
        self._stop_thread()
        self.run_btn.setEnabled(True)
        self.progress.setFormat(t("common.error"))
        self._log(f"{t('common.error')}: {message}")

    def _stop_thread(self):
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait(3000)
            self._thread = None
            self._worker = None

    # ------------------------------------------------------------------ #
    def _log(self, text: str):
        self.log.append(text)

    def _render(self, res: dict):
        for name, tile in self.tiles.items():
            if name == "selected":
                tile.set_value(f"{res['n_selected']} / {res['n_features']}")
            elif name == "speedup":
                tile.set_value(f"{res['speedup']:.2f}x")
            elif name == "auc":
                tile.set_value(f"{res['auc']:.3f}")
            else:
                tile.set_value(f"{res[name] * 100:.2f}%")

        self._log(f"{t('exp.n_train')}: {res['n_train']}   "
                  f"{t('exp.n_test')}: {res['n_test']}")
        self._log(f"{t('exp.train_acc')}: {res['train_accuracy'] * 100:.2f}%   "
                  f"{t('exp.test_acc')}: {res['accuracy'] * 100:.2f}%")
        self._log(f"{t('exp.n_selected')}: {res['n_selected']}")
        self._log(f"{t('exp.time_select')}: {res['select_seconds']:.2f}s   "
                  f"{t('exp.time_fit')}: {res['fit_seconds']:.2f}s")
        self._log(f"{t('exp.time_all')}: {res['all_features_seconds']:.2f}s   "
                  f"{t('exp.speedup')}: {res['speedup']:.2f}x")
        for it, cost in enumerate(res["convergence"], start=1):
            self._log(f"  {t('exp.iteration')} {it:>3}   "
                      f"{t('exp.best_cost')} {cost:.5f}")

        self._draw_convergence(res["convergence"])
        self._draw_roc(res["roc"], res["auc"])
        self._draw_cm(res)
        self._draw_features(res["selected_features"])
        self._render_hypotheses(res)

    def _render_hypotheses(self, res: dict):
        """Hypotheses 1-3 of the thesis, checked against this very run."""
        while self.hyp_lay.count():
            item = self.hyp_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        b = res["baseline"]
        rows = [
            [t("common.metric"), t("exp.with_all"), t("exp.with_subset"),
             t("exp.difference")],
        ]
        for key, en, ar in (("accuracy", "Accuracy", "الدقة"),
                            ("precision", "Precision", "الإحكام"),
                            ("recall", "Recall", "الاستدعاء"),
                            ("f1", "F1-score", "معيار F1"),
                            ("auc", "AUC", "المساحة تحت المنحنى")):
            fmt = (lambda v: f"{v:.3f}") if key == "auc" else (lambda v: f"{v * 100:.2f}%")
            delta = res[key] - b[key]
            sign = "+" if delta >= 0 else "−"
            rows.append([pick((en, ar)), fmt(b[key]), fmt(res[key]),
                         f"{sign}{abs(delta):.3f}" if key == "auc"
                         else f"{sign}{abs(delta) * 100:.2f}%"])
        rows.append([t("exp.features_used"), str(res["n_features"]),
                     str(res["n_selected"]),
                     f"−{res['n_features'] - res['n_selected']}"])
        rows.append([t("exp.time_fit"), f"{res['all_features_seconds']:.2f}s",
                     f"{res['fit_seconds']:.2f}s", f"{res['speedup']:.2f}x"])
        self.hyp_lay.addWidget(make_table(
            rows[0], rows[1:], stretch_col=0, max_height=280))

        for idx, en, ar in (
            (1, "Hypothesis 1", "الفرضية 1"),
            (2, "Hypothesis 2", "الفرضية 2"),
            (3, "Hypothesis 3", "الفرضية 3")):
            self.hyp_lay.addWidget(
                muted(f"{pick((en, ar))}: {pick(thesis_data.HYPOTHESES[idx - 1])}"))

    def _draw_empty(self):
        for ax, key in ((self.conv_ax, "exp.convergence"),
                        (self.roc_ax, "exp.roc"),
                        (self.cm_ax, "exp.cm")):
            ax.clear()
            style_axes(ax)
            ax.text(0.5, 0.5, t("chart.no_data"), ha="center", va="center",
                    fontsize=9, color=theme.TEXT_MUTED, wrap=True)
            ax.set_xticks([])
            ax.set_yticks([])
        self.conv_canvas.draw()
        self.roc_canvas.draw()
        self.cm_canvas.draw()

    def _draw_convergence(self, curve):
        ax = self.conv_ax
        ax.clear()
        style_axes(ax, t("exp.convergence"))
        ax.plot(range(1, len(curve) + 1), curve, color=theme.ACCENT,
                linewidth=1.8)
        ax.set_xlabel(t("chart.iteration"), fontsize=8,
                      color=theme.TEXT_MUTED)
        ax.set_ylabel(t("chart.cost"), fontsize=8, color=theme.TEXT_MUTED)
        self.conv_fig.tight_layout()
        self.conv_canvas.draw()

    def _draw_roc(self, roc, auc):
        ax = self.roc_ax
        ax.clear()
        style_axes(ax, f"{t('exp.roc')}   AUC = {auc:.3f}")
        ax.plot(roc["fpr"], roc["tpr"], color=theme.ACCENT, linewidth=1.8,
                label=f"AUC = {auc:.3f}")
        ax.plot([0, 1], [0, 1], "--", color=theme.TEXT_MUTED, linewidth=1)
        ax.set_xlabel(t("chart.fpr"), fontsize=8, color=theme.TEXT_MUTED)
        ax.set_ylabel(t("chart.tpr"), fontsize=8, color=theme.TEXT_MUTED)
        self.roc_fig.tight_layout()
        self.roc_canvas.draw()

    def _draw_cm(self, res):
        ax = self.cm_ax
        ax.clear()
        style_axes(ax, t("exp.cm"))
        cm = np.array(res["confusion_matrix"])
        ax.imshow(cm, cmap="Blues", aspect="auto")
        names = engine.THESIS[res["dataset_key"]]["class_names"]
        ax.set_xticks([0, 1], names, fontsize=8)
        ax.set_yticks([0, 1], names, fontsize=8)
        ax.set_xlabel(t("chart.predicted"), fontsize=8, color=theme.TEXT_MUTED)
        ax.set_ylabel(t("chart.actual"), fontsize=8, color=theme.TEXT_MUTED)
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                        fontsize=11, color="white" if cm[i, j] > cm.max() / 2
                        else theme.TEXT)
        self.cm_fig.tight_layout()
        self.cm_canvas.draw()

    def _draw_features(self, features):
        while self.feat_lay.count():
            item = self.feat_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self.feat_lay.addWidget(muted(f"{len(features)} " + pick(("features",
                                                                  "سمة"))))
        text = QLabel(sep().join(features) if features else "—")
        text.setWordWrap(True)
        text.setObjectName("Body")
        text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.feat_lay.addWidget(text)

    # ------------------------------------------------------------------ #
    def on_show(self):
        if self._result is None:
            self._draw_empty()

    def retranslate(self):
        super().retranslate()
        for name, tile in self.tiles.items():
            tile.set_label(pick(self.metric_labels[name]))
        self._draw_empty() if self._result is None else self._render(
            self._result)
