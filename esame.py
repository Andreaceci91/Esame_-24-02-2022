
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name = name


    def get_data(self):

        # Controllo Apertura del file
        try:
            file = open(self.name,'r')
            file.readline()

        except:
            raise ExamException("Errore nell'apertura del file")

        data = []

        for item in file:

            element = item.split(',')

            element[-1] = element[-1].strip()
            
            # Controllo Conversione a intero e non negativo
            try:
                app = element[0].split('-')

                test_int_1 = int(app[0])
                test_int_2 = int(app[1])
                test_int_3 = int(element[1])

                if test_int_1 and test_int_2 and test_int_3 > 0:
                    data.append([element[0], element[1]])

            except:
                #print("Errore nella conversione a intero")
                pass

        file.close()

        if len(data) == 0:
            raise ExamException('Lista vuota')

        for i in range(len(data)-1):
            
            if data[i][0] >= data[i+1][0]:
                raise ExamException("TimeStamp non ordinato o duplicato")

        return data

def detect_similar_monthly_variations(time_series, years):
    
    list_app = []

    for item in time_series:
        app = item[0].split('-')

        list_app.append(int(app[0]))

    # Uso SET, collezione non ordinata e unica di elementi
    list_app = list(set(list_app))

    # Controllo se anni presenti nel dataset
    for item in years:
        if item not in list_app:
            raise ExamException("Anno cercato non presente nel dataset")

    if years[0]+1 != years[1]:
        raise ExamException("Anni forniti non consecutivi")

    listyear0 = []
    listyear1 = []

    for item in time_series:

        year_app = int((item[0].split('-'))[0])
        day_app = int((item[0].split('-'))[1])
        num_app = int(item[1])

        if int(year_app) == years[0]:
            listyear0.append([year_app,day_app,num_app])

        if int(year_app) == years[1]:
            listyear1.append([year_app, day_app, num_app])
    
    diff_list0 = []
    diff_list1 = []

    i = 0
    j = 0

    while i < 10:

        #print(" ")
        #print('i:', i)
        #print('mese corr:', ((listyear0[i][1])), '- mese succ:', listyear0[i+1][1] )
        #print('pass corr:', ((listyear0[i][2])), '- pass succ:', listyear0[i+1][2] )

        if (listyear0[i][1])+1 == (listyear0[i+1][1]):
            #print('Consecutivo')

            app = abs((listyear0[i][2]) -  listyear0[i+1][2])

            diff_list0.append(app)
            i += 1

        else:
            #print(" ")
            #print('Non consecutivo')   
            j = (listyear0[i][1])

            while j != (listyear0[i+1][1]):
                #print("j:", j, '- mese targhet', listyear0[i+1][1])
                #print('Append None')
                diff_list0.append(None)
                j += 1

            i += 1

    print('Lunghezza', len(diff_list0)) 

    for item in diff_list0:
        print(item)
        pass



#==============================
#  Main
#==============================

file = CSVTimeSeriesFile('/Users/andrea/Desktop/Esame_24_02_2022/data.csv')

df = file.get_data()

#for item in df:
#    print(item)

detect_similar_monthly_variations(df,[1949,1950])
