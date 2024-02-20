import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    rss_element = xml_tree.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': "http://www.itunes.com/dtds/podcast-1.0.dtd",
        'xmlns:content': "http://purl.org/rss/1.0/modules/content/"
    })

    channel_element = xml_tree.SubElement(rss_element, 'channel')
    link_prefix = yaml_data['link']

    xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
    xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
    xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix}).text = link_prefix

    for item in yaml_data['items']:  # Corrected the key for items
        item_element = xml_tree.SubElement(channel_element, 'item')
        xml_tree.SubElement(item_element, 'title').text = item['title']
        xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']  # Should be within item_element
        xml_tree.SubElement(item_element, 'description').text = item['description']  # Corrected key 'description'

        enclosure = xml_tree.SubElement(item_element, 'enclosure', {  # Corrected indentation
            'url': link_prefix + item['file'],  # Corrected key 'file'
            'type': 'audio/mpeg',
            'length': str(item['length'])  # Converted length to string
        })

    output_tree = xml_tree.ElementTree(rss_element)
    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
