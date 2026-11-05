# Protein-stability confidence study: reusable data

Data supporting **Investigating the Relationship Between AI-Based Structure Prediction Confidence and Experimentally Determined Protein Stability**, CSAI 2026 paper 129.

## Scope

The original study contains 20 canonical WT proteins, ten single-amino-acid substitutions per protein, and three seed labels (42, 43, 44) for each of 220 input sequences under each of Boltz-2, Chai-1 and Biohub ESMFold2. This gives 1,980 prediction profiles and 200 experimental mutation labels. The files here contain the inputs and confidence observations needed to reproduce the reported analyses and the revision's baseline comparisons. No new model inference was performed for the revision.

Experimental ΔΔG values are in kcal/mol, in the Pak et al. Supplementary Table S1 convention: positive is destabilizing and negative is stabilizing. No further sign reversal was applied. pLDDT observations are computational confidence values on the 0–100 scale, not experimental energies.

## Contents

- `raw_data/`: all 220 sequences, all 200 experimental labels/source identifiers, 232,551 residue-level confidence values, 1,980 sequence–seed summaries, 1,800 matched-seed mutation differences, 600 mutation-level model summaries, and original descriptive/association tables.
- `revision_analysis/`: fixed hydrophobicity/BLOSUM62 feature values, model–baseline paired comparisons, all per-protein correlations, figures, portable analysis scripts, and detailed statistical methods. The CSV files retain substantially more precision than printed tables.
- `runtime/`: individual recorded timings and their original completion-record contents, batch progress times, timestamp intervals, and clearly scoped protocol documentation.
- `SOURCE_PROVENANCE.json` and `native_confidence_audit.json`: source-file lineage, original array verification and limitations.
- `DATA_MANIFEST.json`: SHA-256 and byte size of each included file.

The `raw_data` CSVs are byte-identical copies of their archived source tables. Confidence-profile exports preserve the original float32 scaling. Global confidence uses the archived native-array mean; recomputing a mean from the rounded-by-scaling residue export in double precision can differ by approximately 0.00003 pLDDT points. The provided sequence–seed mean table preserves the historical calculation exactly.

The package includes the confidence data used by the paper, not all 1,980 mmCIF coordinate files or model weights. `coordinate_manifest.csv` preserves original coordinate/confidence file checksums and relative paths as provenance. Historical assay constructs were not independently reconstructed; canonical sequence agreement does not establish assay-construct agreement. Package versions and checkpoint revisions are not equally well documented across models.

## Reproduce

With Python, NumPy, pandas, SciPy and Matplotlib installed:

1. Run `python validate_dataset.py` from this directory to validate coverage, mutation identities, confidence profiles, seed differences, aggregation, timing records and included-file hashes.
2. Run `python revision_analysis/calculate_baselines.py`.
3. Run `python revision_analysis/analyze_model_comparisons.py`.

The two analysis scripts write derived files only within `revision_analysis`. They do not run archived inference code, access a remote service or alter the source tables. Their dependencies and versions are documented in `revision_analysis/BASELINE_METHODS.md`. The archived inference code in `runtime/*.source.txt` is reference text with the machine-specific root replaced by a placeholder, not a turnkey installation or an instruction to rerun models.

## Interpretation

The fixed baselines are unfitted association features, not calibrated ΔΔG estimators. Paired bootstrap comparisons did not establish an improvement of local model-confidence association over signed Kyte–Doolittle hydrophobicity change. Within-protein intervals use only ten selected mutations and are descriptive, with explicit distributional and independence assumptions. Compute records have different scopes and concurrent resource use, so they do not provide an isolated architecture-speed benchmark. See the methods files for full limitations.

## Experimental source

Pak MA, et al. Using AlphaFold to predict the impact of single mutations on protein stability and function. PLoS One. 2023;18:e0282689. https://doi.org/10.1371/journal.pone.0282689

Canonical sequence provenance is retained in `raw_data/wt_inventory_20.csv`. Baseline references are supplied in the revision methods.

## Upstream rights

See `THIRD_PARTY_NOTICES.md` and `licenses/BIOPYTHON_LICENSE.rst` for upstream attribution, licenses and recorded transformations. The repository does not apply a blanket license to third-party data or imply upstream endorsement.
