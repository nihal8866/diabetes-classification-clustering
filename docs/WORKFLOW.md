# Working agreement

## Workspace

Open the project root folder in both Codex and VS Code. Both tools work on the same files; no copying between them is needed. Save notebook edits before asking Codex to inspect them, and avoid editing the same file in both tools simultaneously.

## Learning cycle

1. Review the concepts needed for the current phase.
2. Nihal proposes an approach or attempts a small step before receiving a solution.
3. Run the smallest useful increment in VS Code.
4. Inspect the result and explain new code line by line.
5. Debug with hints before replacing code.
6. Complete the phase's concrete checks and explain-it-back checkpoint.
7. Update the learning log and decision log, then commit the verified stage.

## Notebook conventions

- Start with one notebook: `notebooks/01_diabetes_analysis.ipynb`.
- Use numbered Markdown sections: objective, data inspection, split strategy and EDA, preprocessing, classification, clustering, evaluation, error analysis, and conclusions.
- Use paths relative to the project root, with an explicit root check when the notebook is created.
- Keep raw data unchanged. Exclude identifiers and CLASS from model input features.
- Reserve test data before model selection; fit learned preprocessing only on training data.
- Do not use CLASS to fit clustering. Use labels only for external evaluation afterward.
- Record interpretations next to figures and metrics.
- Before delivery, restart the kernel and run every cell in order, then save outputs.

## Git stages

Commit small, verified milestones: organization, environment, data audit, EDA/preprocessing, classification, clustering, evaluation, report, and final reproducibility check.

Git setup, remote creation, and push commands will be taught when we reach that step. A push uploads commits to GitHub; a commit saves a local milestone. Do not commit credentials, virtual environments, or notebook checkpoints. Check dataset redistribution terms before uploading raw files.
