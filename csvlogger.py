# csvlogger.py
#
# Cameron F Abrams cfa22@drexel.edu
# Drexel University
# Department of Chemical and Biological Engineering
#
# Logs structured data from a serial port to a csv file
#
import serial
import pandas as pd
import argparse as ap
from pathlib import Path

p=ap.ArgumentParser()
p.add_argument('-bs',metavar='buffer-size',type=int,default=10,help='default buffer size (lines)')
p.add_argument('-o',metavar='outfile-name',type=str,default="dat.out",help='output data file')
p.add_argument('-p',metavar='serial-port',type=str,default="/dev/ttyACM0",help='serial port')
args=p.parse_args()

my_file=Path(args.o)
if my_file.is_file():
    print('Error: {:s} exists.'.format(args.o))
    exit()
try:
    ser = serial.Serial(args.p,9600)
except:
    print('Error: cannot open serial port {:s}'.format(args.p))
    exit()

ser.close()
ser.open()

# list of column names
labels=[]
# data buffer; dict-of-lists keyed on column names
data={}

nlinesread=0
loginitiated=False
while True:
    serline=ser.readline()
    tokens=serline.decode().strip().split()
    nlinesread+=1
    if tokens[0]=='#LABELS':
        # this is a line with column labels;
        # if list of labels is not set, set it
        if len(labels)!=0 and 'PLACEHOLDER' in labels[0]:
            # we have placeholder labels, so 
            # replace them with these new labels
            for l,nl in zip(labels,tokens[1:]):
                data[nl]=data[l]
                del data[l]
        labels = tokens[1:]
    elif len(tokens)>1:
        # this is assumed to be a line of valid data
        if len(labels) == 0:
            # we've got data but haven't set the labels yet
            # so make some placeholder labels
            labels = ['PLACEHOLDER'+str(_) for _ in range(len(tokens))] 
        if len(data) == 0:
            # no columns exist yet in the data buffer;
            # create each column as a list keyed by its label
            for l,t in zip(labels,tokens):
                data[l]=[float(t)]
        else:
            # append each datum to its column in the buffer
            for l,t in zip(labels,tokens):
                data[l].append(float(t))
    if nlinesread%args.bs==0:
        if not loginitiated:
            if len(labels)==0 or 'PLACEHOLDER' in labels[0]:
                # wait until we have labels and they are not placeholders
                continue
            else:
                print('# Initiating log {:s}'.format(args.o))
                df=pd.DataFrame.from_dict(data)
                df.to_csv(args.o,index=False)
                loginitiated=True
                # empty the data buffer
                for l in labels:
                    data[l]=[]
        else:
            print('# Logging {:d} lines of buffered data'.format(len(data[labels[0]])))
            df=pd.DataFrame.from_dict(data)
            df.to_csv(args.o,mode='a',index=False,header=False)
            for l in labels:
                data[l]=[]
