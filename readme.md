### 运行逻辑
先运行server_list_parser，再运行server_parser

# 2023-04-15 - 2023-04-22
forward=ssh://sshocean-w1evacj3pitw:dvcmbsy831o7@nl01.sshocean.net:22
forward=ssh://sshocean-kt4l8xtf68oo:vdtpz9muvrht@sg05.ssh0.net:22

forward=ssh://shxruWcyAqJk-vpnjantit.com:bLfRSIuBeThk@95.183.11.162:22
forward=ssh://7FHKcbI80eQJ-vpnjantit.com:KgR7oVPAJXKC@38.54.63.251:22
forward=ssh://ByFWJ5krlpbj-vpnjantit.com:Yiyq23pNvsE1@46.246.98.117:22
forward=ssh://Ix7HJ5XWXq81-vpnjantit.com:F2x3ZpdP4D4Z@51.79.243.229:22

forward=ssh://Mctws1oFGQYC-vpnjantit.com:lGFlmNWNf7LL@195.123.228.112:22
forward=ssh://ci3TQUBV0Cwu-vpnjantit.com:3JAzWf15IX1w@195.123.228.18:22
forward=ssh://tOTatZfUQsuR-vpnjantit.com:W6H4aak9bBz6@192.99.247.52:22
forward=ssh://rgHgodxXE6vU-vpnjantit.com:gOE6M3zcHZFE@62.233.57.53:22
forward=ssh://Wmlry5key9ap-vpnjantit.com:VfFz0ahRKHqb@51.75.74.253:22
forward=ssh://sb54ujIwVcIo-vpnjantit.com:9QQlUMUBsoin@51.68.172.194:22
forward=ssh://syTN3SqzycIj-vpnjantit.com:223kXz7BdwoC@217.160.33.100:22
forward=ssh://yHxWAtIdnkHH-vpnjantit.com:ZMvzvTnSDQ6u@92.243.93.246:22


### 打包
sudo apt-get install zlib1g-dev python3-pip default-jdk openjdk-11-jdk-headless ecj zip unzip autoconf automake libtool pkg-config libffi-dev git tree libssl-dev openssl tmux

pip install cython
echo 'export PATH=/home/admin/.local/bin:$PATH' >>~/.bashrc
echo 'export PATH=~/glider:$PATH' >>~/.bashrc
source ~/.bashrc


git clone https://github.com/kivy/buildozer.git
cd buildozer
sudo python3 setup.py install

cd /home/admin/.buildozer/android/platform/android-sdk
unzip commandlinetools-linux-6514223_latest

mkdir ~/down & cd ~/down
wget https://github.com/nadoo/glider/releases/download/v0.16.3/glider_0.16.3_linux_armv7.tar.gz
tar -zxvf glider_0.16.3_linux_armv7.tar.gz
mkdir ~/gliderapp & cd ~/gliderapp
cp ~/down/glider_0.16.3_linux_armv7/usr/bin/glider ./glider.o
vi main.py
vi glider.conf


buildozer init
vi buildozer.spec
buildozer android debug

$$\mathbf{C} = \frac{1}{N-1} \mathbf{\bar{X}}^T \mathbf{\bar{X}} \tag{1}$$
$$\mathbf{C} = \mathbf{U} \mathbf{\Lambda} \mathbf{U}^T \tag{2}$$
$$\mathbf{y} = \mathbf{W}^T (\mathbf{x} - \mathbf{\mu}) \tag{3}$$
