[app]

title = VmessSpider
package.name = vmess_spider
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,requests,urllib3,chardet,idna,lxml,tqdm
android.permissions = android.permission.INTERNET, (name=android.permission.WRITE_EXTERNAL_STORAGE;maxSdkVersion=18)

orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = arm64-v8a
android.allow_backup = True
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false


[buildozer]

log_level = 2
warn_on_root = 1