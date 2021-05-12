# plot.py
import matplotlib.pyplot as plt
import argparse as ap
import numpy as np
import pandas as pd
from pathlib import Path 
p=ap.ArgumentParser()
p.add_argument('-f',type=str,default='out.csv',help='file')
p.add_argument('-x',type=int,default=0,help='x column')
p.add_argument('-y',type=int,action='append',default=[],help='y columns')
p.add_argument('-endzoom',type=float,default=0.0,help='zoom in on this fraction of data at end')
p.add_argument('-horizontal',type=float,default=0.0,help='draw a horizontal line')
args=p.parse_args()

df=pd.read_csv(args.f)

fig,ax=plt.subplots(1,1,figsize=(7,6))
ax.set_xlabel(df.columns[args.x])
ax.set_ylabel(','.join([df.columns[x] for x in args.y]))
end=len(df)
begin=int(args.endzoom*len(df))
print(begin,end)
for y in args.y:
    ax.plot(df[df.columns[args.x]][begin:end],df[df.columns[args.y]][begin:end],label=df.columns[y])
if args.horizontal!=0.0:
    ax.plot(df[df.columns[args.x]][begin:end],[args.horizontal]*len(df[df.columns[args.x]][begin:end]),'k-')
plt.savefig('out.png')

