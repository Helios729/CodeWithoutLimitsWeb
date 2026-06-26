"""
Code Without Limits — Learning Curriculum (v2).

Save 1 of 3: Learning (L) modules from "Code Block for Learning and Quiz
Modules_APP Today.pdf". Each module has 4 sub-modules, each with L1/L2/L3
Bloom learning objectives, a lesson body, and 3-5 source citations.

Save 2 will add Quiz (Q) modules (9 × 20 questions = 180 graded items).
Save 3 will add the 18 microenterprise project modules from the companion PDF.
"""

# Source pool. Every URL is publicly accessible academic / standards material.
# Keys match the S1/S2 references used in the PDF so future edits stay traceable.
CITATIONS = {
    "aima":         {"url": "https://aima.cs.berkeley.edu/",                                              "institution": "Russell & Norvig — AIMA 4th ed. (UC Berkeley)"},
    "mit_6034":     {"url": "https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/",       "institution": "MIT OCW 6.034 Artificial Intelligence"},
    "stanford_hai": {"url": "https://hai.stanford.edu/",                                                  "institution": "Stanford HAI"},
    "turing_paper": {"url": "https://www.csee.umbc.edu/courses/471/papers/turing.pdf",                    "institution": "Turing — Computing Machinery and Intelligence (1950)"},
    "blooms":       {"url": "https://www.bloomstaxonomy.net/",                                            "institution": "Bloom's Revised Taxonomy"},
    "roediger":     {"url": "https://pubmed.ncbi.nlm.nih.gov/16507066/",                                  "institution": "Roediger & Karpicke — Test-Enhanced Learning"},
    "ebbinghaus":   {"url": "http://psychclassics.yorku.ca/Ebbinghaus/memory.htm",                        "institution": "Ebbinghaus — Memory (1885)"},
    "sweller":      {"url": "https://doi.org/10.1207/s15516709cog1202_4",                                 "institution": "Sweller — Cognitive Load"},
    "ed_gov":       {"url": "https://www2.ed.gov/rsc/publications/evidence-based-practices-online-learning.pdf", "institution": "U.S. Dept. of Education — Evidence-Based Online Learning"},
    "eu_hleg":      {"url": "https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai", "institution": "European Commission HLEG — Trustworthy AI Guidelines"},
    "obermeyer":    {"url": "https://pubmed.ncbi.nlm.nih.gov/31649194/",                                  "institution": "Obermeyer et al. — Dissecting Racial Bias in an Algorithm (Science 2019)"},
    "jobin":        {"url": "https://arxiv.org/abs/1906.11668",                                           "institution": "Jobin, Ienca & Vayena — Global Landscape of AI Ethics (Nature MI 2019)"},
    "gender_shades":{"url": "http://proceedings.mlr.press/v81/buolamwini18a.html",                        "institution": "Buolamwini & Gebru — Gender Shades (FAccT 2018)"},
    "nist_rmf":     {"url": "https://airc.nist.gov/RMF",                                                  "institution": "NIST AI Risk Management Framework 1.0"},
    "mit_6006":     {"url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",  "institution": "MIT OCW 6.006 Introduction to Algorithms"},
    "stanford_cs161":{"url": "https://web.stanford.edu/class/cs161/",                                     "institution": "Stanford CS161 Algorithms"},
    "sedgewick":    {"url": "https://algs4.cs.princeton.edu/home/",                                       "institution": "Sedgewick & Wayne — Algorithms 4e (Princeton)"},
    "python_docs":  {"url": "https://docs.python.org/3/tutorial/",                                        "institution": "Python Software Foundation — Official Tutorial"},
    "mit_6001":     {"url": "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/", "institution": "MIT OCW 6.0001 Introduction to Python"},
    "vanderplas":   {"url": "https://jakevdp.github.io/WhirlwindTourOfPython/",                           "institution": "VanderPlas — A Whirlwind Tour of Python"},
    "islr":         {"url": "https://www.statlearning.com/",                                              "institution": "James, Witten, Hastie & Tibshirani — ISLR 2e"},
    "murphy_ml":    {"url": "https://probml.github.io/pml-book/book1.html",                               "institution": "Murphy — Probabilistic ML (MIT Press 2022)"},
    "cs229":        {"url": "https://cs229.stanford.edu/",                                                "institution": "Stanford CS229 Machine Learning"},
    "sklearn":      {"url": "https://scikit-learn.org/stable/user_guide.html",                            "institution": "Scikit-learn User Guide"},
    "mit_6s191":    {"url": "http://introtodeeplearning.com/",                                            "institution": "MIT 6.S191 Introduction to Deep Learning"},
    "deep_learning":{"url": "https://www.deeplearningbook.org/",                                          "institution": "Goodfellow, Bengio & Courville — Deep Learning (MIT Press)"},
    "cs231n":       {"url": "https://cs231n.stanford.edu/",                                               "institution": "Stanford CS231n Computer Vision"},
    "attention":    {"url": "https://arxiv.org/abs/1706.03762",                                           "institution": "Vaswani et al. — Attention Is All You Need"},
    "nature_dl":    {"url": "https://www.nature.com/articles/nature14539",                                "institution": "LeCun, Bengio & Hinton — Deep Learning (Nature 2015)"},
    "cs224n":       {"url": "https://web.stanford.edu/class/cs224n/",                                     "institution": "Stanford CS224N NLP"},
    "jurafsky":     {"url": "https://web.stanford.edu/~jurafsky/slp3/",                                   "institution": "Jurafsky & Martin — Speech and Language Processing 3e (draft)"},
    "bert":         {"url": "https://arxiv.org/abs/1810.04805",                                          "institution": "Devlin et al. — BERT (NAACL 2019)"},
    "huggingface":  {"url": "https://huggingface.co/docs/transformers/index",                             "institution": "Hugging Face Transformers Documentation"},
    "mit_6_4210":   {"url": "https://manipulation.csail.mit.edu/",                                       "institution": "MIT OCW 6.4210 Robotic Manipulation"},
    "probabilistic":{"url": "https://probabilistic-robotics.org/",                                       "institution": "Thrun, Burgard & Fox — Probabilistic Robotics (MIT Press)"},
    "siciliano":    {"url": "https://link.springer.com/book/10.1007/978-1-84628-642-1",                  "institution": "Siciliano et al. — Robotics (Springer)"},
    "sutton_barto": {"url": "http://incompleteideas.net/book/the-book-2nd.html",                          "institution": "Sutton & Barto — Reinforcement Learning 2e"},
    "mit_6_4321":   {"url": "https://underactuated.mit.edu/",                                            "institution": "MIT OCW 6.4321 Underactuated Robotics"},
}


# Frameworks kept from v1 for the Studio's "Insert template" picker — still useful.
PROMPT_FRAMEWORKS = [
    {"id": "RTF", "name": "RTF — Role · Task · Format", "purpose": "Smallest reliable prompt scaffold.",
     "template": "Role: <role>.\nTask: <single verb-driven task>.\nFormat: <exact output shape>.",
     "example": "Role: A community health worker.\nTask: Explain dehydration signs.\nFormat: 5 bullets, ≤80 words."},
    {"id": "CO-STAR", "name": "CO-STAR — Context · Objective · Style · Tone · Audience · Response",
     "purpose": "Production-grade scaffold when ambiguity is costly.",
     "template": "Context: <…>.\nObjective: <…>.\nStyle: <…>.\nTone: <…>.\nAudience: <…>.\nResponse: <…>.",
     "example": "Context: 14-year-olds in Brazil learning AI.\nObjective: Define 'token'.\nStyle: Conversational.\nTone: Encouraging.\nAudience: 9th grade.\nResponse: 3 sentences + 1 analogy."},
    {"id": "ERA", "name": "ERA — Expectation · Role · Action", "purpose": "Rapid code/task delegation.",
     "template": "Expectation: <deliverable>.\nRole: <expert>.\nAction: <steps>.",
     "example": "Expectation: HTML page showing today's date.\nRole: Mobile-first engineer.\nAction: Single file, inline CSS, no libraries."},
    {"id": "RISE", "name": "RISE — Role · Input · Steps · Expectation", "purpose": "Multi-step reasoning workflows.",
     "template": "Role: <expert>.\nInput: <raw data>.\nSteps: <numbered>.\nExpectation: <final format>.",
     "example": "Role: Microenterprise coach.\nInput: 'I sell banana chips at $0.50/bag.'\nSteps: 1) 3 weak points 2) 1 AI asset each 3) revenue lift.\nExpectation: 3-row table."},
    {"id": "CREATE", "name": "CREATE — Character · Request · Examples · Adjustments · Type · Extras",
     "purpose": "Consistent batch outputs (marketing, templates).",
     "template": "Character: <…>.\nRequest: <…>.\nExamples: <2-3>.\nAdjustments: <…>.\nType: <format>.\nExtras: <constraints>.",
     "example": "Character: Youth radio host.\nRequest: 3 captions for recycling drive.\nExamples: 'Trash to treasure — Sat 10am.'\nType: Plain text.\nExtras: ≤80 chars."},
    {"id": "RSTI", "name": "RSTI — Restate · Simplify · Test · Iterate", "purpose": "Debug failing prompts.",
     "template": "Restate: <model restates ask>.\nSimplify: <one measurable goal>.\nTest: <tiny case>.\nIterate: <add 1 constraint>.",
     "example": "Restate: 'Add two numbers.'\nSimplify: 1 input, 1 button.\nTest: 2+2=4.\nIterate: add ×, retest."},
]


def _S(*keys):
    """Convert short citation keys to full citation dicts."""
    return [k for k in keys]  # store keys; resolved later in attach_citations


# ----------------------------------------------------------------------
# 9 Learning (L) modules. Sub-module objectives come verbatim from PDF.
# Lesson body is a 2-3 sentence synthesis — readable on a phone in 60s.
# ----------------------------------------------------------------------
MODULES = [
    {
        "module_id": "L01-intro-to-ai", "title": "Introduction to AI", "persona": "Foundations",
        "tagline": "Define AI, distinguish narrow from general, and trace its history from Turing to Transformers.",
        "color": "brand",
        "submodules": [
            {"id": "1.1", "title": "What is Artificial Intelligence?", "objective": "Define AI and the four AIMA quadrants (think/act × human/rational); distinguish narrow AI from AGI.",
             "lesson": "AI = systems that perceive, reason, and act. Russell & Norvig organize definitions on two axes — standard (human vs. rational) and activity (think vs. act). Narrow AI excels at one task; AGI (still hypothetical) would generalize across tasks the way a human does.",
             "sources": _S("aima", "mit_6034", "stanford_hai")},
            {"id": "1.2", "title": "A Brief History of AI", "objective": "Name the milestones — Turing 1950, Dartmouth 1956, AlexNet 2012, Transformer 2017 — and explain the AI Winters.",
             "lesson": "AI's history is a cycle of hype and winters. Symbolic systems dominated 1956–1980s until they couldn't scale. The 2012 AlexNet ImageNet win launched the deep-learning era; the 2017 Transformer paper made today's LLMs possible.",
             "sources": _S("turing_paper", "aima", "mit_6034")},
            {"id": "1.3", "title": "Learning Paradigms and Problem Domains", "objective": "Compare supervised, unsupervised, and reinforcement learning; classify a real-world system by paradigm.",
             "lesson": "Supervised learning needs labeled data (X-ray → 'pneumonia'). Unsupervised finds structure without labels (customer segmentation). Reinforcement learns from a reward signal (game-playing, robot walking). Most production AI is supervised.",
             "sources": _S("aima", "islr", "sutton_barto")},
            {"id": "1.4", "title": "Intelligent Agents and Rational Decision-Making", "objective": "Apply the PEAS framework; classify agents (reflex, model-based, goal-based, utility-based, learning).",
             "lesson": "PEAS = Performance measure, Environment, Actuators, Sensors. A thermostat is a simple reflex agent; a chess engine is goal-based; a self-driving car is a learning utility-based agent in a partially observable, stochastic environment.",
             "sources": _S("aima", "mit_6034")},
        ],
    },
    {
        "module_id": "L02-edtech-learning-science", "title": "EdTech & Learning Science", "persona": "Pedagogy",
        "tagline": "Bloom's Taxonomy, retrieval practice, cognitive load, and how AI fits into evidence-based learning design.",
        "color": "brandSecondary",
        "submodules": [
            {"id": "2.1", "title": "Bloom's Revised Taxonomy", "objective": "State the six levels (Remember → Create) and their cognitive verbs; map a question to its Bloom level.",
             "lesson": "Anderson & Krathwohl (2001) revised Bloom's 1956 taxonomy into six rising levels: Remember, Understand, Apply, Analyze, Evaluate, Create. Each level has signature verbs (define, explain, calculate, distinguish, judge, design). Quiz items should target a specific level — and your quizzes in this app are tagged L1/L2/L3.",
             "sources": _S("blooms", "ed_gov")},
            {"id": "2.2", "title": "Memory, Forgetting & Retrieval Practice", "objective": "Define spaced repetition, retrieval practice, and interleaving; explain why testing beats re-reading.",
             "lesson": "Ebbinghaus showed memory decays exponentially without review. Roediger & Karpicke (2006) proved that retrieving information from memory (testing) produces stronger retention than passive re-reading — the 'testing effect.' Spaced repetition + interleaving exploits this.",
             "sources": _S("ebbinghaus", "roediger")},
            {"id": "2.3", "title": "Cognitive Load Theory", "objective": "Distinguish intrinsic, extraneous, and germane cognitive load; redesign an instruction to reduce extraneous load.",
             "lesson": "Sweller (1988): working memory is finite. Intrinsic load = inherent task difficulty. Extraneous load = bad instructional design. Germane load = effortful schema-building. Good teaching minimizes extraneous load so working memory can do the productive work.",
             "sources": _S("sweller", "ed_gov")},
            {"id": "2.4", "title": "Assessment Design & AI in Education", "objective": "Distinguish formative from summative assessment; design a 5-question mini-quiz hitting L1, L2, L3.",
             "lesson": "Formative assessment guides learning in progress (this app's quizzes). Summative assessment certifies what was learned. AI tutors must be calibrated for both — and must always reveal their grounding sources so students learn to verify, not just receive.",
             "sources": _S("blooms", "ed_gov", "stanford_hai")},
        ],
    },
    {
        "module_id": "L03-ai-ethics", "title": "AI Ethics & Responsible Use", "persona": "Trustworthy AI",
        "tagline": "Bias, fairness, transparency, accountability — and the EU + NIST frameworks that govern real deployments.",
        "color": "brand",
        "submodules": [
            {"id": "3.1", "title": "Core AI Ethics Concepts", "objective": "Define bias, fairness, transparency, accountability, and privacy in the AI context.",
             "lesson": "Ethical AI isn't a single property — it's a portfolio. Bias is when outputs systematically disadvantage a group; fairness is the absence of that disadvantage. Transparency is the ability to inspect the system; accountability is the ability to hold someone responsible.",
             "sources": _S("eu_hleg", "jobin")},
            {"id": "3.2", "title": "Bias in AI Systems", "objective": "Explain how training-data bias propagates; compare individual vs. group fairness.",
             "lesson": "Buolamwini & Gebru (2018) showed commercial face-recognition systems had 34% error on dark-skinned women vs. <1% on light-skinned men — training data was the cause. Obermeyer et al. (2019) found a hospital triage algorithm systematically under-served Black patients because it used cost as a proxy for need.",
             "sources": _S("gender_shades", "obermeyer")},
            {"id": "3.3", "title": "EU Trustworthy AI & Governance Frameworks", "objective": "List the 7 EU HLEG requirements and the 4 NIST AI RMF functions (Govern, Map, Measure, Manage).",
             "lesson": "EU's 7 requirements: human agency, technical robustness, privacy, transparency, diversity & fairness, societal well-being, accountability. NIST's RMF gives a process: Govern (policy), Map (context), Measure (test), Manage (deploy & monitor).",
             "sources": _S("eu_hleg", "nist_rmf")},
            {"id": "3.4", "title": "Responsible AI in Practice", "objective": "Audit a real AI deployment for bias sources and propose concrete mitigations.",
             "lesson": "Practical mitigations: balance training data, run disparate-impact tests by subgroup, log every decision for audit, give users a path to contest outputs, and keep a human in the loop on consequential decisions (hiring, loans, medical, legal).",
             "sources": _S("eu_hleg", "nist_rmf", "jobin")},
        ],
    },
    {
        "module_id": "L04-algorithms", "title": "Algorithms & Data Structures", "persona": "Computer Science Core",
        "tagline": "Big-O, arrays, hash tables, sorting, and graph traversal — the universal vocabulary of efficient code.",
        "color": "brandSecondary",
        "submodules": [
            {"id": "4.1", "title": "Big-O & Complexity Analysis", "objective": "Define time/space complexity in Big-O; rank common operations by complexity.",
             "lesson": "Big-O describes how runtime grows with input size. O(1) constant (hash lookup), O(log n) logarithmic (binary search), O(n) linear (single pass), O(n log n) (merge sort), O(n²) (nested loops). Pick the smallest order that solves the problem.",
             "sources": _S("mit_6006", "stanford_cs161")},
            {"id": "4.2", "title": "Core Data Structures", "objective": "Match arrays, linked lists, stacks, queues, hash tables, and BSTs to their time complexities for each operation.",
             "lesson": "Array: O(1) index, O(n) insert. Linked list: O(n) index, O(1) insert at head. Hash table: O(1) average lookup, O(n) worst. BST: O(log n) balanced, O(n) degenerate. Choose by access pattern.",
             "sources": _S("mit_6006", "sedgewick")},
            {"id": "4.3", "title": "Sorting Algorithms", "objective": "Trace insertion, merge, and quick sort; explain why merge sort is O(n log n) via recurrence.",
             "lesson": "Insertion sort: O(n²), simple. Merge sort: O(n log n) always, divide-and-conquer with a recurrence T(n) = 2T(n/2) + O(n). Quick sort: O(n log n) average, O(n²) worst (bad pivot). For real code, just use the language's built-in.",
             "sources": _S("mit_6006", "stanford_cs161", "sedgewick")},
            {"id": "4.4", "title": "Graph Algorithms", "objective": "Compare DFS and BFS in data structures, order, and use cases; choose Dijkstra vs. A* for shortest path.",
             "lesson": "DFS uses a stack, goes deep first (good for cycle detection). BFS uses a queue, explores in layers (shortest unweighted path). Dijkstra finds shortest weighted path. A* adds a heuristic to focus search.",
             "sources": _S("mit_6006", "sedgewick")},
        ],
    },
    {
        "module_id": "L05-python", "title": "Python Fundamentals", "persona": "Programming",
        "tagline": "Types, control flow, functions, and the list/dict/comprehension idioms that power most modern ML code.",
        "color": "brand",
        "submodules": [
            {"id": "5.1", "title": "Types, Variables & Operators", "objective": "Identify Python's built-in types; explain mutable vs. immutable with examples.",
             "lesson": "Immutable: int, float, str, tuple — safe to share. Mutable: list, dict, set — modifying one reference modifies all. This single distinction explains 80% of beginner Python bugs.",
             "sources": _S("python_docs", "mit_6001")},
            {"id": "5.2", "title": "Control Flow", "objective": "Use if/elif/else, for, while; explain the difference between iterating a list and a range.",
             "lesson": "Python control flow is whitespace-sensitive. `for x in [1,2,3]` iterates values directly (no index needed). `range(n)` produces a lazy iterator, not a list — efficient for large loops.",
             "sources": _S("python_docs", "mit_6001")},
            {"id": "5.3", "title": "Functions & Scope", "objective": "Define function, parameter, argument, scope, module; write a function returning multiple values.",
             "lesson": "`def f(x, y=0):` declares a function with a default. Variables inside a function are local; reading from enclosing scope works, writing requires `nonlocal` or `global`. Modules group related functions in a single .py file.",
             "sources": _S("python_docs", "vanderplas")},
            {"id": "5.4", "title": "Lists, Dicts & Comprehensions", "objective": "Write a list comprehension equivalent to a for-loop; pick between list, dict, and set for a task.",
             "lesson": "`[x*2 for x in nums if x>0]` is faster and clearer than the equivalent loop. Dicts give O(1) keyed lookup. Sets give O(1) membership + deduplication. Comprehensions also work for dict and set.",
             "sources": _S("python_docs", "vanderplas")},
        ],
    },
    {
        "module_id": "L06-machine-learning", "title": "Machine Learning", "persona": "Statistical Learning",
        "tagline": "Supervised vs. unsupervised, gradient descent, overfitting, and the train/validate/test split.",
        "color": "brandSecondary",
        "submodules": [
            {"id": "6.1", "title": "Supervised Learning Fundamentals", "objective": "Distinguish supervised, unsupervised, RL; explain the train/validation/test split.",
             "lesson": "Train data fits the model; validation data tunes hyperparameters; test data gives an unbiased final estimate. Never touch the test set during training — that's the cardinal rule of ML.",
             "sources": _S("islr", "cs229", "sklearn")},
            {"id": "6.2", "title": "Gradient Descent & Model Training", "objective": "Explain how gradient descent minimizes a loss function; describe SGD vs. batch vs. mini-batch.",
             "lesson": "Gradient descent walks the loss surface downhill: w ← w − η·∇L(w). Batch uses all data per step (slow, stable). SGD uses one example (fast, noisy). Mini-batch (32–256) is the practical default.",
             "sources": _S("islr", "cs229", "murphy_ml")},
            {"id": "6.3", "title": "Overfitting, Underfitting & Regularization", "objective": "Diagnose overfit vs. underfit from learning curves; prescribe regularization, more data, or simpler model.",
             "lesson": "Overfit: low training error, high validation error → reduce capacity, add L1/L2, or get more data. Underfit: high error everywhere → increase capacity or features. Cross-validation gives the most honest signal.",
             "sources": _S("islr", "cs229")},
            {"id": "6.4", "title": "Decision Trees, Ensembles & Unsupervised", "objective": "Explain how a random forest improves on a single tree; describe k-means clustering.",
             "lesson": "A single tree overfits easily. A random forest averages many trees trained on bootstrap samples + random feature subsets — variance drops dramatically. K-means clusters without labels by minimizing within-cluster distance.",
             "sources": _S("islr", "murphy_ml", "sklearn")},
        ],
    },
    {
        "module_id": "L07-neural-networks", "title": "Neural Networks & Deep Learning", "persona": "Deep Learning",
        "tagline": "Neurons, backprop, CNNs, and the Transformer architecture that powers today's LLMs.",
        "color": "brand",
        "submodules": [
            {"id": "7.1", "title": "Neurons, Layers & Activations", "objective": "Identify neurons, weights, biases; name activations (ReLU, sigmoid, tanh, softmax) and their use cases.",
             "lesson": "A neuron computes z = w·x + b then applies a non-linearity. ReLU (max(0,z)) is the modern default — cheap, doesn't saturate. Softmax converts logits into class probabilities for the final layer.",
             "sources": _S("mit_6s191", "deep_learning")},
            {"id": "7.2", "title": "Backpropagation & Training", "objective": "Explain how the chain rule enables backprop; compare dropout, batch-norm, and weight decay.",
             "lesson": "Backprop computes ∂L/∂w for every weight via the chain rule, then SGD updates. Dropout randomly zeros activations during training — a simple, powerful regularizer. Batch norm stabilizes deep nets. Weight decay = L2 regularization.",
             "sources": _S("mit_6s191", "deep_learning", "nature_dl")},
            {"id": "7.3", "title": "Convolutional Neural Networks", "objective": "Explain why CNNs suit image data; design a small CNN for image classification and justify each layer.",
             "lesson": "CNNs exploit translation invariance — a cat is a cat anywhere in the image. Conv layers learn local feature detectors; pooling reduces spatial resolution; the final dense layers classify. Conv → ReLU → Pool, repeated.",
             "sources": _S("cs231n", "deep_learning")},
            {"id": "7.4", "title": "Transformers & Transfer Learning", "objective": "Explain self-attention; describe transfer learning and when to fine-tune.",
             "lesson": "Self-attention lets every token attend to every other token in parallel — solving RNNs' sequential bottleneck. Transfer learning: take a pre-trained model (BERT, GPT), fine-tune on your small dataset. This is how modern NLP works.",
             "sources": _S("attention", "deep_learning")},
        ],
    },
    {
        "module_id": "L08-nlp", "title": "Natural Language Processing", "persona": "Language AI",
        "tagline": "Tokenization, embeddings, BERT, GPT — and the responsible NLP that minor-facing systems require.",
        "color": "brandSecondary",
        "submodules": [
            {"id": "8.1", "title": "Text Preprocessing & Classical Representations", "objective": "Define tokenization, stemming, lemmatization; compare bag-of-words, TF-IDF, and embeddings.",
             "lesson": "Bag-of-words ignores order. TF-IDF down-weights frequent words. Modern NLP usually skips both in favor of contextual embeddings, but tokenization is still the first step of every pipeline.",
             "sources": _S("jurafsky", "cs224n")},
            {"id": "8.2", "title": "Word Embeddings & Sequence Models", "objective": "Explain how word2vec learns embeddings from context; describe encoder-decoder + attention.",
             "lesson": "word2vec's skip-gram learns vectors so similar words sit close in vector space — 'king − man + woman ≈ queen'. Encoder-decoder + attention enabled the first usable neural machine translation; attention later became the whole architecture.",
             "sources": _S("jurafsky", "cs224n", "attention")},
            {"id": "8.3", "title": "BERT, GPT & Pre-trained LMs", "objective": "Distinguish BERT (encoder, masked LM) from GPT (decoder, next-token); explain pre-training + fine-tuning.",
             "lesson": "BERT masks tokens and predicts them bidirectionally — great for classification. GPT predicts the next token left-to-right — great for generation. Both are pre-trained on huge corpora, then fine-tuned for your task.",
             "sources": _S("bert", "attention", "huggingface")},
            {"id": "8.4", "title": "Core NLP Tasks & Responsible NLP", "objective": "Compare sentiment, NER, and translation; design safeguards for a minor-facing chatbot.",
             "lesson": "Sentiment classifies polarity. NER finds entities (people, places, dates). Translation maps language pairs. For minor-facing systems: RLHF for age-appropriate alignment + RAG grounded in verified curriculum to prevent confident hallucinations.",
             "sources": _S("jurafsky", "huggingface", "eu_hleg")},
        ],
    },
    {
        "module_id": "L09-robotics", "title": "Robotics & Autonomous Systems", "persona": "Robotics",
        "tagline": "Kinematics, sensors, SLAM, and the safety frameworks that govern autonomous vehicles.",
        "color": "brand",
        "submodules": [
            {"id": "9.1", "title": "Robot Anatomy — Kinematics, Sensors, Actuators", "objective": "Define DoF, sense-plan-act cycle; identify sensor roles (LIDAR, camera, IMU, encoders).",
             "lesson": "A 6-DoF arm can position and orient an end-effector anywhere reachable. Sense-plan-act is the canonical control loop. LIDAR gives precise 3D geometry; cameras give semantics; IMU + encoders give pose estimates. Fusion beats any one alone.",
             "sources": _S("siciliano", "probabilistic")},
            {"id": "9.2", "title": "Kinematics & Motion Planning", "objective": "Distinguish forward from inverse kinematics; compare workspace and configuration space planning.",
             "lesson": "Forward kinematics: joints → end-effector. Inverse: end-effector → joints (often multi-solution). Plan in configuration space (one dim per joint) so obstacles and joint limits become explicit C-space regions.",
             "sources": _S("siciliano", "mit_6_4210", "mit_6_4321")},
            {"id": "9.3", "title": "Localization, Mapping & SLAM", "objective": "Distinguish localization, mapping, and SLAM; explain particle filters and loop closure.",
             "lesson": "SLAM solves the chicken-and-egg problem of building a map while tracking position in it. Particle filters represent belief as weighted samples — perfect for multi-modal uncertainty. Loop closure corrects accumulated drift by recognizing a revisited place.",
             "sources": _S("probabilistic", "siciliano")},
            {"id": "9.4", "title": "Autonomous Systems, RL & Safety Ethics", "objective": "Name the 4 AV stack layers; evaluate ethical trade-offs of deploying autonomy in public space.",
             "lesson": "AV stack: perception → localization → planning → control. SAE Level 4 = full autonomy within an ODD; Level 5 = anywhere, any conditions (not yet shipped). Real ethics work isn't the trolley problem — it's ODD enforcement, sensor fusion, and human-takeover handoffs.",
             "sources": _S("siciliano", "probabilistic", "sutton_barto", "mit_6_4321")},
        ],
    },
]


# ----------------------------------------------------------------------
# Helpers used by server.py
# ----------------------------------------------------------------------
def find_module(module_id: str):
    for m in MODULES:
        if m["module_id"] == module_id:
            return m
    return None


def find_submodule(module_id: str, sub_id: str):
    m = find_module(module_id)
    if not m:
        return None, None
    for s in m["submodules"]:
        if s["id"] == sub_id:
            return m, s
    return m, None


def attach_citations(submodule: dict) -> dict:
    """Replace short citation keys with full {url, institution} dicts."""
    out = dict(submodule)
    out["sources"] = [CITATIONS[k] for k in submodule.get("sources", []) if k in CITATIONS]
    if submodule.get("framework"):
        framework = next((f for f in PROMPT_FRAMEWORKS if f["id"] == submodule["framework"]), None)
        if framework:
            out["framework"] = framework
    return out
