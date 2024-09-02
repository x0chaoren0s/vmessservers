import json

# print(os.listdir('results/'))
with open('results/freevpn.conf', 'r') as fin:
    lines = fin.readlines()
# date_end = lines[0].split(' - ')[1].strip() # # 2024-09-02 - 2024-09-05
node_links = [l.strip() for l in lines if l.startswith('vless://')]

outbound_template = {
    # "tag": "s165",
    "protocol": "vless",
    "settings": {
        "vnext": [
            {
                # "address": "auc-s165.v2sv.xyz",
                # "port": 8880,
                "users": [
                    {
                        # "id": "66726565-7670-4e2e-b573-2d7162727476",
                        "alterId": 0,
                        "email": "t@t.tt",
                        "security": "auto",
                        "encryption": "none"
                    }
                ]
            }
        ]
    },
    "streamSettings": {
        "network": "ws",
        "wsSettings": {
            # "path": "/freevpn/freevpn.us-qbrtvmc2p/AU",
            "headers": {
                # "Host": "auc-s165.v2sv.xyz"
            }
        }
    },
    "mux": {
        "enabled": False,
        "concurrency": -1
    }
}
with open('v2ray_template.json', 'r') as fin:
    v2ray_config = json.load(fin)

for node_link in node_links:
    # vless://66726565-7670-4e2e-b573-2d6f6c626e65@hkc-s144.v2sv.xyz:8880
    # ?encryption=none&security=none&type=ws
    # &host=hkc-s144.v2sv.xyz
    # &path=%2Ffreevpn%2Ffreevpn.us-olbnelrtu%2FHK
    # #2024-09-05 freevpn: Hong Kong, Hong Kong
    address = node_link.split('host=')[1].split('&')[0]
    port = int(node_link.split(':')[2].split('?')[0])
    path = node_link.split('path=')[1].split('#')[0].replace('%2F', '/')
    id = node_link.split('vless://')[1].split('@')[0]
    ps = node_link.split('#')[1].strip()
    tag = f"{ps} {address}"
    outbound = outbound_template.copy()
    outbound["settings"]["vnext"][0]["address"] = address
    outbound["settings"]["vnext"][0]["port"] = port
    outbound["settings"]["vnext"][0]["users"][0]["id"] = id
    outbound["streamSettings"]["wsSettings"]["path"] = path
    outbound["streamSettings"]["wsSettings"]["headers"] = {"Host": address}
    outbound["tag"] = tag
    v2ray_config["outbounds"].append(outbound)
    v2ray_config["observatory"]['subjectSelector'].append(tag)
    v2ray_config["routing"]['balancers'][0]['selector'].append(tag)

with open('results/v2ray_config.conf', 'w') as fout:
    json.dump(v2ray_config, fout, indent=4)