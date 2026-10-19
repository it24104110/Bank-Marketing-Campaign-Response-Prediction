# Problem Framing Canvas – Group 2026-DS-02

**Domain:** Banking & Finance · **Track:** Guided Data Track · **Dataset:** UCI Bank Marketing (`bank-additional-full.csv`)

| Element | Definition |
|---|---|
| **Business scenario** | A Portuguese retail bank runs telephone marketing campaigns to sell term deposits. Most calls do not lead to a subscription (≈11% success), so call-centre time is spent mostly on clients who say no. |
| **Stakeholder** | The bank's marketing / campaign managers who plan the call list, and the call-centre team that carries it out. |
| **Decision need** | *Before* a campaign starts: which clients should be contacted first, and which client/campaign characteristics are linked to a "yes"? |
| **Primary lens** | **Campaign Response Prediction:** estimate each client's likelihood of subscribing so the call list can be ranked. |
| **Secondary lens** | **Marketing Profile Analysis:** identify the characteristics associated with subscription (from EDA and model interpretation) to explain the predictions and guide campaign targeting. It supports the primary lens: prediction says *who*, profiling explains *why*. |
| **Unit of analysis** | One row = one client contacted in a campaign (last contact of that campaign), described by client, contact, campaign-history and economic-context attributes. To be confirmed in data understanding (Step 2). |
| **ML task** | Supervised binary classification. |
| **Target** | `y`: has the client subscribed to a term deposit? (`yes` = positive class, `no`). |
| **Output** | A probability score per client → ranked call list; plus a yes/no decision at a business-chosen threshold, and a set of evidence-based response profiles. |
| **Allowed inputs** | Only information available **before** the call: client data, contact channel/timing, previous-campaign history, economic indicators. `duration` is excluded (known only after the call; see decision D3). |
| **Success criteria** | (1) Clearly outperforms the Logistic Regression baseline and the "always no" reference on PR-AUC and recall/F1 for the `yes` class; (2) useful ranking, e.g. the top-scored 20% of clients captures a much larger share of subscribers than 20%; (3) results are stable across cross-validation folds; (4) profiles are interpretable to non-technical managers. |
| **Key constraints / risks** | Strong class imbalance; missing values coded as `"unknown"`; potential leakage (`duration`); data from 2008–2010 in one country (may not generalise); sensitive attributes (age, marital status) raise fairness concerns. |
| **Business value** | Fewer wasted calls and lower campaign cost, more subscriptions per call, less customer annoyance from unwanted calls, and clearer understanding of which client segments respond. |
| **What the model is NOT for** | Automatically excluding customers from products, or making credit decisions; it only supports prioritisation of marketing calls, with human oversight. |
