import json
from pathlib import Path

SRC = Path("resources/Start_From_Here.ipynb")
DST = Path("notebooks/quantum_pqk_hackathon.ipynb")

TITLE = """# UW–IBM QML Hackathon: Classical vs Projected Quantum Kernels

> 🆕 **Our notebook.** Cells from `# Start From Here` onward are IBM/UW's starter cells, reproduced **unchanged**. Everything marked **🆕 Our addition** is ours.
>
> Task: predict CAR T-cell cytotoxicity (binary) from 4 signaling-motif slots, comparing an RBF-SVM on classical one-hot features against an RBF-SVM on pre-computed quantum projections.
"""

ENVCHECK = """# 🆕 Our addition: confirm the kernel is the project environment
import sys, platform
print("Python:    ", sys.version.split()[0], "|", platform.system())
print("Executable:", sys.executable)
"""

nb = json.loads(SRC.read_text(encoding="utf-8"))
use_ids = nb.get("nbformat_minor", 0) >= 5

def cell(kind, cid, text):
    c = {"cell_type": kind, "metadata": {}, "source": text.splitlines(keepends=True)}
    if kind == "code":
        c["execution_count"] = None
        c["outputs"] = []
    if use_ids:
        c["id"] = cid
    return c

ibm_cells = nb["cells"]
for c in ibm_cells:
    if c["cell_type"] == "code":
        c["outputs"] = []
        c["execution_count"] = None

nb["cells"] = [cell("markdown", "ours-title", TITLE),
               cell("code", "ours-envcheck", ENVCHECK)] + ibm_cells
nb["metadata"]["kernelspec"] = {
    "display_name": "qpqk-env", "language": "python", "name": "qpqk-env"}

DST.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote {DST}: {len(ibm_cells)} IBM cells (unchanged) + 2 of ours")