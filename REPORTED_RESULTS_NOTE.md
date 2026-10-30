# Reported results are not replicated results

`data/reported_feature_results.csv` is a transcription of Table 2 (pp. 21-22) of the supplied 48-page 2026 thesis. The reported Welch t statistics, Holm-adjusted p-values, Cohen's d, and group means are historical manuscript claims and have **not** been recomputed from email-level observations. Numeric `p < .001` is represented as literal `<.001`, not an invented exact p-value.

The independent demonstration under `src/` is a newly created implementation. It uses illustrative sentence splitting, simplified syllable estimation, and selected contraction expansion; it is **not** the original research code and cannot be used to claim reproduction of the manuscript's findings. The 8 example emails are fabricated.
