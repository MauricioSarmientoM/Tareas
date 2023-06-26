class Date():
    def __init__(self, day = 1, month = 1, year = 1984):
        self.__day = day
        self.__month = month
        self.__year = year
    def __str__(self) -> str:
        return f'{self.__year}/{self.__month}/{self.__day}'
    def Set(self, day = 0, month = 0, year = 0):
        if day > 0:
            self.__day = day
        if month > 0:
            self.__month = month
        if year > 0:
            self.__year = year
        return self
    def __eq__(self, other) -> bool:
        if self.__day == other.__day and self.__month == other.__month and self.__year == other.__year:
            return True
        return False
    def __ne__(self, other) -> bool:
        return not self == other
    @property
    def getDay(self) -> int:
        return self.__day
    @property
    def getMonth(self) -> int:
        return self.__month
    @property
    def getYear(self) -> int:
        return self.__year
class DNI():
    def __init__(self, number = 6942011, owner = 'Григори Перельмал', dateEmission = Date(day = 19, month = 1, year = 2034), dateExpire = Date(day = 19, month = 1, year = 2038)):
        self.__number = number
        self.__owner = owner
        self.__dateEmission = dateEmission
        self.__dateExpire = dateExpire
    def __str__(self) -> str:
        return f'{self.__owner}, {self.__number}\nEmitted: {self.__dateEmission}\nExpires: {self.__dateExpire}'
    def Set(self, number = 0, owner = '', dateEmission = Date(), dateExpire = Date()):
        if number > 0:
            self.__number = number
        if owner != '':
            self.__owner = owner
        if dateEmission != Date():
            self.__dateEmission = dateEmission
        if dateExpire != Date():
            self.__dateExpire = dateExpire
        return self
    @property
    def getNumber(self) -> int:
        return self.__number
    @property
    def getOwner(self) -> str:
        return self.__owner
    @property
    def getDateEmission(self) -> Date:
        return self.__dateEmission
    @property
    def getDateExpire(self) -> Date:
        return self.__dateExpire

date = Date(day = 25, month = 1, year = 2023)
date2 = Date(day = 25, month = 1, year = 2027)
print(date)
print(date2)
date2.Set(year = 2030)
print(date2.getYear)
grigori = DNI()
print(grigori)
celes = DNI(number = 6969696, owner = 'Self Spectrum', dateEmission = date, dateExpire = date2)
print(celes)
celes.Set(dateExpire = Date(22, 9, 3000))
print(celes.getDateExpire)
