import xml.etree.ElementTree as ET  # подключаем The ElementTree XML
import CommentForXml as Comment
import xml.dom.minidom
import GlobalVariables as GV
import os

# словарь
# elements = {"element1": {"armName": "", "ethernet-adapter": "", "ethernet-adapter_1": "", "io-server": ""},
#             "element2": {"armName": "", "ethernet-adapter": "", "ethernet-adapter_1": "", "io-server": ""}}
elements = {}


def gen_net_xml(_LocalRemote, _DomainName, _NodeName, _NetEnterPort, _ParentAgentPort):
    # root
    # <Alpha.Net.Agent Name="GB_GES" NetEnterPort="1010" ParentAgentPort="1020">

    root = ET.Element("Alpha.Net.Agent")

    if _LocalRemote == "Local":
        root.set("Name", _NodeName)
        root.set("NetEnterPort", _NetEnterPort)
        root.set("ParentAgentPort", _ParentAgentPort)
    elif _LocalRemote == "Remote":
        root.set("Name", _DomainName)
        root.set("NetEnterPort", _NetEnterPort)
        root.set("ParentAgentPort", _ParentAgentPort)
        ET.SubElement(root[0], "ChildAgents")









    # root.Options
    ET.SubElement(root, 'Options LoggerLevel="2"')

    # циклом проходим по списку комментариев и добавляем их в xml
    for index, value in enumerate(
            Comment.listOfnetComments):
        root.insert(index, ET.Comment(value))

    # pretty_xml_as_string
    pretty_xml_as_string = xml.dom.minidom.parseString(
        ET.tostring(root, encoding='utf-8', method='xml',
                    xml_declaration=True).decode('UTF-8')).toprettyxml()  # приводим xml к "нормальному" виду
    return pretty_xml_as_string
#############################


def gen_domain_xml():
    # root
    # <Alpha.Domain.Agent Name="NDA">
    root = ET.Element("Alpha.Domain.Agent")
    root.set("Name", "NDA")
    root.insert(0, ET.Comment(Comment.domaincomment1))  # вставляем комментарий

    # EntryPointNetAgent
    # <EntryPointNetAgent Name="local" Address="127.0.0.1" Port="1010"/>
    ET.SubElement(root, "EntryPointNetAgent")
    root[1].set("Name", "local")
    root[1].set("Address", "127.0.0.1")
    root[1].set("Port", "1010")
    root[1].insert(0, ET.Comment(Comment.domaincomment2))  # вставляем комментарий

    # InstalledComponents
    # < InstalledComponents >
    #     < Alpha.Server Name = "Server_1" ServiceName = "Alpha.Server" DefaultActivation = "1" / >
    # < / InstalledComponents >

    ET.SubElement(root, "InstalledComponents")
    ET.SubElement(root[2], "Alpha.Server")
    root[2][0].set("Name", "Server_1")
    root[2][0].set("ServiceName", "Alpha.Server")
    root[2][0].set("DefaultActivation", "1")
    #root.insert(1, ET.Comment(Comment.domaincomment2))  # вставляем комментарий
    # Server
    # < Server >
    #   < Components StoragePath = "c:\DomainStorage\cache\server" >
    #       < Component InstalledName = "Server_1" Name = "Server" StorageLimitSize = "0" StorageLimitNum = "0" / >
    #   < / Components >
    # < / Server >

    ET.SubElement(root, "Server")
    ET.SubElement(root[3], "Components")
    ET.SubElement(root[3][0], "Component")
    root[3][0].set("StoragePath", "c:\DomainStorage\cache\server")
    root[3][0][0].set("InstalledName", "Server_1")
    root[3][0][0].set("Name", "Server")
    root[3][0][0].set("StorageLimitSize", "0")
    root[3][0][0].set("StorageLimitNum", "0")

    # Options LoggerLevel
    ET.SubElement(root, 'Options LoggerLevel="2"')

    pretty_xml_as_string = xml.dom.minidom.parseString(
        ET.tostring(root, encoding='utf-8', method='xml',
                    xml_declaration=True).decode('UTF-8')).toprettyxml()  # приводим xml к "нормальному" в
    print(pretty_xml_as_string)
#############################


def get_data_from_Tree(_domain_address, value_in):
    GV.domain_address = _domain_address
    for x in value_in:
        if x.tag == "{automation.deployment}domain-node":
            # print("ARM_name=", x.get("name"))
            # print("ARM_address=", x.get("address"))
            GV.node_name = x.get("name")
            GV.node_address = x.get("address")
        if x.tag == "{automation.ethernet}ethernet-adapter":
            # print("addressEthernet=", x.get("address"))
            GV.ethernet_address = x.get("address")
        if x.tag == "{server}io-server":
            # print("nameServer=", x.get("name"))
            GV.server_name = x.get("name")
        get_data_from_Tree(_domain_address, x)
#############################


def select_value(_maxlength, _attempt):
    print("Введите число от 1 до", _maxlength, ":")
    for i in range(_attempt):
        temp = input()
        if temp.isdigit() and 1 <= int(temp) <= _maxlength:
            return int(temp)
            break
        else:
            print('Необходимо ввести число от 1 до', _maxlength, 'количество попыток', 2 - i, ':')
    else:
        return - 1
#############################


# запись данных в файл
def save_data_to_file(fileName, textSave):
    with open(fileName, "w") as filetowrite:
        filetowrite.write(textSave)
#############################


