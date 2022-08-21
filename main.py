import Data_processing_functions as Data
import os
import Data_processing_functions as DP
import xml.etree.ElementTree as ET  # подключаем The ElementTree XML
import GlobalVariables as GV

# Переменные
selected_file_name = ""
RootTree = ""
domain_Name = ""
domains_data = {"Domains": {}}
Selected_Domain = ""
Selected_Deployment = 0

# Получаем список файлов
files_list = []
[files_list.append(f) for f in os.listdir(os.getcwd()) if ".omx" in f]  # Создаем список файлов с расширением omx
if len(files_list) > 1:  # выбор файла
    print('Необходимо выбрать файл для использования:')
    [print(files_list.index(i) + 1, i) for i in files_list]
    selected_file_name = files_list[DP.select_value(len(files_list), 3) - 1]
    print("Выбран файл:", selected_file_name)
elif len(files_list) == 1:
    selected_file_name = files_list[0]
    print("Найден файл:", selected_file_name)
else:
    print("Файлы не наедены")
# del files_list  # удаляем переменную со списком файлов

# чтение данных из файла
with open(selected_file_name, 'r', encoding="UTF-8") as f:  # Проходим по всем строкам файла проекта
    tree = ET.parse(f)
    RootTree = tree.getroot()

# поиск данных домена
for RootElement in RootTree:  # проходим по всему дереву
    if RootElement.tag == "{automation.deployment}domain":  # ищем тег с названием домена
        temp1 = {RootElement.get("name"):{}}
        for NodeElement in RootElement:
            if NodeElement.tag == "{automation.deployment}domain-node":
                temp_domains_data = {}
                temp_domains_data[NodeElement.get("name")] = Data.get_data_from_Tree(NodeElement)
                temp1[RootElement.get("name")].update(temp_domains_data)
                domains_data["Domains"].update(temp1)
print(domains_data)

# Выбор домена
# dict - {'Domains': {'Domain': {'ethernet-adapter': {'EthernetAdapter': '192.168.0.1',
# 'EthernetAdapter1': '192.168.0.2'}, 'domain_name': 'ARM', 'domain_address': 'ARM_1', 'server_name': '1Server1'},
# 'Domain1': {'ethernet-adapter': {'EthernetAdapter': '192.168.0.1', 'EthernetAdapter1': '192.168.0.2'},
# 'domain_name': 'ARM22', 'domain_address': 'ARM_1', 'server_name': '1Server1'}}}
# domain_len = len(domains_data["Domains"])
# if domain_len > 1:
#     print("Необходимо выбрать Домен для генерации xml файлов (выбрав соответствующее число)\nДоступные домены:")
#     for i in domains_data["Domains"]:
#         print(list(domains_data["Domains"].keys()).index(i) + 1, i)
#     Selected_Domain = list(domains_data["Domains"].keys())[DP.select_value(domain_len, 3) - 1]
# else:
#     Selected_Domain = list(domains_data["Domains"].keys())[0]
#     print("Доступен один домен:", Selected_Domain)
#
# Data.gen_net_xml("Remote", domains_data["Domains"][Selected_Domain])
#
# # Выбор развертования
# print('Сгенерировать xml для локального развертывания конфигурации или для удаленного ?\n1 Локальное развертывание\n2'
#       'Удаленное развертывание')
# # Selected_Deployment = DP.select_value(2, 3)
# Selected_Deployment = 2
#
# # print(domains_data["Domains"][list(domains_data["Domains"].keys())[Selected_Domain]]["domain_address"])
# # print(domains_data["Domains"])
# domain_address = domains_data["Domains"][Selected_Domain]["domain_address"]
# node_address = domains_data["Domains"][Selected_Domain]["node_address"]
# ethernet_address = domains_data["Domains"][Selected_Domain]["ethernet_address"]
# print(domain_address, node_address, ethernet_address)
# if Selected_Deployment == 1:
#     print(list(domains_data["Domains"].keys())[Selected_Domain])
# elif Selected_Deployment == 2:
#     net_xml = DP.gen_net_xml("Remote", Selected_Domain, "1010", "1020")  # для удаленного развертования нужно указать
#     # <Alpha.Net.Agent Name="domain_address">
#     #
#     print(net_xml)
#     DP.save_data_to_file("alpha.net.agent.xml", net_xml)

# DP.gen_local_domain_xml()

# print(list(domains_data["Domains"].keys())[Selected_Domain])

# WorkWithFile.get_data_from_file("testProject.omx")
# DataFunc.gen_domain_xml_str()
# DataFunc.select_domain()
# DataFunc.select_deployment()
# WorkWithFile.save_data_to_file("alpha.net.agent.xml", GlobalVariables.net_pretty_xml)
# DataFunc.gen_domain_xml_str()
# WorkWithFile.set_data_to_file("alpha.domain.agent.xml", GlobalVariables.domain_pretty_xml)

# DataFunc.gen_net_xml_str()
# DataFunc.gen_domain_xml_str()
# WorkWithFile.get_list_of_files()


# obj = DM._domain_elements()
# obj.create_exemplar("local1","ARM1","127.1.1.0","AlphaServer")
# print(obj._domain)
