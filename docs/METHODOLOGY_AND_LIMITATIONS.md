# Research methodology and fidelity limits

## Original 2026 term paper (as reported)

1. Data: two human-authored files (`legit.csv` and `phishing.csv`, 1,000 messages each) from the Kaggle *Human-LLM Generated Phishing-Legitimate Emails* collection; no LLM-generated subset in this analysis.
2. Cleaning: Unicode/case/space normalization for duplicate detection (original bodies preserved). Removed duplicate texts, reducing 2,000 to 1,193 unique records (701 legitimate / 492 phishing); manually reviewed language detection; excluded 36 non-English texts and 9 texts under 20 English alphabetic words. Four flagged texts were manually retained as English. Final 1,148 records (695 legitimate / 453 phishing).
3. NLP features: 19 frequency, lexical, affective and stylistic measures. Counts normalized per 100 alphabetic words; MATTR window size 20; Flesch Reading Ease; NRC Emotion Lexicon. Appendix A lists word categories.
4. Inference: Welch independent-group t-tests for all 19 features, Holm-adjusted p-values (alpha=0.05), Cohen's d with phishing-minus-legitimate sign. Balanced check: random selection of 453 legitimate emails (seed 42) compared with all 453 phishing.
5. Interpretation: differences are group-level corpus patterns, discussed through Interpersonal Deception Theory. The paper **did not train/evaluate a classifier**.

## Newly authored demonstration (this repository)

- Source code is an independently written **illustrative adaptation**, not the author's original lost code.
- The CLI accepts CSV rows with `id,label,text` and computes 16 core transparent features, or 19 if a researcher provides a properly licensed local NRC Emotion Lexicon TSV.
- The demonstration has only fictional email examples. Its output is unrelated to the reported 1,148-email findings.
- Tokenization, contraction handling, sentence segmentation and Flesch syllable counts are approximate and may differ from the original NLTK/lexicon pipeline. No independent data cleaning, manual language review or split sampling procedure is automatically reproduced.
- The packaged table and plot reproduce **reported printed numbers**, not recomputed statistical estimates.

## Methodological limitations

- No email-level data, original scripts, full lexicon snapshots or intermediate validation logs were supplied; the historical statistics cannot be independently reproduced from the ZIP.
- Source dataset's human-authorship/label correctness, chronology, recruitment and population representativeness were not independently audited.
- Unequal email lengths and genres can confound surface-feature differences; per-100-word normalization does not eliminate all genre effects.
- Multiple tests were corrected via Holm, but feature dependence and other sampling biases remain important.
- No phishing-detection accuracy, precision, recall or F1 was measured in the original paper.
- Use only properly licensed sources for any future raw data or lexicons; avoid distributing messages with personal information.
