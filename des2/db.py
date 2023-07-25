from pymysql import connect
from enum import Enum
class OrderBy(Enum):
    ASC = 0
    DESC = 1
class DB():
    def __init__(self, host : str = 'localhost', user : str = 'root', password : str = '', database : str = '') -> None:
        try:
            self.connection = connect(
                host = host,
                user = user,
                password = password,
                database = database)
            self.cursor = self.connection.cursor()
            print('Connected Succesfully!')
        except:
            try:
                self.connection = connect(
                    host = host,
                    user = user,
                    password = password)
                self.cursor = self.connection.cursor()
                self.cursor.execute(f'CREATE DATABASE {database}')
                self.connection.commit()
                print(f'{database} created!')
                self.connection = connect(
                    host = host,
                    user = user,
                    password = password,
                    database = database)
                self.cursor = self.connection.cursor()
                #Hack to autocomplete the necessary stuff
                self.cursor.execute('CREATE TABLE person (rut INT, name VARCHAR(64) NOT NULL, admission DATE NOT NULL, prevision INT, afp INT, salary INT, specialty INT, area INT, unit INT, reason VARCHAR(128), derivation INT, medic INT, occupation INT, box INT, PRIMARY KEY (rut))')
                self.cursor.execute('CREATE TABLE remunerations (id INT, fkPerson INT, brute INT, liquid INT, PRIMARY KEY (id), FOREIGN KEY (fkPerson) REFERENCES person(rut))')
                self.connection.commit()
                print('Connected Succesfully!')
                #db.CreateTable('person', 'rut INT UNIQUE PRIMARY KEY, name VARCHAR(32), admission DATE, afp VARCHAR(16), occupation INT FOREIGN KEY, patient INT FOREIGN KEY')
                #db.CreateTable('occupation', 'id INT PRIMARY KEY AUTO_INCREMENT, salary INT, specialty VARCHAR(16), area VARCHAR(16), unit VARCHAR(16)')
                #db.CreateTable('patient', 'id INT PRIMARY KEY AUTO_INCREMENT, reason VARCHAR(128), derivation INT, medic INT FOREIGN KEY')
            except ConnectionError as e:
                print(e)
    def DropDatabase(self, database):
        try:
            self.cursor.execute(f'DROP DATABASE {database}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def CreateTable(self, table : str = '', data : str = ''):
        try:
            data = f'({",".join(data.split(","))})'
            self.cursor.execute(f'CREATE TABLE {table} {data}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def DropTable(self, table):
        try:
            self.cursor.execute(f'DROP TABLE {table}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def InsertTable(self, table : str, column : str, values : list):
        try:
            if column != '': column = f' ({",".join(column.split(" "))})'
            values = [f'{i}' if not isinstance(i, str) else f'"{i}"' for i in values]
            data = f'({",".join(values)})'
            self.cursor.execute(f'INSERT INTO {table}{column} VALUES {data}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def Select(self, table : str, column : str = '', fetch : int = 1, where : str = '', orderBy : int = OrderBy.ASC, orderByColumn : str = ''):
        try:
            if column == '': column = '*'
            else: column = f'{",".join(column.split(" "))}'
            if where != '': where = f' WHERE {where}'
            if orderByColumn != '': orderByColumn = f' ORDER BY {",".join(orderByColumn.split(" "))} {orderBy.name}'
            self.cursor.execute(f'SELECT {column} FROM {table}{where}{orderByColumn}')
            if fetch < 1:
                return self.cursor.fetchall()
            elif fetch == 1:
                return self.cursor.fetchone()
            elif fetch > 1:
                return self.cursor.fetchmany(fetch)
        except Exception as e:
            print(e)
        return None
    def UpdateSet(self, table : str, column : str, values : list, where : str):
        try:
            if column != '': 
                data = [f'{j} = {k}' for j, k in zip(column.split(" "), [f'{i}' if not isinstance(i, str) else f'"{i}"' for i in values])]
                data = f'{",".join(data)}'
            if where != '': where = f' WHERE {",".join(where.split(","))}'
            self.cursor.execute(f'UPDATE {table} SET {data}{where}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def DeleteTable(self, table : str, where : str = ''):
        try:
            if where != '': where = f' WHERE {",".join(where.split(","))}'
            self.cursor.execute(f'DELETE FROM {table}{where}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
def Main():
    db = DB(database = 'dev2')
    #print(db.Select('person', column = 'rut name', fetch = -1))
    #db.InsertTable(table = 'person', column = 'rut name admission afp occupation', values = [20751584, 'Celes', '2017-03-12', 0, 2])
    #db.DeleteTable(table = 'person', where = '')
    #print(db.Update(table = 'person', column = 'name afp', values = ['Celeste Marambio', '3'], where = 'rut = 20751584').Select(table = 'person', fetch = -1))
    db.DropDatabase('dev2')
if __name__ == '__main__': Main()