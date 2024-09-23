import base64
import xml.etree.ElementTree as ET
import requests


# 获取地址内的内容数量
def ipCount(ip, username, password, ipname):
    com_string = f"{username}:{password}"
    encoded_bytes = base64.b64encode(com_string.encode('utf-8'))
    url = f"http://{ip}:9000/restconf/data/huawei-address-set:address-set/addr-object=public,{ipname}"
    headers = {
        "Connection": "keep-alive",
        "Accept": "application/yang.data+xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/yang.data+xml",
        "Authorization": f"Basic {encoded_bytes.decode('utf-8')}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 204 or response.status_code == 500:
            return None
        response.raise_for_status()
        root = ET.fromstring(response.text)
        if root:
            ns = {'ns': 'urn:huawei:params:xml:ns:yang:huawei-address-set'}
            elements_count = len(root.findall('.//ns:elements', namespaces=ns))
            return str(elements_count)
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"[-] {ip} - {username} - {password} - Request failed: {e}")
        return []
