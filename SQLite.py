import sqlite3
from pathlib import Path

class Sqlite3_Database:
    def __init__(self, db_file_name: str, args: dict, table_name: str) -> None:
        self.table_name = table_name
        self.db_file_name = db_file_name
        self.args = args
        a = self.creating_table()

    def creating_table(self) -> bool:
        if not self.is_file_exist():
            try:
                self.init_sqlite()
                return True
            except Exception as e:
                print(e.__repr__(), e.args)
                return False
        elif not self.is_table_exist():
            try:
                self.init_sqlite()
                return True
            except Exception as e:
                print(e.__repr__(), e.args)
                return False
        else:
            return True

    def sqlite_connect(self) -> sqlite3.Connection:  # Создание подключения к БД
        conn = sqlite3.connect(self.db_file_name, check_same_thread=False)
        conn.execute("pragma journal_mode=wal;")
        return conn

    def is_file_exist(self) -> bool:  # Существует ли файл БД
        db = Path(f"./{self.db_file_name}")
        try:
            db.resolve(strict=True)
            return True
        except FileNotFoundError:
            return False

    def is_table_exist(self) -> bool:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f'''SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type="table" AND name="{self.table_name}")''')
        is_exist = curs.fetchone()[0]
        conn.commit()
        conn.close()
        if is_exist:
            return True
        else:
            return False

    def init_sqlite(self) -> None:
        str_for_sql_req = ''
        if len(self.args) != 0:
            count = 1
            for key in self.args:
                if count == 1:
                    str_for_sql_req = str_for_sql_req + key + ' ' + self.args[key] + ' primary key'
                else:
                    str_for_sql_req = str_for_sql_req + key + ' ' + self.args[key]
                """if args[key].__class__.__name__ == "str":
                    str_for_sql_req+=' text'
                elif args[key].__class__.__name__ in ["int", "bool"]:
                    str_for_sql_req+=' integer'"""
                if count != len(self.args):
                    str_for_sql_req += ', '
                    count += 1
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f'''CREATE TABLE {self.table_name} ({str_for_sql_req})''')
        # c.execute(f'''CREATE TABLE {table_name} (id integer primary key, user_id integer, user_name text,
        # user_surname text, username text)''')
        conn.commit()
        conn.close()

    def get_elem_sqllite3(self, key: int | str) -> tuple | bool:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        if key.__class__.__name__ == "int":
            curs.execute(f'''SELECT * from {self.table_name} where key = {key}''')
        else:
            curs.execute(f'''SELECT * from {self.table_name} where key = "{key}"''')
        answ = curs.fetchone()

        conn.close()

        # print(type(answ), 1000)
        return answ

    def __contains__(self, other: int | str) -> bool:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        # print(123, other)
        if other.__class__.__name__ == "int":
            # print(f"SELECT 1 FROM {self.table_name} WHERE key={other}")
            curs.execute(f"SELECT 1 FROM {self.table_name} WHERE key={other}")
        else:
            # print(f"SELECT 1 FROM {self.table_name} WHERE key='{other}'")
            curs.execute(f"SELECT 1 FROM {self.table_name} WHERE key='{other}'")
        if curs.fetchone() is not None:
            conn.close()
            return True
        else:
            conn.close()
            return False

    def __add_column(self, columns: dict) -> None:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        self.args += columns
        for col_name in columns:
            curs.execute(f"""ALTER TABLE {self.table_name} ADD COLUMN {col_name} '{columns[col_name]}'""")
        conn.close()

    def add_row(self, values: tuple) -> None:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        insert_vals_str = ''
        for i in range(len(values)):
            insert_vals_str += '?'
            if len(values) - 1 != i:
                insert_vals_str += ', '
        # print(f"""INSERT INTO {self.table_name} VALUES ({insert_vals_str})\n""", values)
        curs.execute(f"""INSERT INTO {self.table_name} VALUES ({insert_vals_str})""", values)
        conn.commit()
        conn.close()

    def del_row(self, key: int | str) -> None:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        if key.__class__.__name__ == "int":
            curs.execute(f"""DELETE FROM {self.table_name} WHERE key = {key}""")
        else:
            curs.execute(f"""DELETE FROM {self.table_name} WHERE key = '{key}'""")
        conn.commit()
        conn.close()

    def update_info(self, elem) -> None:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        info = elem.get_tuple()
        count = 0
        for column_name in self.args:
            curs.execute(f"""UPDATE {self.table_name} SET {column_name} = ? WHERE key = ?""", (info[count], elem.key))
            count += 1
        conn.commit()
        conn.close()

    def get_keys(self) -> list:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f"""SELECT key FROM {self.table_name}""")
        grand_tuple = curs.fetchall()
        conn.commit()
        conn.close()
        keys = [key[0] for key in grand_tuple]
        return keys