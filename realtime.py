import serial
import matplotlib.pyplot as plt
from iapws import IAPWS97

plt.ion()
fig,ax=plt.subplots(nrows=3,ncols=1)
ax[2].set_xlabel('time (s)')
ax[2].set_ylabel('T (C)')
ax[1].set_ylabel('$y_w$')
ax[0].set_ylabel('$h_r$')
ser = serial.Serial('/dev/ttyACM0',9600)
ser.close()
ser.open()
h_in=[]
h_out=[]
t_in=[]
t_out=[]
pw_i=[]
pw_o=[]
t_cal=[]
seconds=[]
i = 0
while True:
    data = ser.readline()
    tokens=data.decode().split()
    if len(tokens) < 5:
        continue
    h_in.append(float(tokens[0]))
    t_in.append(float(tokens[1]))
    h_out.append(float(tokens[2]))
    t_out.append(float(tokens[3]))
    t_cal.append(float(tokens[4]))
    sat_steam=IAPWS97(T=t_in[-1]+273.15,x=1)
    pvap_in = sat_steam.P/9.86923
    pw_in=h_in[-1]*pvap_in
    sat_steam=IAPWS97(T=t_out[-1]+273.15,x=1)
    pvap_out = sat_steam.P/9.86923
    pw_out=h_out[-1]*pvap_out
    pw_i.append(pw_in)
    pw_o.append(pw_out)
    seconds.append(i)
    ax[0].scatter(i, h_in[-1], color='blue')
    ax[0].scatter(i, h_out[-1], color='red')
    ax[1].scatter(i, pw_in, color='blue')
    ax[1].scatter(i, pw_out, color='red')
    ax[2].scatter(i, t_in[-1], color='blue')
    ax[2].scatter(i, t_out[-1], color='red')
    ax[2].scatter(i, t_cal[-1], color='black')
    i += 1
    plt.show()
    plt.pause(1)
