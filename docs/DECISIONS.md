# Final decision log

- Preserve raw data; standardize Gender/CLASS whitespace and capitalization only.
- Retain numeric extremes pending unit and source verification; do not infer corrections.
- Exclude ID, No_Pation and CLASS from inputs.
- Group identical input features to prevent exact-feature overlap; patient identity remains uncertain.
- Use the first five-fold grouped holdout with seed 42: 799/201 records.
- Use the same five training-only grouped folds for model comparison; fit preprocessing inside each fold.
- Select random forest by macro-F1, giving equal class weight. CV macro-F1: 0.915 versus 0.658.
- Freeze configuration before test evaluation; preserve all labels after observing errors.
- Fit K-means without labels, initially K=3; report geometry and class agreement separately.
- Record limitations: seven P test records, uncertain patient identity, unverified values/units and label provenance.
