Timestamp-Level CARE Results

This file summarizes how to produce the numeric CARE components and save the CARE figure used in the README.

1) Generate the CARE outputs and figure

- Open and run `src/Timestamp_Ensemble_CARE.ipynb` (preferably after activating the project's virtual environment).
- The final plotting cell has been patched to save the CARE figure at:

  assets/readme_figures/Timestamp_Ensemble_CARE_care.png

- To run the notebook headlessly (if `nbconvert` is available):

```bash
source env/bin/activate
python -m nbconvert --to notebook --execute src/Timestamp_Ensemble_CARE.ipynb --output executed_Timestamp_Ensemble_CARE.ipynb
```

2) Quick extraction of numeric results

After running the notebook, the following quick Python snippet computes TP counts, mean lead time, and bootstrap CI for the mean lead time:

```python
import pandas as pd
import numpy as np
fm = pd.read_csv('feature_matrix_58events.csv')

# True positives
tp = fm[(fm['label'] == 'anomaly') & (fm['alarm_triggered'])]
lead = tp['lead_time_h'].dropna().values

print('Detected failures (TP):', len(lead))
print('Mean lead time (hours):', np.mean(lead))
print('Std (hours):', np.std(lead))

# Bootstrap 95% CI for mean lead time
def bootstrap_mean(arr, n=2000):
    bs = [np.mean(np.random.choice(arr, size=len(arr), replace=True)) for _ in range(n)]
    return np.percentile(bs, [2.5, 97.5])

if len(lead) > 0:
    print('Bootstrap 95% CI (mean):', bootstrap_mean(lead))
```

3) Statistical tests to quantify "early-ness"

- One-sample t-test (H0: mean lead time == 0): `scipy.stats.ttest_1samp(lead, 0)`
- Wilcoxon signed-rank test (non-parametric): `scipy.stats.wilcoxon(lead - 0)`
- Mann–Whitney U to compare detected vs missed anomalies:

```python
from scipy.stats import mannwhitneyu

detected = fm[(fm['label']=='anomaly') & (fm['alarm_triggered'])]['lead_time_h'].dropna()
missed = fm[(fm['label']=='anomaly') & (~fm['alarm_triggered'])]['lead_time_h'].dropna()
if len(detected)>0 and len(missed)>0:
    print('Mann-Whitney U p:', mannwhitneyu(detected, missed, alternative='greater').pvalue)
```

Interpretation notes

- If the one-sample test p-value < 0.05 and mean lead time > 0, alarms are significantly early on average.
- A bootstrap CI for the mean that does not include 0 supports robustness of the positive lead time estimate.
- A significant Mann–Whitney U (detected > missed) suggests the detector finds events with stronger early signatures.

4) Next actions

- If you'd like, I can try to run the notebook here and attach the produced `assets/readme_figures/Timestamp_Ensemble_CARE_care.png` and a small `results_summary.md` with the actual numeric outputs. If running here is blocked, follow the headless `nbconvert` command above on your machine.

---

**Embedded Figures**

Below are the key figures used to interpret the CARE results. If you re-run the notebooks with saving enabled these will be refreshed.

CARE components and lead-time histogram:

![CARE components & lead-time histogram](assets/readme_figures/Timestamp_Ensemble_CARE_cell012_out01.png)

Power-curve cleaning plot (for reference):

![Power curve](assets/readme_figures/EDA_Wind_Farm_C_cell023_out02.png)

Supervised model diagnostics (example):

![Supervised diagnostics](assets/readme_figures/Supervised_Learning_cell031_out01.png)
