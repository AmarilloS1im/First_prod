import os
import uuid
import csv
class Main:
    def __init__(self,file,custom_dict = None):
        if os.path.isfile(file):
            self.__file = file
        else:
            raise ValueError('Only a file object can be passed to the Main class parameter "file"')
        self.__extension = None
        self.__file_name = None

        self.__uuid_dict = {}
        self.__uuid = str(uuid.uuid4())
        if self.__uuid in self.__uuid_dict.keys():
            self.__uuid = str(uuid.uuid4())
            self.__uuid_dict[self.__uuid] = self.file_name
        else:
            self.__uuid_dict[self.__uuid] = self.file_name

        if os.path.isfile(custom_dict):
            self.__custom_dict = custom_dict
            self.__main_dict = self.main_dict

    @property
    def file(self):
        return self.__file

    @property
    def extension(self):
        self.__extension = self.__file.split('.')[-1]
        return self.__extension

    @property
    def file_name(self):
        self.__file_name = self.__file.split('.')[:-1]
        out_str = ''
        for items in self.__file_name:
            out_str = out_str + items + '.'
        self.__file_name = out_str
        return self.__file_name

    @property
    def uuid(self):
        return self.__uuid

    @property
    def uuid_file(self):
        return self.__uuid + '.' + self.__extension

    def get_uuid_dict_info(self):
        return self.__uuid_dict

    @property
    def main_dict(self):
        my_dict = []
        with open(rf"dummy\translated_words_dict_file.csv") as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            for row in file_reader:
                tmp_dict = [row[0], row[1]]
                my_dict.append(tmp_dict)
        self.__main_dict = list(sorted(my_dict, key=lambda item: len(item[0]), reverse=True))
        return self.__main_dict

    def set_custom_dict(self, value):
        my_dict = []
        with open(value, 'r', encoding='utf-8-sig') as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            for row in file_reader:
                tmp_dict = [row[0], row[1]]
                my_dict.append(tmp_dict)
        self.__custom_dict = list(sorted(my_dict, key=lambda item: len(item[0]), reverse=True))

    def get_custom_dict(self):
        return self.__custom_dict





