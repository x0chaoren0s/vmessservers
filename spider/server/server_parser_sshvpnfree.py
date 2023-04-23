import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent)


from .server_parser_base import Server_parser_base, By
from ..server_list.server_list_parser_sshvpnfree import SLP_SSHVPNFREE

from selenium.webdriver.support.wait import WebDriverWait

class Server_parser_sshvpnfree(Server_parser_base):
    name = 'sshvpnfree'
    def __init__(self, server_dict: dict = None, server_list_parser = SLP_SSHVPNFREE, interval_sec: int = 0) -> None:
        super().__init__(server_dict, server_list_parser, interval_sec, use_selenium=True)

    def filling_form_via_selenium(self, driver_in_form_page) -> dict:
        driver = driver_in_form_page
        ret = dict()
        
        input_pass = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, '//input[@id="password"]'))
        input_pass.clear()
        input_pass.send_keys(self.getRandStr(12))

        button_create = driver.find_element(By.XPATH, '//button[@type="submit"]')
        button_create.click() # 此时已提交

        try:
            input_date_create = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, '//div[@class="panel-body"]/div[2]/div[@class="col-xs-8"][11]/div/input'))
        except:
            ret['error_info'] = 'server in maintenance, or some other thing wrong.'
            return ret
        ret['date_create'] = input_date_create.get_attribute('value').strip()
        input_date_expire = driver.find_element(By.XPATH, '//div[@class="panel-body"]/div[2]/div[@class="col-xs-8"][12]/div/input')
        ret['date_expire'] = input_date_expire.get_attribute('value').strip()
        text_config = driver.find_element(By.XPATH, '//div[@class="panel-body"]/div[2]/div[@class="col-xs-8"][14]/div/textarea')
        ret['config'] = text_config.text.strip()

        return ret
        

SP_SSHVPNFREE = Server_parser_sshvpnfree()