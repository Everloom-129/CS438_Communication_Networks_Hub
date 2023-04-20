import sys
import time
import pywifi
import csv
from pywifi import const

def scan_wifi(interface):
    interface.scan()
    time.sleep(3)  # Give some time for the scan to complete
    networks = interface.scan_results()

    wifi_data = []

    for network in networks:
        ssid = network.ssid
        bssid = network.bssid
        signal_strength = network.signal

        wifi_data.append([ssid, bssid, signal_strength])
        print(f"SSID: {ssid}, BSSID: {bssid}, Signal Strength: {signal_strength} dBm")

    return wifi_data

def main():
    print("start finding wifi connection")
    wifi = pywifi.PyWiFi()

    if len(sys.argv) > 1:
        interface_name = sys.argv[1]
    else:
        interface_name = None
    
    for iface in wifi.interfaces():
        if interface_name is None or iface.name() == interface_name:
            interface = iface
            break
    else:
        print(f"No Wi-Fi interface with name '{interface_name}' found.")
        sys.exit(1)

    print(f"Scanning Wi-Fi networks on interface {interface.name()}")

    with open("raw_data.csv", mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["SSID", "BSSID", "Signal Strength"])
        FLAG = 0
        while FLAG<3:
            wifi_data = scan_wifi(interface)
            for data in wifi_data:
                csv_writer.writerow(data)

            time.sleep(5)  # Wait for 5 seconds before scanning again
            FLAG += 1
if __name__ == "__main__":
    main()
