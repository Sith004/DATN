"""
Inspect the exact source of mapping cell and transform cell in Notebook 02.
"""
import json, sys

sys.stdout.reconfigure(encoding='utf-8')

NOTEBOOK_PATH = r"F:\DATN\project\notebooks\02_Preprocessing.ipynb"

with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

TARGET_CELLS = []
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    joined = "".join(cell["source"])
    if "map_categorical_anomalies" in joined and "THỐNG KÊ SAU KHI MAPPING" in joined:
        TARGET_CELLS.append(("MAPPING CELL", i, cell["source"]))
    if "X_train_proc.head()" in joined:
        TARGET_CELLS.append(("TRANSFORM CELL", i, cell["source"]))

for label, idx, src in TARGET_CELLS:
    print(f"\n=== {label} (index {idx}) ===")
    code = "".join(src)
    print(code)
    print("--- Compile check ---")
    try:
        compile(code, f"cell_{idx}", "exec")
        print("SYNTAX OK")
    except SyntaxError as e:
        print(f"SYNTAX ERROR: {e}")
