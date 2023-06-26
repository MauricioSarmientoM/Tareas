from typing import Self
from datetime import datetime
class Phone:
    def __init__(self, brand : str, model : str) -> None:
        self.brand = brand
        self.model = model
        self.linked = []
    def Call(self, other : Self) -> Self:
        self.linked.append(other)
    def Hangout(self):
        self.linked = []
class PhoneOld(Phone):
    def __init__(self, brand : str, model : str, reason : str, owner : str):
        super().__init__(brand, model)
        self.reason = reason
        self.owner = owner
class PhoneNew(Phone):
    def __init__(self, brand : str, model : str, price : int, dateIntroduced : datetime):
        super().__init__(brand, model)
        self.price = price
        self.date = dateIntroduced
        self.gallery = []
    def TakePhoto(self):
        self.gallery.append(datatime.today())

def main():
    a = PhoneOld()

if __name__ == '__main__':
    main()
