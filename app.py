import requests
import xml.etree.ElementTree as ET

# Fetch the XML data from the URL
url = "https://www.boty-dux.cz/medfeet_feed.xml"
response = requests.get(url)
xml_data = response.content

# Parse the XML data
root = ET.fromstring(xml_data)

# Namespace
ns = {'ns': 'http://www.zbozi.cz/ns/offer/1.0'}

# Dictionary to store the data organized by ITEMGROUP_ID
product_groups = {}

# Iterate through each SHOPITEM in the XML
for item in root.findall('ns:SHOPITEM', ns):
    product_name = item.find('ns:PRODUCTNAME', ns).text
    item_group_id = item.find('ns:ITEMGROUP_ID', ns).text
    code = item.find('ns:CODE', ns).text
    stock = item.find('ns:STOCK', ns).text

    # If the ITEMGROUP_ID is not in the dictionary, initialize it
    if item_group_id not in product_groups:
        product_groups[item_group_id] = {
            'product_name': product_name.split(' - ')[0],  # Assuming the name before the first '-' is consistent
            'sizes': [],
            'stocks': []
        }

    # Add the size (from CODE) and stock to the corresponding ITEMGROUP_ID
    product_groups[item_group_id]['sizes'].append(code.split('-')[-1])
    product_groups[item_group_id]['stocks'].append(stock)

# Generate the HTML output
html_output = "<html><head><title>Chung-shi sklady</title></head><body>"

# Loop through each product group to create an HTML table
for item_group_id, details in product_groups.items():
    html_output += f"<h2>{details['product_name']}</h2>"
    html_output += "<table border='1' cellpadding='5' cellspacing='0'>"

    # Size row
    html_output += "<tr>"
    for size in details['sizes']:
        html_output += f"<th>{size}</th>"
    html_output += "</tr>"

    # Stock row
    html_output += "<tr>"
    for stock in details['stocks']:
        html_output += f"<td>{stock}</td>"
    html_output += "</tr>"

    html_output += "</table><br>"

html_output += "</body></html>"

# Save the HTML to a file
with open("index.html", "w") as file:
    file.write(html_output)

print("HTML report generated successfully.")