'''本脚本用于清洗网上公开的订阅链接。仅收纳归类hk、tw、jp的节点'''

import requests, json, base64, os, shutil
from tqdm import tqdm
from xray2glider import Glider_config_convertor

regions = ['hk', 'tw', 'jp', '_']

region_keys = {
    'hk': ['🇭🇰', 'hk', 'Hk', 'HK', 'hong kong', 'hongkong', 'Hong kong', 'Hongkong', 'Hong Kong', 'HongKong', 'HONG KONG', 'HONGKONG', '香港'],
    'tw': ['🇹🇼', 'tw', 'Tw', 'TW', 'tai wan',   'taiwan',   'Tai wan',   'Taiwan',   'Tai Wan',   'TaiWan',   'TAI WAN',   'TAIWAN',   '台湾',
                                   'tai pei',   'taipei',   'Tai pei',   'Taipei',   'Tai Pei',   'TaiPei',   'TAI PEI',   'TAIPEI',   '台北'],
    'jp': ['🇯🇵', 'jp', 'Jp', 'JP', 'japan', 'Japan', 'JAPAN', '日本',
                                   'tokyo', 'Tokyo', 'TOKYO', '东京',
                                   'osaka', 'Osaka', 'OSAKA', '大阪'],
    '_': []
}

nodes = { # xray config
    'hk': set(),
    'tw': set(),
    'jp': set(),
    '_': set()
}

glider_nodes = { # glider config
    'hk': set(),
    'tw': set(),
    'jp': set(),
    '_': set()
}

sublinks = [
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

def link_region(line: str) -> str:
    ret = '_'
    host, ps = '', ''
    if line.startswith('vless://') or line.startswith('ss://') or line.startswith('trojan://'):
        try:
            socket = line.split('@')[1].split('?')[0]
            host = socket[:socket.rfind(':')]
            ps = line.split('#')[1]
            ps = ps
        except IndexError:
            pass
    elif line.startswith('vmess://'):
        config_dict = json.loads(base64.b64decode(line.split('vmess://')[1]).decode())
        host = config_dict.get('add', '')
        ps = config_dict.get('ps', '')
    if host != '':
        for region in regions:
            if any([key in host+ps for key in region_keys[region]]):
                ret = region
                break
    return ret

for sublink in tqdm(sublinks, desc='clean subs'):
    while True:
        try:
            lines = requests.get(sublink, proxies={'https':'http://127.0.0.1:7602'}).content.decode()
            break
        except:
            pass
    try:
        lines = base64.b64decode(lines).decode()
    except:
        pass
    lines = lines.split('\n')
    for line in lines:
        nodes[link_region(line)].add(line.strip()+'\n')

for region in regions[:-1]:
    glider_nodes[region] = {Glider_config_convertor().convert(xraylink) for xraylink in nodes[region]}-{''}

# print(nodes)
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)  
for region in regions[:-1]:
    with open(f'{script_dir}/../results/{region}.txt', 'w', encoding='utf8') as fout:
        fout.writelines(nodes[region])
    with open(f'{script_dir}/../results/{region}.conf', 'w', encoding='utf8') as fout:
        fout.writelines(glider_nodes[region])
    
shutil.copy(f'{script_dir}/../results/glider_sub_template.conf',f'{script_dir}/../results/glider_sub.conf')
with open(f'{script_dir}/../results/glider_sub.conf', 'a', encoding='utf8') as fout:
    fout.writelines(['\n'])
    for region in regions[:-1]:
        fout.writelines(['\n','# '+region,'\n'])
        fout.writelines(glider_nodes[region])
