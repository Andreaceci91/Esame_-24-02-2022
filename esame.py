
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):

        try:
            data = open(self.name, 'r')
            data.readline()
        except:
            raise ExamException("Errore nell'apertura del file")

        data_new = []

        for item in data:

            element = item.split(',')
            element[1] = element[1].strip()

            data_new.append(element)

        return data_new


file = CSVTimeSeriesFile('/Users/andrea/Desktop/Esame_24_02_2022/data.csv')

data = file.get_data()

for item in data:
    print(item)


'''
print('**************')

print(data[1][1])
'''