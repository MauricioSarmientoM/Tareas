from tkinter import Tk, Label, Entry, Button, Menu, StringVar, IntVar, Event
from tkinter.ttk import Frame, Combobox, Treeview
from tkinter.messagebox import showerror, showwarning, askquestion
from hospital import Hospital, RUT, Specialty, Area, AFP, Prevision, Unit, Derivation, Medic, Administrative, Patient
from db import DB, OrderBy
from enum import Enum
from datetime import date
class AdminUIState(Enum):
    Insert = 0
    Select = 1
    Delete = 2
    Update = 3
class WindowUIState(Enum):
    Medic = 0
    Admin = 1
    Patient = 2
class UI(Frame):
    def __init__(self, hospital : Hospital, db : DB) -> None:
        self.window = Tk()
        self.name = hospital.name
        self.window.geometry("800x600")
        super().__init__(self.window)
        self.hospital = hospital
        self.db = db
        self.vars = {}
        self.items = {}
        self.menu = {}
        self.adminUiState = AdminUIState.Insert
        self.windowUiState = WindowUIState.Medic
        #See if db has what it needs
        try:
            data = self.db.Select(table = 'person',
                            fetch = -1,
                            where = f'occupation = 1')
            for i in data:
                self.hospital.workers.append(Medic(RUT(i[0]), name = i[1], admission = i[2], prevision = Prevision(i[3]), afp = AFP(i[4]), salary = i[5], specialty = Specialty(i[6]), area = Area(i[7])))
            data = self.db.Select(table = 'person',
                            fetch = -1,
                            where = f'occupation = 2')
            for i in data:
                self.hospital.workers.append(Medic(RUT(i[0]), name = i[1], admission = i[2], prevision = Prevision(i[3]), afp = AFP(i[4]), salary = i[5], specialty = Specialty(i[6]), area = Area(i[7])))
        except Exception as e:
            showerror('Error', message = e)
    def Login(self):
        self.vars = {}
        self.items = {}
        self.vars['name'] = StringVar()
        self.vars['rut'] = StringVar()
        self.items['name'] = Label(text = self.hospital.name)
        self.items['name'].place(x = 40, y = 100)
        self.items['rut'] = Entry(textvariable = '', width = 30)
        self.items['rut'].place(x = 75, y = 240)
        return self
    def Base(self):
        #Estableshing brand new page
        self.vars = {}
        self.items = {}
        self.menu = {}
        #Setting upper stuff
        self.menu['topbar'] = Menu(self.window)
        #self.menu['files'] = Menu(self.menu['topbar'], tearoff = 0)
        self.menu['settings'] = Menu(self.menu['topbar'], tearoff = 1)
        self.menu['settings'].add_command(label = 'Change to Medic/TENS', command = self.WindowStateMedic)
        self.menu['settings'].add_command(label = 'Change to Administration', command = self.WindowStateAdmin)
        self.menu['settings'].add_command(label = 'Change to Patients', command = self.WindowStatePatient)
        self.menu['settings'].add_separator()
        self.menu['settings'].add_command(label = 'Change to Insert Mode', command = self.AdminStateInsert)
        self.menu['settings'].add_command(label = 'Change to Select Mode', command = self.AdminStateSelect)
        self.menu['settings'].add_command(label = 'Change to Update Mode', command = self.AdminStateUpdate)
        self.menu['settings'].add_command(label = 'Change to Delete Mode', command = self.AdminStateDelete)
        self.menu['inputs'] = Menu(self.menu['topbar'], tearoff = 2)
        self.menu['inputs'].add_command(label = 'Clear Inputs', command = self.ClearVars)
        #self.menu['topbar'].add_cascade(label = 'File', menu = self.menu['files'])
        self.menu['topbar'].add_cascade(label = 'Settings', menu = self.menu['settings'])
        self.menu['topbar'].add_cascade(label = 'Input', menu = self.menu['inputs'])
        self.window.config(menu = self.menu['topbar'])
        if self.windowUiState == WindowUIState.Medic: self.AdminMedics()
        if self.windowUiState == WindowUIState.Admin: self.AdminAdmin()
        if self.windowUiState == WindowUIState.Patient: self.AdminPatient()
        return self
    def AdminMedics(self):
        #Setting variables
        self.vars['name'] = StringVar()
        self.vars['rut'] = StringVar()
        self.vars['year'] = IntVar()
        self.vars['month'] = IntVar()
        self.vars['day'] = IntVar()
        self.vars['salary'] = IntVar()
        self.vars['search'] = StringVar()
        #Setting visible stuff
        self.items['medicTable'] = Treeview(self.window, height = 27, columns = ['#0', '#1'])
        self.items['medicTable'].place(x = 300, y = 10)
        self.items['medicTable'].column('#0', width = 10)
        self.items['medicTable'].heading('#0', text = 'N', anchor = 'center')
        self.items['medicTable'].column('#1', width = 150)
        self.items['medicTable'].heading('#1', text = 'RUT', anchor = 'center')
        self.items['medicTable'].column('#2', width = 320)
        self.items['medicTable'].heading('#2', text = 'Name', anchor = 'center')
        self.items['medicTable'].bind('<Double-1>', self.SelectUpdateMedicTable)
        try:
            data = self.db.Select(table = 'person',
                            column = 'rut name',
                            fetch = -1,
                            where = 'occupation = 1')
            if data is not None:
                for i in data:
                    self.items['medicTable'].insert('', 0, values = i)
        except Exception as e:
            showerror(e)
        #Specific stuff
        if self.adminUiState != AdminUIState.Delete or self.adminUiState != AdminUIState.Select:
            self.SetGenericItems()
            self.items['salaryLabel'] = Label(self.window, text = 'Salary')
            self.items['salaryEntry'] = Entry(self.window, textvariable = self.vars['salary'], width = 30)
            self.items['specialtyLabel'] = Label(self.window, text = 'Specialty')
            self.items['specialtyCombobox'] = Combobox(self.window, state = 'readonly', values = ['Pediatrics', 'Anesteology', 'Cardiology', 'Gastroenterology', 'General', 'Gynecology', 'Obstetrics'])
            self.items['areaLabel'] = Label(self.window, text = 'Area')
            self.items['areaCombobox'] = Combobox(self.window, state = 'readonly', values = ['Null', 'Extern', 'Emergency', 'Pediatrics', 'Operating', 'Hospitalization', 'ICU'])
        if self.adminUiState == AdminUIState.Insert:
            self.items['nameLabel'].place(x = 10, y = 10)
            self.items['nameEntry'].place(x = 10, y = 30)
            self.items['rutLabel'].place(x = 10, y = 60)
            self.items['rutEntry'].place(x = 10, y = 80)
            self.items['dateLabel'].place(x = 10, y = 110)
            self.items['yearLabel'].place(x = 10, y = 130)
            self.items['yearEntry'].place(x = 10, y = 150)
            self.items['monthLabel'].place(x = 100, y = 130)
            self.items['monthEntry'].place(x = 100, y = 150)
            self.items['dayLabel'].place(x = 190, y = 130)
            self.items['dayEntry'].place(x = 190, y = 150)
            self.items['previsionLabel'].place(x = 10, y = 180)
            self.items['previsionCombobox'].place(x = 10, y = 200)
            self.items['previsionCombobox'].current(0)
            self.items['salaryLabel'].place(x = 10, y = 230)
            self.items['salaryEntry'].place(x = 10, y = 250)
            self.items['afpLabel'].place(x = 10, y = 280)
            self.items['afpCombobox'].place(x = 10, y = 300)
            self.items['afpCombobox'].current(0)
            self.items['specialtyLabel'].place(x = 10, y = 330)
            self.items['specialtyCombobox'].place(x = 10, y = 350)
            self.items['specialtyCombobox'].current(0)
            self.items['areaLabel'].place(x = 10, y = 380)
            self.items['areaCombobox'].place(x = 10, y = 400)
            self.items['areaCombobox'].current(0)
            self.items['insertButton'] = Button(self.window, text = 'Insert', command = self.InsertMedicTable, width = 30)
            self.items['insertButton'].place(x = 10, y = 540)
        elif self.adminUiState == AdminUIState.Update:
            self.items['searchLabel'] = Label(self.window, text = 'Search by RUT')
            self.items['searchLabel'].place(x = 10, y = 10)
            self.items['searchEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
            self.items['searchEntry'].place(x = 10, y = 30)
            self.items['nameLabel'].place(x = 10, y = 100)
            self.items['nameEntry'].place(x = 10, y = 130)
            self.items['rutLabel'].place(x = 10, y = 160)
            self.items['rutEntry'].place(x = 10, y = 180)
            self.items['dateLabel'].place(x = 10, y = 210)
            self.items['yearLabel'].place(x = 10, y = 230)
            self.items['yearEntry'].place(x = 10, y = 250)
            self.items['monthLabel'].place(x = 100, y = 230)
            self.items['monthEntry'].place(x = 100, y = 250)
            self.items['dayLabel'].place(x = 190, y = 230)
            self.items['dayEntry'].place(x = 190, y = 250)
            self.items['previsionLabel'].place(x = 10, y = 280)
            self.items['previsionCombobox'].place(x = 10, y = 300)
            self.items['previsionCombobox'].current(0)
            self.items['salaryLabel'].place(x = 10, y = 330)
            self.items['salaryEntry'].place(x = 10, y = 350)
            self.items['afpLabel'].place(x = 10, y = 380)
            self.items['afpCombobox'].place(x = 10, y = 400)
            self.items['afpCombobox'].current(0)
            self.items['specialtyLabel'].place(x = 10, y = 430)
            self.items['specialtyCombobox'].place(x = 10, y = 450)
            self.items['specialtyCombobox'].current(0)
            self.items['areaLabel'].place(x = 10, y = 480)
            self.items['areaCombobox'].place(x = 10, y = 500)
            self.items['areaCombobox'].current(0)
            self.items['updateButton'] = Button(self.window, text = 'Update', command = self.UpdateMedicTable, width = 30)
            self.items['updateButton'].place(x = 10, y = 540)
        elif self.adminUiState == AdminUIState.Delete:
            self.items['searchLabel'] = Label(self.window, text = 'Search by RUT')
            self.items['searchLabel'].place(x = 10, y = 10)
            self.items['searchEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
            self.items['searchEntry'].place(x = 10, y = 30)
            self.items['deleteButton'] = Button(self.window, text = 'Delete', command = self.AskIfDelete, width = 30)
            self.items['deleteButton'].place(x = 10, y = 540)
        return self
    def AdminAdmin(self):
        #Setting variables
        self.vars['name'] = StringVar()
        self.vars['rut'] = StringVar()
        self.vars['year'] = IntVar()
        self.vars['month'] = IntVar()
        self.vars['day'] = IntVar()
        self.vars['salary'] = IntVar()
        self.vars['search'] = StringVar()
        #Setting visible stuff
        self.items['adminTable'] = Treeview(self.window, height = 27, columns = ['#0', '#1'])
        self.items['adminTable'].place(x = 300, y = 10)
        self.items['adminTable'].column('#0', width = 10)
        self.items['adminTable'].heading('#0', text = 'N', anchor = 'center')
        self.items['adminTable'].column('#1', width = 150)
        self.items['adminTable'].heading('#1', text = 'RUT', anchor = 'center')
        self.items['adminTable'].column('#2', width = 320)
        self.items['adminTable'].heading('#2', text = 'Name', anchor = 'center')
        self.items['adminTable'].bind('<Double-1>', self.SelectUpdateAdminTable)
        try:
            data = self.db.Select(table = 'person',
                            column = 'rut name',
                            fetch = -1,
                            where = 'occupation = 2')
            if data is not None:
                for i in data:
                    self.items['adminTable'].insert('', 0, values = i)
        except Exception as e:
            showerror(e)
        #Specific stuff
        if self.adminUiState != AdminUIState.Delete or self.adminUiState != AdminUIState.Select:
            self.SetGenericItems()
            self.items['salaryLabel'] = Label(self.window, text = 'Salary')
            self.items['salaryEntry'] = Entry(self.window, textvariable = self.vars['salary'], width = 30)
            self.items['unitLabel'] = Label(self.window, text = 'Administrative Unit')
            self.items['unitCombobox'] = Combobox(self.window, state = 'readonly', values = ['General', 'Personal', 'Chief'])
        if self.adminUiState == AdminUIState.Insert:
            self.items['nameLabel'].place(x = 10, y = 10)
            self.items['nameEntry'].place(x = 10, y = 30)
            self.items['rutLabel'].place(x = 10, y = 60)
            self.items['rutEntry'].place(x = 10, y = 80)
            self.items['dateLabel'].place(x = 10, y = 110)
            self.items['yearLabel'].place(x = 10, y = 130)
            self.items['yearEntry'].place(x = 10, y = 150)
            self.items['monthLabel'].place(x = 100, y = 130)
            self.items['monthEntry'].place(x = 100, y = 150)
            self.items['dayLabel'].place(x = 190, y = 130)
            self.items['dayEntry'].place(x = 190, y = 150)
            self.items['previsionLabel'].place(x = 10, y = 180)
            self.items['previsionCombobox'].place(x = 10, y = 200)
            self.items['previsionCombobox'].current(0)
            self.items['salaryLabel'].place(x = 10, y = 230)
            self.items['salaryEntry'].place(x = 10, y = 250)
            self.items['afpLabel'].place(x = 10, y = 280)
            self.items['afpCombobox'].place(x = 10, y = 300)
            self.items['afpCombobox'].current(0)
            self.items['unitLabel'].place(x = 10, y = 330)
            self.items['unitCombobox'].place(x = 10, y = 350)
            self.items['unitCombobox'].current(0)
            self.items['insertButton'] = Button(self.window, text = 'Insert', command = self.InsertAdminTable, width = 30)
            self.items['insertButton'].place(x = 10, y = 540)
        elif self.adminUiState == AdminUIState.Update:
            self.items['searchLabel'] = Label(self.window, text = 'Search by RUT')
            self.items['searchLabel'].place(x = 10, y = 10)
            self.items['searchEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
            self.items['searchEntry'].place(x = 10, y = 30)
            self.items['nameLabel'].place(x = 10, y = 100)
            self.items['nameEntry'].place(x = 10, y = 130)
            self.items['rutLabel'].place(x = 10, y = 160)
            self.items['rutEntry'].place(x = 10, y = 180)
            self.items['dateLabel'].place(x = 10, y = 210)
            self.items['yearLabel'].place(x = 10, y = 230)
            self.items['yearEntry'].place(x = 10, y = 250)
            self.items['monthLabel'].place(x = 100, y = 230)
            self.items['monthEntry'].place(x = 100, y = 250)
            self.items['dayLabel'].place(x = 190, y = 230)
            self.items['dayEntry'].place(x = 190, y = 250)
            self.items['previsionLabel'].place(x = 10, y = 280)
            self.items['previsionCombobox'].place(x = 10, y = 300)
            self.items['previsionCombobox'].current(0)
            self.items['salaryLabel'].place(x = 10, y = 330)
            self.items['salaryEntry'].place(x = 10, y = 350)
            self.items['afpLabel'].place(x = 10, y = 380)
            self.items['afpCombobox'].place(x = 10, y = 400)
            self.items['afpCombobox'].current(0)
            self.items['unitLabel'].place(x = 10, y = 430)
            self.items['unitCombobox'].place(x = 10, y = 450)
            self.items['unitCombobox'].current(0)
            self.items['updateButton'] = Button(self.window, text = 'Update', command = self.UpdateAdminTable, width = 30)
            self.items['updateButton'].place(x = 10, y = 540)
        elif self.adminUiState == AdminUIState.Delete:
            self.items['searchLabel'] = Label(self.window, text = 'Search by RUT')
            self.items['searchLabel'].place(x = 10, y = 10)
            self.items['searchEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
            self.items['searchEntry'].place(x = 10, y = 30)
            self.items['deleteButton'] = Button(self.window, text = 'Delete', command = self.AskIfDelete, width = 30)
            self.items['deleteButton'].place(x = 10, y = 540)
        return self
    def AdminPatient(self):
        #Setting variables
        self.vars['name'] = StringVar()
        self.vars['rut'] = StringVar()
        self.vars['year'] = IntVar()
        self.vars['month'] = IntVar()
        self.vars['day'] = IntVar()
        self.vars['reason'] = StringVar()
        self.vars['search'] = StringVar()
        #Setting visible stuff
        self.items['patientTable'] = Treeview(self.window, height = 27, columns = ['#0', '#1'])
        self.items['patientTable'].place(x = 300, y = 10)
        self.items['patientTable'].column('#0', width = 10)
        self.items['patientTable'].heading('#0', text = 'N', anchor = 'center')
        self.items['patientTable'].column('#1', width = 150)
        self.items['patientTable'].heading('#1', text = 'RUT', anchor = 'center')
        self.items['patientTable'].column('#2', width = 320)
        self.items['patientTable'].heading('#2', text = 'Name', anchor = 'center')
        self.items['patientTable'].bind('<Double-1>', self.SelectUpdatePatientTable)
        try:
            data = self.db.Select(table = 'person',
                            column = 'rut name',
                            fetch = -1,
                            where = 'occupation = 3')
            if data is not None:
                for i in data:
                    self.items['patientTable'].insert('', 0, values = i)
        except Exception as e:
            showerror(e)
        #Specific stuff
        if self.adminUiState != AdminUIState.Delete or self.adminUiState != AdminUIState.Select:
            self.SetGenericItems()
        if self.adminUiState == AdminUIState.Insert:
            self.items['nameLabel'].place(x = 10, y = 10)
            self.items['nameEntry'].place(x = 10, y = 30)
            self.items['rutLabel'].place(x = 10, y = 60)
            self.items['rutEntry'].place(x = 10, y = 80)
            self.items['dateLabel'].place(x = 10, y = 110)
            self.items['yearLabel'].place(x = 10, y = 130)
            self.items['yearEntry'].place(x = 10, y = 150)
            self.items['monthLabel'].place(x = 100, y = 130)
            self.items['monthEntry'].place(x = 100, y = 150)
            self.items['dayLabel'].place(x = 190, y = 130)
            self.items['dayEntry'].place(x = 190, y = 150)
            self.items['previsionLabel'].place(x = 10, y = 180)
            self.items['previsionCombobox'].place(x = 10, y = 200)
            self.items['previsionCombobox'].current(0)
            self.items['afpLabel'].place(x = 10, y = 230)
            self.items['afpCombobox'].place(x = 10, y = 250)
            self.items['afpCombobox'].current(0)
            self.items['reasonLabel'].place(x = 10, y = 280)
            self.items['reasonEntry'].place(x = 10, y = 300)
            self.items['derivationLabel'].place(x = 10, y = 330)
            self.items['derivationCombobox'].place(x = 10, y = 350)
            self.items['derivationCombobox'].current(0)
            self.items['insertButton'] = Button(self.window, text = 'Insert', command = self.InsertPatientTable, width = 30)
            self.items['insertButton'].place(x = 10, y = 540)
        elif self.adminUiState == AdminUIState.Update:
            self.items['searchLabel'] = Label(self.window, text = 'Search by RUT')
            self.items['searchLabel'].place(x = 10, y = 10)
            self.items['searchEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
            self.items['searchEntry'].place(x = 10, y = 30)
            self.items['nameLabel'].place(x = 10, y = 100)
            self.items['nameEntry'].place(x = 10, y = 130)
            self.items['rutLabel'].place(x = 10, y = 160)
            self.items['rutEntry'].place(x = 10, y = 180)
            self.items['dateLabel'].place(x = 10, y = 210)
            self.items['yearLabel'].place(x = 10, y = 230)
            self.items['yearEntry'].place(x = 10, y = 250)
            self.items['monthLabel'].place(x = 100, y = 230)
            self.items['monthEntry'].place(x = 100, y = 250)
            self.items['dayLabel'].place(x = 190, y = 230)
            self.items['dayEntry'].place(x = 190, y = 250)
            self.items['previsionLabel'].place(x = 10, y = 280)
            self.items['previsionCombobox'].place(x = 10, y = 300)
            self.items['previsionCombobox'].current(0)
            self.items['afpLabel'].place(x = 10, y = 330)
            self.items['afpCombobox'].place(x = 10, y = 350)
            self.items['afpCombobox'].current(0)
            self.items['reasonLabel'].place(x = 10, y = 380)
            self.items['reasonEntry'].place(x = 10, y = 400)
            self.items['derivationLabel'].place(x = 10, y = 430)
            self.items['derivationCombobox'].place(x = 10, y = 450)
            self.items['derivationCombobox'].current(0)
            self.items['updateButton'] = Button(self.window, text = 'Update', command = self.UpdatePatientTable, width = 30)
            self.items['updateButton'].place(x = 10, y = 540)
        elif self.adminUiState == AdminUIState.Delete:
            self.items['searchLabel'] = Label(self.window, text = 'Search by RUT')
            self.items['searchLabel'].place(x = 10, y = 10)
            self.items['searchEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
            self.items['searchEntry'].place(x = 10, y = 30)
            self.items['deleteButton'] = Button(self.window, text = 'Delete', command = self.AskIfDelete, width = 30)
            self.items['deleteButton'].place(x = 10, y = 540)
        return self
    def SetGenericItems(self):
        self.items['nameLabel'] = Label(self.window, text = 'Name')
        self.items['nameEntry'] = Entry(self.window, textvariable = self.vars['name'], width = 30)
        self.items['rutLabel'] = Label(self.window, text = 'RUT')
        self.items['rutEntry'] = Entry(self.window, textvariable = self.vars['rut'], width = 30)
        self.items['dateLabel'] = Label(text = 'Admission Date')
        self.items['yearLabel'] = Label(text = 'Year')
        self.items['yearEntry'] = Entry(self.window, textvariable = self.vars['year'], width = 8)
        self.items['monthLabel'] = Label(text = 'Month')
        self.items['monthEntry'] = Entry(self.window, textvariable = self.vars['month'], width = 8)
        self.items['dayLabel'] = Label(text = 'Day')
        self.items['dayEntry'] = Entry(self.window, textvariable = self.vars['day'], width = 8)
        self.items['previsionLabel'] = Label(self.window, text = 'Prevision')
        self.items['previsionCombobox'] = Combobox(self.window, state = 'readonly', values = ['FONASA', 'ISAPRE', 'Particular'])
        self.items['afpLabel'] = Label(self.window, text = 'AFP')
        self.items['afpCombobox'] = Combobox(self.window, state = 'readonly', values = ['Capital', 'Cuprum', 'Habitat', 'Modelo', 'Planvital', 'Provida', 'Uno'])
    def ClearItems(self):
        for i in self.items.values():
            i.destroy()
        self.items.clear()
        self.Base()
    def ClearVars(self):
        for i in self.vars.values():
            i.set('')
    def WindowStateMedic(self):
        self.windowUiState = WindowUIState.Medic
        self.ClearItems()
    def WindowStateAdmin(self):
        self.windowUiState = WindowUIState.Admin
        self.ClearItems()
    def WindowStatePatient(self):
        self.windowUiState = WindowUIState.Patient
        self.ClearItems()
    def AdminStateInsert(self):
        self.adminUiState = AdminUIState.Insert
        self.ClearItems()
    def AdminStateDelete(self):
        self.adminUiState = AdminUIState.Delete
        self.ClearItems()
    def AdminStateSelect(self):
        self.adminUiState = AdminUIState.Select
        self.ClearItems()
    def AdminStateUpdate(self):
        self.adminUiState = AdminUIState.Update
        self.ClearItems()
    def SelectUpdateMedicTable(self, event : Event):
        try:
            item = self.items['medicTable'].identify('item', event.x, event.y)
            rut = int(self.items['medicTable'].item(item, 'values')[0])
            data = self.db.Select(table = 'person', fetch = 1, where = f'occupation = 1 AND rut = {rut}')
            self.vars['search'].set(RUT(data[0]).__str__())
            self.vars['rut'].set(RUT(data[0]).__str__())
            self.vars['name'].set(data[1])
            self.vars['year'].set(data[2].year)
            self.vars['month'].set(data[2].month)
            self.vars['day'].set(data[2].day)
            self.items['previsionCombobox'].set(data[3])
            self.items['afpCombobox'].set(data[4])
            self.vars['salary'].set(data[5])
            self.items['specialtyCombobox'].set(data[6])
            self.items['areaCombobox'].set(data[7])
        except:
            pass
    def SelectUpdateAdminTable(self, event : Event):
        try:
            item = self.items['adminTable'].identify('item', event.x, event.y)
            rut = int(self.items['adminTable'].item(item, 'values')[0])
            data = self.db.Select(table = 'person', fetch = 1, where = f'occupation = 2 AND rut = {rut}')
            self.vars['search'].set(RUT(data[0]).__str__())
            self.vars['rut'].set(RUT(data[0]).__str__())
            self.vars['name'].set(data[1])
            self.vars['year'].set(data[2].year)
            self.vars['month'].set(data[2].month)
            self.vars['day'].set(data[2].day)
            self.items['previsionCombobox'].set(data[3])
            self.items['afpCombobox'].set(data[4])
            self.vars['salary'].set(data[5])
            self.items['unitCombobox'].set(data[8])
        except:
            pass
    def SelectUpdatePatientTable(self, event : Event):
        try:
            item = self.items['patientTable'].identify('item', event.x, event.y)
            rut = int(self.items['patientTable'].item(item, 'values')[0])
            data = self.db.Select(table = 'person', fetch = 1, where = f'occupation = 3 AND rut = {rut}')
            self.vars['search'].set(RUT(data[0]).__str__())
            self.vars['rut'].set(RUT(data[0]).__str__())
            self.vars['name'].set(data[1])
            self.vars['year'].set(data[2].year)
            self.vars['month'].set(data[2].month)
            self.vars['day'].set(data[2].day)
            self.items['previsionCombobox'].set(data[3])
            self.items['afpCombobox'].set(data[4])
            self.vars['reason'].set(data[9])
            self.items['derivationCombobox'].set(data[10])
        except:
            pass
    def InsertMedicTable(self):
        try:
            if RUT.ValidateRut(str(self.vars['rut'].get())):
                medic = Medic(name = self.vars['name'].get(), rut = RUT(int(''.join(str(self.vars['rut'].get()).split('-')[0].split('.')))), admission = date(self.vars['year'].get(), self.vars['month'].get(), self.vars['day'].get()), afp = AFP.Validate(self.items['afpCombobox'].get()), area = Area.Validate(self.items['areaCombobox'].get()), prevision = Prevision.Validate(self.items['previsionCombobox'].get()), salary = self.vars['salary'].get(), specialty = Specialty.Validate(self.items['specialtyCombobox'].get()))
                self.hospital.workers.append(medic)
                self.db.InsertTable(table = 'person', column = 'rut name admission prevision afp salary specialty area occupation', values = [medic.rut.rut, medic.name, medic.admission.__str__(), medic.prevision.value, medic.afp.value, medic.salary, medic.specialty.value, medic.area.value, 1])
                self.ClearItems()
        except Exception as e:
            showwarning('Error', message = e)
    def InsertAdminTable(self):
        try:
            if RUT.ValidateRut(str(self.vars['rut'].get())):
                admin = Administrative(name = self.vars['name'].get(), rut = RUT(int(''.join(str(self.vars['rut'].get()).split('-')[0].split('.')))), admission = date(self.vars['year'].get(), self.vars['month'].get(), self.vars['day'].get()), afp = AFP.Validate(self.items['afpCombobox'].get()), area = Area.Validate(self.items['areaCombobox'].get()), prevision = Prevision.Validate(self.items['previsionCombobox'].get()), salary = self.vars['salary'].get(), unit = Unit.Validate(self.items['unitCombobox'].get()))
                self.hospital.workers.append(admin)
                self.db.InsertTable(table = 'person', column = 'rut name admission prevision afp salary unit occupation', values = [admin.rut.rut, admin.name, admin.admission.__str__(), admin.prevision.value, admin.afp.value, admin.salary, admin.unit.value, 2])
                self.ClearItems()
        except Exception as e:
            showwarning('Error', message = e)
    def InsertPatientTable(self):
        try:
            if RUT.ValidateRut(str(self.vars['rut'].get())):
                patient = Patient(name = self.vars['name'].get(), rut = RUT(int(''.join(str(self.vars['rut'].get()).split('-')[0].split('.')))), admission = date(self.vars['year'].get(), self.vars['month'].get(), self.vars['day'].get()), afp = AFP.Validate(self.items['afpCombobox'].get()), area = Area.Validate(self.items['areaCombobox'].get()), prevision = Prevision.Validate(self.items['previsionCombobox'].get()), reason = self.vars['reason'].get(), derivation = Derivation.Validate(self.items['derivationCombobox'].get()))
                box = self.hospital.Admit(patient)
                self.db.InsertTable(table = 'person', column = 'rut name admission prevision afp reason derivation box occupation', values = [patient.rut.rut, patient.name, patient.admission.__str__(), patient.prevision.value, patient.afp.value, patient.reason, patient.derivation.value, box, 3])
                self.ClearItems()
        except Exception as e:
            showwarning('Error', message = e)
    def UpdateMedicTable(self):
        try:
            if RUT.ValidateRut(str(self.vars['search'].get())):
                medic : Medic = None
                rut = int(''.join(str(self.vars['search'].get()).split('-')[0].split('.')))
                for i in self.hospital.workers:
                    if i.rut.rut == rut:
                        medic = i
                        rut = i.rut.rut
                        break
                if not medic is None:
                    medic.name = str(self.vars['name'].get())
                    medic.rut = RUT(int(''.join(str(self.vars['rut'].get()).split('-')[0].split('.'))))
                    medic.admission = date(self.vars['year'].get(), self.vars['month'].get(), self.vars['day'].get())
                    medic.afp = AFP.Validate(self.items['afpCombobox'].get())
                    medic.area = Area.Validate(self.items['areaCombobox'].get())
                    medic.prevision = Prevision.Validate(self.items['previsionCombobox'].get())
                    medic.salary = self.vars['salary'].get()
                    medic.specialty = Specialty.Validate(self.items['specialtyCombobox'].get())
                    self.db.UpdateSet(table = 'person', column = 'rut name admission prevision afp salary specialty area', values = [medic.rut.rut, medic.name, medic.admission.__str__(), medic.prevision.value, medic.afp.value, medic.salary, medic.specialty.value, medic.area.value], where = f'rut = {rut}')
                    self.ClearItems()
        except Exception as e:
            showwarning("Error", message = e)
    def UpdateAdminTable(self):
        try:
            if RUT.ValidateRut(str(self.vars['search'].get())):
                admin : Administrative = None
                rut = int(''.join(str(self.vars['search'].get()).split('-')[0].split('.')))
                for i in self.hospital.workers:
                    if i.rut.rut == rut:
                        admin = i
                        rut = i.rut.rut
                        break
                if not admin is None:
                    admin.name = str(self.vars['name'].get())
                    admin.rut = RUT(int(''.join(str(self.vars['rut'].get()).split('-')[0].split('.'))))
                    admin.admission = date(self.vars['year'].get(), self.vars['month'].get(), self.vars['day'].get())
                    admin.afp = AFP.Validate(self.items['afpCombobox'].get())
                    admin.prevision = Prevision.Validate(self.items['previsionCombobox'].get())
                    admin.salary = self.vars['salary'].get()
                    admin.unit = Unit.Validate(self.items['unitCombobox'].get())
                    self.db.UpdateSet(table = 'person', column = 'rut name admission prevision afp salary unit', values = [admin.rut.rut, admin.name, admin.admission.__str__(), admin.prevision.value, admin.afp.value, admin.salary, admin.unit.value], where = f'rut = {rut}')
                    self.ClearItems()
        except Exception as e:
            showwarning("Error", message = e)
    def DeletePersonTable(self, occupation : int):
        try:
            if RUT.ValidateRut(str(self.vars['search'].get())):
                rut = int(''.join(str(self.vars['search'].get()).split('-')[0].split('.')))
                if self.windowUiState != WindowUIState.Patient: self.db.DeleteTable(table = 'remunerations', where = f'fkPerson = {rut}')
                self.db.DeleteTable(table = 'person', where = f'occupation = {occupation} AND rut = {rut}')
                self.ClearItems()
        except Exception as e:
            showwarning("Error", message = e)
    def AskIfDelete(self):
        if askquestion('Delete', f'{self.vars["name"].get()} will be deleted from the system along all their data, are you sure?') == 'yes':
            if self.windowUiState == WindowUIState.Medic: self.DeletePersonTable(1)
            elif self.windowUiState == WindowUIState.Admin: self.DeletePersonTable(2)
            elif self.windowUiState == WindowUIState.Patient: self.DeletePersonTable(3)
