import Data_processing_functions as DP
import xml.etree.ElementTree as ET  # подключаем The ElementTree XML
import GlobalVariables
import os


# запись данных в файл
def save_data_to_file(fileName, textSave):
    with open(fileName, "w") as filetowrite:
        filetowrite.write(textSave)