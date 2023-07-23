from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge()      # Edge浏览器

# 打开网页
url='https://zhuanlan.zhihu.com/p/111859925'
driver.get(url) # 打开url网页 比如 driver.get("http://www.baidu.com")
driver.find_element(By.XPATH, )