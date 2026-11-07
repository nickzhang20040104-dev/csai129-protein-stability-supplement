# CSAI 2026 Paper 129 - Supplementary Materials

**Investigating the Relationship Between AI-Based Structure Prediction Confidence and Experimentally Determined Protein Stability**

Ningquan Zhang, Chen Tang, Hui Lin and Billy Li.

This repository hosts the self-contained publication appendix. The online version reproduces all seven supplementary tables, eight figure images and accompanying scientific text from the appendix PDF. Presentation changes do not change the results or conclusions.

## Read or download

- [Read the full appendix online](Appendix.md)
- [Download the appendix PDF directly](https://raw.githubusercontent.com/nickzhang20040104-dev/csai129-protein-stability-supplement/main/supplement/CSAI129_Supplementary_Information.pdf)

The online appendix renders as a normal GitHub page, without the embedded PDF viewer. The direct PDF link also bypasses that viewer. If a GitHub PDF preview shows an error, use either link above.

## Appendix index

| Section | Contents |
| --- | --- |
| [Scope and definitions](Appendix.md#scope) | Study panel, endpoints and supplementary-release scope |
| [Analysis](Appendix.md#analysis) | Fixed baselines, cluster bootstrap and interval assumptions |
| [Figure S1](Appendix.md#figure-s1) | Analysis workflow |
| [Table S1](Appendix.md#table-s1) | 20-protein inventory |
| [Table S2](Appendix.md#table-s2) | Local and global association summaries |
| [Table S3](Appendix.md#table-s3) | Confidence changes by stability direction |
| [Table S4 and Figure S2](Appendix.md#table-s4) | Fixed sequence-baseline comparisons |
| [Table S5](Appendix.md#table-s5) | 200 experimental mutation labels and source identifiers |
| [Software](Appendix.md#software) | Inference provenance and software limitations |
| [S6](Appendix.md#s6) | Recorded execution costs and environment |
| [S7](Appendix.md#s7) | Paired model-minus-baseline comparisons |
| [S8 and Figures S3-S4](Appendix.md#s8) | Per-protein forest and all 60 local scatter panels |
| [S9](Appendix.md#s9) | Data integrity and analysis provenance |
| [References](Appendix.md#references) | Sources needed for standalone reading |

## Scope of this release

This release contains only the publication appendix in PDF and directly readable Markdown, its embedded figure images, and this explanatory README. It does not include raw prediction outputs, intermediate processing files, source scripts or separate machine-readable data exports. The main manuscript and reviewer correspondence are not included.

The analyses are exploratory confidence-stability associations on 200 mutations from 20 selected proteins. They do not establish calibrated energy prediction, a decisive model ranking or a controlled inference-speed benchmark.

The experimental-label table is reproduced with source attribution to Pak et al., Supplementary Table S1 (https://doi.org/10.1371/journal.pone.0282689), derived from ThermoMutDB (https://doi.org/10.1093/nar/gkaa925). Upstream material retains its original rights; this repository does not grant a new license to third-party material.

## Version note

The appendix-only release and its online reading format are dated 7 November 2026. The PDF is unchanged from the appendix-only release. Earlier Git history may contain a broader data package; this release scope does not imply that historical copies have been erased.
