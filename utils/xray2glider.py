import json, base64, requests
from urllib.parse import unquote

# forward=tls://hk3.vpnjantit.com:10001?skipVerify=true,ws://@/vpnjantit,vmess://none:7b7f36c6-7010-11ef-a00e-00163e0f2d4d@hk3.vpnjantit.com:10001?alterID=0
# vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIjB8LWh0dHBzOi8vdC5tZS9NclhiaW4tNTciLA0KICAiYWRkIjogImljb29rLnR3IiwNCiAgInBvcnQiOiAiMjA4NiIsDQogICJpZCI6ICJlOWUzY2MxMy1kYjQ4LTRjYzEtOGMyNC03NjI2NDM5YTUzMzkiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogImlwMS4xNzg5MDM0Lnh5eiIsDQogICJwYXRoIjogImdpdGh1Yi5jb20vQWx2aW45OTk5IiwNCiAgInRscyI6ICIiLA0KICAic25pIjogIiIsDQogICJhbHBuIjogIiIsDQogICJmcCI6ICIiDQp9

class Glider_config_convertor:
    def convert(self, xraylink: str) -> str:
        xraylink = xraylink.strip()
        ret = ''
        if xraylink.startswith('vmess://'):
            ret = self.vmess(xraylink)
        elif xraylink.startswith('trojan://'):
            ret = self.trojan(xraylink)
        elif xraylink.startswith('vless://'):
            ret = self.vless(xraylink)
        return ret

    def post_process(self, purelink) -> str:
        return f'forward={purelink}\n'

    def trojan(self, nodelink: str) -> str:
        # 'forward=trojan://20aab1a3-ae35-493e-a869-afec1f01d48f@hk1.trojanvpn.de:2053?skipVerify=true'
        #   trojan://pass@host:port[?serverName=SERVERNAME][&skipVerify=true][&cert=PATH]
        #   trojanc://pass@host:port     (cleartext, without TLS)
        # 'trojan://dc2d9db59868ba6b@139.162.111.25:3306?security=tls&sni=TG.WangCai2&type=ws&host=TG.WangCai_1&path=%2Fgateway%2Fconnect#%F0%9F%94%92%20TR-WS-TLS%20%F0%9F%87%AF%F0%9F%87%B5%20JP-139.162.111.25%3A3306'
        passwd = nodelink.split('trojan://')[1].split('@')[0]
        hostport = nodelink.split('@')[1].split('?')[0]
        data = nodelink.split('?')[1].split('#')[0].split('&')
        data = {kv.split('=')[0]:kv.split('=')[1] for kv in data if '=' in kv}
        security = data.get('security', 'none')
        purelink = f'trojan://{passwd}@{hostport}?skipVerify=true'
        if security=='none':
            purelink = f'trojanc://{passwd}@{hostport}'
        else:
            transport = data.get('type', 'ws')
            path = unquote(data.get('path', '')).replace(' ','').replace('@','').replace(':','')
            path = path if path.startswith('/') else '/'+path
            fakehost = data.get('host', '')
            if transport=='ws':
                purelink = f"tls://{hostport}?skipVerify=true,ws://@{path}&host={fakehost},trojanc://{passwd}@{hostport}"
            elif transport=='tcp':
                purelink = f'trojan://{passwd}@{hostport}?skipVerify=true'
        return self.post_process(purelink)
    
    def vless(self, nodelink: str) -> str:
        # forward=ws://sgc-s132.v2sv.xyz:8880/freevpn/freevpn.us-e7s9etrsu/SG,vless://66726565-7670-4e2e-b573-2d6537733965@sgc-s132.v2sv.xyz:8880
        'vless://d342d11e-d424-4583-b36e-524ab1f0afa4@38.207.172.42:80?encryption=none&security=none&type=ws&host=a.ssll.gay&path=Telegram%F0%9F%87%A8%F0%9F%87%B3%20%40WangCai_8%20%2F%3Fed%3D2048#%F0%9F%94%92%20VL-WS-NA%20%F0%9F%87%AD%F0%9F%87%B0%20HK-38.207.172.42%3A80'
        'vless://d7dd3a35-b68b-4992-b319-a85b8a1fc8e5@183.178.22.246:11417?encryption=none&security=tls&sni=dns68.putata.eu.org&type=ws&host=dns68.putata.eu.org&path=%2F%3Fed%3D2048fp%3Drandomized#15%7CHK_speednode_0216'
        uuid = nodelink.split('vless://')[1].split('@')[0]
        hostport = nodelink.split('@')[1].split('?')[0]
        data = nodelink.split('?')[1].split('#')[0].split('&')
        data = {kv.split('=')[0]:kv.split('=')[1] for kv in data}
        purelink = f'vless://{uuid}@{hostport}'
        transport = data.get('type', 'ws')
        path = unquote(data.get('path', '')).replace(' ','').replace('@','').replace(':','')
        path = path if path.startswith('/') else '/'+path
        fakehost = data.get('host', '')
        if transport=='ws':
            if data.get('security', 'tls') == 'tls':
                purelink = f"tls://{hostport}?skipVerify=true,ws://@{path}&host={fakehost},{purelink}"
            else:
                purelink = f"ws://{hostport}{path}&host={fakehost},{purelink}"
        elif transport=='tcp':
            if data.get('security', 'tls') == 'tls':
                purelink = f"tls://{hostport}?skipVerify=true,{purelink}"
        return self.post_process(purelink)    

    def vmess(self, nodelink: str) -> str:
        config_dict = json.loads(base64.b64decode(nodelink.split('vmess://')[1]).decode())
        # ['v', 'ps', 'add', 'port', 'id', 'aid', 'scy', 'net', 'type', 'host', 'path', 'tls', 'sni', 'alpn', 'fp']
        # 主协议层
        # vmess://[security:]uuid@host:port[?alterID=num]
        security = config_dict.get('scy', 'auto') # auto / none / aes-128-gcm / chacha20-poly1305 / zero
        uuid = config_dict.get('id', '')
        host = config_dict.get('add', '')
        port = config_dict.get('port', '')
        aid = config_dict.get('aid', '')
        ret0 = f'vmess://{security+":" if security!="auto" else ""}{uuid}@{host}:{port}?alterID={aid}'
        # 传输方式层 transport: tcp / ws // kcp /// grcp / h2 /quic
        # Websocket with a specified proxy protocol:
        #   ws://host:port[/path][?host=HOST],scheme://
        # TLS and Websocket with a specified proxy protocol:
        #   tls://host:port[?skipVerify=true][&serverName=SERVERNAME],ws://[@/path[?host=HOST]],scheme://
        net = config_dict.get('net', '')
        path = unquote(config_dict.get('path', '')).replace(' ','').replace('@','').replace(':','')
        path = path if path.startswith('/') else '/'+path
        fakehost = config_dict.get('host', '')
        tls = config_dict.get('tls', '')
        if tls=='tls':
            ret1 = f'ws://@{path}&host={fakehost},' if net=='ws' else ''
        else:
            ret1 = f'ws://{host}:{port}{path}&host={fakehost},' if net=='ws' else ''
        # 传输安全层 tls
        #   tls://host:port?cert=PATH&key=PATH[&alpn=proto1][&alpn=proto2]
        alpn = config_dict.get('alpn', '')
        ret2 = f'tls://{host}:{port}?skipVerify=true{"&alpn="+alpn if alpn!="" else ""},' if tls=='tls' else ''
        purelink = f'{ret2}{ret1}{ret0}'
        return self.post_process(purelink)

if __name__=='__main__':
    # with open('hk.txt', 'r') as fin:
    #     xraylinks = [line.strip() for line in fin.readlines()]
    # gliderlinks = [Glider_config_convertor().vmess(link) for link in xraylinks]
    # # print(gliderlinks)
    # with open('hk.conf', 'w') as fout:
    #     fout.writelines([link+'\n' for link in set(gliderlinks)])
    print('vless ws tls')
    link='vless://d342d11e-d424-4583-b36e-524ab1f0afa4@38.207.172.42:80?encryption=none&security=none&type=ws&host=a.ssll.gay&path=Telegram%F0%9F%87%A8%F0%9F%87%B3%20%40WangCai_8%20%2F%3Fed%3D2048#%F0%9F%94%92%20VL-WS-NA%20%F0%9F%87%AD%F0%9F%87%B0%20HK-38.207.172.42%3A80'
    print(Glider_config_convertor().vless(link))
    # print('trojan ws tls')
    # link='trojan://dc2d9db59868ba6b@139.162.111.25:3306?security=tls&sni=TG.WangCai2&type=ws&host=TG.WangCai_1&path=%2Fgateway%2Fconnect#%F0%9F%94%92%20TR-WS-TLS%20%F0%9F%87%AF%F0%9F%87%B5%20JP-139.162.111.25%3A3306'
    # print(Glider_config_convertor().trojan(link))
    # print('vmess auto tcp')
    # link='vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIvCfh63wn4ewIOmmmea4ryjmsrnnrqE656C06Kej6LWE5rqQ5ZCbMi4wKSIsDQogICJhZGQiOiAiNS4xODEuMTMyLjIzNSIsDQogICJwb3J0IjogIjMxMzcyIiwNCiAgImlkIjogIjBiYjg4ZWVhLTczYTUtNGUzNy1hYzhiLTAzMDkwYTU3YWNiYSIsDQogICJhaWQiOiAiMCIsDQogICJzY3kiOiAiYXV0byIsDQogICJuZXQiOiAidGNwIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIiIsDQogICJwYXRoIjogIi8iLA0KICAidGxzIjogIiIsDQogICJzbmkiOiAiIiwNCiAgImFscG4iOiAiIiwNCiAgImZwIjogIiINCn0='
    # print(Glider_config_convertor().vmess(link))
    # print('vmess auto tcp(伪装域名)')
    # link='vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIvCfh63wn4ewIDEzfPCfh63wn4ewIOmmmea4r3xAcmlwYW9qaWVkaWFuIiwNCiAgImFkZCI6ICJhbWJ4eGljMDFoay5kb3JhYmJiLnRvcCIsDQogICJwb3J0IjogIjQ0ODAxIiwNCiAgImlkIjogImFjOTJkZmI2LWNlNWItNGMyYi05YzFjLTU5Yjk3NzA5MDFmYyIsDQogICJhaWQiOiAiMCIsDQogICJzY3kiOiAiYXV0byIsDQogICJuZXQiOiAidGNwIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogImFtYnh4aWMwMWhrLmRvcmFiYmIudG9wIiwNCiAgInBhdGgiOiAiLyIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiLA0KICAiYWxwbiI6ICIiLA0KICAiZnAiOiAiIg0KfQ=='
    # print(Glider_config_convertor().vmess(link))
    # print('vmess auto tcp tls')
    # link='vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIvCfh63wn4ewIOmmmea4ryjmsrnnrqE656C06Kej6LWE5rqQ5ZCbMi4wKSIsDQogICJhZGQiOiAiMTAzLjE3My4xNzguMTEwIiwNCiAgInBvcnQiOiAiNDA0NDMiLA0KICAiaWQiOiAiQjI1NjA1NDgtNUY3NS0zMDE1LTgyRjktMUMzREY4NjI4MDA5IiwNCiAgImFpZCI6ICIwIiwNCiAgInNjeSI6ICJhdXRvIiwNCiAgIm5ldCI6ICJ0Y3AiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAibm9kZS5uYXBzdGVybmV0di5jb20iLA0KICAicGF0aCI6ICIvIiwNCiAgInRscyI6ICJ0bHMiLA0KICAic25pIjogIiIsDQogICJhbHBuIjogIiIsDQogICJmcCI6ICIiDQp9'
    # print(Glider_config_convertor().vmess(link))
    # print('vmess auto ws')
    # link='vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIvCflJIgVk0tV1MtTkEg8J+HrfCfh7AgSEstNjIuNzIuMTYzLjU0OjEwMDAxIiwNCiAgImFkZCI6ICI2Mi43Mi4xNjMuNTQiLA0KICAicG9ydCI6ICIxMDAwMSIsDQogICJpZCI6ICI1NTQyOTY1Ni05YTk0LTQyMmYtOTk3ZC1iMDY3Njk1YmM4OWQiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIiIsDQogICJwYXRoIjogIi8iLA0KICAidGxzIjogIiIsDQogICJzbmkiOiAiIiwNCiAgImFscG4iOiAiIiwNCiAgImZwIjogIiINCn0='
    # print(Glider_config_convertor().vmess(link))
    # print('vmess auto ws tls')
    # link='vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIvCflJIgVk0tV1MtVExTIPCfh7nwn4e8IFRXLTE1NC40MC42MC4xNzI6MTI5NDUiLA0KICAiYWRkIjogIjE1NC40MC42MC4xNzIiLA0KICAicG9ydCI6ICIxMjk0NSIsDQogICJpZCI6ICI4MjU5Y2IxYy1kZDZjLTQ3MzktOWM4OC1hZjU1MGQ5Nzc1MjUiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIiIsDQogICJwYXRoIjogIi8iLA0KICAidGxzIjogInRscyIsDQogICJzbmkiOiAiNTUubHdkaC51cyIsDQogICJhbHBuIjogIiIsDQogICJmcCI6ICIiDQp9'
    # print(Glider_config_convertor().vmess(link))
    # print('vmess auto ws tls(伪装域名)')
    # link='vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIvCflJIgVk0tV1MtVExTIPCfh63wn4ewIEhLLTIxMC4wLjE1OC4yMTk6MTI5MDkiLA0KICAiYWRkIjogIjIxMC4wLjE1OC4yMTkiLA0KICAicG9ydCI6ICIxMjkwOSIsDQogICJpZCI6ICI4MjU5Y2IxYy1kZDZjLTQ3MzktOWM4OC1hZjU1MGQ5Nzc1MjUiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIjE5Lmx3ZGgudXMiLA0KICAicGF0aCI6ICIvIiwNCiAgInRscyI6ICJ0bHMiLA0KICAic25pIjogIjE5Lmx3ZGgudXMiLA0KICAiYWxwbiI6ICJodHRwLzEuMSIsDQogICJmcCI6ICJjaHJvbWUiDQp9'
    # print(Glider_config_convertor().vmess(link))