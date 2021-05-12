import serial
import pandas as pd
import argparse as ap
from pathlib import Path

p=ap.ArgumentParser()
p.add_argument('-write-every',type=int,default=10,help='number of intervals between data file writes')
p.add_argument('-outfile',type=str,default="dat.csv",help='output data file')
args=p.parse_args()

my_file=Path(args.outfile)
if my_file.is_file():
    print('{:s} exists.'.format(args.outfile))
    exit()

ser = serial.Serial('/dev/ttyACM0',9600)
ser.close()
ser.open()

dat={}
#labels = ['time (s)','T (C)', 'P (bar)', 'RH (%)']
#for t in labels:
#    dat[t]=[]
c=0
print(args.write_every)
while True:
    serline=ser.readline()
    tokens=serline.decode().split()
    print(c,c%args.write_every,tokens)
    if len(tokens) < 2:
        # ignore garbage in terminal
        print('Ignoring:',tokens)
        continue
    elif tokens[0]=='#LABELS':
        # autodetect labels
        labels = tokens[1:]
        for l in labels:
            dat[l]=[]
    else:
        for l,t in zip(labels,tokens):
            dat[l].append(float(t))
    if c%args.write_every == 0:
        print('Writing to',args.outfile)
        df=pd.DataFrame.from_dict(dat)
        df.to_csv(args.outfile)

    c+=1
