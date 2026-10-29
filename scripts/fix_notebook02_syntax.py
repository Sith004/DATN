"""
Fix Notebook 02 SyntaxErrors by directly patching the two buggy cells.
The bug: print() strings contain a REAL newline (\\r\\n in JSON) instead of \\n escape.
"""
import json, sys

sys.stdout.reconfigure(encoding='utf-8')

NOTEBOOK_PATH = r"F:\DATN\project\notebooks\02_Preprocessing.ipynb"

with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

# --- Fix Cell index 12: MAPPING cell ---
cell12 = nb["cells"][12]
assert cell12["cell_type"] == "code", "Expected code cell at index 12"
cell12["source"] = [
    'print("=== THỐNG KÊ TRƯỚC KHI MAPPING ===")\n',
    'print("EDUCATION:", df_cleaned[\'EDUCATION\'].value_counts().sort_index().to_dict())\n',
    'print("MARRIAGE :", df_cleaned[\'MARRIAGE\'].value_counts().sort_index().to_dict())\n',
    '\n',
    'df_mapped = map_categorical_anomalies(df_cleaned)\n',
    '\n',
    'print("\\n=== THỐNG KÊ SAU KHI MAPPING ===")\n',
    'print("EDUCATION:", df_mapped[\'EDUCATION\'].value_counts().sort_index().to_dict())\n',
    'print("MARRIAGE :", df_mapped[\'MARRIAGE\'].value_counts().sort_index().to_dict())',
]

# Verify fix
code12 = "".join(cell12["source"])
try:
    compile(code12, "cell_12", "exec")
    print("Cell 12 (mapping): SYNTAX OK after fix")
except SyntaxError as e:
    print(f"Cell 12 (mapping): STILL BROKEN: {e}")

# --- Fix Cell index 27: TRANSFORM cell ---
cell27 = nb["cells"][27]
assert cell27["cell_type"] == "code", "Expected code cell at index 27"
cell27["source"] = [
    'X_train_proc, X_test_proc, fitted_prep = fit_transform_data(preprocessor, X_train, X_test)\n',
    '\n',
    'print("Kích thước ma trận X_train sau transform:", X_train_proc.shape)\n',
    'print("Kích thước ma trận X_test sau transform :", X_test_proc.shape)\n',
    'print("\\n5 dòng đầu tiên của X_train đã xử lý:")\n',
    'display(X_train_proc.head())',
]

code27 = "".join(cell27["source"])
try:
    compile(code27, "cell_27", "exec")
    print("Cell 27 (transform): SYNTAX OK after fix")
except SyntaxError as e:
    print(f"Cell 27 (transform): STILL BROKEN: {e}")

# Save
with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("\nNotebook saved. Now verifying all cells compile...")

# Verify ALL code cells compile
with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
    nb2 = json.load(f)

errors = []
for i, cell in enumerate(nb2["cells"]):
    if cell["cell_type"] != "code":
        continue
    code = "".join(cell["source"])
    try:
        compile(code, f"cell_{i}", "exec")
    except SyntaxError as e:
        errors.append((i, str(e)))

if errors:
    print(f"\nRemaining SyntaxErrors ({len(errors)}):")
    for idx, msg in errors:
        print(f"  Cell {idx}: {msg}")
else:
    print("\nAll code cells: SYNTAX OK - No errors found!")
