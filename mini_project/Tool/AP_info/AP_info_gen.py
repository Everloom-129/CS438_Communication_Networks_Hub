import pandas as pd
import csv
sheet = pd.read_excel(io = 'AP_BSSID.xlsx')
floor = input("input the floor you want, choice: 0 1 2 3 4 all\n")
data = []
AP_range = [(1,19),(20,58),(59,98),(99,135),(135,171)]
for i in sheet.index.values:
    row_data = sheet.loc[i,['Access_Point_Name','Wired_MAC_Address','BSSID_MAC','SSID_2.4_and_5']].to_dict()

    data.append(row_data)
if (floor == "all"):
    f = open('AP_info_all.csv','w')
else:
    file_name = "AP_info_" + "L" + floor + ".csv"
    print(file_name)
    f = open(file_name, "w")
writer = csv.writer(f)
header = ['Access_Point_Name', 'BSSID-MAC','SSID-2.4_and_5']
writer.writerow(header)
row = []
for i in range(0,len(data)):
    name = data[i]['Access_Point_Name']
    name_id = int(name.split('-')[2])

    if (floor != "all"):
        if name_id < AP_range[int(floor)][0] or name_id > AP_range[int(floor)][1]: continue
    BSSID = data[i]['BSSID_MAC'].split('\n')
    SSID = data[i]['SSID_2.4_and_5'].split('\n')
    for j in range(0, len(BSSID)):
        row = [name, BSSID[j], SSID[j]]
        writer.writerow(row)
f.close()
print(name, BSSID, SSID)