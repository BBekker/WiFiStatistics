import pandas
import matplotlib.pyplot as plt
import sys

argv = sys.argv
data = pandas.read_csv(argv[1],nrows=int(argv[2]), header=None, names=['timestamp','chan','signal','datarate','phy','crc','length'])

CRC vs signal strengh

bysignal = data.groupby('signal')['crc'].mean()
samples = data.groupby('signal')['crc'].count()
plt.figure()
fig =bysignal.plot(title='percentage of correctly received packets vs signal strength')
samples.plot(ax=fig, secondary_y=True)
plt.show()


bylength = data.groupby('length')['crc'].mean().rolling(10).mean()
samples = data.groupby('length')['crc'].count()
plt.figure()
fig =bylength.plot(title='percentage of correctly received packets vs packet length', logx=True)
samples.plot(ax=fig, secondary_y=True)
fig.right_ax.set_yscale('log')
plt.show()

bysignal = data.groupby(['signal','chan'])['crc'].mean()
print(bysignal)
samples = data.groupby(['signal','chan'])['crc'].count()
plt.figure()
fig =bysignal.unstack().plot(subplots=True,title='percentage of correctly received packets vs signal strength')
#samples.unstack().plot(ax=fig, secondary_y=True)
plt.show()