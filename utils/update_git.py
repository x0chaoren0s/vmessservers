import os, shutil

def update_git():
    # if not os.path.exists('chores'):
    #     os.system('git clone https://github.com/x0chaoren0s/chores.git')
    
    # for conf in os.listdir('results'):
    #     if conf.endswith('.conf'):
    #         shutil.copy(f'results/{conf}', f'chores/{conf}')

    # os.system('cd chores & git add . & git commit -m configs & git push')
    folders_py = [
        'spider/server_list',
        'spider/server',
        'utils',
        '.',
    ]
    files_chore = [
        'free_servers.txt',
        'readme.md',
        'msedgedriver.exe',
    ]
    for folder in folders_py:
        os.system(f"git add {folder}/*.py & git commit -m spider_update & git push")
    for file in files_chore:
        os.system(f"git add {file} & git commit -m chore_file_update & git push")


if __name__ == '__main__':
    update_git()