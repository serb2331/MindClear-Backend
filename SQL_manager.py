import mysql.connector
class SqlConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database")
        except mysql.connector.Error as error:
            print("Error: ", error)
    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Disconnected from MySQL database")
    def insert(self, table, data):
        try:
            columns = ', '.join(data.keys())
            entries = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({entries})"
            print(query)
            values = tuple(data.values())
            self.cursor.execute(query, values)
            self.connection.commit()
            return 0
        except mysql.connector.Error as error:
            print("Error inserting data:", error)
            return 1
    def search(self, table, data):
        try:
            if len(data) != 0:
                columns = ', '.join(data.keys())
                entries = ' AND '.join([f"{key} = %s" for key in data])
                query = f"SELECT * FROM {table} WHERE {entries}"
                values = tuple(data.values())
                self.cursor.execute(query, values)
                return self.cursor.fetchall()
            else:
                query = f"SELECT * FROM {table}"
                values = tuple(data.values())
                self.cursor.execute(query, values)
                return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print("Error searching data:", error)
            return 1
    def isDataInTable(self, table, data):
        try:
            result = self.search(table, data)
            if result:
                return True
            else:
                return False
        except mysql.connector.Error as error:
            print("Error searching data:", error)
            return 1

    def update(self, table, data, condition):
        if len(data) == 0:
            return 0
        try:
            set_values = ', '.join([f"{key} = %s" for key in data.keys()])
            where_condition = ' AND '.join([f"{key} = %s" for key in condition.keys()])
            query = f"UPDATE {table} SET {set_values} WHERE {where_condition}"
            values = tuple(data.values()) + tuple(condition.values())
            self.cursor.execute(query, values)
            self.connection.commit()
            return 0
        except mysql.connector.Error as error:
            print("Error updating data:", error)
            return 1

    def delete(self, table, condition):
        if len(condition) == 0:
            return 0
        try:
            where_condition = ' AND '.join([f"{key} = %s" for key in condition.keys()])
            query = f"DELETE FROM {table} WHERE {where_condition}"
            values = tuple(condition.values())
            self.cursor.execute(query, values)
            self.connection.commit()
            return 0
        except mysql.connector.Error as error:
            print("Error deleting data:", error)
            return 1
