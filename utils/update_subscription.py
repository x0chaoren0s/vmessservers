import os, shutil

def update_subscription():
    if not os.path.exists('chores'):
        os.system('git clone https://github.com/x0chaoren0s/chores.git')
    
    for conf in os.listdir('results'):
        if conf.endswith('.conf'):
            shutil.copy(f'results/{conf}', f'chores/{conf}')

    os.system('cd chores & git add . & git commit -m configs & git push -f')


if __name__ == '__main__':
    update_subscription()