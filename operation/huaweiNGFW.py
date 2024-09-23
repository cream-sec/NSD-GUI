import base64
import requests


def NgfwLogin(ip,username, password):
    com_string = username+":" + password
    com_string_bytes = com_string.encode('utf-8')
    encoded_bytes = base64.b64encode(com_string_bytes)
    url = "http://" + ip + ":9000/restconf/data/ietf-system:system-state?content=all"
    headers = {
        "Conncection": "keep-alive",
        "Accept": "application/yang.data+xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/yang.data+xml",
        "Authorization": "Basic " + encoded_bytes.decode('utf-8')
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(f"[-] {ip} -{username}- {password} - Failed!!")
    except requests.exceptions.RequestException as e:
            print(f"[-] {ip} - {username} - {password} - Request failed: {e}")
