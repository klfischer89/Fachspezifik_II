import xml.etree.ElementTree as ET
tree = ET.parse('data\data.xml')

root = tree.getroot()
print(root.tag)

for mitarbeiter in root.findall('mitarbeiter'):
    position = mitarbeiter.find('position').text
    gehalt = mitarbeiter.find('gehalt').text
    print(position)
    print(gehalt)

import requests
try:
    response = requests.get()
    response.raise_for_status()
    print(response.json())
except requests.exceptions.HTTPError as e:
    print("HTTP-Fehler: ", e)