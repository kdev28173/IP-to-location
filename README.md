# IP-to-location
This code maps the IP's which the device is communicating with.
This code only works for pcap files and is not for dynamically taking IPs from device and mapping them.
In this Code I used pygeoip,pyshark,folium libraries.
pygeoip: This is for getting latitude and longitude from a given ip ( Few IPs are not available in the geolitecity.dat so they are not mapped )
pyshark: This is used for reading from a pcap file
folium: To map the latitudes and longitudes.
