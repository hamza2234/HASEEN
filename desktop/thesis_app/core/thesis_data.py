"""Every fact, number and equation printed in the thesis, in one place.

Source documents
----------------
* ``ملخص_حسين_ناصر.pdf`` - the 30-page master's thesis (cover page, abstract,
  chapters 1-5).
* ``hussiandamghan.zip``  - the MATLAB implementation
  (``main.m``, ``GA_PSO_feature_selection.m``, ``fitness_RF.m``,
  ``repair_solution.m``, ``plot_results.m``, ``main.asv``) plus the two
  datasets and the eight result figures.

Where the thesis contradicts itself the contradiction is recorded here and
shown in the application, because the brief is to reproduce the thesis exactly
- not to silently "fix" it.
"""
from __future__ import annotations

# --------------------------------------------------------------------------- #
#  Cover page of the PDF - the student's own information                       #
# --------------------------------------------------------------------------- #
COVER = {
    "university": "Damghan University",
    "university_ar": "جامعة دامغان",
    "degree": "Master's Thesis",
    "degree_ar": "رسالة ماجستير",
    "field": "Computer Science (Soft Computing and Artificial Intelligence)",
    "field_ar": "علوم الحاسوب (الحوسبة اللينة والذكاء الاصطناعي)",
    "title": ("Development of a Hybrid Method Based on Particle Swarm "
              "Optimization and Genetic Algorithm for Selecting an Effective "
              "Feature Subset"),
    "title_ar": ("تطوير طريقة هجينة قائمة على تحسين سرب الجسيمات والخوارزمية "
                 "الجينية لاختيار مجموعة سمات فعّالة"),
    "student": "Hussein Naser Hussein",
    "student_ar": "حسين ناصر حسين",
    "supervisor": "Dr. Abdolali Basiri",
    "supervisor_ar": "د. عبد العلي بصيري",
    "date": "May 2026",
    "date_ar": "مايو 2026",
    "keywords": ["Feature Selection", "Genetic Algorithm",
                 "Particle Swarm Optimization", "Machine Learning",
                 "Random Forest", "Classification"],
    "keywords_ar": ["اختيار السمات", "الخوارزمية الجينية",
                    "تحسين سرب الجسيمات", "تعلّم الآلة",
                    "الغابة العشوائية", "التصنيف"],
}

ABSTRACT_EN = (
    "With the increasing volume of data and the growing number of features in "
    "machine learning problems, feature selection has become one of the most "
    "important stages of data preprocessing. The presence of irrelevant and "
    "redundant features can increase computational complexity, reduce "
    "processing speed, and decrease the performance of classification models. "
    "Therefore, the use of optimization-based methods for selecting effective "
    "features plays a significant role in improving the accuracy and "
    "efficiency of machine learning models. In this study, a hybrid method "
    "based on the PSO and GA metaheuristic algorithms is proposed for optimal "
    "feature selection, and its performance is evaluated using the Random "
    "Forest classifier. In the proposed approach, by simultaneously utilizing "
    "the global search capability of the PSO algorithm and the ability of the "
    "Genetic Algorithm to generate diverse solutions, an optimal subset of "
    "effective features was selected. These selected features were then used "
    "as inputs for the Random Forest classification model. To evaluate the "
    "proposed method, the Spambase and Phishing datasets were employed. The "
    "results showed that in the Spambase dataset, 46 features were selected "
    "from the initial 57 features, and the model achieved an accuracy of "
    "96.79%, precision of 96.40%, recall of 97.89%, and an F1-score of "
    "97.14%. In addition, the AUC value of 0.988 indicated the high capability "
    "of the model in distinguishing between classes. In the Phishing dataset, "
    "22 features were selected from the initial 30 features, and the "
    "classification results included an accuracy of 98.20%, precision of "
    "97.98%, recall of 98.80%, and an F1-score of 98.39%. Furthermore, the "
    "AUC value of 0.996 demonstrated the strong discriminative power of the "
    "selected features in separating classes. Overall, the results of this "
    "research indicate that the hybrid PSO-GA method is an effective approach "
    "for feature selection in classification problems and can improve model "
    "performance, reduce computational complexity, and increase processing "
    "speed while simultaneously decreasing the number of features."
)

ABSTRACT_AR = (
    "مع تزايد حجم البيانات وعدد السمات في مسائل تعلّم الآلة، أصبح اختيار "
    "السمات من أهم مراحل المعالجة المسبقة للبيانات. فوجود سمات غير مهمة أو "
    "مكرّرة يزيد التعقيد الحسابي ويقلّل سرعة المعالجة ويخفض أداء نماذج "
    "التصنيف. لذلك فإن استخدام الطرق القائمة على التحسين لاختيار السمات "
    "الفعالة له دور كبير في رفع دقة نماذج تعلّم الآلة وكفاءتها. تقترح هذه "
    "الدراسة طريقة هجينة مبنية على خوارزميتي التحسين الفوقي PSO و GA "
    "لاختيار السمات المثلى، ويُقيَّم أداؤها باستخدام مصنّف الغابة العشوائية. "
    "في الطريقة المقترحة، وبالاستفادة المتزامنة من قدرة البحث الشامل لدى "
    "خوارزمية PSO ومن قدرة الخوارزمية الجينية على توليد حلول متنوّعة، "
    "اختيرت مجموعة مثلى من السمات الفعّالة، ثم استُخدمت هذه السمات المختارة "
    "مدخلات لنموذج تصنيف الغابة العشوائية. ولتقييم الطريقة المقترحة "
    "استُخدمت مجموعتا بيانات Spambase و Phishing. أظهرت النتائج أنّه في "
    "مجموعة Spambase اختيرت 46 سمة من أصل 57 سمة، وحقّق النموذج دقة 96.79% "
    "وإحكاماً 96.40% واستدعاءً 97.89% ومعيار F1 قدره 97.14%. كما دلّت قيمة "
    "AUC البالغة 0.988 على قدرة النموذج العالية في التمييز بين الفئات. وفي "
    "مجموعة Phishing اختيرت 22 سمة من أصل 30 سمة، وضمّنت نتائج التصنيف دقة "
    "98.20% وإحكاماً 97.98% واستدعاءً 98.80% ومعيار F1 قدره 98.39%. وبيّنت "
    "قيمة AUC البالغة 0.996 قدرة السمات المختارة القوية على التمييز في فصل "
    "الفئات. وإجمالاً تشير نتائج هذا البحث إلى أنّ الطريقة الهجينة PSO–GA "
    "نهج فعّال لاختيار السمات في مسائل التصنيف، ويمكنها تحسين أداء النموذج "
    "وتقليل التعقيد الحسابي وزيادة سرعة المعالجة مع تقليل عدد السمات في آن "
    "واحد."
)

# --------------------------------------------------------------------------- #
#  Research questions / objectives / hypotheses (chapter 1)                    #
# --------------------------------------------------------------------------- #
OBJECTIVES = [
    ("Developing an optimal method for selecting effective features",
     "تطوير طريقة مثلى لاختيار السمات الفعّالة",
     "Design and implement a hybrid PSO-GA algorithm that identifies the "
     "subset of features with the greatest impact on classification accuracy, "
     "while reducing computational complexity.",
     "تصميم وتنفيذ خوارزمية هجينة PSO–GA تحدّد مجموعة السمات الأكثر تأثيراً "
     "في دقة التصنيف، مع تقليل التعقيد الحسابي."),
    ("Improving the accuracy and efficiency of learning models",
     "تحسين دقة نماذج التعلّم وكفاءتها",
     "Use the selected features in an advanced classifier (Random Forest) to "
     "raise accuracy and reduce the error rate while minimizing the number of "
     "features used.",
     "استخدام السمات المختارة في مصنّف متقدّم (الغابة العشوائية) لرفع الدقة "
     "وتقليل نسبة الخطأ مع تقليل عدد السمات المستخدمة."),
]

QUESTIONS = [
    ("Can the hybrid PSO-GA algorithm select an optimal and effective subset "
     "of features to improve the accuracy of learning models?",
     "هل تستطيع الخوارزمية الهجينة PSO–GA اختيار مجموعة سمات مثلى وفعّالة "
     "لتحسين دقة نماذج التعلّم؟"),
    ("Does using the features selected by the proposed algorithm increase the "
     "accuracy of advanced classifiers such as the Random Forest compared with "
     "traditional feature-selection methods?",
     "هل يؤدي استخدام السمات المختارة إلى رفع دقة المصنّفات المتقدمة مثل "
     "الغابة العشوائية مقارنةً بطرق اختيار السمات التقليدية؟"),
    ("Which features have the greatest impact on improving model performance, "
     "and what is their role in increasing accuracy and reducing "
     "computational complexity?",
     "ما السمات الأكثر تأثيراً في أداء النموذج، وما دورها في رفع الدقة "
     "وتقليل التعقيد الحسابي؟"),
]

HYPOTHESES = [
    ("The hybrid algorithm identifies an optimal subset that significantly "
     "improves accuracy compared with using all features.",
     "الخوارزمية الهجينة تحدّد مجموعة مثلى تُحسّن الدقة بشكل ملحوظ مقارنةً "
     "باستخدام كل السمات."),
    ("The selected features significantly raise the accuracy of advanced "
     "classifiers (such as Random Forest) compared with traditional "
     "feature-selection methods.",
     "السمات المختارة ترفع دقة المصنّفات المتقدمة (مثل الغابة العشوائية) "
     "بشكل ملحوظ مقارنةً بالطرق التقليدية."),
    ("The selected subset significantly reduces computational complexity "
     "(training time and number of features) without a noticeable drop in "
     "predictive performance.",
     "المجموعة المختارة تقلّل التعقيد الحسابي (زمن التدريب وعدد السمات) "
     "بشكل ملحوظ دون انخفاض ملحوظ في أداء التنبؤ."),
    ("Some features matter far more than others; removing unimportant or "
     "noisy features increases the stability and generalization of the model.",
     "بعض السمات أكثر تأثيراً بكثير من غيرها، وحذف السمات غير المهمة أو "
     "المشوّشة يزيد استقرار النموذج وقدرته على التعميم."),
]

# --------------------------------------------------------------------------- #
#  Equations (chapter 3)                                                       #
# --------------------------------------------------------------------------- #
EQUATIONS = [
    {
        "no": "3-1",
        "name_en": "Min-Max normalization",
        "name_ar": "التطبيع بطريقة Min-Max",
        "latex": r"X_{norm} = \dfrac{X - X_{min}}{X_{max} - X_{min}}",
        "plain": "X_norm = (X - X_min) / (X_max - X_min)",
        "note_en": "Scales every feature into [0,1] so no feature dominates "
                   "the distance calculations. Uses the dataset-wide min/max.",
        "note_ar": "يحوّل كل سمة إلى المجال [0,1] حتى لا تهيمن سمة على "
                   "حسابات المسافة. يستخدم أصغر وأكبر قيمة في كامل البيانات.",
    },
    {
        "no": "3-2",
        "name_en": "PSO velocity update",
        "name_ar": "تحديث سرعة الجسيم في PSO",
        "latex": r"v_i \leftarrow w\,v_i + c_1 r_1 (pbest_i - x_i) "
                 r"+ c_2 r_2 (gbest - x_i)",
        "plain": "v_i = w*v_i + c1*r1*(pbest_i - x_i) + c2*r2*(gbest - x_i)",
        "note_en": "w = inertia weight (0.7), c1 = cognitive acceleration "
                   "coefficient (1.5), c2 = social acceleration coefficient "
                   "(1.5), r1/r2 = uniform random vectors in [0,1].",
        "note_ar": "w = وزن القصور الذاتي (0.7)، c1 = معامل التسارع المعرفي "
                   "(1.5)، c2 = معامل التسارع الاجتماعي (1.5)، r1 و r2 "
                   "متجهان عشوائيان منتظمان في [0,1].",
    },
    {
        "no": "3-3",
        "name_en": "Sigmoid binarization",
        "name_ar": "التحويل إلى قيم ثنائية بدالة sigmoid",
        "latex": r"s(v_i) = \dfrac{1}{1 + e^{-v_i}}",
        "plain": "s(v_i) = 1 / (1 + exp(-v_i))",
        "note_en": "Converts the real-valued velocity into a probability of "
                   "selecting that feature. The search space is binary, so a "
                   "continuous velocity has to be mapped back to {0,1}.",
        "note_ar": "يحوّل السرعة الحقيقية إلى احتمال اختيار السمة. فضاء البحث "
                   "ثنائي، لذلك لا بد من تحويل السرعة المستمرة إلى 0 أو 1.",
    },
    {
        "no": "3-4",
        "name_en": "Binary position update",
        "name_ar": "تحديث الموضع الثنائي",
        "latex": r"x_i = \begin{cases} 1 & s(v_i) > rand \\ 0 & "
                 r"\text{otherwise} \end{cases}",
        "plain": "x_i = 1 if s(v_i) > rand, else 0",
        "note_en": "rand is a uniform random number in [0,1]; the feature is "
                   "selected when the sigmoid value exceeds it.",
        "note_ar": "rand عدد عشوائي منتظم في [0,1]؛ تُختار السمة إذا تجاوزت "
                   "قيمة sigmoid هذا العدد.",
    },
    {
        "no": "3-5",
        "name_en": "Cost (fitness) function",
        "name_ar": "دالة الكلفة (اللياقة)",
        "latex": r"Cost = (1 - Accuracy) + \alpha \cdot "
                 r"\dfrac{|S|}{|D|}",
        "plain": "Cost = (1 - Accuracy) + alpha * (|S| / |D|)",
        "note_en": "alpha = 0.99. The first term is the classification error, "
                   "the second penalizes large subsets. The MATLAB source "
                   "computes the penalty as |S| / desired instead of |S| / |D|.",
        "note_ar": "alpha = 0.99. الحد الأول هو خطأ التصنيف، والثاني عقوبة "
                   "على كبر حجم المجموعة. شيفرة MATLAB تحسب العقوبة "
                   "|S| / العدد المطلوب بدل |S| / |D|.",
    },
]

# --------------------------------------------------------------------------- #
#  Pre-processing pipeline (chapter 3)                                         #
# --------------------------------------------------------------------------- #
PREPROCESSING = [
    ("Missing values",
     "Missing-value handling",
     "The three nearest neighbors method with K = 3: for each sample with a "
     "missing value, the three closest samples in feature space are found and "
     "the missing value is estimated from the average of the same feature "
     "among them. This preserves the statistical structure of the data and "
     "prevents bias in the data.",
     "القيم المفقودة",
     "معالجة القيم المفقودة",
     "طريقة الجيران الثلاثة الأقرب بمعامل K = 3: لكل عيّنة فيها قيمة مفقودة "
     "تُحدَّد أقرب ثلاث عيّنات في فضاء السمات، وتُقدَّر القيمة المفقودة من "
     "متوسط القيمة نفسها عند هذه العيّنات."),
    ("Normalization",
     "Min-Max normalization",
     "Every feature is rescaled to [0,1] (equation 3-1) so that all features "
     "share one scale and the optimization search is stable.",
     "التطبيع",
     "تطبيع Min-Max",
     "تُعاد كل سمة إلى المجال [0,1] (المعادلة 3-1) لتشترك كل السمات في مقياس "
     "واحد ويكون البحث في خوارزمية التحسين مستقراً."),
    ("Train/test split",
     "Hold-out split",
     "The data is split into a training set and a test set. The training set "
     "trains the model and drives feature selection; the test set is only "
     "touched at the very end, so the feature selection is carried out "
     "without using information from the test data and without the "
     "interference of future information. This prevents overfitting and data "
     "leakage.",
     "التقسيم",
     "تقسيم تدريب/اختبار",
     "تُقسَم البيانات إلى مجموعة تدريب ومجموعة اختبار. التدريب يدرّب النموذج "
     "ويوجّه اختيار السمات، والاختبار لا يُلمَس إلا في النهاية، وهذا يمنع "
     "الإفراط في التعلّم ويوقف تسرّب البيانات."),
]

# --------------------------------------------------------------------------- #
#  The hybrid algorithm, stage by stage (chapter 3, section 2)                 #
# --------------------------------------------------------------------------- #
ALGORITHM_STAGES = [
    ("Encoding",
     "Representation",
     "Each solution is represented as a binary vector (binary chromosome) "
     "whose length equals the number of features: 1 means the feature is "
     "selected, 0 means it is dropped. The search space is therefore 2^n, "
     "which cannot be enumerated directly.",
     "التمثيل",
     "الترميز",
     "كل حل كروموسوم ثنائي بطول عدد السمات: القيمة 1 تعني أن السمة مختارة "
     "و0 تعني محذوفة. فضاء البحث إذن 2^n، وهو ما يستحيل استقصاؤه مباشرةً."),
    ("PSO stage",
     "Particle Swarm Optimization update",
     "Each particle has a binary position and a real-valued velocity. The "
     "velocity is updated by equation 3-2, converted to a selection "
     "probability by the sigmoid (3-3), then binarized (3-4). This guides the "
     "population towards the best regions discovered so far; the inertia "
     "weight balances exploration of the search space against exploitation "
     "of promising areas.",
     "مرحلة PSO",
     "تحديث سرب الجسيمات",
     "لكل جسيم موضع ثنائي وسرعة حقيقية. تُحدَّث السرعة بالمعادلة 3-2، ثم "
     "تُحوَّل إلى احتمال اختيار بدالة sigmoid (3-3)، ثم إلى قيمة ثنائية "
     "(3-4). هذا يوجّه المجتمع نحو أفضل المناطق المكتشفة."),
    ("GA stage",
     "Genetic operators",
     "Two-point crossover first (the thesis text) combines meaningful blocks "
     "of features; then adaptive mutation with a decreasing probability "
     "(0.20 to 0.02) performs a bit value inversion, flipping single bits to "
     "escape local optima and to prevent premature convergence.",
     "مرحلة GA",
     "المعاملات الجينية",
     "التقاطع بنقطتين أولاً (كما في نص الرسالة) يجمع كتلاً ذات معنى من "
     "السمات؛ ثم الطفرة التكيفية باحتمال متناقص (من 0.20 إلى 0.02) تُجري "
     "قلباً لقيمة البتة فتحوّل بتات مفردة للخروج من القيم المثلى المحلية."),
    ("Repair",
     "Feasibility repair",
     "repair_solution.m forces the chromosome to hold exactly the desired "
     "number of selected features, so every candidate solution is comparable.",
     "الإصلاح",
     "إصلاح الحل",
     "الدالة repair_solution.m تجبر الكروموسوم على حمل العدد المطلوب بالضبط "
     "من السمات المختارة، فيكون كل حل مرشّح قابلاً للمقارنة."),
    ("Elitism",
     "Elite retention and external archive",
     "The elite mechanism copies the best individual into the next generation "
     "unchanged, so a good solution is never lost to a random operator. An "
     "external archive records the best answers found during the whole run and "
     "prevents the accumulation of near-duplicate solutions.",
     "النخبة",
     "حفظ النخبة والأرشيف الخارجي",
     "آلية النخبة تنقل أفضل فرد إلى الجيل التالي دون تغيير، فلا يُفقد حل جيد "
     "بسبب معامل عشوائي. ويحفظ أرشيف خارجي أفضل الحلول طوال التنفيذ ويمنع "
     "تكدّس الحلول المتشابهة."),
    ("Fitness",
     "Cost evaluation",
     "The fitness function measures the quality of each subset: if no feature "
     "is selected the cost is 1, otherwise the data is subsampled on the "
     "selected features and the Random Forest is trained with 5-fold "
     "cross-validation and 100 trees per fold, and the average accuracy is "
     "combined with the feature-count penalty (equation 3-5).",
     "اللياقة",
     "تقييم الكلفة",
     "دالة اللياقة تقيس جودة كل مجموعة: إذا لم تُختَر أي سمة فالكلفة 1، "
     "وإلا يُدرَّب مصنّف الغابة العشوائية على السمات المختارة بتحقق متقاطع "
     "خماسي و100 شجرة في كل جزء، ويُدمج متوسط الدقة مع عقوبة عدد السمات "
     "(المعادلة 3-5)."),
]

# --------------------------------------------------------------------------- #
#  The classifier (chapter 3, section 3)                                       #
# --------------------------------------------------------------------------- #
CLASSIFIER_FACTS = [
    ("Algorithm", "Random Forest (ensemble of decision trees)",
     "الخوارزمية", "الغابة العشوائية (تجميع أشجار قرار)"),
    ("Number of trees", "100 trees in the final model (TreeBagger(100, ...))",
     "عدد الأشجار", "100 شجرة في النموذج النهائي"),
    ("Aggregation", "Bagging - each tree is grown on a bootstrap sample drawn "
                    "with replacement",
     "طريقة التجميع", "Bagging — كل شجرة على عيّنة عشوائية بإرجاع"),
    ("Feature sampling", "At each node only a random subset of the features is "
                         "considered for the best split. Every internal node "
                         "of a tree splits the samples it receives; the "
                         "terminal nodes, or leaf nodes, carry the class label "
                         "that the tree proposes",
     "انتقاء السمات", "في كل عقدة تُفحص مجموعة فرعية عشوائية من السمات "
                       "لإيجاد أفضل تقسيم. وكل عقدة داخلية في الشجرة تقسم "
                       "العيّنات الواصلة إليها، أما العقد الطرفية (الأوراق) "
                       "فتحمل اسم الفئة التي تقترحها الشجرة"),
    ("Decision rule", "Majority voting mechanism: every one of the 100 trees "
                      "votes for a label and the class with the most votes is "
                      "the final output, which neutralizes individual tree "
                      "errors and raises the final accuracy",
     "آلية القرار", "تصويت الأغلبية: كل شجرة من الأشجار المئة تصوّت لفئة، "
                     "والفئة الأكثر أصواتاً هي المخرج النهائي، وهذا يحيّد "
                     "أخطاء الأشجار المفردة ويرفع الدقة النهائية"),
    ("Variance", "The 100-tree configuration keeps an optimal balance "
                 "between classification accuracy and computational "
                 "complexity, and ensures that the variance of the model is "
                 "minimized",
     "التباين", "إعداد المئة شجرة يحقق توازناً أمثل بين دقة التصنيف والتعقيد "
                "الحسابي، ويضمن تقليل تباين النموذج"),
    ("Split criterion", "Gini index (Gini impurity) is used to determine the "
                        "best feature for splitting nodes and to minimize data "
                        "impurity at each stage. The thesis also describes the "
                        "split as chosen at each node using criteria such as "
                        "reducing uncertainty or increasing entropy",
     "معيار التقسيم", "يُستخدم مؤشر جيني (Gini impurity) لتحديد أفضل سمة "
                       "لتقسيم العقد وتقليل شوائب البيانات في كل مرحلة. وتصف "
                       "الرسالة أيضاً اختيار التقسيم في كل عقدة بمعايير مثل "
                       "تقليل عدم اليقين أو زيادة الإنتروبيا"),
    ("Why it is used", "Its ensemble learning structure learns complex "
                       "patterns and effectively counters overfitting; the two "
                       "levels of randomization (bootstrap sampling and random "
                       "feature selection) decorrelate the trees and raise the "
                       "structural diversity of the model. Because the trees "
                       "are built independently, the ensemble implicitly "
                       "benefits from a form of parallel learning, which also "
                       "raises computational efficiency. Each tree keeps "
                       "splitting until stopping criteria such as reaching a "
                       "certain depth are met.",
     "سبب اختياره", "بنية التعلّم التجميعي تتعلّم أنماطاً معقدة وتقاوم "
                    "الإفراط في التعلّم؛ ومستويا العشوائية (العيّنة بالإرجاع "
                    "وانتقاء السمات) يقلّلان الارتباط بين الأشجار ويرفعان "
                    "تنوّع النموذج البنيوي. ولأن الأشجار تُبنى باستقلالية "
                    "يستفيد التجميع ضمناً من شكل من التعلّم المتوازي، وهو ما "
                    "يرفع الكفاءة الحسابية أيضاً. وتستمر كل شجرة في التقسيم "
                    "حتى تتحقق معايير توقّف مثل بلوغ عمق معيّن."),
    ("Batch nature and retraining",
     "Unlike some progressive algorithms, Random Forest has a batch nature: "
     "after the initial training the structure of the trees stays fixed, and "
     "if data has to be changed or added the model must be retrained from the "
     "beginning. In this study the model is retrained at every fitness "
     "calculation using only the selected features of that same stage, so the "
     "measured quality of each subset reflects the real behavior of the "
     "classifier under future conditions.",
     "الطبيعة الدفعية وإعادة التدريب",
     "بخلاف بعض الخوارزميات التقدمية، فإن الغابة العشوائية ذات طبيعة دفعية: "
     "فبعد التدريب الأولي يبقى بنية الأشجار ثابتة، وإذا لزم تغيير البيانات "
     "أو إضافتها وجب إعادة تدريب النموذج من البداية. وفي هذه الدراسة "
     "يُعاد تدريب النموذج عند كل حساب للياقة باستخدام السمات المختارة في "
     "المرحلة نفسها فقط، فيعكس قياس جودة كل مجموعة السلوك الحقيقي للمصنّف "
     "في الظروف المستقبلية."),
]

# --------------------------------------------------------------------------- #
#  Evaluation metrics                                                          #
# --------------------------------------------------------------------------- #
METRICS = [
    ("Accuracy", "الدقة", "(TP + TN) / (TP + TN + FP + FN)",
     "Share of all predictions that were correct.",
     "نسبة كل التنبؤات الصحيحة."),
    ("Precision", "الإحكام", "TP / (TP + FP)",
     "Of everything flagged as the positive class, how much really was.",
     "من كل ما صُنّف في الفئة الموجبة، كم كان فعلاً منها."),
    ("Recall", "الاستدعاء", "TP / (TP + FN)",
     "Of everything that really was positive, how much was found.",
     "من كل ما هو فعلاً في الفئة الموجبة، كم تم اكتشافه."),
    ("F1-score", "معيار F1", "2 * (P * R) / (P + R)",
     "Harmonic mean of precision and recall; balances the two.",
     "المتوسط التوافقي بين الإحكام والاستدعاء؛ يوازن بينهما."),
    ("AUC", "المساحة تحت المنحنى", "integral of TPR over FPR",
     "Area under the ROC curve, which plots TPR against FPR at different "
     "decision thresholds and so measures the discriminative ability of the "
     "model. 1.0 is a perfect separator, 0.5 is random guessing.",
     "المساحة تحت منحنى ROC الذي يرسم نسبة الإيجابيات الصحيحة مقابل نسبة "
     "الإيجابيات الخاطئة عند عتبات قرار مختلفة، فيقيس قدرة النموذج على "
     "التمييز. القيمة 1.0 فصل مثالي، و0.5 تخمين عشوائي."),
    ("Sensitivity", "الحساسية", "TPR = TP / (TP + FN)",
     "Same quantity as recall: the share of real positives that were found. "
     "The thesis stresses that in phishing detection both sensitivity and "
     "specificity are crucial.",
     "الكمية نفسها التي يقيسها الاستدعاء: نسبة الحالات الموجبة الحقيقية التي "
     "تم اكتشافها. وتشدّد الرسالة على أن الحساسية والنوعية معاً حرجتان في "
     "كشف التصيّد."),
    ("Specificity", "النوعية", "TNR = TN / (TN + FP)",
     "The share of real negatives that were correctly rejected; the complement "
     "of the false positive rate.",
     "نسبة الحالات السالبة الحقيقية التي رُفضت بشكل صحيح؛ وهي مكمّل نسبة "
     "الإيجابيات الخاطئة."),
]

# --------------------------------------------------------------------------- #
#  Chapter 4 - the numbers, plus the contradictions                            #
# --------------------------------------------------------------------------- #
CH4_PAGE24 = {
    "spambase": {"accuracy": 96.33, "precision": 95.43, "recall": 94.65,
                 "f1": 95.04},
    "phishing": {"accuracy": 98.20, "precision": 97.98, "recall": 98.80,
                 "f1": 98.39},
}

CONFLICTS = [
    {
        "topic_en": "Mutation rate (Pm)",
        "topic_ar": "معدّل الطفرة (Pm)",
        "text_en": "Decreases adaptively from 0.20 at the start to 0.02 at "
                   "the end of the run.",
        "text_ar": "يتناقص تكيفياً من 0.20 في البداية إلى 0.02 في النهاية.",
        "table_en": "Table 4-4 lists a constant 0.2.",
        "table_ar": "الجدول 4-4 يذكر القيمة الثابتة 0.2.",
        "code_en": "GA_PSO_feature_selection.m uses a constant "
                   "mutation_rate = 0.2.",
        "code_ar": "الملف GA_PSO_feature_selection.m يستخدم 0.2 ثابتة.",
    },
    {
        "topic_en": "Inertia weight (w)",
        "topic_ar": "معامل القصور الذاتي (w)",
        "text_en": "Decreases linearly from 0.9 to 0.4 over the iterations.",
        "text_ar": "يتناقص خطياً من 0.9 إلى 0.4 على مدى التكرارات.",
        "table_en": "Table 4-4 lists a constant 0.7.",
        "table_ar": "الجدول 4-4 يذكر القيمة الثابتة 0.7.",
        "code_en": "The MATLAB source hard-codes w = 0.7.",
        "code_ar": "شيفرة MATLAB تثبّت w = 0.7.",
    },
    {
        "topic_en": "Learning coefficients (c1, c2)",
        "topic_ar": "معاملا التعلّم (c1, c2)",
        "text_en": "Both are taken as 2.",
        "text_ar": "كلاهما يأخذ القيمة 2.",
        "table_en": "Table 4-4 lists 1.5 for both.",
        "table_ar": "الجدول 4-4 يذكر 1.5 لكل منهما.",
        "code_en": "The MATLAB source sets c1 = c2 = 1.5.",
        "code_ar": "شيفرة MATLAB تضبط c1 = c2 = 1.5.",
    },
    {
        "topic_en": "Crossover type",
        "topic_ar": "نوع التقاطع",
        "text_en": "Two-point crossover with cut points between 2 and "
                   "nVar-1.",
        "text_ar": "تقاطع بنقطتين، ونقطتا القطع بين 2 و nVar-1.",
        "table_en": "Table 4-4 lists Single Point.",
        "table_ar": "الجدول 4-4 يذكر التقاطع النقطي (نقطة واحدة).",
        "code_en": "The implemented crossover is a single blend step "
                   "(alpha*parent1 + (1-alpha)*parent2).",
        "code_ar": "التقاطع المنفّذ خطوة خلط واحدة "
                   "(alpha*الأب1 + (1-alpha)*الأب2).",
    },
    {
        "topic_en": "Population size (nPop)",
        "topic_ar": "حجم المجتمع (nPop)",
        "text_en": "The text states 20 and justifies it as a balance between "
                   "search quality and time.",
        "text_ar": "النص يذكر 20 ويبرّرها بأنها توازن بين جودة البحث والزمن.",
        "table_en": "Table 4-4 lists 20.",
        "table_ar": "الجدول 4-4 يذكر 20.",
        "code_en": "main.m actually passes nPop = 10.",
        "code_ar": "الملف main.m يمرّر فعلياً nPop = 10.",
    },
    {
        "topic_en": "Desired feature count (Spambase)",
        "topic_ar": "عدد السمات المطلوبة (Spambase)",
        "text_en": "46 features selected from the initial 57 (abstract and "
                   "chapter 4).",
        "text_ar": "46 سمة مختارة من أصل 57 (الملخص والفصل الرابع).",
        "table_en": "Table 4-4 does not give a count.",
        "table_ar": "الجدول 4-4 لا يعطي عدداً.",
        "code_en": "main.m uses desired_features = 47.",
        "code_ar": "الملف main.m يستخدم desired_features = 47.",
    },
    {
        "topic_en": "Spambase metric values",
        "topic_ar": "قيم مقاييس Spambase",
        "text_en": "Abstract and conclusion: accuracy 96.79%, precision "
                   "96.40%, recall 97.89%, F1 97.14%.",
        "text_ar": "الملخص والاستنتاج: الدقة 96.79%، الإحكام 96.40%، "
                   "الاستدعاء 97.89%، F1 97.14%.",
        "table_en": "Page 24 gives a different set: 96.33%, 95.43%, 94.65%, "
                    "95.04%.",
        "table_ar": "صفحة 24 تعطي مجموعة مختلفة: 96.33% و95.43% و94.65% "
                    "و95.04%.",
        "code_en": "The published confusion matrix [[538,20],[23,339]] yields "
                   "accuracy 95.33% and precision 94.43%, matching neither "
                   "set.",
        "code_ar": "مصفوفة الالتباس المنشورة [[538,20],[23,339]] تعطي دقة "
                   "95.33% وإحكاماً 94.43%، ولا تطابق أيّاً من المجموعتين.",
    },
    {
        "topic_en": "Cross-validation",
        "topic_ar": "التحقق المتقاطع",
        "text_en": "5-fold cross-validation inside the fitness function.",
        "text_ar": "تحقق متقاطع خماسي داخل دالة اللياقة.",
        "table_en": "Table 4-4 lists K = 5.",
        "table_ar": "الجدول 4-4 يذكر K = 5.",
        "code_en": "fitness_RF.m does not cross-validate; it fits one "
                   "TreeBagger(50) on the training data and scores it on the "
                   "same data.",
        "code_ar": "الدالة fitness_RF.m لا تُجري تحققاً متقاطعاً؛ تدرّب "
                   "TreeBagger(50) على بيانات التدريب وتقيّمها على نفسها.",
    },
]

# --------------------------------------------------------------------------- #
#  Chapter 1 - problem statement and importance of the research                #
# --------------------------------------------------------------------------- #
PROBLEM_STATEMENT_EN = (
    "As large and complex datasets become common, the sheer number of features "
    "has turned into one of the main challenges in machine learning and data "
    "analysis. Features may be textual, numeric, structural or behavioral, and "
    "each contributes differently to the prediction models. Many of them are "
    "unimportant, redundant or noisy, and using them lowers accuracy, raises the "
    "error rate and increases computational complexity. Ineffective features "
    "also inflate the dimensionality of the data, and with it the training time "
    "and the consumption of computational resources, while the overall "
    "efficiency of the learning process drops. Selecting effective features in "
    "an optimal, targeted way is therefore a crucial preprocessing step: it "
    "simplifies models, cuts computational cost and raises prediction accuracy. "
    "The feature selection problem can be seen as a multi-objective optimization "
    "problem whose goal is to maximize prediction accuracy and minimize the "
    "number of features used at the same time. In practice the search space of "
    "all possible feature combinations is far too large to explore exhaustively, "
    "which is why researchers turn to intelligent, population-based algorithms "
    "that can search a large feature space efficiently and find optimal subsets."
)
PROBLEM_STATEMENT_AR = (
    "مع انتشار البيانات الكبيرة والمعقّدة، أصبح العدد الكبير من السمات أحد "
    "أهم التحديات في تعلّم الآلة وتحليل البيانات. فقد تكون السمات نصية أو "
    "عددية أو بنيوية أو سلوكية، ولكل منها إسهام مختلف في نماذج التنبؤ. وكثير "
    "منها غير مهم أو مكرّر أو مشوّش، واستخدامه يخفض الدقة ويرفع نسبة الخطأ "
    "ويزيد التعقيد الحسابي. كما أن السمات غير الفعّالة تضخّم أبعاد البيانات، "
    "ومعها زمن التدريب واستهلاك الموارد الحسابية، بينما تنخفض الكفاءة العامة "
    "لعملية التعلّم. لذلك فإن الاختيار الأمثل والموجَّه للسمات الفعّالة خطوة "
    "معالجة مسبقة بالغة الأهمية: فهي تبسّط النماذج وتقلّل الكلفة الحسابية "
    "وترفع دقة التنبؤ. ويمكن النظر إلى مسألة اختيار السمات كمسألة تحسين "
    "متعددة الأهداف هدفها تعظيم دقة التنبؤ وتقليل عدد السمات المستخدمة في "
    "الوقت نفسه. وعملياً فإن فضاء البحث بكل التوليفات الممكنة للسمات أكبر "
    "كثيراً من أن يُستكشف استكشافاً شاملاً، ولذلك يتجه الباحثون إلى الخوارزميات "
    "الذكية القائمة على الجمهرة القادرة على البحث بكفاءة في فضاء سمات واسع "
    "وإيجاد المجموعات المثلى."
)

IMPORTANCE_EN = (
    "With the increase in the volume and complexity of data in various machine "
    "learning problems, the presence of a large number of features has become "
    "one of the main challenges in data analysis. Many of these features are "
    "unimportant, redundant or noisy, and their use can reduce the accuracy of "
    "models, increase the error rate and increase computational complexity; "
    "effective feature selection therefore plays a key role in improving "
    "accuracy, reducing data volume and increasing the efficiency of models. "
    "The feature selection problem can be defined as a multi-objective "
    "optimization problem whose simultaneous goal is to maximize the prediction "
    "accuracy and minimize the number of features used, and because the search "
    "space has such large dimensions it is practically impossible to explore "
    "all possible combinations of features. To solve this problem, the use of "
    "intelligent and population-based algorithms is proposed. Particle Swarm "
    "Optimization is able to find effective subsets of features by searching "
    "the solution space as a group, but it may get stuck in local optima. The "
    "Genetic Algorithm, on the other hand, raises search diversity through "
    "crossover and mutation operators but usually converges more slowly. "
    "Combining the two prevents the search from getting stuck in local optima "
    "and improves the feature selection process while keeping the search speed. "
    "The main goal of this research is to develop an intelligent, optimal "
    "method for feature selection based on a combination of particle swarm "
    "optimization and a genetic algorithm that can identify an effective subset "
    "of features, raise the accuracy of learning models, and at the same time "
    "reduce computational complexity and processing time. The method can serve "
    "as a general feature selection framework in various machine learning "
    "problems and is highly generalizable."
)
IMPORTANCE_AR = (
    "مع تزايد حجم البيانات وتعقيدها في مسائل تعلّم الآلة المختلفة، أصبح وجود "
    "عدد كبير من السمات أحد التحديات الرئيسية في تحليل البيانات. وكثير من هذه "
    "السمات غير مهم أو مكرّر أو مشوّش، واستخدامها يقلّل دقة النماذج ويزيد معدّل "
    "الخطأ والتعقيد الحسابي؛ لذلك فإن اختيار السمات الفعّال يؤدي دوراً محورياً "
    "في رفع الدقة وتقليل حجم البيانات وزيادة كفاءة النماذج. ويمكن تعريف مسألة "
    "اختيار السمات كمسألة تحسين متعدّدة الأهداف هدفها المتزامن تعظيم دقة "
    "التنبؤ وتقليل عدد السمات المستخدمة، ولأن فضاء البحث بهذه الأبعاد الكبيرة "
    "يستحيل عملياً استقصاء جميع التوليفات الممكنة للسمات. ولحلّ هذه المسألة "
    "يُقترح استخدام الخوارزميات الذكية والقائمة على المجتمع. وخوارزمية سرب "
    "الجسيمات قادرة على إيجاد مجموعات سمات فعّالة بالبحث الجماعي في "
    "فضاء الحلول، لكنها قد تعلق في الأمثلة المحلية. أما الخوارزمية الجينية "
    "فترفع تنوّع البحث عبر عاملي التقاطع والطفرة، لكنها عادةً أبطأ في التقارب. "
    "والجمع بينهما يمنع البحث من التعلّق في الأمثلة المحلية ويحسّن عملية اختيار "
    "السمات مع الحفاظ على سرعة البحث. والهدف الرئيسي من هذا البحث هو تطوير "
    "طريقة ذكية ومثلى لاختيار السمات قائمة على الجمع بين تحسين سرب الجسيمات "
    "والخوارزمية الجينية، قادرة على تحديد مجموعة سمات فعّالة ورفع دقة نماذج "
    "التعلّم وتقليل التعقيد الحسابي وزمن المعالجة في الوقت نفسه. ويمكن استخدام "
    "هذه الطريقة كإطار عام لاختيار السمات في مسائل تعلّم الآلة المختلفة، وهي "
    "عالية القابلية للتعميم."
)

# --------------------------------------------------------------------------- #
#  Chapter 4 - convergence behavior, per dataset                              #
# --------------------------------------------------------------------------- #
CONVERGENCE = {
    "spambase": {
        "start_cost": "2.2e-3",
        "final_cost": "1e-3",
        "stable_from": 17,
        "en": "The cost falls uniformly and stepwise over the 20 iterations. In "
              "the first iterations it sits around 2.2e-3, a mix of the "
              "classification error and the relatively large feature count. "
              "Relatively large jumps follow, caused by the genetic component "
              "(crossover and mutation) creating high diversity in the initial "
              "population and rapidly exploring different parts of the search "
              "space. In the middle the cost keeps falling with a gentler slope, "
              "the equilibrium stage where PSO uses the collective knowledge and "
              "individual experience of the particles to head for more stable "
              "regions. After about 17 iterations the cost stabilizes around "
              "1e-3 and barely moves until the end, which means a balance between "
              "classification accuracy and the number of selected features has "
              "been reached and further optimization has no noticeable effect. "
              "At the end of the optimization process the hybrid PSO-GA "
              "algorithm identified and selected 46 features from the initial 57 "
              "features of the Spambase dataset as the more effective and "
              "important features.",
        "ar": "تنخفض الكلفة بانتظام وعلى شكل درجات خلال التكرارات العشرين. وفي "
              "التكرارات الأولى تستقر حول 2.2e-3، وهي مزيج من خطأ التصنيف وعدد "
              "السمات الكبير نسبياً. ثم تُلاحَظ قفزات كبيرة نسبياً سببها المكوّن "
              "الجيني (التقاطع والطفرة) الذي يُنشئ تنوّعاً عالياً في المجتمع "
              "الأولي ويستكشف أجزاء مختلفة من فضاء البحث بسرعة. وفي منتصف "
              "المسار تستمر الكلفة في الانخفاض بميل ألطف، وهي مرحلة التوازن حيث "
              "يستخدم PSO المعرفة الجماعية والخبرة الفردية للجسيمات للتوجّه إلى "
              "مناطق أكثر استقراراً. وبعد نحو 17 تكراراً تستقر الكلفة حول 1e-3 "
              "ولا تكاد تتغيّر حتى النهاية، وهذا يعني تحقّق توازن بين دقة التصنيف "
              "وعدد السمات المختارة وأن التحسين الإضافي بلا أثر ملحوظ. وفي نهاية "
              "عملية التحسين حدّدت الخوارزمية الهجينة PSO–GA واختارت 46 سمة من "
              "أصل 57 سمة أولية في مجموعة Spambase باعتبارها السمات الأكثر "
              "فعالية وأهمية.",
    },
    "phishing": {
        "start_cost": "steep drop",
        "final_cost": "stable",
        "stable_from": 9,
        "en": "The cost falls with a steep slope in the initial iterations, which "
              "shows the algorithm succeeded in discarding a large portion of "
              "unsuitable feature combinations very early and moving towards more "
              "promising areas. After that the slope becomes gentler and the "
              "curve gradually approaches a stable region; from about the ninth "
              "iteration onwards the cost changes very little, indicating a "
              "converged state where further improvements are possible only on a "
              "very small scale. The search has reached a good balance between "
              "broad search early and focused search late, and aimless "
              "fluctuations and getting stuck in shallow spots have been avoided. "
              "The final result on the phishing dataset is that out of the "
              "initial 30 features, 22 features have been selected as the "
              "superior feature set; besides reducing the data volume and "
              "simplifying the model, selecting this optimal subset has increased "
              "the processing speed and focused the model on the features that "
              "are truly influential in distinguishing healthy and phishing "
              "samples.",
        "ar": "تنخفض الكلفة بميل حاد في التكرارات الأولى، وهذا يدل على أن "
              "الخوارزمية نجحت في إسقاط جزء كبير من توليفات السمات غير المناسبة "
              "في مرحلة مبكرة جداً والتوجّه إلى مناطق أكثر إشراقاً في فضاء البحث. "
              "وبعد ذلك يصبح الميل ألطف ويقترب المنحنى تدريجياً من منطقة "
              "مستقرة؛ فمن نحو التكرار التاسع تصبح تغيّرات الكلفة محدودة جداً، "
              "وهذا يدل على بلوغ حالة تقارب لا تُتاح فيها تحسينات إضافية إلا على "
              "نطاق ضيق جداً. وقد بلغ البحث توازناً جيداً بين البحث الواسع في "
              "البداية والبحث المركّز في النهاية، مع تجنّب التذبذب العشوائي "
              "والتعلّق في مواضع ضحلة. والنتيجة النهائية لتشغيل الخوارزمية على "
              "مجموعة Phishing هي أنّه من أصل ثلاثين سمة أولية اختيرت 22 سمة "
              "كمجموعة السمات المتفوّقة؛ وإلى جانب تقليل حجم البيانات وتبسيط "
              "النموذج، فقد رفع اختيار هذه المجموعة المثلى سرعة المعالجة "
              "وركّز النموذج على السمات المؤثرة فعلاً في التمييز بين العيّنات "
              "السليمة وعيّنات التصيّد.",
    },
}

# --------------------------------------------------------------------------- #
#  Chapter 5 - conclusion                                                      #
# --------------------------------------------------------------------------- #
CONCLUSION_EN = (
    "The results show that the hybrid PSO-GA method is an effective approach "
    "for feature selection in classification problems. It improved model "
    "performance, reduced computational complexity and increased processing "
    "speed while simultaneously decreasing the number of features. The "
    "stability of the results across two different datasets indicates the "
    "reliability and generalizability of the method. Finally, it can be "
    "stated that feature selection using metaheuristic algorithms, especially "
    "hybrid methods, can play an important role in increasing the efficiency "
    "of machine learning models, and the method presented in this research "
    "has also been able to provide acceptable results in this field."
)

CONCLUSION_AR = (
    "أظهرت النتائج أن الطريقة الهجينة PSO–GA منهج فعّال لاختيار السمات في "
    "مسائل التصنيف. فقد حسّنت أداء النموذج وقلّلت التعقيد الحسابي ورفعت سرعة "
    "المعالجة، مع تقليل عدد السمات في الوقت نفسه. واستقرار النتائج على "
    "مجموعتي بيانات مختلفتين يدل على موثوقية الطريقة وقابليتها للتعميم. "
    "وخلاصة القول إنّ اختيار السمات باستخدام الخوارزميات الفوقية، ولا سيّما "
    "الطرق الهجينة، يمكن أن يؤدي دوراً مهماً في رفع كفاءة نماذج تعلّم الآلة، "
    "وقد تمكّنت الطريقة المقدَّمة في هذا البحث أيضاً من تقديم نتائج مقبولة "
    "في هذا المجال."
)

# --------------------------------------------------------------------------- #
#  What the desktop application can and cannot do                              #
# --------------------------------------------------------------------------- #
SCOPE_LIMITS = [
    ("Email detection",
     "Reads the e-mail body text only and converts it into the 57 Spambase "
     "attributes (word frequencies, character frequencies, capital-run "
     "lengths). It does not open attachments, does not read SMTP headers and "
     "does not check the sender's reputation. In this dataset 'fake' means "
     "unsolicited bulk or fraudulent mail (spam).",
     "كشف البريد",
     "يقرأ نص البريد فقط ويحوّله إلى سمات Spambase السبع والخمسين (تكرار "
     "الكلمات، تكرار المحارف، أطوال سلاسل الأحرف الكبيرة). لا يفتح المرفقات "
     "ولا يقرأ ترويسات SMTP ولا يفحص سمعة المرسل. وكلمة «مزيف» هنا تعني "
     "البريد الجماعي غير المرغوب أو الاحتيالي (Spam)."),
    ("Website detection",
     "Reads the URL string only and derives the 30 Phishing-Websites "
     "attributes from it. Attributes the original study obtained by fetching "
     "the page (favicon, request URLs, anchors, form handlers, redirects, "
     "mouse events, iframe, statistical reports) cannot be derived from a "
     "string; they take the dataset's majority value, except that a domain in "
     "the built-in trusted table takes the benign value. Trust indicators "
     "(domain age, traffic, PageRank, Google index, DNS record, SSL) come from "
     "that same table, so an unknown domain is never given the benefit of the "
     "doubt.",
     "كشف المواقع",
     "يقرأ الرابط فقط ويستخرج منه سمات «Phishing Websites» الثلاثين. أما "
     "السمات التي حصلت عليها الدراسة الأصلية بجلب الصفحة (الأيقونة، روابط "
     "الموارد، روابط الوسوم، هدف النموذج، إعادة التوجيه، أحداث الفأرة، "
     "الإطارات، التقارير الإحصائية) فلا يمكن استخراجها من نص الرابط؛ تأخذ "
     "القيمة الأغلبية في البيانات، إلا إذا كان النطاق في جدول النطاقات "
     "الموثوقة فيأخذ القيمة السليمة. ومؤشرات الثقة (عمر النطاق، الزيارات، "
     "ترتيب الصفحة، فهرسة Google، سجل DNS، شهادة SSL) تأتي من الجدول نفسه، "
     "فلا يُمنح نطاق مجهول أي شك إيجابي."),
    ("Verdict",
     "The output is a strong statistical indicator, not proof. The Random "
     "Forest votes across 100 trees; the confidence is the share of trees "
     "that agreed. Always confirm the real domain or sender before acting.",
     "القرار",
     "الناتج مؤشر إحصائي قوي وليس دليلاً قاطعاً. فالغابة العشوائية تصوّت عبر "
     "100 شجرة، والثقة هي نسبة الأشجار التي اتفقت. تحقّق دائماً من النطاق أو "
     "المرسل الحقيقي قبل أن تتصرّف."),
]
