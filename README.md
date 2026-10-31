# Diabetes Classification and Clustering

Associate ML Engineer take-home assignment by Nihal Mahato. All analysis runs locally without paid APIs or a GPU.

## Deliverables

- [Executed notebook](notebooks/01_diabetes_analysis.ipynb)
- [PDF report](reports/diabetes_report.pdf): black Times New Roman text
- [Package versions](requirements.txt)

## Dataset

Download the spreadsheet from the assignment's [Mendeley dataset, version 1](https://data.mendeley.com/datasets/wj9rwkp9c2/1). Extract and place it at `data/raw/dataset.xlsx`. Raw data is excluded from Git. Expected dimensions: 1,000 rows and 14 columns, including CLASS, ID, No_Pation, Gender, and ten numeric measurements. Preserve the original file.

## Setup on Windows

```powershell
git clone https://github.com/nihal8866/diabetes-classification-clustering.git
cd diabetes-classification-clustering
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Open the project in VS Code with the Microsoft Python and Jupyter extensions. Open the notebook, choose `.venv` as the kernel, restart the kernel and Run All. Use Python 3.10.11. The notebook finds data from the repository root or notebooks folder. Saved outputs allow review without execution.

Run the reproducibility check from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts/verify_notebook.py
```

This executes all code cells in a fresh process and verifies the principal report metrics without modifying the saved notebook.

## Methods and results

- Standardize text labels; retain flagged numerical values pending verification.
- Exclude identifiers and CLASS from inputs. Keep identical feature records together.
- Fixed grouped split: 799 training / 201 test rows. Five training-only grouped CV folds compare classifiers.
- Scaling and Gender encoding are fitted inside model pipelines within each fold.
- Random forest mean CV macro-F1: 0.915; logistic regression: 0.658.
- Final random forest test accuracy: 0.985; macro-F1: 0.973; three errors.
- K-means K=3: training silhouette 0.183 and ARI 0.572. Classes and clusters only partially align.

Only seven P test records exist. Perfect P test results do not establish perfect generalization. Patient identity, units, unusual values, and label provenance remain uncertain. Feature grouping does not guarantee patient-level independence. Scores for classification and clustering are not directly comparable. This is not a clinically validated diagnostic system.

## Navigation and submission

`assignment/`: task statement; `data/raw/`: local original data; `notebooks/`: analysis; `reports/`: PDF; `docs/`: decisions and workflow; `scripts/`: verification.

Submit the executed notebook, requirements.txt and PDF, plus the repository link if requested. Confirm private-repository reviewer access. See docs/SUBMISSION_CHECKLIST.md. A GitHub push is not an employer-portal submission.
