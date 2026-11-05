"""Reproduce model associations and calculate revision additions from recovered data.

Input normalized_model_mutations.csv must contain original unrounded seed means:
mutation_id, protein, model, ddg_exp_kcal_mol, local_delta_mean, global_delta_mean.
Rows are unique by (model, mutation_id). Models: Boltz-2, Chai-1, ESMFold2.
Uses saved cluster resamples from calculate_baselines.py, not independent draws.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import pearsonr,spearmanr,rankdata,norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

P=Path(__file__).resolve().parent
MODELS=['Boltz-2','Chai-1','ESMFold2']
COLORS={'Boltz-2':'#2665A0','Chai-1':'#A05A20','ESMFold2':'#247565'}
df=pd.read_csv(P/'normalized_model_mutations.csv')
base=pd.read_csv(P/'baseline_mutation_values.csv').sort_values(['protein','mutation_id']).reset_index(drop=True)
assert len(df)==600 and not df.duplicated(['model','mutation_id']).any()
assert set(df.model)==set(MODELS)
proteins=sorted(base.protein.unique())
cluster_indices=np.stack([base.index[base.protein==p].to_numpy() for p in proteins])
draws=np.load(P/'bootstrap_cluster_draws.npy')
indices=cluster_indices[draws].reshape(len(draws),len(base))
y=base.ddg_exp_kcal_mol.to_numpy();yb=y[indices]
def rowcor(a,b):
    a=a-a.mean(axis=-1,keepdims=True);b=b-b.mean(axis=-1,keepdims=True)
    return (a*b).sum(axis=-1)/np.sqrt((a*a).sum(axis=-1)*(b*b).sum(axis=-1))
def stats(x):
    xb=x[indices]
    return {'pearson_r':(pearsonr(x,y).statistic,rowcor(xb,yb)),
            'spearman_rho':(spearmanr(x,y).statistic,rowcor(rankdata(xb,axis=-1),rankdata(yb,axis=-1)))}
pooled=[]; model_boot={}; arrays={}; per=[]
for model in MODELS:
    d=df[df.model==model].set_index('mutation_id').loc[base.mutation_id].reset_index()
    assert np.allclose(d.ddg_exp_kcal_mol,y,rtol=0,atol=1e-12)
    assert (d.protein.to_numpy()==base.protein.to_numpy()).all()
    for endpoint,col in [('local','local_delta_mean'),('global','global_delta_mean')]:
        x=d[col].to_numpy();arrays[(model,endpoint)]=x
        for metric,(point,boot) in stats(x).items():
            lo,hi=np.quantile(boot,[.025,.975]);model_boot[(model,endpoint,metric)]=boot
            pooled.append(dict(model=model,endpoint=endpoint,metric=metric,estimate=point,ci95_low=lo,ci95_high=hi))
        for protein,idx in zip(proteins,cluster_indices):
            r=pearsonr(x[idx],y[idx]).statistic;rho=spearmanr(x[idx],y[idx]).statistic
            z=np.arctanh(np.clip(r,-.999999999999,.999999999999));w=norm.ppf(.975)/np.sqrt(len(idx)-3)
            lo,hi=np.tanh([z-w,z+w])
            per.append(dict(protein=protein,model=model,endpoint=endpoint,n=len(idx),pearson_r=r,pearson_fisher95_low=lo,pearson_fisher95_high=hi,spearman_rho=rho))
pooled=pd.DataFrame(pooled);pooled.to_csv(P/'model_pooled_correlations.csv',index=False,float_format='%.12g')
per=pd.DataFrame(per);per.to_csv(P/'per_protein_correlations.csv',index=False,float_format='%.12g')
btab=pd.read_csv(P/'baseline_correlations.csv');bb=np.load(P/'baseline_bootstrap_distributions.npz')
pair=[]
for model in MODELS:
    for metric in ['pearson_r','spearman_rho']:
        mp=float(pooled[(pooled.model==model)&(pooled.endpoint=='local')&(pooled.metric==metric)].estimate.iloc[0])
        for feature in ['delta_hydrophobicity_kd','blosum62_score']:
            bp=float(btab[(btab.feature==feature)&(btab.metric==metric)].estimate.iloc[0])
            dif=model_boot[(model,'local',metric)]-bb[feature+'__'+metric]
            lo,hi=np.quantile(dif,[.025,.975]);pair.append(dict(model=model,endpoint='local',baseline=feature,metric=metric,difference_model_minus_baseline=mp-bp,ci95_low=lo,ci95_high=hi))
pair=pd.DataFrame(pair);pair.to_csv(P/'paired_model_baseline_differences.csv',index=False,float_format='%.12g')
np.savez_compressed(P/'model_bootstrap_distributions.npz',**{'__'.join(k):v for k,v in model_boot.items()})

# Keep the main figure legible at its final 12.4 cm column width.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
fig,axs=plt.subplots(1,3,figsize=(12.4/2.54,6.1/2.54),sharex=True,sharey=True)
for ax,model in zip(axs,MODELS):
    x=arrays[(model,'local')]
    ax.scatter(y,x,s=5,alpha=.70,color=COLORS[model],edgecolors='none')
    ax.axhline(0,c='.7',lw=.5);ax.axvline(0,c='.7',lw=.5)
    ax.set_xlim(-5.5,12);ax.set_ylim(-47,41)
    ax.set_xticks([-5,0,5,10]);ax.set_yticks([-40,-20,0,20,40]);ax.tick_params(length=2,pad=2,labelsize=8)
    r=pearsonr(x,y).statistic;rho=spearmanr(x,y).statistic
    letter=chr(ord('a')+MODELS.index(model))
    ax.set_title(f'({letter}) {model}\nr = {r:.3f}; ρ = {rho:.3f}',fontsize=8,pad=5)
axs[0].set_ylabel('Local ΔpLDDT (points)',fontsize=8,labelpad=2)
fig.supxlabel('Experimental ΔΔG (kcal/mol)',fontsize=8,y=.015)
fig.subplots_adjust(left=.12,right=.99,bottom=.22,top=.79,wspace=.13)
for ext in ['png','pdf']:fig.savefig(P/f'main_local_scatter.{ext}',dpi=350)
plt.close(fig)

# Per-protein forest: common −1 to 1 correlation axis across models.
fig,axs=plt.subplots(1,3,figsize=(9,6.8),sharex=True,sharey=True)
for ax,model in zip(axs,MODELS):
    d=per[(per.model==model)&(per.endpoint=='local')].set_index('protein').loc[proteins]
    r=d.pearson_r.to_numpy();lo=d.pearson_fisher95_low.to_numpy();hi=d.pearson_fisher95_high.to_numpy()
    ax.errorbar(r,np.arange(20),xerr=[r-lo,hi-r],fmt='o',markersize=3.5,c=COLORS[model],elinewidth=1,capsize=2)
    ax.axvline(0,c='.6',lw=.8);ax.set_xlim(-1.02,1.02);ax.set_xticks([-1,-.5,0,.5,1]);ax.set_title(model,fontsize=11)
    ax.set_yticks(np.arange(20));ax.set_yticklabels(proteins,fontsize=9)
    ax.set_xlabel('Pearson r and approximate 95% CI',fontsize=9)
axs[0].invert_yaxis();fig.suptitle('Within-protein local confidence–stability associations (n = 10 each)',fontsize=12)
fig.tight_layout(rect=(0,0,1,.96))
for ext in ['png','pdf']:fig.savefig(P/f'per_protein_local_forest.{ext}',dpi=220,bbox_inches='tight')
plt.close(fig)

# Five pages, four protein rows by three model columns. Scales vary by protein
# but are shared across all three models in each row (explicit in figure note).
for page in range(5):
    fig,axs=plt.subplots(4,3,figsize=(8.3,10.0))
    for row,protein in enumerate(proteins[page*4:page*4+4]):
        idx=base.index[base.protein==protein].to_numpy();xx=y[idx]
        allv=np.concatenate([arrays[(m,'local')][idx] for m in MODELS])
        xpad=max(.4,(xx.max()-xx.min())*.12);ypad=max(1.,(allv.max()-allv.min())*.12)
        for col,model in enumerate(MODELS):
            ax=axs[row,col]; yy=arrays[(model,'local')][idx]
            ax.scatter(xx,yy,s=20,c=COLORS[model],edgecolors='white',lw=.4)
            ax.axhline(0,c='.7',lw=.6);ax.axvline(0,c='.7',lw=.6)
            ax.set_xlim(min(0,xx.min())-xpad,max(0,xx.max())+xpad)
            ax.set_ylim(min(0,allv.min())-ypad,max(0,allv.max())+ypad)
            d=per[(per.protein==protein)&(per.model==model)&(per.endpoint=='local')].iloc[0]
            # The estimate text is outside the axes, so it never obscures a mutation.
            ax.set_title(f'{protein} | {model}\nr = {d.pearson_r:.2f} [{d.pearson_fisher95_low:.2f}, {d.pearson_fisher95_high:.2f}]; ρ = {d.spearman_rho:.2f}',fontsize=9,pad=7)
            if col==0:ax.set_ylabel('Local ΔpLDDT (points)',fontsize=9)
            if row==3:ax.set_xlabel('Experimental ΔΔG (kcal/mol)',fontsize=9)
            ax.tick_params(labelsize=8)
    fig.suptitle(f'Per-protein scatterplots ({page+1}/5): ten mutations per panel',fontsize=13)
    fig.tight_layout(rect=(0,.025,1,.97),h_pad=2,w_pad=1.2)
    fig.text(.5,.01,'Scales vary by protein; three model panels share scales within each row. Intervals are descriptive Fisher-z 95% CIs.',ha='center',fontsize=8)
    for ext in ['png','pdf']:fig.savefig(P/f'per_protein_scatter_page_{page+1}.{ext}',dpi=220)
    plt.close(fig)
print('POOLED\n',pooled.to_string(index=False))
print('PAIRED\n',pair.to_string(index=False))
print('NEGATIVE LOCAL SPEARMAN COUNTS\n',per[per.endpoint=='local'].groupby('model').spearman_rho.apply(lambda x:int((x<0).sum())))

