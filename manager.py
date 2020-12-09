from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from time import sleep
import re

class Manage:

    def browse_window(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://router.asus.com')

    def log(self):
        username = self.driver.find_element_by_name('login_username')
        passw = self.driver.find_element_by_name('login_passwd')
        log_button = self.driver.find_element_by_class_name('button')
        username.send_keys('admin')
        passw.send_keys('12345')
        log_button.click()

    def _exit(self):
        exit_btn = self.driver.find_element_by_xpath('//*[@id="TopBanner"]/div/a[1]/div')
        exit_btn.click()
        Alert(self.driver).accept()
        self.driver.close()

    def check_visitors(self):
        sleep(1)
        client_btn = self.driver.find_element_by_xpath('//*[@id="clients_td"]/input')
        client_btn.click()
        sleep(2)
        client = []
        clients = self.driver.find_elements_by_class_name('viewclientlist_clientName_edit')
        for i in range(len(clients)):
            ips = self.driver.find_element_by_xpath(f'//*[@id="tb_all_list"]/tbody/tr[{i+1}]/td[4]')
            mac = self.driver.find_element_by_xpath(f'//*[@id="tb_all_list"]/tbody/tr[{i+1}]/td[5]')
            time_in = self.driver.find_element_by_xpath(f'//*[@id="tb_all_list"]/tbody/tr[{i+1}]/td[9]')
            result = re.sub('DHCP', '', ips.text)
            result = re.sub('Static', '', ips.text)
            result = result.replace('\n', '')
            client.append(f'{clients[i].text} | {result} | {mac.text} | {time_in.text}\n')
        
        client = ''.join(client)
        exit_button = self.driver.find_element_by_xpath('//*[@id="clientlist_viewlist_block"]/div[2]/img')
        exit_button.click()
        return client
        
    def change_pass(self, new_pass):
        sleep(1)
        wireless_netw = self.driver.find_element_by_xpath('//*[@id="Advanced_Wireless_Content_menu"]/table/tbody/tr/td[2]')
        wireless_netw.click()
        paswrd_line = self.driver.find_element_by_xpath('//*[@id="WLgeneral"]/tbody/tr[12]/td/input')
        paswrd_line.clear()
        paswrd_line.send_keys(new_pass)
        apply_button = self.driver.find_element_by_xpath('//*[@id="applyButton"]')
        apply_button.click()
        sleep(1.5)
        self.driver.close()

    def block_profile(self, mac_adress):
        print(mac_adress)
        wireless_netw = self.driver.find_element_by_xpath('//*[@id="Advanced_Wireless_Content_menu"]/table/tbody/tr/td[2]')
        wireless_netw.click()
        sleep(2)
        filter_ = self.driver.find_element_by_xpath('//*[@id="Advanced_ACL_Content_tab"]/span')
        filter_.click()
        adress_line = self.driver.find_element_by_xpath('//*[@id="MainTable2"]/tbody/tr[2]/td[1]/input')
        adress_line.send_keys(mac_adress)
        add = self.driver.find_element_by_xpath('//*[@id="MainTable2"]/tbody/tr[2]/td[2]/input')
        add.click()
        apply_button = self.driver.find_element_by_xpath('//*[@id="submitBtn"]/input')
        apply_button.click()
        self.driver.close()
