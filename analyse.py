import pyshark
import sys

capture = pyshark.FileCapture(sys.argv[1]);

for cap in capture:
	if cap.wlan.fcs_status == 0:
		print(cap)