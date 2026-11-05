"""Read-only checks of the published confidence-analysis dataset.

Requires NumPy and pandas. Does not run model inference or modify source data.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd

P=Path(__file__).resolve().parent
R=P/'raw_data'
seq=pd.read_csv(R/'model_sequences_220.csv').set_index('sequence_id')
pairs=pd.read_csv(R/'mutant_pairs_200.csv').set_index('mutant_id')
res=pd.read_csv(R/'per_residue_plddt_0_100.csv')
summary=pd.read_csv(R/'per_sequence_seed_confidence.csv')
seed=pd.read_csv(R/'matched_seed_differences.csv')
mut=pd.read_csv(R/'mutation_level_recomputed.csv')
assert len(seq)==220 and len(pairs)==200
assert pairs.groupby('uniprot').size().eq(10).all() and pairs.uniprot.nunique()==20
for sid,row in seq.iterrows():
    assert len(row.sequence)==row.length_aa
    assert hashlib.sha256(row.sequence.encode()).hexdigest()==row.sequence_sha256
for mid,row in pairs.iterrows():
    wt=seq.loc[row.wt_id].sequence;mt=seq.loc[mid].sequence;i=int(row.position_1based)-1
    assert len(wt)==len(mt) and sum(a!=b for a,b in zip(wt,mt))==1
    assert wt[i]==row.wt_residue and mt[i]==row.mt_residue
assert len(res)==232551 and len(summary)==1980 and len(seed)==1800 and len(mut)==600
assert not res.duplicated(['model','sequence_id','seed_label','position_1based']).any()
assert np.isfinite(res.plddt_0_100).all() and res.plddt_0_100.between(0,100).all()
for key,g in res.groupby(['model','sequence_id','seed_label']):
    g=g.sort_values('position_1based');s=seq.loc[key[1]].sequence
    assert ''.join(g.residue)==s and g.position_1based.tolist()==list(range(1,len(s)+1))
ri=res.set_index(['model','sequence_id','seed_label','position_1based']).plddt_0_100
si=summary.set_index(['model','sequence_id','seed_label']).global_plddt_0_100
max_local=0.;max_global=0.
for row in seed.itertuples(index=False):
    i=int(pairs.loc[row.mutant_id].position_1based)
    l=ri.loc[(row.model,row.mutant_id,row.seed_label,i)]-ri.loc[(row.model,row.wt_id,row.seed_label,i)]
    g=si.loc[(row.model,row.mutant_id,row.seed_label)]-si.loc[(row.model,row.wt_id,row.seed_label)]
    max_local=max(max_local,abs(l-row.local_delta_plddt));max_global=max(max_global,abs(g-row.global_delta_plddt))
assert max_local<1e-10 and max_global<1e-10
agg=seed.groupby(['model','mutant_id']).agg(local_mean=('local_delta_plddt','mean'),local_sd=('local_delta_plddt','std'),global_mean=('global_delta_plddt','mean'),global_sd=('global_delta_plddt','std'))
mi=mut.set_index(['model','mutant_id']).loc[agg.index]
for c in agg.columns:assert np.allclose(agg[c],mi[c],rtol=0,atol=1e-10)
assert np.allclose(mut.experimental_ddg_kcal_mol,pairs.loc[mut.mutant_id].experimental_ddg_kcal_mol,rtol=0,atol=1e-12)
timing=pd.read_csv(P/'runtime/per_inference_seconds.csv',float_precision='round_trip')
assert len(timing)==1320 and not timing.duplicated(['model','sequence_id','seed']).any()
assert (timing.seconds>0).all() and timing.status.eq('sequence_and_plddt_validated').all()
records=[json.loads(line) for line in (P/'runtime/per_inference_complete_records.jsonl').read_text().splitlines()]
ti=timing.set_index(['model','sequence_id','seed'])
for entry in records:
    row=entry['record'];t=ti.loc[(row['model'],row['id'],row['seed'])]
    assert float(row['seconds'])==float(t.seconds) and row['sequence']==seq.loc[row['id']].sequence
# Baseline CSVs must preserve exact mathematical ties and match published stats.
from decimal import Decimal
kd={'A':'1.8','R':'-4.5','N':'-3.5','D':'-3.5','C':'2.5','Q':'-3.5','E':'-3.5','G':'-0.4','H':'-3.2','I':'4.5','L':'3.8','K':'-3.9','M':'1.9','F':'2.8','P':'-1.6','S':'-0.8','T':'-0.7','W':'-0.9','Y':'-1.3','V':'4.2'}
bd=pd.read_csv(P/'revision_analysis/baseline_mutation_values.csv',float_precision='round_trip')
expected=np.array([float(Decimal(kd[m])-Decimal(kd[w])) for w,m in zip(bd.wt_aa,bd.mutant_aa)])
assert np.array_equal(expected,bd.delta_hydrophobicity_kd.to_numpy())
assert np.array_equal(bd.delta_hydrophobicity_kd.rank().to_numpy(),bd.delta_hydrophobicity_tenths.rank().to_numpy())
bstats=pd.read_csv(P/'revision_analysis/baseline_correlations.csv');boots=np.load(P/'revision_analysis/baseline_bootstrap_distributions.npz')
for row in bstats.itertuples(index=False):
    x=bd[row.feature];y=bd.ddg_exp_kcal_mol
    if row.metric=='spearman_rho':x=x.rank(method='average');y=y.rank(method='average')
    estimate=np.corrcoef(x,y)[0,1];assert abs(estimate-row.estimate)<1e-11
    lo,hi=np.quantile(boots[row.feature+'__'+row.metric],[.025,.975])
    assert abs(lo-row.ci95_low)<1e-11 and abs(hi-row.ci95_high)<1e-11
manifest=P/'DATA_MANIFEST.json'
if manifest.exists():
    for entry in json.loads(manifest.read_text())['files']:
        f=P/entry['path'];assert f.stat().st_size==entry['bytes']
        assert hashlib.sha256(f.read_bytes()).hexdigest()==entry['sha256'],entry['path']
print(json.dumps({'status':'PASS','sequences':len(seq),'mutations':len(pairs),'prediction_profiles':len(summary),'residue_values':len(res),'seed_differences':len(seed),'model_mutation_summaries':len(mut),'max_local_seed_difference_error':max_local,'max_global_seed_difference_error':max_global,'timed_items':len(timing),'baseline_exact_ties_verified':True},indent=2))
