import asyncio  
import socket  
import time  
import requests  
import json  
import base64  
import traceback  
import subprocess  
import signal  
from aiostream import stream  
from urllib.parse import unquote
from normalize_date import normalized_local_date

# Your error definitions and function implementations here...  
class Tcp_Ping_Error(Exception):  
    def __init__(self, msg):  
        self.msg = msg  
    def __str__(self):  
        return self.msg  
class Udp_Ping_Error(Exception):  
    def __init__(self, msg):  
        self.msg = msg  
    def __str__(self):  
        return self.msg  

class Forwarding_Error(Exception):  
    def __init__(self, msg):  
        self.msg = msg  
    def __str__(self):  
        return self.msg  

def tcp_ping(host, port, timeout=2) -> bool:  
    try:  
        status = False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.settimeout(timeout)  
        # start_time = time.time()  
        sock.connect((host, int(port)))  
        # end_time = time.time()  
        # latency = (end_time - start_time) * 1000  # Convert to milliseconds  
        sock.close()
        status = True
    finally:
        return status
    
def udp_ping(host, port, timeout=2) -> bool:  
    try:  
        status = False
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        sock.settimeout(timeout)  
        message = b'\x00'  
        # start_time = time.time()  
        sock.sendto(message, (host, int(port)))  
        data, _ = sock.recvfrom(1024)  # Buffer size is 1024 bytes  
        # end_time = time.time()  
        # latency = (end_time - start_time) * 1000  # Convert to milliseconds  
        sock.close()
        status = True
    finally:
        return status

def decode_raw_link(raw_link):
    # 转换成和vmess解码后统一的格式
    ret = dict()
    if raw_link.startswith('vmess://'):
        encoded_json = raw_link.split("://")[1]  
        # Decode the Base64 encoded JSON  
        decoded_bytes = base64.urlsafe_b64decode(encoded_json + "==")  # Add padding  
        decoded_json = decoded_bytes.decode('utf-8')
        ret = json.loads(decoded_json)
        ret['net_security'] = ret.get('tls', '')
    elif raw_link.startswith('vless://'):
        ret['id'] = raw_link.split('://')[1].split('@')[0]
        ret['add'] = raw_link.split('@')[1].split(':')[0]
        ret['port'] = raw_link.split('@')[1].split(':')[1].split('?')[0]
        ret.update({kv.split('=')[0]:kv.split('=')[1] for kv in raw_link.split('?')[1].split('#')[0].split('&')})
        ret['net'] = ret.get('type', 'tcp')
        ret['net_security'] = ret.get('security', '')
        ret['ps'] = raw_link.split('#')[1]
    elif raw_link.startswith('trojan://'):
        ret['password'] = raw_link.split('://')[1].split('@')[0]
        ret['add'] = raw_link.split('@')[1].split(':')[0]
        ret['port'] = raw_link.split('@')[1].split(':')[1].split('?')[0]
        ret.update({kv.split('=')[0]:kv.split('=')[1] for kv in raw_link.split('?')[1].split('#')[0].split('&')})
        ret['net'] = ret.get('type', 'tcp')
        ret['net_security'] = ret.get('security', '')
        ret['ps'] = raw_link.split('#')[1]
    elif raw_link.startswith('hysteria2://'):
        ret['password'] = raw_link.split('://')[1].split('@')[0]
        ret['add'] = raw_link.split('@')[1].split(':')[0]
        ret['port'] = raw_link.split('@')[1].split(':')[1].split('?')[0]
        ret.update({kv.split('=')[0]:kv.split('=')[1] for kv in raw_link.split('?')[1].split('#')[0].split('&')})
        ret['net'] = ret.get('type', 'tcp')
        ret['net_security'] = ret.get('security', '')
        ret['ps'] = raw_link.split('#')[1]
    elif raw_link.startswith('ss://'):
        ret['encryption'] = base64.b64decode(raw_link.split('://')[1].split('@')[0]).decode().split(':')[0]
        ret['password'] = base64.b64decode(raw_link.split('://')[1].split('@')[0]).decode().split(':')[1]
        ret['add'] = raw_link.split('@')[1].split(':')[0]
        ret['port'] = raw_link.split('@')[1].split(':')[1].split('?')[0]
        ret['ps'] = raw_link.split('#')[1]
    ret['protocol'] = raw_link.split('://')[0]
    if 'path' in ret:
        ret['path'] = unquote(ret['path'])
    return ret

def find_available_port(min=10000, start=10000, max=20000):  
    found = False  
    while not found:  
        for port in range(start, max + 1):  
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
                try:  
                    s.bind(('localhost', port))  
                    found = True  
                    break  
                except OSError:  
                    continue  
        start = min  
    return port  

def save_xray_config(node, port) -> str:  
    xray_config_inbounds = {  
        "inbounds": [  
            {  
                "tag": "socks",  
                "port": port,  
                "listen": "127.0.0.1",  
                "protocol": "socks",  
                "sniffing": {  
                    "enabled": True,  
                    "destOverride": ["http", "tls"],  
                    "routeOnly": False  
                },  
                "settings": {  
                    "auth": "noauth",  
                    "udp": True,  
                    "allowTransparent": False  
                }  
            }  
        ]  
    }  
    xray_config_outbounds = {  
        "outbounds": [  
            {  
                "tag": "proxy",
                "protocol": node["protocol"],  
                "settings": {  
                    "vnext": [  
                        {  
                            "address": node["add"],
                            "port": int(node["port"]),
                            "users": [
                                {
                                    "id": node["id"],
                                    "alterId": int(node.get("aid",0)),
                                    "security": node.get("scy", "auto"),
                                    "encryption": node.get("encryption", ""),
                                }
                            ]  
                        }  
                    ] if node["protocol"] in ['vmess', 'vless'] else [],
                    "servers": [
                        {
                            "address": "36.151.192.201",
                            "method": "chacha20",
                            "ota": False,
                            "password": "wwTIozXY",
                            "port": 27131,
                            "level": 1
                        }
                    ] if node["protocol"] in ['trojan'] else [],
                },  
                "streamSettings": {  
                    "network": node.get("net", "tcp"),  
                    "security": node.get("net_security", ""),  
                    "tlsSettings": {  
                        "allowInsecure": True,  
                        "serverName": node.get("sni", ""),  
                        "show": False,  
                    } if node.get("net_security", "") == "tls"  else {},  
                    "realitySettings": {
                        "serverName": node.get("sni", ""),  
                        "fingerprint": node.get("fp", ""),  
                        "show": False,
                        "publicKey": node.get("pbk", ""),  
                        "shortId": node.get("sid", ""),  
                        "spiderX": ""
                    } if node.get("net_security", "") == "reality"  else {},  
                    "wsSettings": {  
                        "path": node.get("path", ""),  
                        "headers": {  
                            "Host": node.get("host", ""),  
                        },  
                    } if node.get("net") == "ws" else {},  
                    "grpcSettings": {
                        "serviceName": node.get("serviceName", ""),  
                        "multiMode": False,
                        "idle_timeout": 60,
                        "health_check_timeout": 20,
                        "permit_without_stream": False,
                        "initial_windows_size": 0
                    } if node.get("net") == "grpc" else {},  
                    "httpSettings": {
                        "path": node.get("path", ""),  
                    } if node.get("net") == "http" else {},  
                    "mux": {  
                        "enabled": False,  
                        "concurrency": -1,  
                    }
                },
                "type": node["protocol"],  
                "server": node["add"],
                "server_port": int(node["port"]),
                "up_mbps": 100,
                "down_mbps": 100,
                "password": node.get("password", ''),
                "tls": {
                    "enabled": True,
                    "server_name": node.get("sni", ""),
                    "insecure": True,
                },
            }  
        ]  
    }  

    with open('results/xray_test_template.json', 'r', encoding='utf8') as fin:  
        xray_config_full = json.load(fin)  
    xray_config_full['inbounds'] = xray_config_inbounds['inbounds']  
    xray_config_full['outbounds'] = xray_config_outbounds['outbounds']  
    xray_config_file = f'results/xray_test_{port}.json'  
    with open(xray_config_file, 'w', encoding='utf8') as fout:  
        json.dump(xray_config_full, fout, ensure_ascii=False, indent=2)  
    return xray_config_file  

async def async_run_xray(xray_config_file):  
    process = subprocess.Popen(  
        ["xray", "run", "-c", xray_config_file],  
        stdout=subprocess.PIPE,  
        stderr=subprocess.PIPE,  
        stdin=subprocess.PIPE,  
        text=True  
    )  
    return process  

def stop_xray(process) -> None:  
    if process is not None:  
        process.send_signal(signal.SIGINT)  
        process.wait()  

async def async_test_google(port, retry=3):  
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'cookie': 'OTZ=7752127_24_24__24_; SEARCH_SAMESITE=CgQImZwB; SID=g.a000oghPyVp4lzbdbSSIjuyxaJy8szEo83tjqxFkcqjNoeo70BkoeTx8aOseOcFKJ_oVusCDBwACgYKAUUSARYSFQHGX2MizfVw_9BJDq8mqciNwX9aOBoVAUF8yKqYqB48D1AXII0JjlWQ0K2k0076; __Secure-1PSID=g.a000oghPyVp4lzbdbSSIjuyxaJy8szEo83tjqxFkcqjNoeo70Bkow0aM0L2uy4f7pbw2WpO_7gACgYKAUQSARYSFQHGX2MioVSEt7BuirRGD3SY_8xvRhoVAUF8yKoms7ld2FxVnpL7pKGuLFVa0076; __Secure-3PSID=g.a000oghPyVp4lzbdbSSIjuyxaJy8szEo83tjqxFkcqjNoeo70BkonfTF_2yxQX2xCz1HlwEsggACgYKAUASARYSFQHGX2MiZh9CkydJXuc2omp276RKgRoVAUF8yKriXtyxaBYv6PmLJzSeySZD0076; HSID=A1b6xUJviVEKqsF7B; SSID=A3aV-aZBJpkdyOgdD; APISID=hBLFIVYvgF0EUhGO/AxRPhYXjK_Kox8oA6; SAPISID=B6ea6LesKDrfGc2w/AS1Ecvg6js2RqlOxY; __Secure-1PAPISID=B6ea6LesKDrfGc2w/AS1Ecvg6js2RqlOxY; __Secure-3PAPISID=B6ea6LesKDrfGc2w/AS1Ecvg6js2RqlOxY; AEC=AVYB7cqoFSWFzfZ5AppKTfExeNkpDVPAaqvLEMPGAcvwmv7trN2A8YtLTw; NID=518=vyRto-MpnHHGF_lgHML24CmXJhlI9qy_wrqLNkNEMdZXHQxDyDWgqVzpTcZrx6nZex2B8-8lHN4fCqh6YgjwDl8nafQYrTMVfzn0kw5-VoexoebXYClHE6fj4GGFJjX-XeMUZx3yk47O-bPvNRa0-o9ShJ8PKn95-hy4fNPgC7SoDFBRvs9m_htVywRfA8x2-2pO5jzCyB7bM5JwP68UqeXCD1_77nUflnQr3VpmGVjnLryIYIQJRcwZF_S-p_khyMDgPnEeVAw-l5zK8wJ_GjWG_hmpLepcVomYHeDxmSwZLuej2czzt6qFeT3yF4grAfItmmSn11NIcX9ASbXeu6Rib8zxxU4ylU3z5inWVs6XalicOXjlpd9DXs81VjbwhfbO1Pbzf14R1jal5_fI_-NzN36NtkPuhciyytZMEhAGJATz9v3ntvPG4ZBQC1TlNhqv38kzVDdINzfBu9-bxSKfiJIlLbr11Zna5fwxXiemxewiRtXzSNkIa687VcV0i4b5o0j3asocjJrh5MLe5GiuANAVbxV5GyjNQTnOOdkENjoy13yNj6RnQLfUDqZFYvqV9-6zSFYfF2-wB-CqnfRctuVxCvpCZchQbY1bnycZ-W5LOjQRreJFoR0pD6ybrB3rJB22c_U6_onsnwUOj5SYuZ_q8n8vBw8BAiTdqd5UGCLYknUGu43aLePTxfC9_kBvx33QdCOryge8KZPILD4YWZ0syYTzKfZau4R6sVoM8cohuMM11gKYGU0Pstr08eW-9Pm9uSPf_Ib6CGwZWkqpyMHGUqY4Quh500L0xxw; __Secure-1PSIDTS=sidts-CjIBQlrA-FzxruKP_qkjqqXeeWbfTV1nav95dYMPv4m2b_EvySMjbVzxD9wZPTawn9gnjBAA; __Secure-3PSIDTS=sidts-CjIBQlrA-FzxruKP_qkjqqXeeWbfTV1nav95dYMPv4m2b_EvySMjbVzxD9wZPTawn9gnjBAA; __Secure-ENID=22.SE=AA3F4Qkglnvrxhqde6FnYurSBm_eNWIE5E5o58MVUazI0gaQzwbFDVA7ZNsScsbymowX02MrBckad7JvZLxG719Y-2XABlppVj3o_50-L6PxHIqoy0Xvd-7hWv0sk98pTpWvWc_FKC-I7j2S2mF-CRTIOeF5V-a6lZIedSj-xuFpSjxjRcOxvDIsTc6uZ3XdWJpChuM_V7U7MByoJelf2SJB0gQNCfHiy_Ptn_LBHaeVlNL03jdU6K2MYLeVQHdMW7oGvpkhxKstG8pxK9ArBLieCFcP-X4yS5Z97bXYuc89OLA2e7R_SJ_5q2_WrSQFZc6VmQgkZpHbnW677jqJNR5n224vHqUgA8MWeGI31Uf6zX7wOBBogVaao1OlWZSLgk6etYC8-PLRhG_G; DV=I6sXXW2ndKuqIBy4P1MyROswfsPBIxkijpdIBVqZRgMAAGAUsbpzQL8yQwEAAICIXxvmwpdnUwAAACZXk6Owkfa-FwAAABomwfjlk8qDDjABEL5WPJip-J-2A0wAuAcYAITsZEQdARMAAeKmUP1K13dKwARAxZ0VC0zG_L0TMAEA; SIDCC=AKEyXzW3NTnS9Wpyg1KIneFkWAKRnBJswv2OPRcyGAT53q2yFXqpAHUuzMAv5FiTd7XVA01EgA; __Secure-1PSIDCC=AKEyXzV5TA1YskyZEuHrWkhlK_4OuQV0xigJmZ0HokDxSDUYtZU-jcn_1BVO5HITdE3NcuaaJA; __Secure-3PSIDCC=AKEyXzW3OiZxa_4rrs_ks6_VcZKVd4n-ToudE7yV6-Pz6ocAovIsvyjCO_-LyEAjR2tN4E0PSA',
        'dnt': '1',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.google.com/',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="129", "Google Chrome";v="129"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-form-factors': '"Desktop"',
        'sec-ch-ua-full-version': '"129.0.6668.71"',
        'sec-ch-ua-full-version-list': '"Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.71", "Google Chrome";v="129.0.6668.71"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    try:  
        res = requests.get('https://www.google.com', proxies={'https': f'http://127.0.0.1:{port}'}, headers=headers)  
        if res.status_code != 200:  
            raise Forwarding_Error(f'google response != 200')  
        return "Success"  
    except Exception as e:  
        if retry>0:
            return await async_test_google(port, retry-1)
        return str(e)

async def async_test_one_link(link):  
    yield_ret = {'status': False, 'link': link, 'error_info': ''}
    process = None
    try:  
        link_json = decode_raw_link(link)  
        assert link_json['protocol'] in ['vmess', 'vless', 'trojan']
        if link_json['protocol'] in ['vmess', 'vless', 'trojan']:
            assert tcp_ping(link_json['add'], link_json['port']), 'Tcp_Ping_Error'
        port = find_available_port()  
        xray_config_file = save_xray_config(link_json, port)  
        process = await async_run_xray(xray_config_file)  
        await asyncio.sleep(0.3)  # Wait for the server to start  
        test_result = await async_test_google(port)  
        if test_result == "Success":  
            yield_ret['status'] = True  # Use yield to make this an async generator  
    except (Tcp_Ping_Error, Forwarding_Error, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:  
        yield_ret['error_info'] = str(e)
    except AssertionError as e:  
        yield_ret['error_info'] = str(e)
    except Exception as e:  
        traceback.print_exc()
        yield_ret['error_info'] = str(e)
    finally:  
        stop_xray(process)  
        yield yield_ret  # Ensure every invocation is followed by a yield 

async def main():  
    subscriptions = [
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt', # Updating Every 10 minutes.
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub2.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub3.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub4.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub5.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub6.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub7.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub8.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub9.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub20.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub21.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub22.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub23.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub24.txt',
        'https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub25.txt', # Updating Every 10 minutes.

        'https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/server.txt', # 看历史好像是30min更新
        'https://raw.githubusercontent.com/abshare/abshare.github.io/main/README.md', # 每日分享
        'https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub' # 6小时更新一次  需要先把整个文件做base64解码
    ] 

    available_links = set()
    for i,subscription in enumerate(subscriptions,start=1):
        # Load links from subscription  
        while True:  
            try:  
                lines = requests.get(subscription, proxies={'https': 'http://127.0.0.1:7602'}).content.decode()  
                break  
            except Exception:  
                pass  # Simple retry mechanic  

        try:  
            lines = base64.b64decode(lines).decode()  
        except Exception:  
            pass  

        links = lines.split('\n')  
        links = [link.strip().replace('`','') for link in links if link.startswith('vmess://') or link.startswith('vless://')]  
#         links = [
# 'vless://5f0b2bda-0457-5e95-ba0e-9a425356f4cb@188.114.96.216:80?encryption=none&security=none&type=ws&host=wwww.speedtest.net.xn--Join.ELiV2RY.io.ie1.vless.Sitespeedtest.net.&path=%2F-%40ELiV2RY-%40ELiV2RY%F0%9F%92%83%F0%9F%92%83%F0%9F%92%83%F0%9F%92%83%F0%9F%92%83%F0%9F%92%83-ELeNaTheGreatDictator#%F0%9F%91%89%F0%9F%86%94%20%40v2ray_configs_pool%F0%9F%93%A1%F0%9F%87%A8%F0%9F%87%A6Canada',
#         ]

        # Use aiostream to merge results from each async iterable generated by magic_async_fun  
        combine = stream.merge(*(async_test_one_link(link) for link in links))  

        async with combine.stream() as streamer:  
            j = 0
            async for test_result in streamer:
                j += 1
                print(f'{i}/{len(subscriptions)} {j}/{len(links)}', end=' ')
                print(test_result['link'] if test_result['status'] else test_result['error_info'])
                if test_result['status']:  # Only collect successful links  
                    available_links.add(test_result['link'])

    # Save available links to file  
    with open('results/available_links.txt', 'w') as fout:
        print(f'# {len(available_links)} - {normalized_local_date()}')
        print(f'# {len(available_links)} - {normalized_local_date()}', file=fout)
        for link in available_links:  
            print(link, file=fout)  

if __name__ == "__main__":  
    asyncio.run(main())  
    # print(udp_ping('40.76.225.108',443))