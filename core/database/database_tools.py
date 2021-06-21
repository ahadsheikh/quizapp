from core.database.schema import APP_NAME
from django.conf import settings

from core.exceptions import FieldNotFoundException, ConnectionBeenClosedException
import cx_Oracle


class DBModel:
    table_name = ""
    fields = []

    def __init__(self):
        if settings.CUSTOM_DB_CONFIG:
            try:
                self.connection = cx_Oracle.connect(
                    user=settings.CUSTOM_DB_CONFIG['user'],
                    password=settings.CUSTOM_DB_CONFIG['password'],
                    dsn=settings.CUSTOM_DB_CONFIG['dsn']
                )
                self._conn_open = True

            except:
                print("Couldn't connect the database.")

        else:
            raise Exception(
                """
                Database Configuration not found in settings file.
                example:
                CUSTOM_DB_CONFIG = {
                    'user': '<username>',
                    'password': '<password>',
                    'dsn': '<dsn string>'
                }
                """
            )

    # Make object from list of collunms and data
    def __make_obj(self, collumns, data):
        if len(collumns) == len(data):
            res = {}
            for i in range(len(collumns)):
                res[(collumns[i][0]).lower()] = data[i]
            return res
        else:
            raise Exception("Object Creation from fetched row: Collumn length and Data length not same")

    def find(self):
        if self._conn_open:
            SQL = f"SELECT * FROM {self.table_name}"
            try:
                cursor = self.connection.cursor()
                cursor.execute(SQL)
                rows = []
                for row in cursor:
                    rows.append(self.__make_obj(cursor.description, row))

                return rows
            except cx_Oracle.Error as err:
                print(err)
        else:
            raise ConnectionBeenClosedException("This model object connection has been closed.")
        
        return None

    def find_by_id(self, id):
        if self._conn_open and id:
            SQL = f"SELECT * from {self.table_name} WHERE id={id}"
            try:
                cursor = self.connection.cursor()
                cursor.execute(SQL)
                rows = None
                for row in cursor:
                    rows = self.__make_obj(cursor.description, row)
                
                return rows
            except cx_Oracle.Error as err:
                print(err)
        else:
            raise ConnectionBeenClosedException("This model object connection has been closed.")
        
        return None

    def __all_create_field_exist(self, obj):
        validated_data = {}
        validated_field = []
        for field in self.fields:
            if field[1] and field[0] in obj:
                validated_data[field[0]] = obj[field[0]]
                validated_field.append(field[0])

            elif not field[1] and field[0] in obj:
                validated_data[field[0]] = obj[field[0]]
                validated_field.append(field[0])

            elif field[1] and not field[0] in obj:
                raise FieldNotFoundException("required field not found")
            else:
                continue
        
        return validated_field, validated_data

    def __execute_sql_for_insert(self, fields, data):
        insert_name = ""
        insert_value = ""
        for f in fields:
            insert_name += f"{f},"
            insert_value += f":{f},"
        
        insert_name = insert_name[:len(insert_name)-1]
        insert_value = insert_value[:len(insert_value)-1]        

        SQL = f"INSERT INTO {self.table_name}({insert_name}) VALUES({insert_value})"
        try:
            cursor = self.connection.cursor()
            cursor.execute(SQL, data)
            self.connection.commit()
        except cx_Oracle.Error as err:
            print(err)

    def create(self, given_data=None, **kwargs):
        if self._conn_open:
            if given_data:
                field, data = self.__all_create_field_exist(given_data)
                self.__execute_sql_for_insert(field, data)

            elif kwargs:
                field, data = self.__all_create_field_exist(kwargs)
                self.__execute_sql_for_insert(field, data)

            else:
                raise FieldNotFoundException("required field not found")

        else:
            raise ConnectionBeenClosedException("This model object connection has been closed.")

    def __execute_sql_for_update(self, id, data):
        partial_sql = ""
        for key, value in data.items():
            if isinstance(value, int):
                partial_sql += f"{key}={value},"
            else:
                partial_sql += f"{key}='{value}',"
            
        partial_sql = partial_sql[:len(partial_sql)-1]
        SQL = f"UPDATE {self.table_name} SET {partial_sql} WHERE id={id}"
        print(SQL)
        try:
            cursor = self.connection.cursor()
            cursor.execute(SQL)
            self.connection.commit()
        except cx_Oracle.Error as err:
            print(err)

    def update_by_id(self, id, data=None, **kwargs):
        if self._conn_open:
            if data:
                self.__execute_sql_for_update(id, data)

            elif kwargs:
                self.__execute_sql_for_update(id, kwargs)

            else:
                raise FieldNotFoundException("required field not found")

        else:
            raise ConnectionBeenClosedException("This model object connection has been closed.")

    def delete_by_id(self, id):
        if self._conn_open and id:
            res = self.find_by_id(id)
            SQL = f"DELETE from {self.table_name} WHERE id={id}"
            try:
                cursor = self.connection.cursor()
                cursor.execute(SQL)
                self.connection.commit()
                return res
            except cx_Oracle.Error as err:
                print(err)
        else:
            raise ConnectionBeenClosedException("This model object connection has been closed.")

        return None

    def execute_select_sql(self, sql):
        if 'SELECT' in sql or 'select' in sql:
            try:
                cursor = self.connection.cursor()
                cursor.execute(sql)
                rows = []
                for row in cursor:
                    rows.append(self.__make_obj(cursor.description, row))

                return rows
            except cx_Oracle.Error as err:
                print(err)
        
        return None

    def close(self):
        self.connection.close()
        self.conn_open = False
        
    