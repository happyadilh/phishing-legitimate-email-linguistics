"""CLI usage: python -m phishing_language.cli demo|extract|compare|reported"""
import argparse,csv,json,random
from pathlib import Path
from .features import extract,read_emolex
from .analysis import compare


def read_rows(path):
    with open(path,newline='',encoding='utf-8-sig') as f:
        yield from csv.DictReader(f)


def write_rows(path,rows):
    rows=list(rows)
    if not rows:raise ValueError('No output records')
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def run_extract(inp,out,lexicon=None):
    lex=read_emolex(lexicon)
    rows=[]
    for i,r in enumerate(read_rows(inp),1):
        label=r.get('label','').strip().lower()
        if label not in ('phishing','legitimate'):
            raise ValueError(f'Row {i} needs label phishing or legitimate')
        text=r.get('text','')
        if len(text.split())<3:raise ValueError(f'Row {i} has insufficient text')
        rows.append({'id':r.get('id',str(i)),'label':label,**extract(text,lex)})
    write_rows(out,rows)
    return rows


def run_compare(inp,out):
    data=list(read_rows(inp))
    fields=[key for key in data[0] if key not in ('label','id')]
    groups={}
    for field in fields:
        p=[]; l=[]
        for row in data:
            val=row[field]
            if not val:continue
            (p if row['label']=='phishing' else l).append(float(val))
        if len(p)>=2 and len(l)>=2:groups[field]=(p,l)
    if not groups:raise ValueError('No valid numeric features with 2+ messages per group')
    stats=compare(groups)
    write_rows(out,stats)
    return stats


def main():
    parser=argparse.ArgumentParser(description='Transparent illustrative linguistic analysis; not original research reproduction')
    sub=parser.add_subparsers(dest='command',required=True)
    ex=sub.add_parser('extract');ex.add_argument('--input',required=True);ex.add_argument('--output',required=True);ex.add_argument('--nrc-lexicon')
    co=sub.add_parser('compare');co.add_argument('--input',required=True);co.add_argument('--output',required=True)
    dem=sub.add_parser('demo');dem.add_argument('--output-dir',default='demo_output')
    rep=sub.add_parser('reported');rep.add_argument('--input',default='data/reported_feature_results.csv')
    args=parser.parse_args()
    if args.command=='extract':
        print('Extracted',len(run_extract(args.input,args.output,args.nrc_lexicon)),'rows (new illustrative implementation)')
    elif args.command=='compare':
        print('Compared',len(run_compare(args.input,args.output)),'features (not original manuscript data)')
    elif args.command=='demo':
        out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
        extracted=run_extract('data/demo_emails.csv',out/'demo_features.csv')
        compared=run_compare(out/'demo_features.csv',out/'demo_comparisons.csv')
        print('DEMONSTRATION ONLY:',len(extracted),'fictional messages,',len(compared),'features; no historical replication.')
    else:
        rows=list(read_rows(args.input))
        print('HISTORICALLY REPORTED TABLE ONLY:',len(rows),'features; no raw email data or original scripts.')

if __name__=='__main__':main()
