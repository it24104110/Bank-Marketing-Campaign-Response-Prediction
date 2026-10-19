"""Build the single submission notebook from the stage notebooks and the docs.

Run from the project root:  python src/build_final_notebook.py
It (1) draws the workflow diagram, (2) merges notebooks 00-07 in order (code without outputs),
and (3) inserts the rubric evidence (canvas, logs, decision log, profiles, recommendations,
model card, AI-use declaration) as markdown cells at the right places.
Re-running it overwrites the merged notebook, so outputs must be produced again (Restart & Run All).
"""
import base64
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NB_DIR, DOCS, FIG = ROOT / "notebooks", ROOT / "docs", ROOT / "figures"
OUT = NB_DIR / "IT3091_2026-DS-02_final_notebook.ipynb"

PARTS = [
    ("00_setup_and_data_loading", "Setup and Data Loading"),
    ("01_eda", "Data Understanding and EDA"),
    ("02_preprocessing", "Preprocessing and Feature Engineering"),
    ("03_validation", "Validation Design"),
    ("04_modelling", "Modelling: Baseline and Three Alternatives"),
    ("05_evaluation", "Evaluation on the Test Set"),
    ("06_interpretation", "Interpretation and Marketing Profile Analysis"),
    ("07_final_model", "Final Model Selection and Deployment Package"),
]
# Rubric evidence inserted after a given part: part index -> list of (doc file, heading)
AFTER_PART = {
    1: [("eda_insight_log.md", "EDA Insight Log")],
    2: [("preprocessing_log.md", "Preprocessing / Feature Log")],
    4: [("model_comparison.md", "Model / Method Comparison")],
    6: [("marketing_profiles.md", "Marketing Profiles (secondary lens)")],
    7: [("model_card.md", "Model Card"),
        ("recommendations.md", "Recommendations, Limitations and Stakeholder Value")],
}
K, J, U, T = "Karunathilaka S.H.T.R", "Jayasuriya J.A.Y.N", "Thulmanthi W.A.S", "Thennakoon T.M.S.D"
PART_OWNER = {0: U, 1: K, 2: J, 3: T, 4: "all members (one model each, see the sections below)", 5: T, 6: U, 7: U}
# Section headings (start of a markdown cell) that get their own owner note
SECTION_OWNER = {
    "## 2. Logistic Regression: baseline": K, "## 3. Decision Tree: alternative 1": J,
    "## 4. Random Forest: alternative 2": U, "## 5. XGBoost: alternative 3": T,
    "## 6. Model comparison": T, "## 8. Imbalance strategy check": U,
    "## 4. Logistic Regression odds ratios": K, "## 5. Readable segment rules": J,
    "## 7. Responsible-AI check": J,
}
WORKFLOW = [
    ("1. Business problem\nframing", "Problem framing canvas"),
    ("2. Dataset\nunderstanding", "Parts 0-1: fingerprint,\ndata dictionary"),
    ("3. Data quality\n& EDA", "Part 1: EDA insight log"),
    ("4. Preprocessing\n& features", "Part 2: preprocessing log,\npipelines"),
    ("5. Validation\ndesign", "Parts 2-3: split,\n5-fold CV, metrics"),
    ("6. Baseline &\nalternatives", "Part 4: LR, DT,\nRF, XGBoost"),
    ("7. Evaluation &\ncomparison", "Parts 4-5: CV, test,\nbootstrap, thresholds"),
    ("8. Interpretation\n& profiles", "Part 6: SHAP, segments,\nfairness"),
    ("9. Final method\nselection", "Part 7: Random Forest,\noperating rules"),
    ("10. Recommendation\n& limitations", "Part 7: recommendations,\nmodel card"),
]


def draw_workflow(path):
    fig, ax = plt.subplots(figsize=(13, 6.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    w, h = 2.25, 1.55
    xs = [0.2 + i * 2.55 for i in range(5)]
    for i, (step, where) in enumerate(WORKFLOW):
        row = 0 if i < 5 else 1
        col = i if row == 0 else 9 - i          # snake layout: second row runs right to left
        x, y = xs[col], 4.2 if row == 0 else 1.2
        color = "#d6eaf8" if i not in (5, 6) else "#fdebd0"
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=color, ec="#1b4f72", lw=1.4))
        ax.text(x + w / 2, y + h * 0.68, step, ha="center", va="center", fontsize=9.5, weight="bold", linespacing=1.1)
        ax.text(x + w / 2, y + h * 0.27, where, ha="center", va="center", fontsize=7.8, color="#34495e", linespacing=1.1)
        if i < 9:
            if i == 4:      # down arrow at the end of row 1
                ax.annotate("", xy=(x + w / 2, 1.2 + h + 0.05), xytext=(x + w / 2, y - 0.05),
                            arrowprops=dict(arrowstyle="->", lw=1.6, color="#1b4f72"))
            elif row == 0:
                ax.annotate("", xy=(x + w + 0.3, y + h / 2), xytext=(x + w + 0.02, y + h / 2),
                            arrowprops=dict(arrowstyle="->", lw=1.6, color="#1b4f72"))
            else:
                ax.annotate("", xy=(x - 0.3, y + h / 2), xytext=(x - 0.02, y + h / 2),
                            arrowprops=dict(arrowstyle="->", lw=1.6, color="#1b4f72"))
    ax.text(6.5, 0.45, "Decision log (D1-D30) records the options, choice, reason and evidence at every step  ·  "
            "test set locked from step 4 until step 7", ha="center", fontsize=9, style="italic", color="#555")
    ax.set_title("Workflow: from business problem to recommendation", fontsize=13, weight="bold")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)


def demote(md_text, title):
    """Turn a doc's top-level '# ...' heading into a '## title' heading for use inside the notebook."""
    md_text = re.sub(r"^# [^\n]*\n", "", md_text.strip(), count=1)
    md_text = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", md_text, flags=re.M)   # shift sub-headings down
    return f"## {title}\n\n{md_text}"


def decision_rows():
    """Parse docs/decision_log.md -> header line, separator line, list of (part index, row line)."""
    lines = [l for l in (DOCS / "decision_log.md").read_text(encoding="utf-8").splitlines() if l.startswith("|")]
    header, sep, rows = lines[0], lines[1], lines[2:]
    parsed = []
    for row in rows:
        step = row.split("|")[2]
        step_no = int(re.findall(r"\d+", step)[-1])          # last step mentioned (e.g. '2 EDA -> 4 Validation' -> 4)
        part = 0 if step_no == 0 else step_no - 1            # step 2 -> part 1, ..., step 8 -> part 7
        parsed.append((part, row))
    return header, sep, parsed


def main():
    md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
    FIG.mkdir(exist_ok=True)
    wf_path = FIG / "fig00_workflow.png"
    draw_workflow(wf_path)
    header, sep, decisions = decision_rows()

    toc = "\n".join(f"| Part {i} | {t} | `notebooks/{n}.ipynb` |" for i, (n, t) in enumerate(PARTS))
    cells = [md(f"""# IT3091 Machine Learning – Bank Marketing: Campaign Response Prediction
**Group 2026-DS-02 · Lab group Y3.S1.WD.DS.0102 · Guided Data Track (Banking & Finance)**

| Student No | Name | Model owned | Main stage owned |
|---|---|---|---|
| IT24103860 | Karunathilaka S.H.T.R | Logistic Regression (baseline) | Problem framing, EDA, data dictionary (Part 1) |
| IT24104178 | Jayasuriya J.A.Y.N | Decision Tree | Preprocessing & features (Part 2), responsible-AI check (Part 6 §7) |
| IT24104110 | Thulmanthi W.A.S | Random Forest (final model) | Interpretation (Part 6), final model (Part 7), notebook integration |
| IT24103869 | Thennakoon T.M.S.D | XGBoost | Validation design (Part 3), test evaluation (Part 5) |

Each part and each model section starts with an *Owner* note; all members reviewed every part (decision D30).

**Primary lens:** Campaign Response Prediction: rank clients by likelihood of subscribing to a term deposit, *before* calling.
**Secondary lens:** Marketing Profile Analysis: which client and campaign characteristics are linked to subscribing.

**Dataset:** UCI Bank Marketing, `bank-additional-full.csv` (41,188 × 21; SHA-256 `74adfc57…afb4d8`).
Moro, Cortez & Rita (2014), *Decision Support Systems* 62, 22–31, doi:10.1016/j.dss.2014.03.001.

**How to run:** Kernel → Restart & Run All (≈ 50–60 min, mostly Part 4). Needs the project folders `data/`, `src/`, `models/`,
`results/`, `figures/` next to this notebook's folder. Shared code: `src/config.py`, `src/preprocessing.py`, `src/evaluation.py`.

## Contents
| Section | Content |
|---|---|
| A | Problem framing canvas |
| B | Workflow diagram |
| Parts 0–7 | Analysis (each part ends with **"Decisions made in this part"** from the decision log) |
| C | Appendix: full decision log (D1–D30) |
| D | AI-use declaration |
| E | References |

| Part | Content | Stage notebook |
|---|---|---|
{toc}
"""),
             md(demote((DOCS / "problem_framing_canvas.md").read_text(encoding="utf-8"), "A. Problem Framing Canvas"))]

    wf_cell = md("## B. Workflow Diagram\nThe 10-step workflow from the initial report, and where each step is carried out in this notebook. "
                 "Orange steps involve model training and evaluation.\n\n![workflow](attachment:fig00_workflow.png)")
    wf_cell["attachments"] = {"fig00_workflow.png": {"image/png": base64.b64encode(wf_path.read_bytes()).decode()}}
    cells.append(wf_cell)

    for i, (name, title) in enumerate(PARTS):
        nb = nbf.read(NB_DIR / f"{name}.ipynb", as_version=4)
        first = True
        for c in nb.cells:
            if c.cell_type == "markdown":
                src = c.source
                if first and src.startswith("# "):
                    src = re.sub(r"^# [^\n]*", f"# Part {i} – {title}\n**Owner:** {PART_OWNER[i]}", src, count=1)
                    src = src.replace("**IT3091 Machine Learning · Group 2026-DS-02 · Bank Marketing**\n", "")
                for heading, person in SECTION_OWNER.items():
                    if src.startswith(heading):
                        first_line, _, rest = src.partition("\n")
                        src = f"{first_line}\n*Owner: {person}*\n{rest}"
                cells.append(md(src))
            else:
                cells.append(code(c.source))
            first = False
        for doc, heading in AFTER_PART.get(i, []):
            cells.append(md(demote((DOCS / doc).read_text(encoding="utf-8"), f"Part {i} · {heading}")))
        part_rows = [row for part, row in decisions if part == i]
        if part_rows:
            cells.append(md(f"## Part {i} · Decisions made in this part\n*From the decision log (full log: Appendix C).*\n\n"
                            + "\n".join([header, sep] + part_rows)))

    cells.append(md("# C. Appendix: Full Decision Log\nEvery important decision with the options considered, the choice, the reason "
                    "and the evidence. **Final** = agreed and applied.\n\n" + "\n".join([header, sep] + [r for _, r in decisions])))
    cells.append(md(demote((DOCS / "ai_use_declaration.md").read_text(encoding="utf-8"), "D. AI-Use Declaration")))
    cells.append(md("""# E. References
- Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to predict the success of bank telemarketing. *Decision Support Systems*, 62, 22–31. https://doi.org/10.1016/j.dss.2014.03.001
- Dua, D., & Graff, C. UCI Machine Learning Repository: Bank Marketing. https://archive.ics.uci.edu/dataset/222/bank+marketing
- Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. *JMLR*, 12, 2825–2830.
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proc. KDD*, 785–794.
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *NeurIPS*, 30.
- Chawla, N. V. et al. (2002). SMOTE: Synthetic minority over-sampling technique. *JAIR*, 16, 321–357."""))

    out = nbf.v4.new_notebook()
    out.cells = cells
    out.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nbf.write(out, OUT)
    print(f"Wrote {OUT.name}: {len(cells)} cells ({sum(c.cell_type == 'code' for c in cells)} code), "
          f"{len(decisions)} decisions placed")


if __name__ == "__main__":
    main()
