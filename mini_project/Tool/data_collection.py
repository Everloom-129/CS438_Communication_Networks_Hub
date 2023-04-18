import os
import sys
import csv
import time
from scapy.all import *


def signal_handler(signal, frame):
    sys.exit(0)


def callback(packet):
    if packet.haslayer(Dot11):
        if packet.type == 0 and packet.subtype == 8:
            bssid = packet.addr2
            ssid = packet.info.decode("utf-8")
            signal_strength = -(256 - packet.notdecoded[-4:-3][0])

            print(f"SSID: {ssid}, BSSID: {bssid}, Signal Strength: {signal_strength} dBm")


if __name__ == "__main__":
    interface = "wlan0"

    if len(sys.argv) > 1:
        interface = sys.argv[1]

    if os.geteuid() != 0:
        print("Please run this script as root.")
        sys.exit(1)

    print(f"Sniffing on interface {interface}")
    sniff(iface=interface, prn=callback, store=0)
