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


def find_available_port(min_port=10000, start_port=-1, max_ports=20):  
    start_port = max(min_port, start_port)
    if hasattr(find_available_port, 'last_port'):
        start_port = find_available_port.last_port
    found = False
    while not found:
        for port in range(start_port, min_port+max_ports):  
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
                try:  
                    s.bind(('localhost', port))  
                    found = True  
                    break  
                except OSError:  
                    continue  
        start_port = min_port
    find_available_port.last_port = port
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
    try:  
        # 测的是YouTube上一个视频的封面图
        res = requests.get('https://i.ytimg.com/vi/EMTTPIZlXCw/hq720.jpg', proxies={'https': f'http://127.0.0.1:{port}'}, timeout=1.0)  
        if res.status_code != 200:  
            raise Forwarding_Error(f'google response != 200')  
        return "Success"  
    except Exception as e:  
        if retry>0:
            return await async_test_google(port, retry-1)
        return str(e)

async def async_test_one_link(link, semaphore):  
    yield_ret = {'status': False, 'link': link, 'error_info': ''}
    process = None
    async with semaphore:  # Use semaphore to limit concurrent tasks 
        try:  
            link_json = decode_raw_link(link)  
            assert link_json['protocol'] in ['vmess', 'vless', 'trojan'], "protocal not in ['vmess', 'vless', 'trojan']"
            assert 'add' in link_json in ['vmess', 'vless', 'trojan'], "add not in link_json"
            assert 'port' in link_json in ['vmess', 'vless', 'trojan'], "port not in link_json"
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
        'https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub', # 6小时更新一次  需要先把整个文件做base64解码

        'https://mangaharb.fun:7643/v2ray/available_links.txt'  # 保证现有能用的也留住
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

        links_ = lines.split('\n')  
        links_ = [link.strip().replace('`','') for link in links_ if link.startswith('vmess://') or link.startswith('vless://') or link.startswith('trojan://')]
        links = set()  # 解决几个link连着不换行的情况
        for link in links_:
            starts = []
            def buildStarts(link:str, prefix:str, initstart:int, starts:list) -> None:
                start = link.find(prefix,initstart)
                if start == -1:
                    return
                starts.append(start)
                buildStarts(link, prefix, start+1, starts)
            for prefix in ['vmess://', 'vless://', 'trojan://']:
                buildStarts(link, prefix, 0, starts)
            starts = sorted(starts, reverse=True)
            for start in starts:
                links.add(link[start:])
                link = link[:start]

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