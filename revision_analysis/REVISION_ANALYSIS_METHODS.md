# Model comparisons and per-protein uncertainty

## Source and validation

`normalized_model_mutations.csv` is a column-renamed copy of the original full-precision `local_analysis/analysis/mutation_level_recomputed.csv`, recovered from the 16 September 2026 study. No model output, experimental label or mutation was changed. Original column mappings are `mutant_id → mutation_id`, `uniprot → protein`, `experimental_ddg_kcal_mol → ddg_exp_kcal_mol`, `local_mean → local_delta_mean`, and `global_mean → global_delta_mean`. Model labels were expanded from boltz2/chai1/esmfold2 to Boltz-2/Chai-1/ESMFold2. The other columns retain seed-level variability and source-record identifiers.

The recovered table has 600 unique model–mutation rows: three models on the same 200 mutations, grouped into 20 proteins with ten mutations each. Experimental values, ThermoMutDB identifiers and Pak S1 row numbers match all 200 records recovered independently from the submitted PDF. A separate native-confidence audit verified all 1,980 raw-array hashes and 232,551 residue values against the original completed-run snapshot. The archive audit verified all 1,800 seed-level differences and their mutation-level means and sample SDs. No new model inference was performed.

All 12 pooled correlation estimates and protein-cluster 95% intervals reproduce the submitted manuscript at displayed precision. All 120 per-protein model–endpoint rows, including both Pearson and Spearman coefficients agree with the archived per-protein table within 5 × 10⁻¹³. Local negative-Spearman counts are 14/20 for Boltz-2, 17/20 for Chai-1 and 14/20 for ESMFold2.

## Paired comparisons with fixed baselines

Use the fixed feature definitions and source citations in `BASELINE_METHODS.md`. For each model, baseline and correlation metric, subtract the baseline's coefficient from the model's local ΔpLDDT coefficient. Recalculate this difference within each of the identical 10,000 protein-cluster resamples. Pointwise percentile bounds are the 2.5th and 97.5th percentiles of the paired differences, not differences between separately calculated confidence bounds.

The model-minus-hydrophobicity Spearman differences are 0.123486 [−0.103917, 0.377007] for Boltz-2, −0.040964 [−0.203548, 0.125515] for Chai-1, and −0.025324 [−0.198170, 0.153243] for ESMFold2. All include zero. These results do not establish an improvement over this simple fixed baseline, nor do they prove equivalence. The comparisons concern signed association, not calibrated predictive accuracy or held-out generalization. Exact results for both Pearson and Spearman against both baselines are in `paired_model_baseline_differences.csv`.

For BLOSUM62, local Spearman paired differences are −0.112317 [−0.289804, 0.101731], −0.276768 [−0.462913, −0.061270] and −0.261127 [−0.509801, 0.001274], respectively. Only the Chai pointwise interval excludes zero; there is no multiplicity correction and no isolated model-performance claim.

## Within-protein summaries

Each local and global within-protein Pearson r and Spearman ρ uses the ten mutation-level seed means for that protein. For descriptive Pearson intervals, z = arctanh(r), SE(z) = 1/√(10−3), and the approximate 95% interval is tanh[z ± 1.95996398454 SE(z)]. This Fisher transformation assumes approximately bivariate-normal independent mutation pairs, conditional on the fixed shared predicted WT reference. Ten selected mutations provide imprecise subgroup estimates. These intervals do not propagate shared WT-prediction uncertainty, experimental measurement uncertainty, assay-construct uncertainty or selection uncertainty; they are not multiplicity-adjusted. They are not protein-level superiority tests or simultaneous confidence bands.

Local Pearson r ranges are −0.834 to 0.641 for Boltz-2, −0.959 to 0.557 for Chai-1 and −0.891 to 0.629 for ESMFold2. Local Spearman ranges are −0.830 to 0.648, −0.891 to 0.673 and −0.924 to 0.127, respectively. Both coefficients and all Pearson bounds are retained without selection in `per_protein_correlations.csv`.

## Figures

- `main_local_scatter.png/.pdf`: three models on all 200 mutations, common x/y limits; unjittered experimental ΔΔG versus local ΔpLDDT, with coefficients outside the plot region. Sized 12.4 cm × 6.1 cm with 8-point labels for the main text.
- `per_protein_local_forest.png/.pdf`: all 20 proteins and three models, common correlation scale of −1 to +1 and descriptive Fisher-z 95% intervals.
- `per_protein_scatter_page_1` through `_5`: four proteins per page, three model panels per protein. Scales differ between protein rows to reveal within-protein spread but are common across the three models in each row. Each panel contains all ten mutations, Pearson r/interval and Spearman ρ. No fitted line, jitter, filtering or rescaling of confidence values is applied.

All figures were visually inspected after annotations were moved outside plot regions. All 60 per-protein scatter panels were checked for rendered marks, readable labels, clipping and consistent within-row scales. Coefficients were cross-checked against the source table. Approximate values displayed as −0.00 denote small negative values, not exact zeros; full precision is in the CSV.

## Reproduction

Run `calculate_baselines.py` and then `analyze_model_comparisons.py`. Both read local tables only and write derived outputs. The second script reuses saved bootstrap draws. Source scripts that run or install models were not executed. Data provenance and inference-runtime evidence are separate from these new statistical analyses.

