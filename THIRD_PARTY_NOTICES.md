# Third-party data and notices

This supplement combines original study outputs with attributed upstream scientific data. These notices preserve upstream terms; no blanket license or relicensing of the entire repository is asserted. No upstream author or organization endorses this study.

## Biopython and BLOSUM62

`revision_analysis/BLOSUM62.txt` reproduces the BLOSUM62 matrix from Biopython's `Bio/Align/substitution_matrices/data/BLOSUM62`, Git blob `205f139aa2f8c879f6426708fe316be8bf55f771`:
https://github.com/biopython/biopython/blob/master/Bio/Align/substitution_matrices/data/BLOSUM62

The complete upstream license is retained in `licenses/BIOPYTHON_LICENSE.rst`, retrieved from https://github.com/biopython/biopython/blob/master/LICENSE.rst (Git blob `24531b760a67ee91af123311cfe17a516f3f73f2`). It includes the Biopython License Agreement and BSD 3-Clause text; individual upstream file headers govern their applicable terms. Copyright (c) 1999–2026, The Biopython Contributors. All rights reserved.

Matrix scientific attribution: Henikoff S, Henikoff JG. Amino acid substitution matrices from protein blocks. Proc Natl Acad Sci U S A. 1992;89(22):10915–10919. https://doi.org/10.1073/pnas.89.22.10915

The Kyte–Doolittle scale values were checked against Biopython's `Bio/SeqUtils/ProtParamData.py` (Git blob `59f9ce8354d8418ff96aec826a8e0ff5714e0df5`), whose header states Copyright 2003 Yair Benita. All rights reserved, and permits the Biopython License Agreement or BSD 3-Clause License. The revision script represents the scale as integer tenths to preserve exact ties; it is not a copy of the upstream module. Scientific attribution: Kyte J, Doolittle RF. J Mol Biol. 1982;157(1):105–132. https://doi.org/10.1016/0022-2836(82)90515-0

## Experimental labels from Pak et al. / PLOS

The 200 selected experimental labels and source-record identifiers derive from Supplementary Table S1 of:

Pak MA, Markhieva KA, Novikova MS, Petrov DS, Vorobyev IS, Maksimova ES, Kondrashov FA, Ivankov DN. Using AlphaFold to predict the impact of single mutations on protein stability and function. PLoS One. 2023;18(3):e0282689. https://doi.org/10.1371/journal.pone.0282689

© 2023 Pak et al. The article and its supporting data are distributed under the Creative Commons Attribution license identified by PLOS: https://creativecommons.org/licenses/by/4.0/ . The source article and copyright notice are at https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0282689 . The original thermodynamic measurements were collected through ThermoMutDB and its underlying studies; the ThermoMutDB identifiers and S1 rows are retained for provenance. Changes made here: selection of the study's 200 mutation records, attachment of canonical sequence identifiers, tabular reformatting, and addition of model-derived confidence fields. The S1 ΔΔG signs and values are unchanged.

## UniProt sequences and annotations

WT protein sequences, accessions and annotations derive from the UniProt Consortium's reviewed UniProtKB/Swiss-Prot entries. UniProt applies Creative Commons Attribution 4.0 International to copyrightable parts of its databases. License and attribution terms: https://www.uniprot.org/help/license and https://creativecommons.org/licenses/by/4.0/ . Individual entry URLs, sequence versions and checksums are retained in `raw_data/wt_inventory_20.csv`.

The UniProt Consortium. UniProt: the Universal Protein Knowledgebase in 2025. Nucleic Acids Res. 2025;53(D1):D609–D617. https://doi.org/10.1093/nar/gkae1010

Changes made here: selection of twenty canonical sequences and introduction of the documented single substitutions to generate mutant inputs. Mutant sequences are computational study inputs, not new UniProt reference entries. Canonical-sequence provenance does not establish historical assay-construct matching.
