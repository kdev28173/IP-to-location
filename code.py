import folium
import pygeoip
import pyshark

gi = pygeoip.GeoIP('GeoLiteCity.dat')

# Initialize the map
mapobj = folium.Map(location=['33.43144133557529', '40.07812500000001'],
                    zoom_start=2, zoom_control=True)

# Add a layer to mapobj
sendlayer = folium.FeatureGroup(name='Send').add_to(mapobj)
receivelayer = folium.FeatureGroup(name='Receive').add_to(mapobj)

# Check function to see if ip is available or not
def check(ip):
    if gi.record_by_addr(ip)['latitude'] is None:
        return None
    else:
        return 1

# Function for mappign the data
def mapping(send, receive):
    ignored = [] # This is for IPs which cannot be mapped with the geolitecity dataset
    for i, j in send.items():
        try:
            if (check(str(i)) == 1):
                lat = gi.record_by_addr(i)['latitude']
                lon = gi.record_by_addr(i)['longitude']
                folium.Marker(location=[lat, lon], icon=folium.Icon(color='red', icon='glyphicon-envelope'),
                              tooltip='Packets : ' + str(j)).add_to(sendlayer)
                folium.Circle(location=[lat, lon], radius=2000, color='red', opacity='0.75', fill=True,
                              tooltip='Packets : ' + str(j)).add_to(sendlayer)
                print('Send: ', i, '=', lat, ',', lon)
        except:
            if i not in ignored:
                ignored.append(i)
            pass
    for i, j in receive.items():
        try:
            if (check(str(i)) == 1):
                lat = gi.record_by_addr(i)['latitude']
                lon = gi.record_by_addr(i)['longitude']
                folium.Marker(location=[lat, lon], icon=folium.Icon(color='blue', icon='glyphicon-cloud'),
                              tooltip='Packets : ' + str(j)).add_to(receivelayer)
                folium.Circle(location=[lat, lon], radius=2500, color='blue', opacity='0.75',fill=True,
                              tooltip='Packets : ' + str(j)).add_to(receivelayer)
                print('receive: ', i, '=', lat, ',', lon)
        except:
            if i not in ignored:
                ignored.append(i)
            pass

    folium.LayerControl().add_to(mapobj)
    mapobj.save('hello1.html')
    print('Ignored IP\'s are: ')
    print(ignored)


def main():
    c = pyshark.FileCapture('data.pcap', display_filter='ip') # Use the capture file
    sent_dict = {} # Used for storing the IPs to which the device has sent packets to
    received_dict = {} # # Used for storing the IPs to which the device has received packets from
    
    # get all the unique IP's along with the count
    for i in c:
        src = i.ip.src
        dst = i.ip.dst
        if src not in sent_dict:
            sent_dict[src] = 1
        else:
            sent_dict[src] += 1
        if dst not in received_dict:
            received_dict[dst] = 1
        else:
            received_dict[dst] += 1

# Send the dictionaries to the mapping function
    mapping(sent_dict, received_dict)

if __name__ == '__main__':
    main()
