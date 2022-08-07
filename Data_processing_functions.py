import xml.etree.ElementTree as ET  # подключаем The ElementTree XML
import CommentForXml as Comment
import xml.dom.minidom
import GlobalVariables as GV

# словарь
# elements = {"element1": {"armName": "", "ethernet-adapter": "", "ethernet-adapter_1": "", "io-server": ""},
#             "element2": {"armName": "", "ethernet-adapter": "", "ethernet-adapter_1": "", "io-server": ""}}
elements = {}


def gen_local_net_xml():
    # root
    root = ET.Element("Alpha.Net.Agent")
    root.set("Name", elements["element1"]['armName'])
    root.set("NetEnterPort", "1010")
    root.set("ParentAgentPort", "1020")

    # root.Options
    ET.SubElement(root, 'Options LoggerLevel="2"')

    for index, value in enumerate(
            Comment.listOfnetComments):  # циклом проходим по списку комментариев и добавляем их в xml
        root.insert(index, ET.Comment(value))
    pretty_xml_as_string = xml.dom.minidom.parseString(
        ET.tostring(root, encoding='utf-8', method='xml',
                    xml_declaration=True).decode('UTF-8')).toprettyxml()  # приводим xml к "нормальному" виду
    GV.net_pretty_xml = pretty_xml_as_string



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


def select_domain():
    domain_len = len(GV.domain_exemplar_dict)
    # print(domain_len) количество доменов
    # dict - {ключ: значение} dict_items([('Domain', {'domain_address': 'local', 'ethernet_address': '127.0.0.1', 'server_name': 'Server'})])
    if domain_len >= 1:
        print("Необходимо выбрать Домен для генерации xml файлов (выбрав соответствующее число)\nДоступные домены:")
        for i in GV.domain_exemplar_dict:
            print(list(GV.domain_exemplar_dict.keys()).index(i) + 1, i)
            select_domain(domain_len, 3)
    else:
        print("Выбран Домен:", list(GV.domain_exemplar_dict.keys())[0])
        GV.Selected_Domain = 0

        # for count, i in enumerate(GV.domain_exemplar_dict):  # i - ключи словаря GV.domain_exemplar_dict, выводим
        #     # наеденые домены
        #     print(count+1, i)


def select_deployment():
    print('Сгенерировать xml для локального развертывания конфигурации или для удаленного ?')
    print("1 Локальное развертывание\n2 Удаленное развертывание")
    for i in range(3):
        temp = input()
        if temp.isdigit() and 1 <= int(temp) <= 2:
            GV.Selected_deployment = int(temp)
            break
        else:
            print('Необходимо ввести число от 1 до 2, количество попыток', 2 - i, ':')


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
