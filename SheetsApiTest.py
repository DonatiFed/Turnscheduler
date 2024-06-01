import gspread
from oauth2client.service_account import ServiceAccountCredentials





def SheetsExport(schedule):
    # Definisci gli scope
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # Carica le credenziali dal file JSON
    creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/federicodonati/Downloads/turnscheduler-21773e70ad4e.json', scope)

    # Autenticazione
    client = gspread.authorize(creds)

    # Apri il foglio di lavoro
    spreadsheet = client.open('ApiTest3')
    sheet = spreadsheet.sheet1  # Seleziona il primo foglio di lavoro

   

    # Ottieni tutti i valori della colonna A
    col_a_values = sheet.col_values(1)

    restSet=False
    for employee in schedule.employees: #Stabilisco nome di chi riposa
            if employee.rests:
                employeeResting=employee.name
                restSet=True
    if not restSet:
        employeeResting=schedule.employees[0].name
        restSet=True

    # Trova l'ultimo valore non vuoto nella colonna A e incrementa di 1
    last_week_number = 0
    for value in reversed(col_a_values):
        if value.isdigit():
            last_week_number = int(value)
            break

    current_week_number = last_week_number + 1

    # Definisci una lista per memorizzare i dati dei turni
    data = []

    # Aggiungi una riga vuota per separare le settimane
    data.append([])

    # Ciclo sui giorni dello schedule
    for day in schedule.days:
        row = [""] * 8
        row = [current_week_number, day.dayname]  # Aggiungi il numero della settimana e il nome del giorno
        if day.employees:
            for employee in day.employees:
                row.append(employee.name)  # Aggiungi il nome dell'impiegato alla riga
        else:
            row.append("No turns assigned")  # Se non ci sono impiegati, aggiungi un messaggio appropriato
            
        # Assicurati che la riga abbia abbastanza celle fino alla colonna F
        while len(row) < 6:
            row.append("")  # Aggiungi celle vuote fino alla colonna F
            
        row.append(employeeResting)  # Aggiungi il nome dell'impiegato con 8 ore in meno nella colonna G
        data.append(row)  # Aggiungi la riga alla lista dei dati
        

    # Scrivi i dati dei turni sul foglio di lavoro
    sheet.append_rows(data)  # Aggiungi i nuovi dati
    print("Output scritto su Google Sheets con successo.")

    




    

