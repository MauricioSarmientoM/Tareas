from ui import UI
from hospital import Hospital
from db import DB
def Main():
    ui = UI(Hospital(), DB(database = 'dev2'))
    ui.Base().mainloop()
if __name__ == '__main__': Main()