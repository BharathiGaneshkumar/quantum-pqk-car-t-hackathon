# Projected Quantum Kernels for CAR T-cell Cytotoxicity

Entry for the UW-IBM Quantum Machine Learning Hackathon 2026. We compare a classical RBF-SVM against a projected quantum kernel (PQK) SVM on a small CAR T-cell dataset, then test how far the quantum result holds up.

Everything lives in one notebook: `notebooks/quantum_pqk_hackathon.ipynb`.

## The problem

CAR T-cell constructs are built from 4 signaling motifs, each picked from 15 options. The label is whether a construct shows high (+1) or low (-1) cytotoxicity.

- 246 constructs total, 172 train and 74 test
- Train labels: 83 negative, 89 positive. Test labels: 35 negative, 39 positive
- Metric: weighted F1

## The two pipelines

1. **Classical.** One-hot encode each motif, scale by pi/2, and fit an RBF-SVM on the 60 features.
2. **Quantum.** Run the same 60 features through a ZZFeatureMap on 60 qubits, measure X, Y and Z expectation values per qubit, and fit an RBF-SVM on the resulting 180 features.

Both use IBM's grid search: 13 values of C, 12 values of gamma, 10-fold stratified CV.

## What is IBM's and what is ours

The cells from IBM's `Start From Here` notebook are unchanged. Our additions come after them and are marked with an "OUR ADDITIONS" heading. Every cell has a markdown note explaining what it does.

Our additions:

| Track | What it checks |
|---|---|
| 0 | Repeated CV, paired sign-flip test, McNemar test, nested CV |
| Bonus | Geometric difference g and model complexity, as in the IBM tutorial |
| 2A | Learning curves (does a small training set help the quantum kernel?) |
| 2B | Robustness to feature noise |
| 2C | Shuffling motif combinations, with a logistic regression as an additive reference |
| 2D | Real hardware: 4 samples on ibm_marrakesh vs the shipped projections |
| 1A | Which measurement basis (X, Y, Z) carries the signal |

## Results

The quantum kernel wins on the single test split by 6.9 F1 points. That is the headline, and it does not survive a closer look.

- **McNemar test on the test split:** p = 0.33. The two models disagree on too few constructs to call the win real.
- **Tiny noise changes the winner.** Adding small noise to the test features moves the classical F1 anywhere from 0.74 to 0.82. The 6.9 point gap sits inside that range.
- **Repeated and nested CV:** classical leads by about 4 to 8 points in every view we tried (about 5 points in the repeated CV).
- **Theory metrics:** g is about 1.5 against sqrt(N) = 13.1, and the classical model complexity s_c is about 1.4. Both say a quantum advantage is not expected on this data.
- **Additive reference:** a logistic regression with no motif interactions matches the classical RBF-SVM and is statistically indistinguishable from the quantum model. Shuffling combinations within a class does not hurt either. Most of the signal is per-position, not interaction.
- **2A:** no sign that less training data widens the quantum gap. The 100% point is a single run and is probably a split artifact.
- **2B:** no robust quantum advantage at any noise level we tried.
- **2D:** on hardware, projections differ from the shipped ones by about 1.0 x the column std per run. The Z block correlates well (0.77). X and Y correlate poorly.
- **1A:** nested-CV weighted F1 by measurement basis.

| Features | F1 |
|---|---|
| Classical (60 one-hot) | 0.7503 |
| Quantum, all 180 | 0.7070 |
| X only | 0.7045 |
| Z only | 0.6713 |
| X and Y | 0.6871 |
| Y only | 0.6418 |

We expected Z to carry the signal. It does not. X alone matches all 180 features, and nothing beats classical.

**Bottom line:** on this dataset, we found no evidence of a quantum advantage. The projected quantum kernel is competitive but not better.

A note on g/sqrt(N): it falls as the training size grows, but that is mostly because sqrt(N) grows. We do not read it as a quantum effect.

## How to run

Windows PowerShell:

```powershell
python -m venv qpqk-env
.\qpqk-env\Scripts\Activate.ps1
pip install -r requirements.txt
python -m ipykernel install --user --name qpqk-env
```

Open `notebooks/quantum_pqk_hackathon.ipynb` in VSCode, pick the `qpqk-env` kernel, and run all cells. A full run takes about 25 minutes and needs no QPU time.

### Running on real hardware (Track 2D, optional)

Track 2D is off by default (`RUN_QPU = False`). To run it you need an IBM Quantum account. Save your credentials once at a Python prompt:

```python
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(token="YOUR_API_KEY", instance="YOUR_CRN", overwrite=True)
```

This stores them outside the repo. Do not put keys in the notebook or commit them. One sample cost about 97 QPU seconds in our run, and the free plan gives 10 minutes, so we ran 4 samples.

## Repository layout

```
notebooks/   the consolidated notebook
resources/   IBM's original hackathon and Start From Here notebooks
results/     figures and CSVs written by the notebook
```

Because several cells share one random generator, bootstrap intervals and permutation p-values can shift in the late decimals between runs. The F1 scores are deterministic.

## References

- Utro et al. 2025
- Huang et al. 2021, "Power of data in quantum machine learning"
- Glick et al. 2024, covariant quantum kernels
- Daniels et al. 2022, CAR T-cell signaling motifs

## Credits and license

The hackathon materials were created by Sophy Shin and reviewed by Meltem Tolunay, Olivia Lanes and Alexandre Choquette. Copyright IBM Corp. 2026, with the University of Washington. IBM's cells are reused under the Apache 2.0 license. See `LICENSE` and `NOTICE`.

Our earlier Colab runs also had extra analyses that we did not reproduce here. This notebook only contains what we re-ran from scratch.