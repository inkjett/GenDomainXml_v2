import Data_processing_functions as Data
import GlobalVariables
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
    domain_name = ""
    if RootElement.tag == "{automation.deployment}domain":  # ищем тег с названием домена
        GV.domain_Name = RootElement.get("name")  # ищем имя домена
        print(RootElement.get("name"))
        print(Data.get_data_from_Tree(RootElement)) # вызываем рекурсивную функцию по поиску нужных элементов
        # domains_data["Domains"][GV.domain_Name] = {'domain_address': GV.domain_address,
        #                                            'node_name': GV.node_name,
        #                                            'node_address': GV.node_address,
        #                                            'ethernet_address': GV.ethernet_address,
        #                                            'server_name': GV.server_name}  # domains_data = {"Domains": {
        # # }}вставляем в словарь новую строку
# print(domains_data)

# Выбор домена
# dict - {'Domains': {'Domain': {'domain_address': 'local', 'ethernet_address': '127.0.0.1', 'server_name':
# 'Server'}, 'Domain1': {'domain_address': 'local', 'ethernet_address': '127.0.0.1', 'server_name': 'Server'}}}
#
# domain_len = len(domains_data["Domains"])
# if domain_len > 1:
#     print("Необходимо выбрать Домен для генерации xml файлов (выбрав соответствующее число)\nДоступные домены:")
#     for i in domains_data["Domains"]:
#         print(list(domains_data["Domains"].keys()).index(i) + 1, i)
#     Selected_Domain = list(domains_data["Domains"].keys())[DP.select_value(domain_len, 3) - 1]
# else:
#     Selected_Domain = list(domains_data["Domains"].keys())[0]
#     print("Доступен один домен:", Selected_Domain)
# # print(domains_data["Domains"][Selected_Domain]["domain_address"])
#
# # Выбор развертования
# print('Сгенерировать xml для локального развертывания конфигурации или для удаленного ?\n1 Локальное развертывание\n2 '
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
