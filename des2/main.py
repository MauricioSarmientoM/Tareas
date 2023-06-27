from ui import UI, Hospital, DB
def Main():
    db = DB()
    hospital = Hospital()
    ui = UI(hospital, db)
    ui.Render()
if __name__ == '__main__': Main()