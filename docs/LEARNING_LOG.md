# Learning and verification log

## Concepts practiced

- Classification uses supplied labels; clustering forms groups without them.
- Labels with trailing spaces need normalization before counts and modeling.
- CLASS is the answer, not an input. Identifiers are excluded from model features.
- Grouped splits prevent identical inputs from crossing evaluation boundaries.
- Fit scaling and encoding on training portions and reuse them on validation/test data.
- Accuracy alone can conceal zero minority recall; precision, recall and macro-F1 answer different questions.
- Cluster numbers are arbitrary. Silhouette assesses separation; ARI compares with class labels.
- Model disagreement does not justify changing supplied labels.

## Final verification on October 30 2026

All 44 code cells executed sequentially in a fresh Python process. Assertions confirmed split integrity, three test errors, classifier CV means, held-out accuracy/macro-F1 and clustering scores matching the report. pip check found no broken requirements. The headless runner emitted expected plot-display warnings; saved notebook figures remain included.

## Review before interview

Practice explaining why patient identity remains uncertain, why seven P test records are insufficient for strong claims, and why supervised and clustering scores cannot be directly ranked. Review and rephrase narrative sections where needed to reflect your own understanding.
