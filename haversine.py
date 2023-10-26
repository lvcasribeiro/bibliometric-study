import xml.etree.ElementTree as ET
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance

def find_nearest_waypoints(kml_file, reference_lat, reference_lon):
    tree = ET.parse(kml_file)
    root = tree.getroot()

    waypoints = []

    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name = placemark.find('.//{http://www.opengis.net/kml/2.2}name').text
        coordinates = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates').text
        lon, lat, _ = map(float, coordinates.split(','))

        distance = haversine(reference_lat, reference_lon, lat, lon)

        waypoints.append((name, lat, lon, distance))

    waypoints.sort(key=lambda x: x[3])
    return waypoints[:3]

kml_file = 'merged-kml-file.kml'
reference_lat = 40.0
reference_lon = -75.0

nearest_waypoints = find_nearest_waypoints(kml_file, reference_lat, reference_lon)
for waypoint in nearest_waypoints:
    name, lat, lon, distance = waypoint
    print(f'Waypoint: {name}, Latitude: {lat}, Longitude: {lon}, Distância: {distance} km')
