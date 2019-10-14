import configparser

# coding=utf-8
import configparser


class ReadIni(object):
    def __init__(self, file_name=None, node=None):
        if file_name is None:
            file_name = './config.ini'
        if node is None:
            self.node = 'Test'
        else:
            self.node = node
        self.cf = self.load_ini(file_name)

    @staticmethod
    def load_ini(file_name):
        cf = configparser.ConfigParser()
        cf.read(file_name)
        return cf

    def get_value(self, key):
        data = self.cf.get(self.node, key)
        return data


if __name__ == '__main__':
    read_ini = ReadIni(node='Uat')
    print(read_ini.get_value('password_uat'))
