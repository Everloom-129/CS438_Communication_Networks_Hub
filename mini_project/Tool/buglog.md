# Tool development buglog
Wang,Jie
Wu,Jiaxin

## Coordinate Generation
<--------------------------------------------------------->
                          BUG 0                          
<--------------------------------------------------------->
Time:
    2022.05.07.
Creator:
    Jie Wang.
Description:
    The ap info floor plan naming is incorrect, after checking the floor plan, we recert them.
Solution:
    


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

<--------------------------------------------------------->
                          BUG 2                          
<--------------------------------------------------------->
Time:
    2022.05.10.
Creator:
    Jie Wang.
Description:
    when I was collecting the data, I found the signal strength of one AP diverges greatly at the same point, like this:
    AP1, (x1,y1), -86dB
    AP1, (x1,y1), -60dB

Solution:
    There are several factors that can cause variations in signal strength for the same access point (AP) at the same location:

1. Interference: Wi-Fi signals can be affected by interference from other electronic devices, such as microwaves, cordless phones, and other Wi-Fi networks, which can cause fluctuations in signal strength.

2. Multipath propagation: In an indoor environment, Wi-Fi signals can bounce off walls, ceilings, and other objects, creating multiple paths for the signal to reach the receiver. This can lead to constructive and destructive interference, causing fluctuations in signal strength.

3. Obstacles: Obstacles like walls, furniture, and people can absorb or reflect Wi-Fi signals, causing the signal strength to vary as the environment changes.

4. Antenna orientation: The orientation of the antennas on both the access point and the client device can have a significant impact on the signal strength. Even small changes in the orientation of the device can result in fluctuations in signal strength.

5. Device calibration: The accuracy of the signal strength measurements can also be affected by the calibration of the Wi-Fi hardware on the client device. Different devices or chipsets might report different signal strength values for the same access point.

To minimize fluctuations in signal strength, you can try taking multiple measurements at each location and calculate the average signal strength. Additionally, make sure that there are no significant changes in the environment or the position of the client device during the data collection process.



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