"""Fixed, unsupervised baseline associations for the 200 published panel labels.

Source data: Appendix A2 in CSAI2026_paper__129.pdf; signs unchanged.
Bootstrap: NumPy Generator/default_rng, seed 20260916, 10,000 draws of 20
protein clusters with replacement; retain all 10 records per drawn cluster.
These are post-review exploratory analyses, not preregistered tests.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import rankdata, pearsonr, spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
# Integer tenths preserve exact ties in the published decimal scale.
KD_TENTHS={'A':18,'R':-45,'N':-35,'D':-35,'C':25,'Q':-35,'E':-35,'G':-4,'H':-32,'I':45,'L':38,'K':-39,'M':19,'F':28,'P':-16,'S':-8,'T':-7,'W':-9,'Y':-13,'V':42}
matrix_lines=[l.split() for l in (HERE/'BLOSUM62.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
alphabet=matrix_lines[0]
B62={(row[0],c):float(v) for row in matrix_lines[1:] for c,v in zip(alphabet,row[1:])}
df=pd.read_csv(HERE/'experimental_labels_pdf_recovered.csv')
df['wt_aa']=df.mutation_id.str.split('_').str[1].str[0]
df['mutant_aa']=df.mutation_id.str[-1]
df['delta_hydrophobicity_tenths']=df.mutant_aa.map(KD_TENTHS)-df.wt_aa.map(KD_TENTHS)
df['delta_hydrophobicity_kd']=df.delta_hydrophobicity_tenths/10.0
df['blosum62_score']=[B62[(w,m)] for w,m in zip(df.wt_aa,df.mutant_aa)]
df=df.sort_values(['protein','mutation_id']).reset_index(drop=True)
df.to_csv(HERE/'baseline_mutation_values.csv',index=False,float_format='%.12g')
# CSV round-trip must not split or merge feature ties or change rank estimates.
roundtrip=pd.read_csv(HERE/'baseline_mutation_values.csv')
for feature in ['delta_hydrophobicity_kd','blosum62_score']:
    assert np.array_equal(rankdata(df[feature]),rankdata(roundtrip[feature]))
    assert spearmanr(df[feature],df.ddg_exp_kcal_mol).statistic == spearmanr(roundtrip[feature],roundtrip.ddg_exp_kcal_mol).statistic
assert np.array_equal(rankdata(df.delta_hydrophobicity_kd),rankdata(df.delta_hydrophobicity_tenths))
proteins=sorted(df.protein.unique())
clusters=np.stack([df.index[df.protein==p].to_numpy() for p in proteins])
rng=np.random.default_rng(20260916)
cluster_draws=rng.integers(0,len(proteins),size=(10000,len(proteins)))
indices=clusters[cluster_draws].reshape(10000,len(df))
np.save(HERE/'bootstrap_cluster_draws.npy',cluster_draws)
def rowcor(a,b):
    ac=a-a.mean(axis=-1,keepdims=True);bc=b-b.mean(axis=-1,keepdims=True)
    return (ac*bc).sum(axis=-1)/np.sqrt((ac*ac).sum(axis=-1)*(bc*bc).sum(axis=-1))
y=df.ddg_exp_kcal_mol.to_numpy(); yboot=y[indices]
res=[]
boot={}
for feature in ['delta_hydrophobicity_kd','blosum62_score']:
    x=df[feature].to_numpy(); xb=x[indices]
    for metric in ['pearson_r','spearman_rho']:
        if metric=='pearson_r':
            point=pearsonr(x,y).statistic; vals=rowcor(xb,yboot)
        else:
            point=spearmanr(x,y).statistic
            vals=rowcor(rankdata(xb,axis=-1),rankdata(yboot,axis=-1))
        low,high=np.quantile(vals,[.025,.975])
        res.append({'feature':feature,'metric':metric,'estimate':point,'ci95_low':low,'ci95_high':high,'n_mutations':len(df),'n_proteins':len(proteins),'bootstrap_draws':len(vals),'bootstrap_seed':20260916})
        boot[feature+'__'+metric]=vals
out=pd.DataFrame(res);out.to_csv(HERE/'baseline_correlations.csv',index=False,float_format='%.12g')
np.savez_compressed(HERE/'baseline_bootstrap_distributions.npz',**boot)
# Independent direct SciPy checks on bootstrap samples, including repeated clusters.
for j in [0,1,42,9999]:
    for f in ['delta_hydrophobicity_kd','blosum62_score']:
        a=df[f].to_numpy()[indices[j]];b=y[indices[j]]
        assert np.isclose(boot[f+'__pearson_r'][j],pearsonr(a,b).statistic)
        assert np.isclose(boot[f+'__spearman_rho'][j],spearmanr(a,b).statistic)
assert len(df)==200 and df.mutation_id.nunique()==200
assert np.isclose(y.mean(),1.40655) and np.isclose(np.std(y,ddof=1),2.072103,atol=1e-6)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
fig,axs=plt.subplots(1,2,figsize=(9.0,4.3),sharey=True)
for ax,f,label,color in zip(axs,['delta_hydrophobicity_kd','blosum62_score'],['Signed Δhydrophobicity (Kyte–Doolittle)','BLOSUM62 substitution score'],['#2665A0','#A05A20']):
    ax.scatter(df[f],y,s=18,alpha=.7,c=color,edgecolors='none')
    ax.axhline(0,color='.65',lw=.7);ax.axvline(0,color='.65',lw=.7)
    ax.set_xlabel(label);ax.set_ylim(-5.4,12)
    rows=out[out.feature==f].set_index('metric')
    ax.set_title('r = %.3f [%.3f, %.3f]\nρ = %.3f [%.3f, %.3f]'%tuple(rows.loc[m,v] for m in ['pearson_r','spearman_rho'] for v in ['estimate','ci95_low','ci95_high']),fontsize=9,pad=6)
axs[0].set_ylabel('Experimental ΔΔG (kcal/mol)')
fig.suptitle('Fixed baselines on the same 200 mutations',fontsize=12,y=1.01)
fig.tight_layout()
for ext in ['png','pdf']:fig.savefig(HERE/f'baseline_scatterplots.{ext}',dpi=220,bbox_inches='tight')
print(out.to_string(index=False))

