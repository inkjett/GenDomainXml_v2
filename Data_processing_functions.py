import xml.etree.ElementTree as ET  # подключаем The ElementTree XML
import CommentForXml as Comment
import xml.dom.minidom


def gen_net_xml(_LocalRemote, _DataIn):
    # root
    # <Alpha.Net.Agent Name="GB_GES" NetEnterPort="1010" ParentAgentPort="1020">

    root = ET.Element("Alpha.Net.Agent")
    if _LocalRemote == "Remote":
        print(_DataIn)
        # root.set("Name", _NodeAddress)
        # root.set("NetEnterPort", _NetEnterPort)
        # root.set("ParentAgentPort", _ParentAgentPort)
    # if _LocalRemote == "Local":
    #     root.set("Name", _NodeAddress)
    #     root.set("NetEnterPort", _NetEnterPort)
    #     root.set("ParentAgentPort", _ParentAgentPort)

    #
    # # root.Options
    # ET.SubElement(root, 'Options LoggerLevel="2"')
    #
    # # циклом проходим по списку комментариев и добавляем их в xml
    # for index, value in enumerate(
    #         Comment.listOfnetComments):
    #     root.insert(index, ET.Comment(value))
    #
    # # pretty_xml_as_string
    # pretty_xml_as_string = xml.dom.minidom.parseString(
    #     ET.tostring(root, encoding='utf-8', method='xml',
    #                 xml_declaration=True).decode('UTF-8')).toprettyxml()  # приводим xml к "нормальному" виду
    # return pretty_xml_as_string


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
    # root.insert(1, ET.Comment(Comment.domaincomment2))  # вставляем комментарий
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


def get_data_from_Tree(_valueIn, temp=None):
    # print(_valueIn)
    if not temp:
        temp = {"ethernet-adapter": [], "server_name": []}
    for x in _valueIn:
        if x.tag == "{automation.deployment}domain":
            temp.update({x.get("name"): x.get("address")})
        if x.tag == "{automation.deployment}domain-node":
            temp.update({"domain_name": x.get("name")})
            temp.update({"domain_address": x.get("address")})
        elif x.tag == "{automation.ethernet}ethernet-adapter":
            temp["ethernet-adapter"].append(x.get("address"))
        elif x.tag == "{server}io-server":
            temp["server_name"].append(x.get("name"))
        temp.update(get_data_from_Tree(x, temp))
    return temp


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


# Удаляем ноды в которых нет серверов Alpha.Server - пока не используется
def delete_do_not_contain_AS_node(_ValueIn, _DomainName):
    delete_nodes = []
    for Elements in _ValueIn["Domains"][_DomainName]:
        for SubElements in _ValueIn["Domains"][Elements]:
            if isinstance(_ValueIn.get("Domains")[Elements][SubElements], str) == False:
                if len(_ValueIn.get("Domains")[Elements][SubElements].get("server_name")) == 0:
                    delete_nodes.append(SubElements)
    return delete_nodes


#############################

# Выбор элемента внутри словаря, доделать сделано только для else
def select_unit(_textIn, _dictIn, _elementOne=None, _elementTwo=None):
    print(_textIn)
    if not _elementTwo or not _elementOne:  # весь словарь _dictIn
        for i in _dictIn:
            print(list(_dictIn.keys()).index(i) + 1, i)
    if not _elementTwo:  # один уровень внутрь словаря _dictIn
        for i in _dictIn[_elementOne]:
            print(list(_dictIn[_elementOne].keys()).index(i) + 1, i)
    else:  # два уровня внутрь словаря _dictIn
        for i in _dictIn[_elementOne][_elementTwo]:
            unit_len = len(_dictIn[_elementOne][_elementTwo])
            [print(list(_dictIn[_elementOne][_elementTwo].keys()).index(i) + 1, i)]
        return list(_dictIn[_elementOne][_elementTwo].keys())[select_value(unit_len, 3) - 1]