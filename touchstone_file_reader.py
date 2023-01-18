import numpy as np
import re


class MyError(IOError):
    def __init__(self):
        super(MyError, self).__init__()



class SnpReader:
    def __init__(self):
        self.version = None
        self.number_of_ports = None
        self.two_ports_order = None
        self.number_of_frequencies = None
        self.number_of_noise_frequencies = None
        self.reference = None

        # try:
        #     if self.reference == 1:
        #         raise ValueError
        #     elif self.reference == 2:
        #         raise MyError()
        #
        # except ValueError:
        #     print('alala')
        # except ZeroDivisionError:
        #     print('ololo')
        # except MyError:
        #     print('Not me problem')
        # else:
        #     print(31)
        # finally:
        #     print(123)
        #
        # self.begin_information = None
        # self.end_information = None

    def read_file(self, file_name):
        with open(file_name, 'r') as snp:
            snp = snp.readlines()
        return snp

    def read_version(self, file):
        self.version = str(file[0]).lower()
        if self.version == '[version] 2.0\n':
            print('Touchstone File Format Version 2.0')
        else:
            print('Touchstone File Format Version 1.0')
            self.version = '[version] 1.0'
        return self.version

    def read_numbers_of_ports(self, file):
        self.number_of_ports = int(file[2][18])
        return self.number_of_ports

    def read_two_ports_order(self, file, number_of_ports):
        if number_of_ports == 2:
            if len(file[3]) == 28:
                self.two_ports_order = str(file[3][22:27])
                if self.two_ports_order == '12_21' or self.two_ports_order == '21_12':
                    self.two_ports_order = self.two_ports_order
                else:
                    self.two_ports_order = None
            else:
                self.two_ports_order = None
        else:
            self.two_ports_order = None
        return self.two_ports_order

    def read_number_of_frequencies(self, file):
        words = '[NUMBER OF FREQUENCIES]'
        for line in file:
            if line[0:23].upper() == words:
                self.number_of_frequencies = int(line[24:])
                break
            else:
                self.number_of_frequencies = None
        return self.number_of_frequencies

    def read_number_of_noise_frequencies(self, file):
        words = '[NUMBER OF NOISE FREQUENCIES]'
        for line in file:
            if line[0:29].upper() == words:
                self.number_of_noise_frequencies = int(line[30:])
                break
            else:
                self.number_of_noise_frequencies = None
        return self.number_of_noise_frequencies

    def read_reference(self, file):
        words = '[REFERENCE]'
        n = -1
        for line in file:
            n = n + 1
            if line[0:11].upper() == words:
                print(n)
                print(file[n])
                j = 0
                for new_line in file[n:]:
                    j = j + 1
                    if new_line[0] == '[' and new_line[0:11].upper() != words:
                        print(new_line)
        # new_line = ''
        # line = ''
        # words = '[REFERENCE]'
        # n = -1
        # for line in file:
        #     n = n + 1
        #     if line[0:11].upper() == words:
        #         start = n
        #         # print(file[start])
        #         j = 0
        #         for new_line in file[n:]:
        #             j = j + 1
        #             if new_line[0] == '[':
        #                 stop = j + n
        #                 print(file[stop])
        #                 break
                        # print(file[stop])
                # print(stop)
        # for index, line in enumerate(file):
        #     if words in line:
        #         print(index)
        # for line in file:
        #     if str(line[0:11]).upper() == words:
        #         new_line += line
        #     elif line[0] != '[':
        #         new_line += line
        # print(new_line)
        return self.reference




# 's2p_temp.s2p'

a = SnpReader()
# print(a.read_two_ports_order(a.read_file('s2p_temp.s2p'), a.read_numbers_of_ports(a.read_file('s2p_temp.s2p'))))
print(a.read_reference(a.read_file('s2p_temp.s2p')))
