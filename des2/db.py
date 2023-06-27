from pymysql import connect
class DB():
    def __init__(self, host : str = 'localhost', user : str = 'root', password : str = '', database : str = 'dev2') -> None:
        try:
            self.connection =connect(
                host = host,
                user = user,
                password = password)
            self.cursor = self.connection.cursor()
            self.cursor.execute('CREATE DATABASE dev2')
            self.connection.commit()
            print('Connected Succesfully!')
        except ConnectionError as e:
            print(e)
            self.cursor = None
    def Reconnect(self):
        try:
            self.cursor = connect(
                host = 'localhost',
                user = 'root',
                password = '',
                db = 'dev2'
            ).cursor()
            print('Connected Succesfully!')
        except ConnectionError as e:
            print(e)
            self.cursor = None
        return self
    def CreateTable(self, table : str = ''):
        try:
            self.cursor.execute(f'CREATE TABLE {table}')
            self.connection.commit()
        except Exception as e:
            print(e)
    def InsertTable(self, table : str = '', column : str = '', values : str = ''):
        try:
            if column != '': column = f' ({",".join(column.split(" "))})'
            values = f'({",".join(values.split(" "))})'
            self.cursor.execute(f'INSERT INTO {table}{column} VALUES {values}')
            self.connection.commit()
        except Exception as e:
            print(e)
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
    def Update(self, table : str = '', where : str = ''):
        try:
            if where != '': where = f' WHERE ({",".join(where.split(","))})'
            self.cursor.execute(f'UPDATE {table}{where}')
            self.connection.commit()
        except Exception as e:
            print(e)
    def Delete(self, table : str = '', where : str = ''):
        try:
            if where != '': where = f' WHERE ({",".join(where.split(","))})'
            self.cursor.execute(f'DELETE FROM {table}{where}')
            self.connection.commit()
        except Exception as e:
            print(e)