import pandas as pd
import csv
sheet = pd.read_excel(io = 'AP_BSSID.xlsx')
data = []
for i in sheet.index.values:
    row_data = sheet.loc[i,['Access_Point_Name','Wired_MAC_Address','BSSID-MAC','SSID-2.4_and_5']].to_dict()

    data.append(row_data)
f = open('AP_info_all.csv','w')
writer = csv.writer(f)
header = ['Access_Point_Name', 'BSSID-MAC','SSID-2.4_and_5']
writer.writerow(header)
row = []
for i in range(0,len(data)):
    name = data[i]['Access_Point_Name']
    name_id = int(name.split('-')[2])
    # if name_id < 20 or name_id > 58: continue
    BSSID = data[i]['BSSID-MAC'].split('\n')
    SSID = data[i]['SSID-2.4_and_5'].split('\n')
    for j in range(0, len(BSSID)):
        row = [name, BSSID[j], SSID[j]]
        writer.writerow(row)
f.close()
print(name, BSSID, SSID)