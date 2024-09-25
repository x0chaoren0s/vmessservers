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

# Your error definitions and function implementations here...  
class Tcp_Ping_Error(Exception):  
    def __init__(self, msg):  
        self.msg = msg  
    def __str__(self):  
        return self.msg  

class Forwarding_Error(Exception):  
    def __init__(self, msg):  
        self.msg = msg  
    def __str__(self):  
        return self.msg  

def tcp_ping(host, port, timeout=2) -> float:  
    try:  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.settimeout(timeout)  
        start_time = time.time()  
        sock.connect((host, int(port)))  
        end_time = time.time()  
        latency = (end_time - start_time) * 1000  # Convert to milliseconds  
        sock.close()  
        return latency  
    except (socket.timeout, ConnectionRefusedError):  
        raise Tcp_Ping_Error('socket.timeout or ConnectionRefusedError')  
    except Exception:  
        raise Tcp_Ping_Error('other error')  

def decode_vmess_link(vmess_link):  
    # Strip the vmess:// prefix  
    encoded_json = vmess_link.split("://")[1]  
    # Decode the Base64 encoded JSON  
    decoded_bytes = base64.urlsafe_b64decode(encoded_json + "==")  # Add padding  
    decoded_json = decoded_bytes.decode('utf-8')  
    # Parse the JSON  
    return json.loads(decoded_json)  

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
    use_tls = node.get("tls", "") == "tls"  

    xray_config_inbounds = {  
        "inbounds": [  
            {  
                "tag": "http",  
                "port": port,  
                "listen": "127.0.0.1",  
                "protocol": "http",  
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
                "protocol": "vmess",  
                "settings": {  
                    "vnext": [  
                        {  
                            "address": node["add"],  
                            "port": int(node["port"]),  
                            "users": [  
                                {  
                                    "id": node["id"],  
                                    "alterId": int(node["aid"]),  
                                    "security": node.get("scy", "auto")  
                                }  
                            ]  
                        }  
                    ]  
                },  
                "streamSettings": {  
                    "network": node.get("net", "tcp"),  
                    "security": "tls" if use_tls else "",  
                    "tlsSettings": {  
                        "allowInsecure": True,  
                        "serverName": node.get("sni", ""),  
                        "show": False,  
                    } if use_tls else {},  
                    "wsSettings": {  
                        "path": node.get("path", ""),  
                        "headers": {  
                            "Host": node.get("host", ""),  
                        },  
                    } if node.get("net") == "ws" else {},  
                    "mux": {  
                        "enabled": False,  
                        "concurrency": -1,  
                    }  
                }  
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

async def async_test_google(port):  
    try:  
        res = requests.get('https://www.google.com', proxies={'https': f'http://127.0.0.1:{port}'})  
        if res.status_code != 200:  
            raise Forwarding_Error(f'google response != 200')  
        return "Success"  
    except Exception as e:  
        return str(e)

async def async_test_one_link(link):  
    yield_ret = None
    process = None
    try:  
        link_json = decode_vmess_link(link)  
        tcp_ping(link_json['add'], link_json['port'])  
        port = find_available_port()  
        xray_config_file = save_xray_config(link_json, port)  
        process = await async_run_xray(xray_config_file)  
        await asyncio.sleep(0.3)  # Wait for the server to start  
        test_result = await async_test_google(port)  
        if test_result == "Success":  
            yield_ret = link  # Use yield to make this an async generator  
    except (Tcp_Ping_Error, Forwarding_Error, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:  
        yield_ret = f"Error: {e}"
    except Exception as e:  
        # traceback.print_exc()  
        yield_ret = f"Exception: {e}"
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

    available_links = []  
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
        links = [link.strip().replace('`','') for link in links if link.startswith('vmess://')]  

        # Use aiostream to merge results from each async iterable generated by magic_async_fun  
        combine = stream.merge(*(async_test_one_link(link) for link in links))  

        async with combine.stream() as streamer:  
            j = 0
            async for item in streamer:
                j += 1
                print(f'{i}/{len(subscriptions)} {j}/{len(links)}',item)
                if item is not None:  # Only collect successful links  
                    available_links.append(item)  

    # Save available links to file  
    with open('results/available_links.txt', 'w') as fout:  
        for link in available_links:  
            print(link, file=fout)  

if __name__ == "__main__":  
    asyncio.run(main())  