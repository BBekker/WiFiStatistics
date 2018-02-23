import pyshark
import sys
import csv
import datetime

capture = pyshark.LiveCapture(sys.argv[1], capture_filter="wlan.fc.type eq 2", monitor_mode=True);



with open(datetime.now().isoformat() + '.csv', 'wb') as csvfile:
        fieldnames = ["timestamp", "channel", "signal", "datarate", "phy", "crc", "len"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for cap in capture.sniff_continously():
                row = {"timestamp" : frame.type,
                       "channel" : wlan_radio.channel,
                       "signal" : wlan_radio.signal_dbm,
                       "datarate" : wlan_radio.data_rate,
                       "phy" : wlan_radio.phy,
                       "crc" : wlan.fc.status,
                       "len" : frame.len}
                writer.writerow(row)
                       
