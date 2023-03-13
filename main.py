import json
import Data_processing_functions as Data
import os
import Data_processing_functions as DP
import xml.etree.ElementTree as ET  # подключаем The ElementTree XML
import GlobalVariables as GV

# поиск данных домена
# {'Domains': {'Domain': {'domain_address': 'local',
# 'nodes_data': {'ARM': {'ethernet-adapter': ['192.168.1.1', '192.168.1.2'],
# 'server_name': ['AlphaServer', 'AlphaServer2']},
# Domain - имя домена из поля Имя элемента Alpha.Domain
# nodes_data - элемент с информации в ноде
# ARM - имя ноды из полня Имя элемента Узел Alpha.Domain
# ethernet-adapter - IP адрес  элемент адаптер Ethernet в ARM
# server_name - название Alpha.Server в ARM
# domain_address - адрес домена из поля Адресс элемента Alpha.Domain

# Переменные
selected_file_name = ""
RootTree = ""
AlphaDomain = []  # список Alpha.Domain тип список
domain_Name = ""
domains_data = {"Domains": {}}
Selected_AlphaDomain = ""  # выбранный Alpha.Domain
Selected_Domain = ""  # Выбранный домен
Selected_Node = ""  # Выбранная нода
Selected_Deployment = 0  # Выбранное развертывание 1 локальное 2 уделенное

# Получаем список файлов
files_list = []
# Создаем список файлов с расширением omx - стереть ADS
[files_list.append(f) for f in os.listdir(os.getcwd() + "\ADS") if ".omx" in f[-4:]]
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
with open("ADS/" + selected_file_name, 'r', encoding="UTF-8") as f:  # Проходим по всем строкам файла проекта
    tree = ET.parse(f)
    RootTree = tree.getroot()

# Далее будет откровенный "колхоз", просто чтобы работало
for RootElement in RootTree:  # проходим по всему дереву
    if RootElement.tag == "{automation.deployment}domain":
        AlphaDomain.append(RootElement.get("name"))

# Выбор Alpha.Domain
if len(AlphaDomain) > 1:
    Selected_AlphaDomain = DP.select_unit("Для генерации xml файлов необходимо выбрать домен Alpha.Domain (выбрав соответствующее число)",
                                     AlphaDomain, "Domains")
else:
    Selected_AlphaDomain = AlphaDomain[0]
    print("Доступен только один домен, Alpha.Domain:", Selected_AlphaDomain)




for RootElement in RootTree:  # проходим по всему дереву
    if RootElement.tag == "{automation.deployment}domain":  # ищем тег с названием домена
        if Selected_AlphaDomain == RootElement.get("name"):
            #print("Selected_AlphaDomain =", Selected_AlphaDomain)
            DomainName = {RootElement.get("name"): {"AlphaDomain": RootElement.get("name"), "domain_address": RootElement.get("address"), "nodes_data": {}}}
            #print("DomainName =", DomainName)
            countOfNodeElement = 1
            for NodeElement in RootElement:
                if NodeElement.tag == "{automation.deployment}domain-node":  # Ищем элемент Узел Alph.Domain
                    #print(Data.get_domain_data_from_Tree(NodeElement))
                    nodes_data = {"NodeAlphaDomain" + str(countOfNodeElement): Data.get_domain_data_from_Tree(NodeElement)}

                    print(nodes_data)
                    if len(nodes_data["NodeAlphaDomain" + str(countOfNodeElement)]["ServiceName"]) != 0:
                        DomainName[RootElement.get("name")]["nodes_data"].update(nodes_data)
                        domains_data["Domains"].update(DomainName)
                    #nodes_data = {NodeElement.get("name"): Data.get_domain_data_from_Tree(NodeElement)}
                    #print("nodes_data = ", nodes_data)
                #     if len(nodes_data[NodeElement.get("name")]["ServiceName"]) != 0:
                #         DomainName[RootElement.get("name")]["nodes_data"].update(nodes_data)
                #         domains_data["Domains"].update(DomainName)
                #     else:
                #         print("В узле домена Alpha.Domain:", RootElement.get("name"), " нет экземпляра Alpha.Server")
                # elif NodeElement.tag == "{automation.deployment}workstation":  # Ищем элемент "Рабочее место"
                #     nodes_data = {NodeElement.get("name"): Data.get_workstation_data_from_Tree(NodeElement)}
                #     if len(nodes_data[NodeElement.get("name")]["APserver_name"]) != 0:
                #         DomainName[RootElement.get("name")]["nodes_data"].update(nodes_data)
                #         domains_data["Domains"].update(DomainName)
                    countOfNodeElement += 1


#
#
# for RootElement in RootTree:  # проходим по всему дереву
#     if RootElement.tag == "{automation.deployment}domain":  # ищем тег с названием домена
#         if Selected_AlphaDomain == RootElement.get("name"):
#             #print("Selected_AlphaDomain =", Selected_AlphaDomain)
#             DomainName = {RootElement.get("name"): {"AlphaDomain": RootElement.get("name"), "domain_address": RootElement.get("address"), "nodes_data": {}}}
#             print("DomainName =", DomainName)
#             for NodeElement in RootElement:
#                 if NodeElement.tag == "{automation.deployment}domain-node":  # Ищем элемент Узел Alph.Domain
#                     nodes_data = {NodeElement.get("name"): Data.get_domain_data_from_Tree(NodeElement)}
#                     #print("nodes_data = ", nodes_data)
#                     if len(nodes_data[NodeElement.get("name")]["ASserver_name"]) != 0:
#                         DomainName[RootElement.get("name")]["nodes_data"].update(nodes_data)
#                         domains_data["Domains"].update(DomainName)
#                     else:
#                         print("В узле домена Alpha.Domain:", RootElement.get("name"), " нет экземпляра Alpha.Server")
#                         break
#                 elif NodeElement.tag == "{automation.deployment}workstation":  # Ищем элемент "Рабочее место"
#                     nodes_data = {NodeElement.get("name"): Data.get_workstation_data_from_Tree(NodeElement)}
#                     if len(nodes_data[NodeElement.get("name")]["APserver_name"]) != 0:
#                         DomainName[RootElement.get("name")]["nodes_data"].update(nodes_data)
#                         domains_data["Domains"].update(DomainName)
#
# #print("domains_data=", domains_data)
#
# # Выбор домена
# if len(domains_data["Domains"]) > 1:
#     Selected_Domain = DP.select_unit("Необходимо выбрать Домен для генерации xml файлов (выбрав соответствующее число)",
#                                      domains_data, "Domains")
# else:
#     Selected_Domain = list(domains_data["Domains"].keys())[0]
#     print("Доступен один домен:", Selected_Domain)
#
# # был анахронизм - #1, смотреть внизу списка
#
#
# # Выбор развёртывания
# print('Сгенерировать xml для локального развертывания конфигурации или для удаленного?\n1 Локальное развертывание\n2'
#       ' Удаленное развертывание')
# Selected_Deployment = DP.select_value(2, 3)
#
# if Selected_Deployment == 1:
#     Selected_Node = DP.select_unit("Необходимо выбрать Узел для которого будут сгенерированы xml",
#                                    domains_data["Domains"], Selected_Domain, "nodes_data")
# print(Selected_Node)
# print(domains_data["Domains"])


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




# #1 Удаляем ноды в которых нет серверов Alpha.Server
# delete_nodes = []
# for Elements in domains_data["Domains"]:
#     # print(Elements)
#     for SubElements in domains_data["Domains"][Elements]["nodes_data"]:
#         # print(SubElements)
#         if len(domains_data.get("Domains")[Elements]["nodes_data"][SubElements].get("server_name")) == 0:
#             delete_nodes.append(SubElements)
# for i in delete_nodes:
#     if i in domains_data["Domains"][Selected_Domain]["nodes_data"]:
#         del domains_data["Domains"][Selected_Domain]["nodes_data"][i]
# !!!!!!!!!! анахронизм