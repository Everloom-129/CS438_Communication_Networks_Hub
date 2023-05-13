import pandas as pd
import csv

floor = input("choose floor: 1 3\n")
if (floor == "1"):
    raw_data_path = "raw_data/" + "eduroam" + "_raw_data_" + "L" + floor + ".csv" # eduroam or illinois
    default_info_path = "AP_info/AP_info_L" + floor + ".csv"
else:  
    raw_data_path = "raw_data/" + "Illinois" + "_raw_data_" + "L" + floor + ".csv" # eduroam or illinois
    default_info_path = "AP_info/AP_info_L" + floor + ".csv"
single_path = "analysis/single_AP_strength_L" +floor+" .csv"
strength_dict = {}
MAC_passed = []
test_time = {}
info_dict = {}
with open(raw_data_path,'r') as fp:
    csvreader = csv.reader(fp)
    for line in csvreader:
        if line == ['SSID','BSSID','Signal Strength','current BSSID','x','y']: continue
        SSID, BSSID, RSSI, Cur_BSSID, x,y = line
        if BSSID not in MAC_passed:
            MAC_passed.append(BSSID)
        if (int(Cur_BSSID) != 0): 
            if (BSSID not in info_dict):
                info_dict[BSSID] = []
            else: info_dict[BSSID].append(line)
            if (BSSID not in strength_dict):
                test_time[BSSID] = 1
                strength_dict[BSSID] = int(RSSI)
            else:
                strength_dict[BSSID] = (strength_dict[BSSID] * test_time[BSSID] + int(RSSI))/(test_time[BSSID] + 1)
                test_time[BSSID] += 1

BSSID_AP = {}
with open(default_info_path,'r') as fp_info:
    csvreader = csv.reader(fp_info)
    for line in csvreader:
        if line == ['Access_Point_Name','BSSID-MAC','SSID-2.4_and_5']: continue
        if line == []: continue
        AP, BSSID, SSID = line
        BSSID_AP[BSSID] = AP
AP_used = []
AP_passed = []
for mac in MAC_passed:
    if mac not in BSSID_AP: continue
    if BSSID_AP[mac] not in AP_passed:
        AP_passed.append(BSSID_AP[mac])


with open(single_path, "w") as writing_fp:
    writer = csv.writer(writing_fp)
    writer.writerow(["BSSID","Sinal_strength"])
    for key in strength_dict:
        if key in BSSID_AP:
            writer.writerow([BSSID_AP[key],key, strength_dict[key]])
            if (BSSID_AP[key] not in AP_used):
                AP_used.append(BSSID_AP[key])
        else: writer.writerow(['Unknown',key, strength_dict[key]])

avg_strength = sum(strength_dict.values())/len(strength_dict)
avg_testing_time = sum(test_time.values())/len(test_time)
print("average signal strength of AP is:" + str(avg_strength))
print("average testing time for each AP is:" + str(avg_testing_time))
print("number of mac_address connected:" + str(len(strength_dict)))
print("number of AP connected:" + str(len(AP_used)))
if (floor == "3"):
    print("number of total AP in this floor:" + "37")
else:
    print("number of total AP in this floor:" + "39")
print("number of AP we passed is:" + str(len(AP_passed)))
print("using rate:" + str(len(AP_used)/len(AP_passed) * 100 ) + "%")
