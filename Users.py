from SQLite import Sqlite3_Database
from Enum_classes import Flags, Reminder


class User:
    def __init__(self, key: int = None, flag: Flags = Flags.NONE, payment: bool = False, username: str = None,
                 time_transition_payment: int = None, count_reminder: int = 0, time_reminder: int = 0,
                 reminder: Reminder = Reminder.NONE, key_payment: str = None) -> None:
        self.key: int = key
        self.flag: Flags = flag
        self.payment: bool = payment
        self.username: str = username
        self.time_transition_payment: int = time_transition_payment
        self.count_reminder: int = count_reminder
        self.key_payment = key_payment
        self.time_reminder = time_reminder
        self.reminder = reminder

    def get_tuple(self) -> tuple:
        return (self.key,
                self.flag.value,
                self.payment,
                self.username,
                self.time_transition_payment,
                self.count_reminder,
                self.key_payment,
                self.time_reminder,
                self.reminder.value,
                )


class Users(Sqlite3_Database):
    def __init__(self, db_file_name, args, table_name) -> None:
        Sqlite3_Database.__init__(self, db_file_name, args, table_name)

    def add(self, user: User) -> None:
        self.add_row(user.get_tuple())

    def get(self, id: int) -> User | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = User(
                key=obj_tuple[0],
                flag=Flags(obj_tuple[1]),
                payment=obj_tuple[2],
                username=obj_tuple[3],
                time_transition_payment=obj_tuple[4],
                count_reminder=obj_tuple[5],
                key_payment=obj_tuple[6],
                time_reminder=obj_tuple[7],
                reminder=Reminder(obj_tuple[8]),
            )
            return obj
        return False
