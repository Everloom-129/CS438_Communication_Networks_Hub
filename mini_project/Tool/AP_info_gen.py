import pandas as pd
import csv
sheet = pd.read_excel(io = 'Access Point BSSID Export.xlsx')
data = []
for i in sheet.index.values:
    row_data = sheet.loc[i,['Access Point Name','Wired MAC Address','BSSID MAC','SSID - 2.4 and 5']].to_dict()

    data.append(row_data)
f = open('AP_info.csv','w')
writer = csv.writer(f)
header = ['Access Point Name,', 'BSSID MAC','SSID - 2.4 and 5']
writer.writerow(header)
row = []
for i in range(0,len(data)):
    name = data[i]['Access Point Name']
    name_id = int(name.split('-')[2])
    if name_id < 20 or name_id > 58: continue
    BSSID = data[i]['BSSID MAC'].split('\n')
    SSID = data[i]['SSID - 2.4 and 5'].split('\n')
    for j in range(0, len(BSSID)):
        row = [name, BSSID[j], SSID[j]]
        writer.writerow(row)
f.close()
print(name, BSSID, SSID)