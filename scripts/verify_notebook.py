"""Execute all notebook code in a fresh process and verify report metrics."""
import json
import os
from pathlib import Path
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
from traitlets.config import Config

root = Path(__file__).resolve().parents[1]
os.chdir(root / 'notebooks')
notebook = json.loads((root / 'notebooks/01_diabetes_analysis.ipynb').read_text(encoding='utf-8'))
os.environ['MPLBACKEND'] = 'Agg'
config = Config()
config.HistoryManager.enabled = False
shell = InteractiveShell.instance(config=config)
count = 0
for index, cell in enumerate(notebook['cells']):
    if cell['cell_type'] != 'code':
        continue
    with capture_output() as captured:
        result = shell.run_cell(''.join(cell['source']), store_history=False)
    if result.error_before_exec or result.error_in_exec:
        print(captured.stdout)
        print(captured.stderr)
        raise RuntimeError(f'Cell {index + 1} failed') from (result.error_before_exec or result.error_in_exec)
    if captured.stderr.strip():
        print(f'Cell {index + 1}: {captured.stderr.strip()}')
    count += 1

ns = shell.user_ns
from sklearn.metrics import accuracy_score, f1_score
assert len(ns['X_train']) == 799 and len(ns['X_test']) == 201
assert ns['train_groups'].isdisjoint(ns['test_groups'])
assert not {'CLASS', 'ID', 'No_Pation'} & set(ns['X_train'].columns)
assert int(ns['error_mask'].sum()) == 3
assert round(accuracy_score(ns['y_test'], ns['test_predictions']), 3) == 0.985
assert round(f1_score(ns['y_test'], ns['test_predictions'], average='macro'), 3) == 0.973
assert round(ns['silhouette'], 3) == 0.183
assert round(ns['ari'], 3) == 0.572
assert round(ns['forest_results']['macro_f1'].mean(), 3) == 0.915
assert round(ns['logistic_results']['macro_f1'].mean(), 3) == 0.658
print(f'PASS: {count} code cells executed sequentially in a fresh process.')
print('PASS: split integrity and all principal report metrics match.')
