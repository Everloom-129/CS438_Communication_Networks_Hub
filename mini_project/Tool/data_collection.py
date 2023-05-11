import sys
import time
import pywifi
import csv
import subprocess
import re
from pywifi import const

# TODO laplace smoothing
NumberOfScan = 3 # Take median of each scanning to smooth output
TestPoint    = 5 # Test point used for running program once
input_data_path = "raw_data//eduroam_raw_data_1L.csv"

def scan_wifi(interface):
    interface.scan()
    time.sleep(3)  # Give some time for the scan to complete
    networks = interface.scan_results()
    current_BSSID = get_BSSID()
    wifi_data = []

    for network in networks:
        ssid = network.ssid
        bssid = network.bssid[:-1]

        signal_strength = network.signal
        
        current = 1 if (current_BSSID==bssid) else 0
        if( current == 1 ):
            print("=== ONE exists") 
        wifi_data.append([ssid, bssid, signal_strength, current])
        # print(f"SSID: {ssid}, BSSID: {bssid}, Signal Strength: {signal_strength} dBm, current_bssid: {current}")

    return wifi_data

def get_BSSID():
    # Run the netsh command and capture its output
    output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'])
    # print("output: ", output)
    
    # Use a regular expression to extract the BSSID from the output
    match = re.search(r'BSSID\s+:\s+([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', output.decode('gbk'))
    if match:
        # print("match",match)
        bssid = match.group(0).split(': ')[1].strip()
        print('BSSID of Wi-Fi access point:', bssid)
        ap_name = bssid_to_ap_name(bssid)
        print("AP name is: ",ap_name)
        return bssid
    else:
        print('Unable to find BSSID in netsh output')


def bssid_to_ap_name(bssid):
    bssid_map = {}

    # Read the "AP_info.csv" file and create a dictionary mapping BSSIDs to Access Point names
    with open("AP_info\\AP_info_all.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) < 3:
                continue
            # print("translation!" b)
            ap_name, bssid_mac, _ = row
            bssid_map[bssid_mac] = ap_name

    # Return the Access Point name for the given BSSID
    return bssid_map.get(bssid, "Unknown AP")


def get_current_coordinate():
    # Add a function to get test point (x, y) by manually input
    x,y = input("Enter the xy-coordinate of the test point: ").split(",")
    return int(x), int(y)

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

    raw_data_file = input_data_path

    # Check if the file exists, and if not, create it with headers
    try:
        with open(raw_data_file, "x", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["SSID", "BSSID", "Signal Strength", "current BSSID", "x", "y"])
    except FileExistsError:
        pass  # The file already exists, no need to write headers



    with open(raw_data_file, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["SSID", "BSSID", "Signal Strength", "current BSSID", "x", "y"])
        
        for _ in range(TestPoint):# test five points
            test_times = NumberOfScan
            x,y = get_current_coordinate()
            for i in range(test_times):
                wifi_data = scan_wifi(interface)
                for data in wifi_data:
                    if data[0] == "IllinoisNet" or data[0] == "eduroam":
                        csv_writer.writerow(data + [x,y])
                time.sleep(3)  # Wait for 5 seconds before scanning again


    
if __name__ == "__main__":
    main()