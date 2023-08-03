from tkinter import Tk, Label, Entry, Button, Menu, StringVar, IntVar
from tkinter.ttk import Frame, Combobox, Treeview
from tkinter.messagebox import showerror
from hospital import Hospital, WindowUIState
from enum import Enum
from datetime import date
class AdminUIState(Enum):
    Insert = 0
    Select = 1
    Delete = 2
    Update = 3
class GenPos(Enum):
    Top = 0
    Middle = 1
    Down = 2
class UI(Frame):
    def __init__(self, hospital : Hospital) -> None:
        self.window = Tk()
        self.name = hospital.name
        self.window.geometry("800x600")
        super().__init__(self.window)
        self.hospital = hospital
        self.vars = {}
        self.items = {}
        self.menu = {}
        self.adminUiState = AdminUIState.Insert
        self.windowUiState = WindowUIState.Medic
    def Base(self):
        #Estableshing brand new page
        self.vars = {}
        self.items = {}
        self.menu = {}
        #Setting upper stuff
        self.menu['topbar'] = Menu(self.window)
        #self.menu['files'] = Menu(self.menu['topbar'], tearoff = 0)
        self.menu['settings'] = Menu(self.menu['topbar'], tearoff = 1)
        self.menu['settings'].add_command(label = 'Change to Medic', command = lambda : self.WindowState(WindowUIState.Medic))
        self.menu['settings'].add_command(label = 'Change to TENS', command = lambda : self.WindowState(WindowUIState.TENS))
        self.menu['settings'].add_command(label = 'Change to Administration', command = lambda : self.WindowState(WindowUIState.Admin))
        self.menu['settings'].add_command(label = 'Change to Patients', command = lambda : self.WindowState(WindowUIState.Patient))
        self.menu['settings'].add_separator()
        self.menu['settings'].add_command(label = 'Change to Insert Mode', command = lambda : self.AdminState(AdminUIState.Insert))
        self.menu['settings'].add_command(label = 'Change to Select Mode', command = lambda : self.AdminState(AdminUIState.Select))
        self.menu['settings'].add_command(label = 'Change to Update Mode', command = lambda : self.AdminState(AdminUIState.Update))
        self.menu['settings'].add_command(label = 'Change to Delete Mode', command = lambda : self.AdminState(AdminUIState.Delete))
        self.menu['inputs'] = Menu(self.menu['topbar'], tearoff = 2)
        self.menu['inputs'].add_command(label = 'Clear Inputs', command = self.ClearVars)
        #self.menu['topbar'].add_cascade(label = 'File', menu = self.menu['files'])
        self.menu['topbar'].add_cascade(label = 'Settings', menu = self.menu['settings'])
        self.menu['topbar'].add_cascade(label = 'Input', menu = self.menu['inputs'])
        self.window.config(menu = self.menu['topbar'])
        if self.windowUiState == WindowUIState.Medic: self.AdminMedics()
        if self.windowUiState == WindowUIState.TENS: self.AdminTENS()
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
        #self.items['medicTable'].column('#0', width = 10)
        #self.items['medicTable'].heading('#0', text = 'N', anchor = 'center')
        self.items['medicTable'].column('#1', width = 150)
        self.items['medicTable'].heading('#1', text = 'RUT', anchor = 'center')
        self.items['medicTable'].column('#2', width = 320)
        self.items['medicTable'].heading('#2', text = 'Name', anchor = 'center')
        self.items['medicTable'].bind('<Double-1>', func = lambda : self.hospital.SelectUpdateMedicTable)
        try:
            data = self.hospital.Select(table = 'workers', column = 'rut name', fetch = -1, where = 'occupation = 1')
            if data is not None:
                for i in data: self.items['medicTable'].insert('', 0, values = i)
        except Exception as e: showerror('Error', message = e)
        if self.adminUiState == AdminUIState.Insert: self.SetName(GenPos.Top).SetRut(GenPos.Top).SetDate(GenPos.Top).SetPrevision(GenPos.Top).SetSalary(GenPos.Top).SetAfp(GenPos.Top).SetSpecialty(GenPos.Top).SetButton()
        elif self.adminUiState == AdminUIState.Update: self.SetSearch(GenPos.Top).SetName(GenPos.Middle).SetRut(GenPos.Middle).SetDate(GenPos.Middle).SetPrevision(GenPos.Middle).SetSalary(GenPos.Middle).SetAfp(GenPos.Middle).SetSpecialty().SetButton()
        elif self.adminUiState == AdminUIState.Delete: self.SetSearch(GenPos.Top).SetButton()
        return self
    def AdminTENS(self):
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
        #self.items['medicTable'].column('#0', width = 10)
        #self.items['medicTable'].heading('#0', text = 'N', anchor = 'center')
        self.items['medicTable'].column('#1', width = 150)
        self.items['medicTable'].heading('#1', text = 'RUT', anchor = 'center')
        self.items['medicTable'].column('#2', width = 320)
        self.items['medicTable'].heading('#2', text = 'Name', anchor = 'center')
        self.items['medicTable'].bind('<Double-1>', self.SelectUpdateMedicTable)
        try:
            data = self.hospital.Select(table = 'workers', column = 'rut name', fetch = -1, where = 'occupation = 1')
            if data is not None:
                for i in data: self.items['medicTable'].insert('', 0, values = i)
        except Exception as e: showerror('Error', message = e)
        if self.adminUiState == AdminUIState.Insert: self.SetName(GenPos.Top).SetRut(GenPos.Top).SetDate(GenPos.Top).SetPrevision(GenPos.Top).SetSalary(GenPos.Top).SetAfp(GenPos.Top).SetSpecialty(GenPos.Top).SetArea(GenPos.Top).SetButton()
        elif self.adminUiState == AdminUIState.Update: self.SetSearch(GenPos.Top).SetName(GenPos.Middle).SetRut(GenPos.Middle).SetDate(GenPos.Middle).SetPrevision(GenPos.Middle).SetSalary(GenPos.Middle).SetAfp(GenPos.Middle).SetArea(GenPos.Top).SetSpecialty().SetButton()
        elif self.adminUiState == AdminUIState.Delete: self.SetSearch(GenPos.Top).SetButton()
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
        #self.items['adminTable'].column('#0', width = 10)
        #self.items['adminTable'].heading('#0', text = 'N', anchor = 'center')
        self.items['adminTable'].column('#1', width = 150)
        self.items['adminTable'].heading('#1', text = 'RUT', anchor = 'center')
        self.items['adminTable'].column('#2', width = 320)
        self.items['adminTable'].heading('#2', text = 'Name', anchor = 'center')
        self.items['adminTable'].bind('<Double-1>', self.SelectUpdateAdminTable)
        try:
            data = self.hospital.Select(table = 'workers', column = 'rut name', fetch = -1, where = 'occupation = 2')
            if data is not None:
                for i in data: self.items['adminTable'].insert('', 0, values = i)
        except Exception as e: showerror('Error', message = e)
        #Specific stuff
        if self.adminUiState == AdminUIState.Insert: self.SetName(GenPos.Top).SetRut(GenPos.Top).SetDate(GenPos.Top).SetPrevision(GenPos.Top).SetSalary(GenPos.Top).SetAfp(GenPos.Top).SetUnit(GenPos.Top).SetButton()
        elif self.adminUiState == AdminUIState.Update: self.SetSearch(GenPos.Top).SetName(GenPos.Middle).SetRut(GenPos.Middle).SetDate(GenPos.Middle).SetPrevision(GenPos.Middle).SetSalary(GenPos.Middle).SetAfp(GenPos.Middle).SetButton()
        elif self.adminUiState == AdminUIState.Delete: self.SetSearch(GenPos.Top).SetButton()
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
        #self.items['patientTable'].column('#0', width = 10)
        #self.items['patientTable'].heading('#0', text = 'N', anchor = 'center')
        self.items['patientTable'].column('#1', width = 150)
        self.items['patientTable'].heading('#1', text = 'RUT', anchor = 'center')
        self.items['patientTable'].column('#2', width = 320)
        self.items['patientTable'].heading('#2', text = 'Name', anchor = 'center')
        self.items['patientTable'].bind('<Double-1>', self.SelectUpdatePatientTable)
        try:
            data = self.select.Select(table = 'patients', column = 'rut name', fetch = -1, where = 'occupation = 3')
            if data is not None:
                for i in data: self.items['patientTable'].insert('', 0, values = i)
        except Exception as e: showerror('Error', message = e)
        if self.adminUiState == AdminUIState.Insert: self.SetName(GenPos.Top).SetRut(GenPos.Top).SetDate(GenPos.Top).SetPrevision(GenPos.Top).SetAfp(GenPos.Top).SetReason(GenPos.Top).SetDerivation(GenPos.Top).SetMedic(GenPos.Top).SetButton()
        elif self.adminUiState == AdminUIState.Update: self.SetSearch(GenPos.Top).SetName(GenPos.Middle).SetRut(GenPos.Middle).SetDate(GenPos.Middle).SetPrevision(GenPos.Middle).SetAfp(GenPos.Middle).SetReason(GenPos.Middle).SetDerivation(GenPos.Middle).SetMedic(GenPos.Middle).SetButton()
        elif self.adminUiState == AdminUIState.Delete: self.SetSearch(GenPos.Top).SetButton()
        return self
    def SetName(self, pos : GenPos):
        self.items['nameLabel'] = Label(self.window, text = 'Name')
        self.items['nameEntry'] = Entry(self.window, textvariable = self.vars['name'], width = 30)
        if pos == GenPos.Top:
            self.items['nameLabel'].place(x = 10, y = 10)
            self.items['nameEntry'].place(x = 10, y = 30)
        elif pos == GenPos.Middle:
            self.items['nameLabel'].place(x = 10, y = 100)
            self.items['nameEntry'].place(x = 10, y = 130)
        return self
    def SetRut(self, pos : GenPos):
        self.items['rutLabel'] = Label(self.window, text = 'RUT')
        self.items['rutEntry'] = Entry(self.window, textvariable = self.vars['rut'], width = 30)
        if pos == GenPos.Top:
            self.items['rutLabel'].place(x = 10, y = 60)
            self.items['rutEntry'].place(x = 10, y = 80)
        elif pos == GenPos.Middle:
            self.items['rutLabel'].place(x = 10, y = 160)
            self.items['rutEntry'].place(x = 10, y = 180)
        return self
    def SetDate(self, pos : GenPos):
        self.items['dateLabel'] = Label(text = 'Admission Date')
        self.items['yearLabel'] = Label(text = 'Year')
        self.items['yearEntry'] = Entry(self.window, textvariable = self.vars['year'], width = 8)
        self.items['monthLabel'] = Label(text = 'Month')
        self.items['monthEntry'] = Entry(self.window, textvariable = self.vars['month'], width = 8)
        self.items['dayLabel'] = Label(text = 'Day')
        self.items['dayEntry'] = Entry(self.window, textvariable = self.vars['day'], width = 8)
        if pos == GenPos.Top:
            self.items['dateLabel'].place(x = 10, y = 110)
            self.items['yearLabel'].place(x = 190, y = 130)
            self.items['yearEntry'].place(x = 190, y = 150)
            self.items['monthLabel'].place(x = 100, y = 130)
            self.items['monthEntry'].place(x = 100, y = 150)
            self.items['dayLabel'].place(x = 10, y = 130)
            self.items['dayEntry'].place(x = 10, y = 150)
        elif pos == GenPos.Middle:
            self.items['dateLabel'].place(x = 10, y = 210)
            self.items['yearLabel'].place(x = 190, y = 230)
            self.items['yearEntry'].place(x = 190, y = 250)
            self.items['monthLabel'].place(x = 100, y = 230)
            self.items['monthEntry'].place(x = 100, y = 250)
            self.items['dayLabel'].place(x = 10, y = 230)
            self.items['dayEntry'].place(x = 10, y = 250)
        return self
    def SetPrevision(self, pos : GenPos):
        self.items['previsionLabel'] = Label(self.window, text = 'Prevision')
        self.items['previsionCombobox'] = Combobox(self.window, state = 'readonly', values = ['FONASA', 'ISAPRE', 'Particular'])
        self.items['previsionCombobox'].current(0)
        if pos == GenPos.Top:
            self.items['previsionLabel'].place(x = 10, y = 180)
            self.items['previsionCombobox'].place(x = 10, y = 200)
        elif pos == GenPos.Middle:
            self.items['previsionLabel'].place(x = 10, y = 280)
            self.items['previsionCombobox'].place(x = 10, y = 300)
        return self
    def SetSalary(self, pos : GenPos):
        self.items['salaryLabel'] = Label(self.window, text = 'Salary')
        self.items['salaryEntry'] = Entry(self.window, textvariable = self.vars['salary'], width = 30)
        if pos == GenPos.Top:
            self.items['salaryLabel'].place(x = 10, y = 230)
            self.items['salaryEntry'].place(x = 10, y = 250)
        elif pos == GenPos.Middle:
            self.items['salaryLabel'].place(x = 10, y = 330)
            self.items['salaryEntry'].place(x = 10, y = 350)
        return self
    def SetAfp(self, pos : GenPos):
        self.items['afpLabel'] = Label(self.window, text = 'AFP')
        self.items['afpCombobox'] = Combobox(self.window, state = 'readonly', values = ['Capital', 'Cuprum', 'Habitat', 'Modelo', 'Planvital', 'Provida', 'Uno'])
        self.items['afpCombobox'].current(0)
        if pos == GenPos.Top:
            self.items['afpLabel'].place(x = 10, y = 280)
            self.items['afpCombobox'].place(x = 10, y = 300)
        elif pos == GenPos.Middle:
            self.items['afpLabel'].place(x = 10, y = 380)
            self.items['afpCombobox'].place(x = 10, y = 400)
        return self
    def SetSpecialty(self, pos : GenPos):
        self.items['specialtyLabel'] = Label(self.window, text = 'Specialty')
        self.items['specialtyCombobox'] = Combobox(self.window, state = 'readonly', values = ['Pediatrics', 'Anesteology', 'Cardiology', 'Gastroenterology', 'General', 'Gynecology', 'Obstetrics'])
        self.items['specialtyCombobox'].current(0)
        if pos == GenPos.Top:
            self.items['specialtyLabel'].place(x = 10, y = 330)
            self.items['specialtyCombobox'].place(x = 10, y = 350)
        elif pos == GenPos.Middle:
            self.items['specialtyLabel'].place(x = 10, y = 430)
            self.items['specialtyCombobox'].place(x = 10, y = 450)
        return self
    def SetArea(self, pos :GenPos):
        self.items['areaLabel'] = Label(self.window, text = 'Area')
        self.items['areaCombobox'] = Combobox(self.window, state = 'readonly', values = ['Extern', 'Emergency', 'Pediatrics', 'Operating', 'Hospitalization', 'ICU'])
        self.items['areaCombobox'].current(0)
        if pos == GenPos.Top:
            self.items['areaLabel'].place(x = 10, y = 380)
            self.items['areaCombobox'].place(x = 10, y = 400)
        elif pos == GenPos.Middle:
            self.items['areaLabel'].place(x = 10, y = 480)
            self.items['areaCombobox'].place(x = 10, y = 500)
        return self
    def SetUnit(self, pos : GenPos):
        self.items['unitLabel'] = Label(self.window, text = 'Administrative Unit')
        self.items['unitCombobox'] = Combobox(self.window, state = 'readonly', values = ['General', 'Personal', 'Chief'])
        self.items['unitCombobox'].current(0)
        if pos == GenPos.Top:
            self.items['unitLabel'].place(x = 10, y = 330)
            self.items['unitCombobox'].place(x = 10, y = 350)
        elif pos == GenPos.Middle:
            self.items['unitLabel'].place(x = 10, y = 430)
            self.items['unitCombobox'].place(x = 10, y = 450)
        return self
    def SetReason(self, pos : GenPos):
        self.items['reasonLabel'] = Label(self.window, text = 'Reason')
        self.items['reasonEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
        if pos == GenPos.Top:
            self.items['reasonLabel'].place(x = 10, y = 280)
            self.items['reasonEntry'].place(x = 10, y = 300)
        elif pos == GenPos.Middle:
            self.items['reasonLabel'].place(x = 10, y = 380)
            self.items['reasonEntry'].place(x = 10, y = 400)
        return self
    def SetDerivation(self, pos : GenPos):
        self.items['derivationLabel'] = Label(self.window, text = 'Derivation')
        self.items['derivationCombobox'] = Combobox(self.window, state = 'readonly', values = ['Consult', 'Emergency'])
        self.items['derivationCombobox'].current(0)
        if pos == GenPos.Top:
            self.items['derivationLabel'].place(x = 10, y = 330)
            self.items['derivationCombobox'].place(x = 10, y = 350)
        elif pos == GenPos.Middle:
            self.items['derivationLabel'].place(x = 10, y = 430)
            self.items['derivationCombobox'].place(x = 10, y = 450)
        return self
    def SetMedic(self, pos : GenPos):
        try:
            medics = self.hospital.Select(table = 'workers', column = 'name', fetch = -1)
            self.items['medicLabel'] = Label(self.window, text = 'Administrative Unit')
            self.items['medicCombobox'] = Combobox(self.window, state = 'readonly', values = [i for i in medics])
            self.items['medicCombobox'].current(0)
            if pos == GenPos.Top:
                self.items['unitLabel'].place(x = 10, y = 380)
                self.items['unitCombobox'].place(x = 10, y = 400)
            elif pos == GenPos.Middle:
                self.items['unitLabel'].place(x = 10, y = 480)
                self.items['unitCombobox'].place(x = 10, y = 500)
        except Exception as e: showerror('error', message = e)
        return self
    def SetSearch(self, pos : GenPos):
        self.items['searchLabel'] = Label(self.window, text = 'Search by RUT')
        self.items['searchEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
        if pos == GenPos.Top:
            self.items['searchLabel'].place(x = 10, y = 10)
            self.items['searchEntry'].place(x = 10, y = 30)
        return self
    def SetButton(self):
        if self.adminUiState == AdminUIState.Insert: self.items['insertButton'] = Button(self.window, text = 'Insert', command = lambda : self.hospital.InsertPersonTable(self.windowUiState, self.ClearItems, self.items, self.vars), width = 30)
        elif self.adminUiState == AdminUIState.Update: self.items['updateButton'] = Button(self.window, text = 'Update', command = lambda : self.hospital.UpdatePersonTable(self.windowUiState, self.ClearItems, self.items, self.vars), width = 30)
        elif self.adminUiState == AdminUIState.Delete: self.items['deleteButton'] = Button(self.window, text = 'Delete', command = lambda : self.hospital.AskIfDelete(self.windowUiState, self.ClearItems, self.items, self.vars), width = 30)
        elif self.adminUiState == AdminUIState.Select: self.items['deleteButton'] = Button(self.window, text = 'Delete', command = self.AskIfDelete, width = 30)
        self.items['insertButton'].place(x = 10, y = 540)
        return self
    def ClearItems(self):
        for i in self.items.values(): i.destroy()
        self.items.clear()
        self.Base()
        return self
    def ClearVars(self):
        for i in self.vars.values():
            i.set('')
        return self
    def WindowState(self, state : WindowUIState):
        self.windowUiState = state
        self.ClearItems()
        return self
    def AdminState(self, state : AdminUIState):
        self.adminUiState = state
        self.ClearItems()
        return self