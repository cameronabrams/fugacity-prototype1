# plot.py
# Generates a plot of CSV data
#
# Cameron F Abrams cfa22@drexel.edu
# Drexel University
# Department of Chemical and Biological Engineering
#
import matplotlib.pyplot as plt
import argparse as ap
import numpy as np
import pandas as pd
from iapws import IAPWS97

p=ap.ArgumentParser()
p.add_argument('-f',type=str,default='dat.out',help='file')
p.add_argument('-o',type=str,default='plot.png',help='plot output image file')
p.add_argument('-x',type=int,default=0,help='x column')
p.add_argument('-y',type=int,action='append',default=[],help='y columns')
p.add_argument('-do-pp',action='store_true',help='compute and plot partial pressure')
p.add_argument('-endzoom',type=float,default=0.0,help='zoom in on this fraction of data at end')
p.add_argument('-horizontal',type=float,default=0.0,help='draw a horizontal line')
p.add_argument('-echo-columns',action='store_true',help='list column names and exit')
args=p.parse_args()

try:
    df=pd.read_csv(args.f)
except:
    print('Error reading {:s}'.format(args.f))
    exit()
if args.echo_columns:
    for i,c in enumerate(df.columns):
        print(i,c)
    exit()

if args.do_pp:
    # use the steam tables to get the saturation pressure at 
    # the measured temperature, and then compute the water
    # vapor partial pressure from the measured relative 
    # humidity and the water mole fraction from the
    # measured pressure
    pp=[]
    yi=[]
    for T,P,RH in zip(df['T(C)'],df['P(bar)'],df['RH(%)']):
        if not np.isnan(T) and not np.isnan(P) and not np.isnan(RH):
            sat_steam=IAPWS97(T=(T+273.15),x=1)
            pi=RH*(sat_steam.P/10)
            pp.append(pi)
            yi.append(pi/P)
        else:
            pp.append('nan')
            yi.append('nan')
    args.y.append(len(df.columns))
    df['Pi(bar)']=pp
    args.y.append(len(df.columns))
    df['yi']=yi

end=len(df)
begin=int(args.endzoom*len(df))
xn=df.columns[args.x]
x=df[xn]
yn=[df.columns[i] for i in args.y]
fig,ax=plt.subplots(1,1,figsize=(7,6))
ax.set_xlabel(df.columns[args.x])
ax.set_ylabel(','.join([df.columns[x] for x in args.y]))
for yy in yn:
    y=df[yy]
    print(y)
    ax.plot(x,y,label=yy)
#df.plot(df.columns[args.x],y=[df.columns[i] for i in args.y])
#df.plot('time(s)',y=['Pi(bar)','T(C)'])
if args.horizontal!=0.0:
    ax.plot(df[df.columns[args.x]][begin:end],[args.horizontal]*len(df[df.columns[args.x]][begin:end]),'k-')

plt.legend()
plt.savefig(args.o)
plt.show()

