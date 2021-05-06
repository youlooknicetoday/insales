from lxml import etree

parser = etree.XMLParser(encoding='utf-8', ns_clean=True, recover=True, huge_tree=True)


def read_xml_image(body, fields='all'):
    data = etree.fromstring(body)
    tags = map(lambda node: node.tag, data.xpath('//image')[0].getchildren())
    if fields != 'all' and all(field in tags for field in fields):
        pass
    print(list(data[0]))

    return list(tags)


