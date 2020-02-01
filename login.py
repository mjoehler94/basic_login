# login.py --------------------------
# Author: Matt Oehler

# libraries
import getpass
import sqlite3

# global
_DATABASE_ = "data/user.db"
_LOGIN_OPTION_ = 1
_REGISTER_OPTION_ = 2
_QUIT_OPTION_= 3


class Login():
    def __init__(self, database):
        self.db = database
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.is_open_connection = True

        # create tables if they don't already exist
        self.cursor.execute('''CREATE TABLE  IF NOT EXISTS USER (
                    "UserId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    "DateJoined"	TEXT NOT NULL,
                    "UserName"	TEXT NOT NULL UNIQUE,
                    "Password_Raw"	TEXT NOT NULL,
                    "Password_Encrypted"	TEXT);
                    ''')

        # Save (commit) the changes and close connection
        self.conn.commit()
        self.conn.close()
        self.is_open_connection = False
        return

    def toggle_connection(self, verbose=False):
        if self.is_open_connection:
            self.conn.close()
            self.is_open_connection = False
        else:
            self.conn.open()
            self.is_open_connection = True
        if verbose:
            status = "opened" if self.is_open_connection else "closed"
            print(f"The database has been {status}.")

    @staticmethod
    def prompt_user_input():
        username = input("Username:")
        pwd = input("Password:")
        # pwd = getpass.getpass(prompt='Password: ', stream=None)

        return username, pwd

    def update_db(self):
        pass

    def insert_sample(self):
        if not self.is_open_connection:
            self.toggle_connection()

        # Insert a row of data as a test (R.I.P. KOBE)
        self.cursor.execute("""INSERT INTO USER (DateJoined, UserName, Password_Raw, Password_Encrypted)
                               VALUES (DATETIME('now'), 'KBryant_24', 'mamba','12345');
                            """)
        # close the db
        self.toggle_connection()

    def encrypt(self):
        pass


def main():

    # initialize Login instance ---------------
    login = Login(database=_DATABASE_)

    # Main Menu ------------------
    while True:
        print("Main Menu -------------------------------")
        option = input("""Please enter:
         '1' to Login
         '2' to Register
         '3' to Quit\n-->""")
        try:
            option = int(option)
        except:
            pass
        if option == _QUIT_OPTION_:
            print("Quitting the program.")
            return
        elif option not in [1, 2]:
            print("Invalid Selection. Please try again.")
        else:
            break

    if option == _LOGIN_OPTION_:
        print("Enter your Username and Password to login.")
    elif option == _REGISTER_OPTION_:
        print("To Register, enter in your desired Username then password.")

    # login or register ----------------------------
    username, pwd = login.prompt_user_input()

    print(f"Username: {username}, Password: {pwd}")

    return


if __name__ == '__main__':
    main()
