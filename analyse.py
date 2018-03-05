import pandas
import matplotlib.pyplot as plt
import statsmodels.api as sm
import sys

argv = sys.argv
data = pandas.read_csv(argv[1], nrows = int(argv[2]), header=None, names=['timestamp','chan','signal','datarate','phy','crc','length'])

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


def graph24ghz(data):
    filter = data['chan'].apply(int) < 15
    bysignal = data[filter].groupby('signal')['crc'].mean().rolling(1).mean()
    samples = data[filter].groupby('signal')['crc'].count()
    fig = bysignal[samples > 10].plot(title='5.8 GHz', color='b', style='.-')

    fig2 = samples[samples > 10].plot(ax=fig, secondary_y=True, color='y', style='.-')
    fig2.set_ylabel("samples", color='y')
    fig.set_xlabel("SSI signal strength [dBm]")
    fig.set_ylabel("Percentage of packets correctly received", color='b')
    plt.show()

def graphlength(data):

    samples = data.groupby('length')['crc'].count()
    bylength = data.groupby('length')['crc'].mean()[samples>5].rolling(20).mean()
    plt.figure()
    fig =bylength.plot(title='percentage of correctly received packets vs packet length')
    samples[samples > 10].plot(ax=fig, secondary_y=True)
    fig.right_ax.set_yscale('log')
    plt.show()

lengths = data.groupby('length')['crc'].mean().to_frame().reset_index(level=0)
print(sm.OLS(lengths['length'], lengths['crc']).fit().summary())
sm.graphics.plot_partregress('crc', 'length', ['crc','length'],data=lengths)
plt.show()
#graphlength(data)