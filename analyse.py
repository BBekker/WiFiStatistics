import pandas
import matplotlib.pyplot as plt
import statsmodels.api as sm
import sys
import re
import numpy as np
import math

argv = sys.argv
data = pandas.read_csv(argv[1], nrows = int(argv[2]), header=None, names=['timestamp','chan','signal','datarate','phy','crc','length'])
data['dataratefloat'] = data[['datarate']].applymap(lambda x: float(str(x).split(',')[0]))

print(data)
#print(data.groupby('dataratefloat').count())
#CRC vs signal strength
#
# bysignal = data.groupby('signal')['crc'].mean().rolling(1).mean()
# samples = data.groupby('signal')['crc'].count()
# fig =bysignal[samples>10].plot(title='percentage of correctly received packets vs signal strength', color='b', style='.-')
#
# fig2=samples[samples>10].plot(ax=fig, secondary_y=True, color='y', style='.-')
# fig2.set_ylabel("samples", color='y')
# fig.set_xlabel("SSI signal strength [dBm]")
# fig.set_ylabel("Percentage of packets correctly received", color='b')
# plt.show()


def bydatarate(data):
    bydatarate = data.groupby(['signal','datarate'])['crc'].mean()
    print(bydatarate)
    samples = data.groupby(['signal','datarate'])['crc'].count()
    plt.figure()
    fig =bydatarate.unstack().plot(subplots=True,title='percentage of correctly received packets vs signal strength by datarate')
    #samples.unstack().plot(ax=fig, secondary_y=True)
    plt.show()

def graphall(data):

    # CRC vs signal strength

    bysignal = data.groupby('signal')['crc'].mean().rolling(1).mean()
    samples = data.groupby('signal')['crc'].count()
    fig =bysignal[samples>10].plot(title='percentage of correctly received packets vs signal strength', color='b', style='.-')

    fig2=samples[samples>10].plot(ax=fig, secondary_y=True, color='y', style='.-')
    fig2.set_ylabel("samples", color='y')
    fig.set_xlabel("SSI signal strength [dBm]")
    fig.set_ylabel("Percentage of packets correctly received", color='b')
    plt.show()

def graph58ghz(data):

    filter = data['chan'].apply(int) > 15
    bysignal = data[filter].groupby('signal')['crc'].mean().rolling(1).mean()
    samples = data[filter].groupby('signal')['crc'].count()
    fig = bysignal[samples > 10].plot(title='5.8 GHz', color='b', style='.-')

    fig2 = samples[samples > 10].plot(ax=fig, secondary_y=True, color='y', style='.-')
    fig2.set_ylabel("samples", color='y')
    fig.set_xlabel("SSI signal strength [dBm]")
    fig.set_ylabel("Percentage of packets correctly received", color='b')
    plt.show()

def graph58ghz144mbps(data):

    filter = data['chan'].apply(int) > 15
    bysignal = data[filter][data['dataratefloat'] >= 80].groupby('signal')['crc'].mean().rolling(1).mean()
    samples = data[filter][data['dataratefloat'] >= 80].groupby('signal')['crc'].count()
    fig = bysignal[samples > 10].plot(title='5.8 GHz', color='b', style='.-')

    fig2 = samples[samples > 10].plot(ax=fig, secondary_y=True, color='y', style='.-')
    fig2.set_ylabel("samples", color='y')
    fig.set_xlabel("SSI signal strength [dBm]")
    fig.set_ylabel("Percentage of packets correctly received", color='b')
    plt.show()


def graph24ghz72mbps(data):

    filter = data['chan'].apply(int) < 15
    bysignal = data[filter][data['dataratefloat'] == 24.0 ].groupby('signal')['crc'].mean().rolling(1).mean()
    samples = data[filter][data['dataratefloat'] == 24.0 ].groupby('signal')['crc'].count()
    fig = bysignal[samples > 10].plot(title='correctly received packets at 2.8 GHz, 72.2Mbps', color='b', style='.-')

    fig2 = samples[samples > 10].plot(ax=fig, secondary_y=True, color='y', style='.-')
    fig2.set_ylabel("samples", color='y')
    fig.set_xlabel("SSI signal strength [dBm]")
    fig.set_ylabel("Percentage of packets correctly received", color='b')
    plt.show()

def graph24ghz(data):

    filter = data['chan'].apply(int) < 15
    bysignal = data[filter].groupby('signal')['crc'].mean().rolling(1).mean()
    samples = data[filter].groupby('signal')['crc'].count()
    fig = bysignal[samples > 10].plot(title='correctly received packets at 2.8 GHz, 72.2Mbps', color='b', style='.-')

    fig2 = samples[samples > 10].plot(ax=fig, secondary_y=True, color='y', style='.-')
    fig2.set_ylabel("samples", color='y')
    fig.set_xlabel("SSI signal strength [dBm]")
    fig.set_ylabel("Percentage of packets correctly received", color='b')
    plt.show()

def graphlength(data):

    samples = data.groupby('length')['crc'].count()
    bylength = data.groupby('length')['crc'].mean()[samples>4]
    plt.figure()
    fig =bylength[samples>4].plot(title='correctly received packets vs packet length', color='gray')
    bylength[samples>4].rolling(20).mean().plot(color='black')
    fig.set_ylabel("ratio of correct packets")
    fig.set_xlabel("packet length [Bytes]")
    #samples[samples > 10].plot(ax=fig, secondary_y=True)
    #fig.right_ax.set_yscale('log')
    #l = np.arange(150,1700,1)
    #plt.plot(l, (1 - (0.001**l)))

    plt.show()

    # nf = bylength.to_frame().reset_index().dropna();

    # newindex = pandas.RangeIndex(1,1618,1)

    # resampled = nf.reindex('length',newindex)
    # #resampled.interpolate('index',inplace=True)

    # print(resampled)
    # print(sm.OLS(nf['crc'],nf['length']).fit().summary())

def graphairtime(data):
    data['airtime'] = (data['length'] * 8) / data['dataratefloat']

    samples = data.groupby('airtime')['crc'].count()
    bylength = data.groupby('airtime')['crc'].mean()[samples>4].rolling(5).mean()
    plt.figure()
    fig =bylength[samples>4].plot(title='percentage of correctly received packets vs packet airtime',color='gray')
    bylength[samples>4].rolling(50).mean().plot(color='black')
    fig.set_xlabel("airtime [uS]")
    fig.set_ylabel("non-crc error")
    #samples[samples > 10].plot(ax=fig, secondary_y=True)
    #fig.right_ax.set_yscale('log')
    #l = np.arange(150,1700,1)
    #plt.plot(l, (1 - (0.001**l)))

    plt.show()


def dataratevsstrength(data):
    data['dataratefloat'] = data[['datarate']].applymap(lambda x: float(x.split(',')[0]))
    print(data[data.crc == 1][['crc','signal','dataratefloat']].groupby('signal')['dataratefloat'].max().to_frame())
    fig = data[data.crc == 1][['crc','signal','dataratefloat']].groupby('signal')['dataratefloat'].mean().plot(color='y', style='.-')
    fig2 = data[['crc','signal','dataratefloat']].groupby('signal')['dataratefloat'].mean().plot(color='b', style='.-')
    data[['crc','signal','dataratefloat']].groupby('signal')['dataratefloat'].max().plot(color='b', style='.-')
    data[data.crc == 1][['crc','signal','dataratefloat']].groupby('signal')['dataratefloat'].max().plot(color='y', style='.-')

    data[['crc','signal','dataratefloat']].groupby('signal')['dataratefloat'].min().plot(color='b', style='.-')
    data[data.crc == 1][['crc','signal','dataratefloat']].groupby('signal')['dataratefloat'].min().plot(color='y', style='.-')

    fig.set_ylabel("datarate [Mbps]")
    fig.set_xlabel("SSI signal strength [dBm]")
    fig.legend([fig,fig2],["all packets", "successful packets"])
    plt.show()

graphall(data)
bydatarate(data)
graph58ghz(data)
graph24ghz(data)
graph24ghz72mbps(data)
graphlength(data)
graphairtime(data)
dataratevsstrength(data)
#print(data.groupby('chan')['crc'].mean())
#print(data.groupby('chan')['crc'].count())
