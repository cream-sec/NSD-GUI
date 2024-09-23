import base64
import xml.etree.ElementTree as ET
import requests

# 向某个地址组添加IP地址
def addIP(ip, username, password, ipgroup, address, count):
    com_string = username + ":" + password
    com_string_bytes = com_string.encode('utf-8')
    encoded_bytes = base64.b64encode(com_string_bytes)
    url = "http://" + ip + ":9000/restconf/data/huawei-address-set:address-set/addr-group=public," + ipgroup
    headers = {
        "Conncection": "keep-alive",
        "Accept": "application/yang.data+xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/yang.data+xml",
        "Authorization": "Basic " + encoded_bytes.decode('utf-8')
    }

    addr_group = ET.Element("addr-group")
    for ip, subnet in address:
        elements = ET.SubElement(addr_group, "elements")
        ET.SubElement(elements, "elem-id").text = str(count)
        if subnet:
            ET.SubElement(elements, "address-ipv4").text = f"{ip}/{subnet}"
        else:
            ET.SubElement(elements, "address-ipv4").text = f"{ip}/32"
        count += 1
    xml_data = ET.tostring(addr_group, encoding="unicode")
    response = requests.patch(url, headers=headers, data=xml_data)
    if response.status_code == 200 or response.status_code == 204:
        return True
    else:
        return False

