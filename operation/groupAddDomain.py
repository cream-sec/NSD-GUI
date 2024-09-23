import base64
import requests

# 向某个域名组添加域名
def addDomain(ip, username, password, doaminname, doamins):
    com_string = username + ":" + password
    com_string_bytes = com_string.encode('utf-8')
    encoded_bytes = base64.b64encode(com_string_bytes)
    url = "http://" + ip + ":9000/restconf/data/huawei-domain-set:domain-sets/vsys=public/domain-set=" + doaminname
    headers = {
        "Conncection": "keep-alive",
        "Accept": "application/yang.data+xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/yang.data+xml",
        "Authorization": "Basic " + encoded_bytes.decode('utf-8')
    }
    xml_output = "<domain-set>\n"
    for domain in doamins:
        xml_output += f"  <domain>{domain}</domain>\n"
    xml_output += "</domain-set>"
    response = requests.patch(url, headers=headers, data=xml_output)
    if response.status_code == 200 or response.status_code == 204:
        return True
    else:
        return False