# Publication-readiness audit (2026-10-30)

**Scope:** One original 48-page term-paper PDF from `projects.zip`, plus the earlier repository draft. This release is a GitHub-style portfolio *companion*, not a complete research replication.

## Original study evidence
- Title, author/institution and format verified from pp. 1–5.
- Dataset/source selection, filtering and final counts verified from pp. 14–18.
- All 19 reported feature means, t-values, Holm-adjusted p-values and effect sizes transcribed from Table 2, pp. 21–22.
- Main claim 16 significant features, and balanced 453/453 robustness claim, supported by pp. 22–24.
- Appendix A pp. 47–48 supports feature definitions and vocabulary lists used as inspiration for new code.
- No email-level CSV, original analysis scripts, full NRC lexicon, independent model outputs, or actual detection metrics supplied.

## New deliverables
- Public-safe repository documentation, three-page PDF + Markdown project report, reported-effect-size figure, reported-data CSV.
- New exploratory feature and statistical extraction code, fictional eight-email demonstration data, and unit tests.
- No copyrighted raw email messages, original 48-page thesis, NRC lexicon, credentials or unverified claims of predictive performance included.

## Scientific cautions
- The 19 historic numbers are faithfully reported but not independently recomputed.
- Example pipeline is a newly implemented companion; Flesch syllable counts and preprocessing can differ from the original.
- Sample composition and external dataset labels were not independently verified.
- Adil Hussain confirmed sole authorship and authorized a public MIT-licensed companion release. The original thesis, emails and NRC lexicon remain excluded.

## Current release verification

- Inspected the supplied GitHub-ready ZIP; the original full manuscript was absent and was not re-inspected in this check. Earlier source-page verification above is inherited from the preparation package.
- All 12 current unit tests pass locally with Python 3.14; the eight-message, 16-feature fictional demo also completes.
- Fixed Holm correction to preserve undefined tests as NaN while retaining the full family size; invalid finite probabilities are rejected. Regression checks cover these cases.
- Text scan found no obvious credentials. Original email data, full thesis and NRC lexicon are excluded.
- Code and summary published under MIT with author credit and citation metadata. Historical estimates remain unreproduced.
