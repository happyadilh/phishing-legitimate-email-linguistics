"""Independent statistical calculations for user-supplied feature matrices.

These functions are new transparency tools, NOT the original thesis scripts.
"""
import math


def holm_adjust(p_values):
    """Holm step-down family-wise p-adjustment, preserving original order."""
    n=len(p_values)
    if not n:return []
    if any(not math.isnan(p) and (not math.isfinite(p) or not 0 <= p <= 1) for p in p_values):
        raise ValueError('P-values must be between 0 and 1, or NaN for undefined tests')
    # Undefined tests remain undefined. Retain the full family size so missing
    # tests cannot make the correction less conservative for the remaining ones.
    indices=sorted((i for i in range(n) if not math.isnan(p_values[i])),key=lambda i:p_values[i])
    corrected=[float('nan')]*n
    maximum=0.
    for rank, idx in enumerate(indices):
        maximum=max(maximum,(n-rank)*p_values[idx])
        corrected[idx]=min(1.,maximum)
    return corrected


def cohens_d(phishing,legitimate):
    if len(phishing)<2 or len(legitimate)<2:
        raise ValueError('Need at least two observations per group')
    na,nb=len(phishing),len(legitimate)
    ma,mb=sum(phishing)/na,sum(legitimate)/nb
    sa=sum((x-ma)**2 for x in phishing)/(na-1)
    sb=sum((x-mb)**2 for x in legitimate)/(nb-1)
    pooled=((na-1)*sa+(nb-1)*sb)/(na+nb-2)
    return (ma-mb)/math.sqrt(pooled) if pooled>0 else float('nan')


def compare(groups):
    """groups: dict[str, (phishing values, legitimate values)]. Requires scipy."""
    try:from scipy.stats import ttest_ind
    except ImportError as err:raise RuntimeError('Install scipy to run inferential comparisons') from err
    names=list(groups)
    info=[]
    for name in names:
        phishing,legitimate=groups[name]
        if len(phishing)<2 or len(legitimate)<2:
            raise ValueError(f'Insufficient data for {name}')
        t,p=ttest_ind(phishing,legitimate,equal_var=False)
        info.append({'feature':name,'phishing_mean':sum(phishing)/len(phishing),
                     'legitimate_mean':sum(legitimate)/len(legitimate),
                     'welch_t':float(t),'p_raw':float(p),'cohens_d':cohens_d(phishing,legitimate)})
    adjusted=holm_adjust([r['p_raw'] for r in info])
    for row,p in zip(info,adjusted):row['holm_p']=p
    return info
