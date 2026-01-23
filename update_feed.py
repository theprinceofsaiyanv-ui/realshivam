import xml.etree.ElementTree as ET
import urllib.request
import json

CHANNEL_ID = "UCUktjMxdetLyHb-Pkr4tYPg"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def main():
    xml_data = urllib.request.urlopen(FEED_URL, timeout=30).read()
    root = ET.fromstring(xml_data)

    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "media": "http://search.yahoo.com/mrss/"
    }

    items = []
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", default="", namespaces=ns)
        link_el = entry.find("atom:link", ns)
        link = link_el.attrib.get("href", "") if link_el is not None else ""
        published = entry.findtext("atom:published", default="", namespaces=ns)

        thumb_el = entry.find(".//media:thumbnail", ns)
        thumb = thumb_el.attrib.get("url", "") if thumb_el is not None else ""

        items.append({
            "title": title,
            "link": link,
            "published": published,
            "thumbnail": thumb
        })

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"items": items}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
