import base64
import xml.etree.ElementTree as ET
import requests

# 获取防火墙中的安全策略
def ruleNameAddress(ip, username, password):
    com_string = f"{username}:{password}"
    encoded_bytes = base64.b64encode(com_string.encode('utf-8'))
    url = f"http://{ip}:9000/restconf/data/huawei-security-policy:sec-policy"
    headers = {
        "Connection": "keep-alive",
        "Accept": "application/yang.data+xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/yang.data+xml",
        "Authorization": f"Basic {encoded_bytes.decode('utf-8')}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        ns = {
            'base': 'urn:ietf:params:xml:ns:restconf:base:1.0',
            'huawei': 'urn:huawei:params:xml:ns:yang:huawei-security-policy'
        }
        rules = []
        for rule in root.findall('.//huawei:rule', ns):
            name = rule.find('huawei:name', ns).text
            action = rule.find('huawei:action', ns).text
            enable = rule.find('huawei:enable', ns).text

            source_ips = rule.findall('.//huawei:source-ip/huawei:address-set', ns)
            dest_ips = rule.findall('.//huawei:destination-ip/huawei:address-set', ns)
            source_ipv4s = rule.findall('.//huawei:source-ip/huawei:address-ipv4', ns)
            dest_ipv4s = rule.findall('.//huawei:destination-ip/huawei:address-ipv4', ns)
            domain_sets = rule.findall('.//huawei:domain-set', ns)

            source_ip_list = [ip.text for ip in source_ips] + [ip.text for ip in source_ipv4s]
            dest_ip_list = [ip.text for ip in dest_ips] + [ip.text for ip in dest_ipv4s]
            domain_set_list = [domain.text for domain in domain_sets]

            if not source_ip_list:
                source_ip_list = ["any"]
            if not dest_ip_list:
                dest_ip_list = ["any"]

            rules.append({
                "name": name,
                "action": action,
                "enable": enable,
                "source_addresses": ", ".join(source_ip_list),
                "destination_addresses": ", ".join(dest_ip_list),
                "domain_sets": ", ".join(domain_set_list)
            })

        return rules
    except requests.exceptions.RequestException as e:
        print(f"[-] {ip} - {username} - {password} - Request failed: {e}")
        return []
