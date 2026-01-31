import sys
import os
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def get_last_modified(url):
    """Fetch the Last-Modified header from the URL."""
    try:
        # Use HEAD to get headers without downloading the whole page
        response = requests.head(url, timeout=10, allow_redirects=True)
        last_mod = response.headers.get('Last-Modified')
        
        if last_mod:
            # Parse GMT format: 'Wed, 21 Oct 2015 07:28:00 GMT'
            dt = datetime.strptime(last_mod, '%a, %d %b %Y %H:%M:%S %Z')
            return dt.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Warning: Could not fetch {url} - {e}")
    
    # Fallback to current date if header is missing or request fails
    return datetime.now().strftime('%Y-%m-%d')

def generate_sitemap(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    # Create the root element with the standard sitemap namespace
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Ignore comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            print(f"Processing: {line}")
            lastmod_date = get_last_modified(line)

            # Build XML structure
            url_node = ET.SubElement(urlset, "url")
            ET.SubElement(url_node, "loc").text = line
            ET.SubElement(url_node, "lastmod").text = lastmod_date

    # Pretty-print the XML
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    with open("sitemap.xml", "w", encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print("\nSuccess: sitemap.xml has been generated.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gensitemap.py <filename>")
    else:
        generate_sitemap(sys.argv[1])