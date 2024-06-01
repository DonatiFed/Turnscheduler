import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
import SheetsApiTest as SAT
import random


class Employee:
    def __init__(self, id, name, totalhours, workedlastweekend=False, rests=False):
        self.id = id
        self.name = name
        self.totalhours = totalhours
        self.remaininghours = totalhours
        self.workedlastweekend = workedlastweekend
        self.rests = rests

    def __str__(self):
        return f"Employee: {self.name}, Hours: {self.remaininghours}"
    
class Day:
    def __init__(self, dayname, daynumber, workinghours, employeesnumber):
        self.dayname = dayname
        self.daynumber = daynumber
        self.workinghours = workinghours
        self.employeesnumber = employeesnumber
        self.employeescurrentnumber = 0
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        employee.remaininghours -= self.workinghours
        if self.dayname in ["Saturday", "Sunday"]:
            employee.workedlastweekend = True
        self.employeescurrentnumber += 1

    def __str__(self):
        return self.dayname
    
class TurnsSchedule:
    def __init__(self, weeknumber, employeesnumber):
        self.weeknumber = weeknumber
        self.employeesnumber = employeesnumber
        self.days = []
        self.employees = []

    def addDay(self, day):
        self.days.append(day)

    def addEmployee(self, employee):
        self.employees.append(employee)
    

    def compareEmployees(self, emp1, emp2):
        return emp1.remaininghours > emp2.remaininghours
    
    #RANDOMIZER
    def randomize_schedule(self):
        # Raggruppa i giorni per numero di impiegati
        days_by_capacity = {}
        for day in self.days:
            capacity = len(day.employees)
            if capacity not in days_by_capacity:
                days_by_capacity[capacity] = []
            days_by_capacity[capacity].append(day)

        # Randomizza la distribuzione degli impiegati per ciascun gruppo di giorni
        for capacity, days in days_by_capacity.items():
            employees_list = [day.employees for day in days]
            random.shuffle(employees_list)
            for day, employees in zip(days, employees_list):
                day.employees = employees

        print("Schedule randomizzata con successo.")

    def MakeSchedule(self): #dopo aver aggiunto giorni e impiegati viene chiamato questo metodo
        for i in range(self.employeesnumber):
            self.employees[i].remaininghours = self.employees[i].totalhours

        for i in range(len(self.days)):
            self.days[i].employeescurrentnumber = 0

        self.employees.sort(key=lambda x: x.remaininghours, reverse=True)
        self.decreasereorder(self.employees)
        self.employees.sort(key=lambda x: x.remaininghours, reverse=True)
        for i in range(len(self.days)-1, -1, -1):
            self.employees.sort(key=lambda x: x.remaininghours, reverse=True)
            count = 0
            print(self.days[i].dayname)
            for j in range(self.employeesnumber):
                if self.employees[j].remaininghours >= 4 and count < self.days[i].employeesnumber:
                    self.days[i].add_employee(self.employees[j])
                    #self.employees[j].remaininghours -= 4
                    lastEmployeeIndex = self.days[i].employeescurrentnumber - 1
                    print(f"Employee: {self.days[i].employees[lastEmployeeIndex].name}, Hours: {self.days[i].employees[lastEmployeeIndex].remaininghours}")
                    count += 1

    def decreasereorder(self, v):
        decreased = False
        i = 0
        # Check for an employee with rests set to True
        while not decreased and i <len(v):
            if v[i].rests:
                v[i].remaininghours -= 8
                print(f"questa settimana {v[i].name} fa 8 ore in meno")
                decreased = True
            else:
                i += 1
        # If no employee with rests set to True was found, reduce 8 hours from the first employee
        i=0
        if not decreased :
            v[i].remaininghours -= 8
            v[i].rests=True
            print(f"nessun impiegato con rests=True trovato, {v[i].name} fa 8 ore in meno")
            decreased = True


class TurnsScheduler(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Turns Scheduler")
        self.initUI()
        

    def initUI(self):
        # Layout principale
        layout = QVBoxLayout()

        #rest_Selected=False #variabile per controllare che un solo impiegato faccia 8 ore in meno

        # Gruppo per l'input
        input_group = QVBoxLayout()

        self.name_label = QLabel("Name:")
        input_group.addWidget(self.name_label)

        self.name_entry = QLineEdit()
        input_group.addWidget(self.name_entry)

        self.hours_label = QLabel("Total Hours:")
        input_group.addWidget(self.hours_label)

        self.hours_entry = QLineEdit()
        input_group.addWidget(self.hours_entry)

        
        self.holiday_check = QCheckBox("Rests")
        input_group.addWidget(self.holiday_check)
            
        
        layout.addLayout(input_group)

        # Pulsante per aggiungere impiegati
        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.add_employee)
        layout.addWidget(self.add_button)

        # Pulsante per aggiungere impiegati predefiniti
        self.add_predefined_button = QPushButton("Add Predefined Employees")
        self.add_predefined_button.clicked.connect(self.add_predefined_employees)
        layout.addWidget(self.add_predefined_button)

        # Lista degli impiegati
        self.employee_list = QListWidget()
        layout.addWidget(self.employee_list)

         # Pulsante per aggiornare un impiegato
        self.update_button = QPushButton("Update Employee")
        self.update_button.clicked.connect(self.update_employee)
        layout.addWidget(self.update_button)

        # Pulsante per rimuovere un impiegato
        self.remove_button = QPushButton("Remove Employee")
        self.remove_button.clicked.connect(self.remove_employee)
        layout.addWidget(self.remove_button)

        # Pulsante per eseguire la pianificazione dei turni
        self.make_schedule_button = QPushButton("Make Schedule")

    
        self.make_schedule_button.clicked.connect(self.make_schedule)
        layout.addWidget(self.make_schedule_button)

        # Widget per visualizzare i turni per ogni giorno
        self.schedule_labels = []
        for dayname in ["Monday afternoon", "Tuesday morning", "Tuesday afternoon", "Wednesday morning", "Wednesday afternoon", "Thursday morning", "Thursday afternoon", "Friday morning", "Friday afternoon", "Saturday morning", "Saturday afternoon", "Sunday morning", "Sunday afternoon"]:
            label = QLabel(f"{dayname}:")
            self.schedule_labels.append(label)
            layout.addWidget(label)

        self.setLayout(layout)

        self.employees = []
        self.rest_selected = False #variabile usata per far riposare solo un impiegato

     #CHECK IF REST SELECTED
    def RestAlreadySelected(self):
        self.rest_selected = False  # Reset the rest_selected flag
        for employee in self.employees:
            if employee.rests:
                self.rest_selected = True
                self.holiday_check.setEnabled(False)
                return
        self.holiday_check.setEnabled(True)


    def add_employee(self):
        name = self.name_entry.text().strip()
        total_hours_str = self.hours_entry.text().strip()

        # Controllo sull'input
        if not name:
            QMessageBox.warning(self, "Input Error", "Name cannot be empty")
            return

        try:
            total_hours = int(total_hours_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Total Hours must be a number")
            return

        rests = self.holiday_check.isChecked()
        if rests and self.rest_selected:
            QMessageBox.warning(self, "Input Error", "Only one employee can have rest")
            return
        employee = Employee(id=len(self.employees)+1, name=name, totalhours=total_hours, rests=rests)
        self.employees.append(employee)

        self.employee_list.addItem(str(employee))

        # Pulizia dei campi di input
        self.name_entry.clear()
        self.hours_entry.clear()
        self.holiday_check.setChecked(False)
        self.RestAlreadySelected()


   


#ADD DEFAULT EMPLOYEES LIST
    def add_predefined_employees(self):
        predefined_employees = [ 
            {"name": "Marzia", "totalhours": 40, "rests": False},
            {"name": "Monica", "totalhours": 24, "rests": False},
            {"name": "Francesca", "totalhours": 24, "rests": False},
            {"name": "Angela", "totalhours": 28, "rests": False},
            {"name": "Sara", "totalhours": 20, "rests": False},
            {"name": "Laura", "totalhours": 20, "rests": False}
        ]

        for emp_data in predefined_employees:
            employee = Employee(id=len(self.employees) + 1, name=emp_data["name"], totalhours=emp_data["totalhours"], rests=emp_data["rests"])
            self.employees.append(employee)
            self.employee_list.addItem(str(employee))
            if emp_data["rests"]:
                self.rest_selected = True

        self.RestAlreadySelected()

    
    # METODI PER MODIFICARE EMPLOYEES
    def load_employee_details(self):
        selected_items = self.employee_list.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        selected_employee_str = selected_item.text()
        name, hours = selected_employee_str.split(", ")
        name = name.split(": ")[1]
        hours = int(hours.split(": ")[1])

        selected_employee = next((emp for emp in self.employees if emp.name == name and emp.totalhours == hours), None)
        if not selected_employee:
            return

        self.name_entry.setText(selected_employee.name)
        self.hours_entry.setText(str(selected_employee.totalhours))
        self.holiday_check.setChecked(selected_employee.rests)

    def update_employee(self):
        selected_items = self.employee_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "No employee selected")
            return

        name = self.name_entry.text().strip()
        total_hours_str = self.hours_entry.text().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Name cannot be empty")
            return

        try:
            total_hours = int(total_hours_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Total Hours must be a number")
            return

        rests = self.holiday_check.isChecked()

        selected_item = selected_items[0]
        selected_employee_str = selected_item.text()
        old_name, old_hours = selected_employee_str.split(", ")
        old_name = old_name.split(": ")[1]
        old_hours = int(old_hours.split(": ")[1])

       

        selected_employee = next((emp for emp in self.employees if emp.name == old_name and emp.totalhours == old_hours), None)
        if not selected_employee:
            return


        selected_employee.name = name
        selected_employee.totalhours = total_hours
        selected_employee.rests = rests

        selected_item.setText(f"Employee: {name}, Hours: {total_hours}")

        self.RestAlreadySelected()


    def remove_employee(self):
        selected_items = self.employee_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "No employee selected")
            return

        selected_item = selected_items[0]
        selected_employee_str = selected_item.text()
        name, hours = selected_employee_str.split(", ")
        name = name.split(": ")[1]
        hours = int(hours.split(": ")[1])

        selected_employee = next((emp for emp in self.employees if emp.name == name and emp.totalhours == hours), None)
        if not selected_employee:
            return

        if selected_employee.rests:
            self.rest_selected = False
            self.holiday_check.setEnabled(True)

        self.employees.remove(selected_employee)
        self.employee_list.takeItem(self.employee_list.row(selected_item))
        self.RestAlreadySelected()

    

# MAKE SCHEDULE
    def make_schedule(self): #viene chiamato questo metodo quando viene premuto il pulsante makeschedule
        if not self.employees:
            QMessageBox.warning(self, "Input Error", "Add at least one employee to make schedule")
            return

        weeknumber = 0
        schedule = TurnsSchedule(weeknumber, len(self.employees))
        Mondaypm=Day("Monday afternoon", 0, 4, 3);
        Tuesdayam=Day("Tuesday morning", 1, 4, 2);
        Tuesdaypm=Day("Tuesday afternoon", 1, 4, 3);

        Wednesdayam=Day("Wednesday morning", 2, 4, 2);
        Wednesdaypm=Day("Wednesday afternoon", 2, 4, 3);

        Thursdayam=Day("Thursday morning", 3, 4, 2);
        Thursdaypm=Day("Thursday afternoon", 3, 4, 3);

        Fridayam=Day("Friday morning", 4, 4, 2);
        Fridaypm=Day("Friday afternoon", 4, 4, 3);

        Saturdayam=Day("Saturday morning", 5, 4, 3);
        Saturdaypm=Day("Saturday afternoon", 5, 4, 4);

        Sundayam=Day("Sunday morning", 6, 4, 3);
        Sundaypm=Day("Sunday afternoon", 6, 4, 4);

        schedule.addDay(Mondaypm);
        schedule.addDay(Tuesdayam);
        schedule.addDay(Tuesdaypm);
        schedule.addDay(Wednesdayam);
        schedule.addDay(Wednesdaypm);
        schedule.addDay(Thursdayam);
        schedule.addDay(Thursdaypm);
        schedule.addDay(Fridayam);
        schedule.addDay(Fridaypm);
        schedule.addDay(Saturdayam);
        schedule.addDay(Saturdaypm);
        schedule.addDay(Sundayam);
        schedule.addDay(Sundaypm);


        for i in range(self.employee_list.count()):
            employee_str = self.employee_list.item(i).text()
            name, hours = employee_str.split(", ")
            name = name.split(": ")[1]
            hours = int(hours.split(": ")[1])
            rests = any(employee.name == name and employee.rests for employee in self.employees)
            employee = Employee(id=i+1, name=name, totalhours=hours, rests=rests)
            schedule.addEmployee(employee)

        schedule.MakeSchedule() #MAKE THE SCHEDULE
        schedule.randomize_schedule()  #RANDOMIZE THE SCHEDULE

        # Aggiornamento dell'interfaccia utente con i turni assegnati per ogni giorno
        for i, day in enumerate(schedule.days):
            if day.employees:
                # Concatenazione dei nomi degli impiegati e delle ore rimanenti
                turns_str = ", ".join([f"{employee.name} " for employee in day.employees])
                self.schedule_labels[i].setText(f"{day.dayname}: {turns_str}")
            else:
                # Se non ci sono impiegati assegnati, mostrare un messaggio appropriato
                self.schedule_labels[i].setText(f"{day.dayname}: No turns assigned")

        #Generiamo su google sheets

        SAT.SheetsExport(schedule)

        self.RestAlreadySelected()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TurnsScheduler()
    window.show()
    sys.exit(app.exec_())
