# Fixed-baseline analysis

These exploratory analyses were added during revision. Neither baseline is trained or calibrated to this panel. All 200 mutation labels were retained without exclusion or change of sign.

## Inputs

- Experimental labels were recovered from Table A2 of the original submitted `CSAI2026_paper__129.pdf`, SHA-256 `659d8455e1ff7d7d5ccc2817c06d2aef05ccdecb9c6f55644ed5e7620968d0d3`.
- Exactly 20 protein accessions each contribute 10 unique mutations. The labels have mean 1.40655, sample standard deviation 2.072103 kcal/mol, range −4.73 to 11.4, quartiles 0.0875, 1.125 and 2.2025, and 153 positive, 43 negative and 4 exact-zero values. These reproduce the submitted paper's summaries.
- Positive experimental ΔΔG indicates destabilization. `thermomutdb_id` and `pak_s1_row` preserve published source identifiers.

## Feature definitions

1. `delta_hydrophobicity_kd` = H(mutant amino acid) − H(wild-type amino acid), using the fixed Kyte–Doolittle scale. The values are listed in `calculate_baselines.py` and were checked against Biopython's `Bio/SeqUtils/ProtParamData.py` (Git blob `59f9ce8354d8418ff96aec826a8e0ff5714e0df5`). The scale is represented as exact integer tenths, and mutant-minus-WT subtraction is performed in those integers before dividing by ten. This preserves mathematical ties for rank statistics and after CSV serialization. This is a signed change, not an absolute difference, moving-window average or fitted energy.
2. `blosum62_score` = the untransformed BLOSUM62 matrix entry for the wild-type/mutant amino-acid pair, in the conventional half-bit units. It is not a self-score-subtracted value or a fitted energy. The fixed matrix was retrieved from Biopython's `Bio/Align/substitution_matrices/data/BLOSUM62` (Git blob `205f139aa2f8c879f6426708fe316be8bf55f771`) and retained as `BLOSUM62.txt`.

No sign was selected to maximize association. Both features use only mutation letters, not model outputs, structures or experimental values. The baselines are descriptive associations and are not held-out predictive models.

## Statistical calculation

Pearson r and Spearman ρ were calculated across all 200 mutation records. Spearman ranks assign average ranks to ties. The 95% pointwise intervals are the 2.5th and 97.5th percentiles from 10,000 protein-cluster bootstrap resamples. Each resample draws 20 of the 20 proteins with replacement and retains all 10 mutations of each selected protein, including repeated clusters. The generator is `numpy.random.default_rng(20260916)`, with protein accessions sorted lexicographically. Identical resamples are used for both baselines and all subsequent paired comparisons. Bootstrap draws are saved, not regenerated separately by feature.

These intervals concern panel-level sampling uncertainty conditional on the selected proteins; they do not include experimental measurement error, construct mismatch or model protocol uncertainty. They are not multiplicity-adjusted. Paired comparisons against model confidence features require those features on the same rows and resamples; separate intervals are not sufficient to assert superiority.

## Reproduction and validation

Run `python calculate_baselines.py` in an environment with NumPy, SciPy, pandas and Matplotlib. It recreates baseline CSV files, bootstrap arrays and two scatterplot formats. The run used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pandas 2.2.3 and Matplotlib 3.10.8. Vectorized bootstrap Pearson and Spearman estimates were independently cross-checked against SciPy calls on four resamples, including draws with repeated clusters. Feature ranks and Spearman estimates are asserted identical before and after CSV serialization, and hydrophobicity ranks are asserted identical to exact integer-tenths ranks. The final plot was visually inspected for clipping, label/axis accuracy and retained zero references.

## References

- Kyte J, Doolittle RF. A simple method for displaying the hydropathic character of a protein. J Mol Biol. 1982;157(1):105–132. https://doi.org/10.1016/0022-2836(82)90515-0
- Henikoff S, Henikoff JG. Amino acid substitution matrices from protein blocks. Proc Natl Acad Sci U S A. 1992;89(22):10915–10919. https://doi.org/10.1073/pnas.89.22.10915
- Pak MA, et al. Using AlphaFold to predict the impact of single mutations on protein stability and function. PLoS One. 2023;18:e0282689. https://doi.org/10.1371/journal.pone.0282689

