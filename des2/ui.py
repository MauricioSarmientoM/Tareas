from tkinter import Tk, Label, Entry, Button, Menu, StringVar, IntVar, Event
from tkinter.ttk import Frame, Combobox, Treeview
from tkinter.messagebox import showerror
from hospital import Hospital, WindowUIState, RUT, Prevision, AFP, Specialty, Area, Unit, Derivation
from enum import Enum
from db import OrderBy
class AdminUIState(Enum):
    Insert = 0
    Select = 1
    Delete = 2
    Update = 3
    Remuneration = 4
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
        self.menu['settings'].add_command(label = 'Change to Remuneration Mode', command = lambda : self.AdminState(AdminUIState.Remuneration))
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
        if self.adminUiState == AdminUIState.Insert: self.SetName(GenPos.Top).SetRut(GenPos.Top).SetDate(GenPos.Top).SetPrevision(GenPos.Top).SetSalary(GenPos.Top).SetAfp(GenPos.Top).SetSpecialty(GenPos.Top).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Update: self.SetSearch(GenPos.Top).SetName(GenPos.Middle).SetRut(GenPos.Middle).SetDate(GenPos.Middle).SetPrevision(GenPos.Middle).SetSalary(GenPos.Middle).SetAfp(GenPos.Middle).SetSpecialty(GenPos.Middle).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Delete: self.SetSearch(GenPos.Top).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Remuneration: self.SetTables().SetButton()
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
        if self.adminUiState == AdminUIState.Insert: self.SetName(GenPos.Top).SetRut(GenPos.Top).SetDate(GenPos.Top).SetPrevision(GenPos.Top).SetSalary(GenPos.Top).SetAfp(GenPos.Top).SetSpecialty(GenPos.Top).SetArea(GenPos.Top).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Update: self.SetSearch(GenPos.Top).SetName(GenPos.Middle).SetRut(GenPos.Middle).SetDate(GenPos.Middle).SetPrevision(GenPos.Middle).SetSalary(GenPos.Middle).SetAfp(GenPos.Middle).SetSpecialty(GenPos.Middle).SetArea(GenPos.Middle).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Delete: self.SetSearch(GenPos.Top).SetTables().SetButton()
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
        if self.adminUiState == AdminUIState.Insert: self.SetName(GenPos.Top).SetRut(GenPos.Top).SetDate(GenPos.Top).SetPrevision(GenPos.Top).SetSalary(GenPos.Top).SetAfp(GenPos.Top).SetUnit(GenPos.Top).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Update: self.SetSearch(GenPos.Top).SetName(GenPos.Middle).SetRut(GenPos.Middle).SetDate(GenPos.Middle).SetPrevision(GenPos.Middle).SetSalary(GenPos.Middle).SetAfp(GenPos.Middle).SetUnit(GenPos.Middle).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Delete: self.SetSearch(GenPos.Top).SetTables().SetButton()
        return self
    def AdminPatient(self):
        #Setting variables
        self.vars['name'] = StringVar()
        self.vars['rut'] = StringVar()
        self.vars['year'] = IntVar()
        self.vars['month'] = IntVar()
        self.vars['day'] = IntVar()
        self.vars['reason'] = StringVar()
        self.vars['hDays'] = IntVar()
        self.vars['search'] = StringVar()
        if self.adminUiState == AdminUIState.Insert: self.SetName(GenPos.Top).SetRut(GenPos.Top).SetDate(GenPos.Top).SetPrevision(GenPos.Top).SetAfp(GenPos.Top).SetReason(GenPos.Top).SetDerivation(GenPos.Top).SetMedic(GenPos.Top).SetBox(GenPos.Top).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Update: self.SetSearch(GenPos.Top).SetName(GenPos.Middle).SetRut(GenPos.Middle).SetDate(GenPos.Middle).SetPrevision(GenPos.Middle).SetAfp(GenPos.Middle).SetReason(GenPos.Middle).SetDerivation(GenPos.Middle).SetMedic(GenPos.Middle).SetBox(GenPos.Middle).SetTables().SetButton()
        elif self.adminUiState == AdminUIState.Delete: self.SetSearch(GenPos.Top).SetTables().SetButton()
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
            medics = self.hospital.Select(table = 'workers', column = 'name', fetch = -1, where = 'occupation != 2')
            self.items['medicLabel'] = Label(self.window, text = 'Medic')
            self.items['medicCombobox'] = Combobox(self.window, state = 'readonly', values = [i[0] for i in medics])
            self.items['medicCombobox'].current(0)
            if pos == GenPos.Top:
                self.items['medicLabel'].place(x = 10, y = 230)
                self.items['medicCombobox'].place(x = 10, y = 250)
            elif pos == GenPos.Middle:
                self.items['medicLabel'].place(x = 10, y = 330)
                self.items['medicCombobox'].place(x = 10, y = 350)
        except Exception as e: showerror('error', message = e)
        return self
    def SetBox(self, pos : GenPos):
        try:
            box = self.hospital.Select(table = 'patients', column = 'box', fetch = -1)
            if box == None:
                box = range(1, 6)
            else:
                boxF = ()
                for i in box: boxF += i
                box = list(set(range(1, 6)) - set(boxF))
            self.items['boxLabel'] = Label(self.window, text = 'Box')
            self.items['boxCombobox'] = Combobox(self.window, state = 'readonly', values = [i for i in box])
            self.items['boxCombobox'].current(0)
            if pos == GenPos.Top:
                self.items['boxLabel'].place(x = 10, y = 380)
                self.items['boxCombobox'].place(x = 10, y = 400)
            elif pos == GenPos.Middle:
                self.items['boxLabel'].place(x = 10, y = 480)
                self.items['boxCombobox'].place(x = 10, y = 500)
        except Exception as e: showerror('error', message = e)
        return self
    def SetSearch(self, pos : GenPos):
        self.items['searchLabel'] = Label(self.window, text = 'Search by RUT')
        self.items['searchEntry'] = Entry(self.window, textvariable = self.vars['search'], width = 30)
        if pos == GenPos.Top:
            self.items['searchLabel'].place(x = 10, y = 10)
            self.items['searchEntry'].place(x = 10, y = 30)
        return self
    def SetHDays(self, pos : GenPos):
        self.items['hDaysLabel'] = Label(text = 'Hospitalization Days')
        self.items['hDaysEntry'] = Entry(self.window, textvariable = self.vars['hDays'], width = 8)
        if pos == GenPos.Top:
            self.items['hDaysLabel'].place(x = 90, y = 380)
            self.items['hDaysEntry'].place(x = 90, y = 400)
        elif pos == GenPos.Middle:
            self.items['hDaysLabel'].place(x = 90, y = 480)
            self.items['hDaysEntry'].place(x = 90, y = 500)
        return self
    def SetButton(self):
        if self.adminUiState == AdminUIState.Insert: self.items['button'] = Button(self.window, text = 'Insert', command = lambda : self.hospital.InsertPersonTable(self.windowUiState, self.ClearItems, self.items, self.vars), width = 30)
        elif self.adminUiState == AdminUIState.Update: self.items['button'] = Button(self.window, text = 'Update', command = lambda : self.hospital.UpdatePersonTable(self.windowUiState, self.ClearItems, self.items, self.vars), width = 30)
        elif self.adminUiState == AdminUIState.Delete: self.items['button'] = Button(self.window, text = 'Delete', command = lambda : self.hospital.AskIfDelete(self.windowUiState, self.ClearItems, self.items, self.vars), width = 30)
        elif self.adminUiState == AdminUIState.Select: self.items['button'] = Button(self.window, text = 'Delete', command = self.AskIfDelete, width = 30)
        self.items['button'].place(x = 10, y = 540)
        return self
    def SetTables(self):
        try:
            if self.adminUiState == AdminUIState.Select:
                self.items['genTable'] = Treeview(self.window, height = 27, columns = ['#0', '#1', '#2', '#3', '#4', '#5', '#6'])
                self.items['genTable'].place(x = 10, y = 10)
                self.items['genTable'].column('#0', width = 1)
                self.items['genTable'].column('#1', width = 150)
                self.items['genTable'].heading('#1', text = 'Rut', anchor = 'center')
                self.items['genTable'].column('#2', width = 320)
                self.items['genTable'].heading('#2', text = 'Name', anchor = 'center')
                self.items['genTable'].column('#3', width = 320)
                self.items['genTable'].heading('#3', text = 'Admission', anchor = 'center')
                self.items['genTable'].column('#4', width = 320)
                self.items['genTable'].heading('#4', text = 'AFP Discount', anchor = 'center')
                self.items['genTable'].column('#5', width = 320)
                self.items['genTable'].heading('#5', text = 'Prevision Discount', anchor = 'center')
                if self.windowUiState == WindowUIState.Medic:
                    self.items['genTable'].column('#6', width = 320)
                    self.items['genTable'].heading('#6', text = 'Plus', anchor = 'center')
                    self.items['genTable'].column('#7', width = 320)
                    self.items['genTable'].heading('#7', text = 'Liquid Salary', anchor = 'center')
            elif self.adminUiState == AdminUIState.Remuneration:
                self.items['genTable'] = Treeview(self.window, height = 27, columns = ['#0', '#1', '#2', '#3', '#4', '#5', '#6'])
                self.items['genTable'].place(x = 10, y = 10)
                self.items['genTable'].column('#0', width = 1)
                self.items['genTable'].column('#1', width = 150)
                self.items['genTable'].heading('#1', text = 'ID', anchor = 'center')
                self.items['genTable'].column('#2', width = 320)
                self.items['genTable'].heading('#2', text = 'RUT', anchor = 'center')
                self.items['genTable'].column('#3', width = 320)
                self.items['genTable'].heading('#3', text = 'Brute Salary', anchor = 'center')
                self.items['genTable'].column('#4', width = 320)
                self.items['genTable'].heading('#4', text = 'AFP Discount', anchor = 'center')
                self.items['genTable'].column('#5', width = 320)
                self.items['genTable'].heading('#5', text = 'Prevision Discount', anchor = 'center')
                self.items['genTable'].column('#6', width = 320)
                self.items['genTable'].heading('#6', text = 'Plus', anchor = 'center')
                self.items['genTable'].column('#7', width = 320)
                self.items['genTable'].heading('#7', text = 'Liquid Salary', anchor = 'center')
            else:
                self.items['genTable'] = Treeview(self.window, height = 27, columns = ['#0', '#1'])
                self.items['genTable'].place(x = 300, y = 10)
                self.items['genTable'].column('#0', width = 1)
                #self.items['medicTable'].heading('#0', text = 'N', anchor = 'center')
                self.items['genTable'].column('#1', width = 150)
                self.items['genTable'].heading('#1', text = 'RUT', anchor = 'center')
                self.items['genTable'].column('#2', width = 320)
                self.items['genTable'].heading('#2', text = 'Name', anchor = 'center')
                if self.windowUiState == WindowUIState.Medic:
                    self.items['genTable'].bind('<Double-1>', self.SelectUpdateMedicTable)
                    data = self.hospital.Select(table = 'workers', column = 'rut name', fetch = -1, where = 'occupation = 0')
                    if data is not None:
                        for i in data: self.items['genTable'].insert('', 0, values = i)
                elif self.windowUiState == WindowUIState.TENS:
                    self.items['genTable'].bind('<Double-1>', self.SelectUpdateTENSTable)
                    data = self.hospital.Select(table = 'workers', column = 'rut name', fetch = -1, where = 'occupation = 1')
                    if data is not None:
                        for i in data: self.items['genTable'].insert('', 0, values = i)
                elif self.windowUiState == WindowUIState.Admin:
                    self.items['genTable'].bind('<Double-1>', self.SelectUpdateAdminTable)
                    data = self.hospital.Select(table = 'workers', column = 'rut name', fetch = -1, where = 'occupation = 2')
                    if data is not None:
                        for i in data: self.items['genTable'].insert('', 0, values = i)
                elif self.windowUiState == WindowUIState.Patient:
                    self.items['genTable'].bind('<Double-1>', self.SelectUpdatePatientTable)
                    data = self.hospital.Select(table = 'patients', column = 'rut name', fetch = -1)
                    if data is not None:
                        for i in data: self.items['genTable'].insert('', 0, values = i)
        except Exception as e: showerror('Error', message = e)
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
    def SelectUpdateMedicTable(self, event : Event):
        try:
            item = self.items['genTable'].identify('item', event.x, event.y)
            rut = int(self.items['genTable'].item(item, 'values')[0])
            data = self.hospital.Select(table = 'workers', fetch = 1, where = f'occupation = 0 AND rut = {rut}')
            self.vars['search'].set(RUT(data[0]).__str__())
            self.vars['rut'].set(RUT(data[0]).__str__())
            self.vars['name'].set(data[1])
            self.vars['year'].set(data[2].year)
            self.vars['month'].set(data[2].month)
            self.vars['day'].set(data[2].day)
            self.items['previsionCombobox'].set(Prevision(data[3]).name)
            self.items['afpCombobox'].set(AFP(data[4]).name)
            self.vars['salary'].set(data[5])
            self.items['specialtyCombobox'].set(Specialty(data[6]).name)
        except Exception as e: showerror('Error', message = e)
    def SelectUpdateTENSTable(self, event : Event):
        try:
            item = self.items['genTable'].identify('item', event.x, event.y)
            rut = int(self.items['genTable'].item(item, 'values')[0])
            data = self.hospital.Select(table = 'workers', fetch = 1, where = f'occupation = 1 AND rut = {rut}')
            self.vars['search'].set(RUT(data[0]).__str__())
            self.vars['rut'].set(RUT(data[0]).__str__())
            self.vars['name'].set(data[1])
            self.vars['year'].set(data[2].year)
            self.vars['month'].set(data[2].month)
            self.vars['day'].set(data[2].day)
            self.items['previsionCombobox'].set(Prevision(data[3]).name)
            self.items['afpCombobox'].set(AFP(data[4]).name)
            self.vars['salary'].set(data[5])
            self.items['specialtyCombobox'].set(Specialty(data[6]).name)
            self.items['areaCombobox'].set(Area(data[7]).name)
        except Exception as e: showerror('Error', message = e)
    def SelectUpdateAdminTable(self, event : Event):
        try:
            item = self.items['genTable'].identify('item', event.x, event.y)
            rut = int(self.items['genTable'].item(item, 'values')[0])
            data = self.hospital.Select(table = 'workers', fetch = 1, where = f'occupation = 2 AND rut = {rut}')
            self.vars['search'].set(RUT(data[0]).__str__())
            self.vars['rut'].set(RUT(data[0]).__str__())
            self.vars['name'].set(data[1])
            self.vars['year'].set(data[2].year)
            self.vars['month'].set(data[2].month)
            self.vars['day'].set(data[2].day)
            self.items['previsionCombobox'].set(Prevision(data[3]).name)
            self.items['afpCombobox'].set(AFP(data[4]).name)
            self.vars['salary'].set(data[5])
            self.items['unitCombobox'].set(Unit(data[8]))
        except Exception as e: showerror('Error', message = e)
    def SelectUpdatePatientTable(self, event : Event):
        try:
            item = self.items['genTable'].identify('item', event.x, event.y)
            rut = int(self.items['genTable'].item(item, 'values')[0])
            data = self.hospital.Select(table = 'patients', fetch = 1, where = f'rut = {rut}', orderBy = OrderBy.DESC, orderByColumn = 'id')
            self.vars['search'].set(RUT(data[1]).__str__())
            self.vars['rut'].set(RUT(data[1]).__str__())
            self.vars['name'].set(data[2])
            self.vars['year'].set(data[3].year)
            self.vars['month'].set(data[3].month)
            self.vars['day'].set(data[3].day)
            self.items['previsionCombobox'].set(Prevision(data[4]).name)
            self.items['afpCombobox'].set(AFP(data[5]).name)
            self.vars['reason'].set(data[6])
            self.items['derivationCombobox'].set(Derivation(data[7]))
            self.items['medicCombobox'].set(self.hospital.Select(table = 'workers', column = 'name', where = f'rut = {data[6]}')[0])
            self.items['boxCombobox'].set(0)
        except Exception as e: showerror('Error', message = e)