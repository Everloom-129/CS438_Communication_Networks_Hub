# Tool development buglog
Wang,Jie
Wu,Jiaxin

## Data_collection
1. 


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
    This is beacuse each AP has two signal spectrum 


## Data_preprocessing

## Heatmap_generation

## 