# CSAI 2026 Paper 129: supplementary materials

Supporting materials for **Investigating the Relationship Between AI-Based Structure Prediction Confidence and Experimentally Determined Protein Stability**.

## Read the supplement

- [Supplementary information (PDF)](supplement/CSAI129_Supplementary_Information.pdf)
- [Supplementary information (Word)](supplement/CSAI129_Supplementary_Information.docx)
- [Supplementary information (Markdown)](supplement/CSAI129_Supplementary_Information.md)

The supplement contains the 20-protein inventory, all 200 experimental records, full local/global association summaries, fixed sequence baselines, paired comparisons, execution-time accounting, a per-protein Pearson forest and all 60 local scatter panels.

## Data and reproducibility

See [data guide](README_DATA.md) for file definitions, source provenance, reuse limits and reproduction instructions. The package retains confidence observations for all 1,980 predictions, not model weights or the complete coordinate archive. No new inference was performed for the revision.

Run python validate_dataset.py before reproducing the analysis. [DATA_MANIFEST.json](DATA_MANIFEST.json) records SHA-256 and byte sizes for the public files. Baselines preserve exact hydrophobicity ties before ranking, and all bootstrap comparisons use shared protein-cluster draws.

## Interpretation

These are exploratory confidence–stability associations on 200 mutations from 20 selected proteins. The primary local Spearman model comparisons do not resolve a decisive ranking; paired signed associations do not establish added value over the unfitted hydrophobicity baseline. Within-protein intervals are descriptive and conditional. Recorded inference times are not a controlled speed benchmark.

The main manuscript and private reviewer correspondence are not part of this repository. Upstream data and software retain their original rights; see [third-party notices](THIRD_PARTY_NOTICES.md).
