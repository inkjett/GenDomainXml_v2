import xml.etree.ElementTree as ET  # подключаем The ElementTree XML
import CommentForXml as Comment
import xml.dom.minidom
import GlobalVariables as GV

# словарь
# elements = {"element1": {"armName": "", "ethernet-adapter": "", "ethernet-adapter_1": "", "io-server": ""},
#             "element2": {"armName": "", "ethernet-adapter": "", "ethernet-adapter_1": "", "io-server": ""}}
elements = {}


def gen_local_net_xml(_Name, _NetEnterPort, _ParentAgentPort):
    # root
    root = ET.Element("Alpha.Net.Agent")
    root.set("Name", _Name)
    root.set("NetEnterPort", _NetEnterPort)
    root.set("ParentAgentPort", _ParentAgentPort)

    # root.Options
    ET.SubElement(root, 'Options LoggerLevel="2"')

    for index, value in enumerate(
            Comment.listOfnetComments):  # циклом проходим по списку комментариев и добавляем их в xml
        root.insert(index, ET.Comment(value))
    pretty_xml_as_string = xml.dom.minidom.parseString(
        ET.tostring(root, encoding='utf-8', method='xml',
                    xml_declaration=True).decode('UTF-8')).toprettyxml()  # приводим xml к "нормальному" виду
    return pretty_xml_as_string


def get_data_from_Tree(_domain_address, value_in):
    GV.domain_address = _domain_address
    for x in value_in:
        if x.tag == "{automation.deployment}domain-node":
            # print("ARM=", x.get("address"))
            GV.ARM = x.get("address")
        if x.tag == "{automation.ethernet}ethernet-adapter":
            # print("addressEthernet=", x.get("address"))
            GV.ethernet_address = x.get("address")
        if x.tag == "{server}io-server":
            # print("nameServer=", x.get("name"))
            GV.server_name = x.get("name")
        get_data_from_Tree(_domain_address, x)


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
