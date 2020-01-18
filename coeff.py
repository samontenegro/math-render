from os import path
import csv

class GenericCoefficientArray:

    def __init__(self, FILENAME):
        self.__filename = FILENAME
        self.__coeff_array = [0]

        self.generate_array()

    def coeff(self, i):
        try:
            _value = self.__coeff_array[i]
        except IndexError:
            return 0
        else:
            return _value
    
    def generate_array(self):

        if not path.isfile(self.__filename):
            print("GenericCoeffArray: Warning - file not found, using default array")
        else:
            with open(self.__filename) as file:
                print("GenericCoefficientArray: Loading .csv file")
                _reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
                for row in _reader:
                    for value in row:
                        self.__coeff_array.append(value)

if __name__ == "__main__":
    pass
