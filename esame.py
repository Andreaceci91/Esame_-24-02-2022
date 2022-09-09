
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

        # Se ho errori nell' apertura dei file alzo eccezione
        except:
            raise ExamException("Errore nell'apertura del file")

        # Inizializzo lista vuota
        data = []

        for item in file:

            element = item.split(',')

            element[-1] = element[-1].strip()
            
            # Controllo Conversione a intero e se i valori sono ammissibili
            try:
                app = element[0].split('-')

                test_int_1 = int(app[0])
                test_int_2 = int(app[1])
                test_int_3 = int(element[1])

                # Se i valori presenti nel file sono ammissibili li aggiungo alla lista creata precedentemente
                if test_int_1 and test_int_2 and test_int_3 > 0 and test_int_1 > 0 and test_int_2 > 0 and test_int_2 <= 12:
                    data.append([element[0], element[1]])

            except:
                pass

        # Chiudo il file
        file.close()

        # Controllo che la lista non sia vuota altrimenti alzo eccezione
        if len(data) == 0:
            raise ExamException('Lista vuota')

        # Controllo che non sono presenti TimeStamp duplicati o non ordinati altrimenti alzo eccezione
        for i in range(len(data)-1):

            data_app_corr = data[i][0].split('-')
            anno_corr = int(data_app_corr[0])
            mese_corr = int(data_app_corr[1])

            data_app_succ = data[i+1][0].split('-')
            anno_succ = int(data_app_succ[0])
            mese_succ = int(data_app_succ[1])
            
            #print("i:",data_app_corr,"- i+1", data_app_succ)

            if anno_corr > anno_succ:
                raise ExamException("TimeStamp non ordinato o duplicato")
            else:
                if anno_corr == anno_succ and mese_corr >= mese_succ:
                    raise ExamException("TimeStamp non ordinato o duplicato")

        # Ritorno la lista 
        return data

# Dichiaro funzione che occorre per calcolare la differenza tra gli anni inseriti dall'utente
def detect_similar_monthly_variations(time_series, years):
    
    # Credo una lista vuota di appoggio
    list_app = []

    # converto a intero anni forniti in caso fossero passati come stringhe
    for i in range(len(years)):
        years[i] = int(years[i])
    
    if (years[0])+1 != years[1]:
        raise ExamException("Anni forniti non consecutivi")

    

    # Splitto elementi presenti nella time_series sul carattere "-"
    for item in time_series:
        app = item[0].split('-')

        # Inserisco gli anni presenti nei dati della time_series nella lista di appoggio
        list_app.append(int(app[0]))

    # Uso SET, collezione non ordinata e unica di elementi
    list_app = list(set(list_app))

    # Controllo se anni presenti nel dataset altrimenti alzo eccezione
    for item in years:
        if item not in list_app:
            raise ExamException("Anno cercato non presente nel dataset")

    # Istanzio due liste vuote per inserire i valori degli anni richiesti dall'utente
    listyear0 = []
    listyear1 = []

    # Itero sulla time_series per estrarre i dati richiesti dall'utente assegnandoli alla lista specifica dedicata
    for item in time_series:

        year_app = int((item[0].split('-'))[0])
        day_app = int((item[0].split('-'))[1])
        num_app = int(item[1])

        if int(year_app) == years[0]:
            listyear0.append([year_app,day_app,num_app])

        if int(year_app) == years[1]:
            listyear1.append([year_app, day_app, num_app])
    
    # Istanzio due liste vuote che conterranno le differenze tra i diversi mesi per i due anni richiesti dall'utente
    diff_list0 = []
    diff_list1 = []

    # Assegno a variabile la lunghezza della lista estratta
    lung = len(listyear0)

    # Creo due variabili per controllare se manca il primo o l'ultimo elementi
    missingfirst = False
    missinglast = False

    # Istanzio indice i
    i = 0

    # Controllo se il primo elemento è diverso da Gennaio
    if listyear0[0][1] != 1:
        missingfirst = True
    #print('***** MissingFirst -->', missingfirst)   

    # Se diverso da Gennaio aggiungo in cima alla lista dei "None" fino ad arrivare al mese con cui inizia l'anno
    if missingfirst == True:
        while i+1 < listyear0[0][1]:
            diff_list0.append(None)
            i += 1
    
    # Reimposto indice i
    i = 0

    #Ciclo per tutta la lunghezza della lista
    while i < lung-1:

        #print(" ")

        # Se aggiungendo 1 al mese corrente raggiungo il mese successivo aggiungo alla lista il valore assoluto della differenza
        #print("mese corr", listyear0[i][1], "mese succ:",listyear0[i+1][1])
        if listyear0[i][1]+1 == listyear0[i+1][1]:

            app = abs(listyear0[i][2] - listyear0[i+1][2])
            diff_list0.append(app)
        
        # Altrimenti aggiungo il valore "None" finchè non raggiungo il successivo elemento della lista
        else:
            #print("Diverso")
            j = listyear0[i][1]

            while j < listyear0[i+1][1]:

                #print("j:", j, "confronto con:",listyear0[i+1][1])

                diff_list0.append(None)

                j += 1

        i += 1

    # Controllo se ultimo elemento mese della lista corrisponde a dicembre

    if listyear0[len(listyear0)-1][1] != 12:
        missinglast = True
    #print('***** MissingLast --> ', missinglast)

    # Se ultimo mese della lista non corrisponde a dicembre aggiungo valore "None" alla lista finchè indice non raggiunge 12
    # completando cosi tutti i confronti 
    if missinglast == True:

        i = listyear0[lung-1][1]
        while i < 12:
            diff_list0.append(None)
            i += 1

    #print(" ")
    #print("Lunghezza lista:", len(diff_list0))
    #for item in diff_list0:
        #print(item)
        

# CONTROLLO VALORI SECONDO ANNO

    lung = len(listyear1)
    #print("lung", lung)

    # Creo due variabili per controllare se manca il primo o l'ultimo elementi
    missingfirst = False
    missinglast = False

    # Istanzio indice i
    i = 0

    # Controllo se il primo elemento è diverso da Gennaio
    if listyear1[0][1] != 1:
        missingfirst = True
    #print('***** MissingFirst -->', missingfirst)   

    # Se diverso da Gennaio aggiungo in cima alla lista dei "None" fino ad arrivare al mese con cui inizia l'anno
    if missingfirst == True:
        while i+1 < listyear1[0][1]:
            diff_list1.append(None)
            i += 1
    
    # Reimposto indice i
    i = 0

    #Ciclo per tutta la lunghezza della lista
    while i < lung-1:

        #print(" ")

        # Se aggiungendo 1 al mese corrente raggiungo il mese successivo aggiungo alla lista il valore assoluto della differenza
        #print("mese corr", listyear1[i][1], "mese succ:",listyear1[i+1][1])
        #print("pass corr", listyear1[i][2], "pass succ:",listyear1[i+1][2])
        if listyear1[i][1]+1 == listyear1[i+1][1]:

            app = abs(listyear1[i][2] - listyear1[i+1][2])
            diff_list1.append(app)
        
        # Altrimenti aggiungo il valore "None" finchè non raggiungo il successivo elemento della lista
        else:
            #print("Diverso")
            j = listyear1[i][1]

            while j < listyear1[i+1][1]:

                #print("j:", j, "confronto con:",listyear1[i+1][1])

                diff_list1.append(None)

                j += 1

        i += 1

    # Controllo se ultimo elemento mese della lista corrisponde a dicembre

    if listyear1[len(listyear1)-1][1] != 12:
        missinglast = True
    #print('***** MissingLast --> ', missinglast)

    # Se ultimo mese della lista non corrisponde a dicembre aggiungo valore "None" alla lista finchè indice non raggiunge 12
    # completando cosi tutti i confronti 
    if missinglast == True:

        i = listyear1[lung-1][1]
        while i < 12:
            diff_list1.append(None)
            i += 1

    #print(" ")
    #print("Lunghezza lista:", len(diff_list1))

    #for item in diff_list1:
    #    print(item)

    # Controllo differenza valori dalle liste di differenza precedemente calcolate
    result = []

    for i in range(len(diff_list0)):

        print(diff_list0[i], '-', diff_list1[i])

        if diff_list0[i] == None or diff_list1[i] == None:
            #print('appendo false')
            result.append(False)
        else:

            #print('ABS:', abs(diff_list0[i] - diff_list1[i]))
            if abs(diff_list0[i] - diff_list1[i]) <= 2:
                result.append(True)
            else:
                result.append(False)
    
    print(" ")
    for item in result:
        print(item)

#==============================
#  Main
#==============================

file = CSVTimeSeriesFile('/Users/andrea/Desktop/Esame_24_02_2022/data.csv')

df = file.get_data()

for item in df:
    print(item)

#detect_similar_monthly_variations(df,['1949','1950'])
