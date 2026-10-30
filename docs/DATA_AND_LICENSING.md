# Data, privacy and licensing

The public repository contains no original email bodies and does not redistribute the NRC Emotion Lexicon. A small, entirely fictional demonstration dataset is included as `data/demo_emails.csv`.

- **Original email dataset:** attributed in the term paper to Francesco Greco, *Human-LLM Generated Phishing-Legitimate Emails* on Kaggle: https://www.kaggle.com/datasets/francescogreco97/human-llm-generated-phishing-legitimate-emails . Obtain from the rights holder, inspect its license and permitted uses, and do not automatically publish harvested messages.
- **NRC Emotion Lexicon:** https://www.saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm . Available for research under conditions, including attribution and **no redistribution**. Download only under the applicable license, and pass its locally stored TSV to `--nrc-lexicon`.
- **Historical aggregate data:** `data/reported_feature_results.csv` was transcribed from Table 2 of the uploaded term paper and is attributed to its named author; no original email examples are included.
- **Original thesis:** stored separately by the author; not added to this public package pending rights/privacy/university-policy review.
- **Code license:** Author Adil Hussain confirmed ownership and authorized this companion release under MIT; see `../LICENSE` and `../LICENSE_NOTICE.md`. Historical text, third-party emails and lexicons do not inherit any eventual code license.
- **Security:** the project is about text analysis, not an operational phishing-detection security product. Do not rely on any single linguistic feature to judge whether a message is safe.
