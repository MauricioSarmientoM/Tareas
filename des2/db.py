from pymysql import connect
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
        except ConnectionError as e:
            print(e)
            try:
                self.connection = connect(
                    host = host,
                    user = user,
                    password = password)
                self.cursor = self.connection.cursor()
                self.cursor.execute(f'CREATE DATABASE {database}')
                self.connection.commit()
                self.connection = connect(
                    host = host,
                    user = user,
                    password = password,
                    database = database)
                self.cursor = self.connection.cursor()
            except ConnectionError as e:
                print(e)
    def CreateTable(self, table : str = '', data : str = ''):
        try:
            data = f'({",".join(data.split(","))})'
            self.cursor.execute(f'CREATE TABLE {table} {data}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def DropTable(self, table : str = ''):
        try:
            self.cursor.execute(f'DROP TABLE {table}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def InsertTable(self, table : str = '', column : str = '', values : list = []):
        try:
            if column != '': column = f' ({",".join(column.split(" "))})'
            values = [f'{i}' if not isinstance(i, str) else f'"{i}"' for i in values]
            data = f'({",".join(values)})'
            #print(f'INSERT INTO {table}{column} VALUES {data}')
            self.cursor.execute(f'INSERT INTO {table}{column} VALUES {data}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def Select(self, column : str = '', table : str = '', fetch : int = 1, where : str = ''):
        try:
            if column == '': column = '*'
            else: column = f'({",".join(column.split(" "))})'
            if where != '': where = f' WHERE ({",".join(where.split(","))})'
            self.cursor.execute(f'SELECT {column} FROM {table}{where}')
            if fetch < 1:
                return self.cursor.fetchall()
            elif fetch == 1:
                return self.cursor.fetchone()
            elif fetch > 1:
                return self.cursor.fetchmany(fetch)
        except Exception as e:
            print(e)
        return self
    def Update(self, table : str, column : str, values : str, where : str = ''):
        try:
            if column != '': column = f' ({",".join(column.split(" "))})'
            values = [f'{i}' if not isinstance(i, str) else f'"{i}"' for i in values]
            data = f'({",".join(values)})'
            if where != '': where = f' WHERE ({",".join(where.split(","))})'
            self.cursor.execute(f'UPDATE {table} SET {values}{where}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
    def DeleteTable(self, table : str, where : str = ''):
        try:
            if where != '': where = f' WHERE ({",".join(where.split(","))})'
            self.cursor.execute(f'DELETE FROM {table}{where}')
            self.connection.commit()
        except Exception as e:
            print(e)
        return self
def Main():
    db = DB(database = 'dev2')
    #db.CreateTable('person', 'rut INT UNIQUE PRIMARY KEY, name VARCHAR(32), admission DATE, afp VARCHAR(16), occupation INT FOREIGN KEY, patient INT FOREIGN KEY')
    #db.CreateTable('occupation', 'id INT PRIMARY KEY AUTO_INCREMENT, salary INT, specialty VARCHAR(16), area VARCHAR(16), unit VARCHAR(16)')
    #db.CreateTable('patient', 'id INT PRIMARY KEY AUTO_INCREMENT, reason VARCHAR(128), derivation INT, medic INT FOREIGN KEY')
    #db.InsertTable(table = 'person', column = 'rut name admission afp occupation', values = [16184388, 'Yoselin Marambio', '2017-03-12', 'Uno', 2])
    #db.DeleteTable(table = 'person', where = '')
    #print(db.Select(table = 'person', fetch = -1))
if __name__ == '__main__': Main()