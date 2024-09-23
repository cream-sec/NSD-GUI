import base64
import xml.etree.ElementTree as ET
import requests
# 获取防火墙的中内外网IP映射关系
class NatServerClient:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.ns = {
            'base': 'urn:ietf:params:xml:ns:restconf:base:1.0',
            'nat': 'urn:huawei:params:xml:ns:yang:huawei-nat-server'
        }
        self.server_mappings = []

    def fetch_data(self):
        com_string = f"{self.username}:{self.password}"
        encoded_bytes = base64.b64encode(com_string.encode('utf-8'))
        url = f"http://{self.ip}:9000/restconf/data/huawei-nat-server:nat-server"
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
            tree = ET.ElementTree(ET.fromstring(response.text))
            root = tree.getroot()
            self.server_mappings = root.findall('.//nat:server-mapping', self.ns)
        except requests.exceptions.RequestException as e:
            print(f"[-] {self.ip} - {self.username} - {self.password} - Request failed: {e}")
            self.server_mappings = []

    def parse_data(self):
        result = []
        for mapping in self.server_mappings:
            name = mapping.find('nat:name', self.ns).text if mapping.find('nat:name', self.ns) is not None else 'N/A'
            vsys = mapping.find('nat:vsys', self.ns).text if mapping.find('nat:vsys', self.ns) is not None else 'N/A'
            protocol = mapping.find('nat:protocol', self.ns).text if mapping.find('nat:protocol', self.ns) is not None else 'N/A'
            global_start_ip = mapping.find('nat:global/nat:start-ip', self.ns).text if mapping.find('nat:global/nat:start-ip', self.ns) is not None else 'N/A'
            global_start_port = mapping.find('nat:global-port/nat:start-port', self.ns).text if mapping.find('nat:global-port/nat:start-port', self.ns) is not None else 'N/A'
            global_end_port_elem = mapping.find('nat:global-port/nat:end-port', self.ns)
            global_end_port = global_end_port_elem.text if global_end_port_elem is not None else None
            inside_start_ip = mapping.find('nat:inside/nat:start-ip', self.ns).text if mapping.find('nat:inside/nat:start-ip', self.ns) is not None else 'N/A'
            inside_start_port = mapping.find('nat:inside-port/nat:start-port', self.ns).text if mapping.find('nat:inside-port/nat:start-port', self.ns) is not None else 'N/A'
            inside_end_port_elem = mapping.find('nat:inside-port/nat:end-port', self.ns)
            inside_end_port = inside_end_port_elem.text if inside_end_port_elem is not None else None
            no_reverse = mapping.find('nat:no-reverse', self.ns).text if mapping.find('nat:no-reverse', self.ns) is not None else 'N/A'

            result.append({
                'name': name,
                'vsys': vsys,
                'protocol': protocol,
                'global_start_ip': global_start_ip,
                'global_start_port': global_start_port,
                'global_end_port': global_end_port,
                'inside_start_ip': inside_start_ip,
                'inside_start_port': inside_start_port,
                'inside_end_port': inside_end_port,
                'no_reverse': no_reverse
            })
        return result

    def search(self, ip_address):
        results = []
        for mapping in self.server_mappings:
            global_start_ip = mapping.find('nat:global/nat:start-ip', self.ns).text if mapping.find('nat:global/nat:start-ip', self.ns) is not None else None
            inside_start_ip = mapping.find('nat:inside/nat:start-ip', self.ns).text if mapping.find('nat:inside/nat:start-ip', self.ns) is not None else None
            if global_start_ip == ip_address or inside_start_ip == ip_address:
                name = mapping.find('nat:name', self.ns).text if mapping.find('nat:name', self.ns) is not None else 'N/A'
                vsys = mapping.find('nat:vsys', self.ns).text if mapping.find('nat:vsys', self.ns) is not None else 'N/A'
                protocol = mapping.find('nat:protocol', self.ns).text if mapping.find('nat:protocol', self.ns) is not None else 'N/A'
                global_start_port = mapping.find('nat:global-port/nat:start-port', self.ns).text if mapping.find('nat:global-port/nat:start-port', self.ns) is not None else 'N/A'
                global_end_port_elem = mapping.find('nat:global-port/nat:end-port', self.ns)
                global_end_port = global_end_port_elem.text if global_end_port_elem is not None else None
                inside_start_port = mapping.find('nat:inside-port/nat:start-port', self.ns).text if mapping.find('nat:inside-port/nat:start-port', self.ns) is not None else 'N/A'
                inside_end_port_elem = mapping.find('nat:inside-port/nat:end-port', self.ns)
                inside_end_port = inside_end_port_elem.text if inside_end_port_elem is not None else None
                no_reverse = mapping.find('nat:no-reverse', self.ns).text if mapping.find('nat:no-reverse', self.ns) is not None else 'N/A'

                results.append({
                    'name': name,
                    'vsys': vsys,
                    'protocol': protocol,
                    'global_start_ip': global_start_ip,
                    'global_start_port': global_start_port,
                    'global_end_port': global_end_port,
                    'inside_start_ip': inside_start_ip,
                    'inside_start_port': inside_start_port,
                    'inside_end_port': inside_end_port,
                    'no_reverse': no_reverse
                })
        return results