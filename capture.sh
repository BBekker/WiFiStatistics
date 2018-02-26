
tshark -I -i wlan0mon -Y "wlan.fc.type == 2" -T fields -E separator=, -E quote=d -e frame.time -e wlan_radio.channel -e wlan_radio.signal_dbm -e wlan_radio.data_rate -e wlan_radio.phy -e wlan.fcs.status -e frame.len | gzip > $1.gz
