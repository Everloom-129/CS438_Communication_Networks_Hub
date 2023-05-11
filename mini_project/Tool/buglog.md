# Tool development buglog
Wang,Jie
Wu,Jiaxin

## Data_collection
To do:
Mark test locations on the map, then put the coordinates in a csv.
<--------------------------------------------------------->
                          BUG 1                          
<--------------------------------------------------------->
Time:
    2022.04.19.
Creator:
    Jie Wang
Description:
    In data_collection.py will generate duplicate BSSID info.
    for instance:
    - SSID,BSSID,Signal Strength,Latitude,Longitude
    - eduroam,44:12:44:6d:cd:91:,-68,-1.9893346,30.0861036
    - eduroam,44:12:44:6d:cd:91:,-68,-1.9893346,30.0861036
Solution:
    This is beacuse each AP has two signal spectrum: 2.4G and 5G
    According to the IT team, they are not implicitly shown in the WLAN
    but we can still check the protocol our device is using
    It seems it will automatically select the highest speed one.
    - Jie's laptop can only support WIFI 5, U/D = 520/650 (Mbps)
    - Jiaxin's laptop can support WIFI 6, U/D = 880/910 (Mbps)

    We handle this difference in Data_preprocessing.py

## Data_preprocessing

1st floor: wap-0563-20 to wap-0563-58

To do:
 
<--------------------------------------------------------->
                          BUG 1                          
<--------------------------------------------------------->
Time:
    2022.05.02.
Creator:
    Jiaxin Wu
Description:
For each test location, we need also check which mac address 
we are connecting at that location, and the signal strength of 
that AP will be kept as the signal strength at this location.
    
Solution:
    

## Heatmap_generation


- Image reversed 
    x = n - x?
- data coordinate 
- 
## 