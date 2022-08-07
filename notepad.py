# Словарь, пройтись по словарюи получть значения
# for i in GV.domain_exemplar_dict:  # i - ключи словаря GV.domain_exemplar_dict
#     print(i)
# for key, value in GV.domain_exemplar_dict.items():
#     # print(key, value)
#     for key_in, value_in in value.items():
#         print(key, key_in, value_in)


# получить номер итерации цикла for https://proglib.io/p/python-enumerate-uproshchaem-cikly-s-pomoshchyu-schetchikov-2020-12-08
# for count, i in enumerate(GV.domain_exemplar_dict):  # i - ключи словаря GV.domain_exemplar_dict
#     print(count, i)
# for i in GV.domain_exemplar_dict:  сделано через индекс, создается список и потом получаем его длинну
#     print(list(GV.domain_exemplar_dict.keys()).index(i) + 1, i)